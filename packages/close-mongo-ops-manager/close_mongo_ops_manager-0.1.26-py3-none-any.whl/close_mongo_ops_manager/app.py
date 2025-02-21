from __future__ import annotations

import asyncio
import logging
import os
import argparse
import sys
import time
from urllib.parse import quote_plus


from textual import work
from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import DataTable, Footer, Header
from textual.coordinate import Coordinate
from textual.containers import VerticalScroll

from pymongo.uri_parser import parse_uri

from close_mongo_ops_manager.filterbar import FilterBar
from close_mongo_ops_manager.help_screen import HelpScreen
from close_mongo_ops_manager.kill_confirmation_screen import KillConfirmation
from close_mongo_ops_manager.log_screen import LogScreen
from close_mongo_ops_manager.messages import FilterChanged, OperationsLoaded
from close_mongo_ops_manager.mongodb_manager import MongoDBManager
from close_mongo_ops_manager.operations_view import OperationsView
from close_mongo_ops_manager.statusbar import StatusBar


# Constants
LOG_FILE = "close_mongo_ops_manager.log"
MIN_REFRESH_INTERVAL = 1
MAX_REFRESH_INTERVAL = 10
DEFAULT_REFRESH_INTERVAL = 5
STEP_REFRESH_INTERVAL = 1  # Interval change step


# Set up logging
def setup_logging() -> logging.Logger:
    logger = logging.getLogger("mongo_ops_manager")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s (%(levelname)s): %(message)s")

    fh = logging.FileHandler(LOG_FILE, mode="w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


logger = setup_logging()


class MongoOpsManager(App):
    """Main application class."""

    ENABLE_COMMAND_PALETTE = False

    TITLE = "Close MongoDB Operations Manager"

    AUTO_FOCUS = "OperationsView"

    CSS = """
    MongoOpsManager {
        align: center top;
        padding: 0;
    }

    VerticalScroll {
        width: 100%;
        padding: 0;
        margin: 0;
    }
    """

    BINDINGS = [
        Binding("f1", "show_help", "Help"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+r", "refresh", "Refresh"),
        Binding("ctrl+k", "kill_selected", "Kill Selected"),
        Binding("ctrl+p", "toggle_refresh", "Pause/Resume"),
        Binding("ctrl+s", "sort_by_time", "Sort by Time"),
        Binding("ctrl+l", "show_logs", "View Logs"),
        Binding("ctrl+u", "deselect_all", "Deselect All"),
        Binding("ctrl+a", "select_all", "Select All"),
        Binding(
            "ctrl+equals_sign",
            "increase_refresh",
            "Increase Refresh Interval",
            key_display="^+",
        ),
        Binding(
            "ctrl+minus",
            "decrease_refresh",
            "Decrease Refresh Interval",
            key_display="^-",
        ),
    ]

    auto_refresh: reactive[bool] = reactive(False)
    refresh_interval: reactive[int] = reactive(DEFAULT_REFRESH_INTERVAL)

    def __init__(
        self,
        connection_string: str,
        refresh_interval: int = DEFAULT_REFRESH_INTERVAL,
        namespace: str = "",
        hide_system_ops: bool = True,
    ) -> None:
        super().__init__()
        self.connection_string = connection_string
        self.refresh_interval = refresh_interval
        self.mongodb: MongoDBManager | None = None
        self._refresh_task: asyncio.Task | None = None
        self.log_file = LOG_FILE
        self._status_bar: StatusBar
        self.namespace: str = namespace
        self.hide_system_ops = hide_system_ops

    def validate_refresh_interval(self, value: int) -> int:
        """Validate refresh interval."""
        return max(MIN_REFRESH_INTERVAL, min(value, MAX_REFRESH_INTERVAL))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield FilterBar()
        with VerticalScroll(can_focus=False, can_focus_children=True):
            yield OperationsView()
        yield StatusBar(self.refresh_interval)
        yield Footer()

    async def on_mount(self) -> None:
        self.operations_view = self.query_one(OperationsView)
        self._status_bar = self.query_one(StatusBar)
        self.operations_view.loading = True
        self._status_bar.set_refresh_interval(self.refresh_interval)
        asyncio.create_task(self._setup())

    def action_show_help(self) -> None:
        """Show the help screen."""
        self.push_screen(HelpScreen())

    def action_show_logs(self) -> None:
        """Show the log viewer screen."""
        self.push_screen(LogScreen(self.log_file))

    async def _setup(self) -> None:
        """Initialize MongoDB connection and start operation monitoring."""
        try:
            self.mongodb = await MongoDBManager.connect(
                self.connection_string, self.namespace, self.hide_system_ops
            )
            # Extract connection details for status bar
            parsed_uri = parse_uri(self.connection_string)

            # Safely extract host information with fallbacks
            host_info = "unknown host"
            try:
                nodelist = parsed_uri.get("nodelist")
                if nodelist and len(nodelist) > 0:
                    host, port = nodelist[0]
                    host_info = f"{host}:{port}"
                else:
                    # Fallback: try to extract from connection string directly
                    cleaned_uri = self.connection_string.split("@")[-1].split("/")[0]
                    host_info = cleaned_uri.split("?")[
                        0
                    ]  # Remove query parameters if present
            except Exception as parse_error:
                logger.warning(f"Failed to parse host details: {parse_error}")
                # Use a generic connection success message
                host_info = "MongoDB server"

            self._status_bar.set_connection_status(True, host_info)

            self.refresh_operations()
            self._refresh_task = asyncio.create_task(self.auto_refreshing())
        except Exception as e:
            logger.error(f"Setup error: {e}", exc_info=True)
            self._status_bar.set_connection_status(False)
            self.notify(f"Failed to connect: {e}", severity="error")

    def action_increase_refresh(self) -> None:
        """Increase the refresh interval."""
        new_interval = min(
            MAX_REFRESH_INTERVAL, self.refresh_interval + STEP_REFRESH_INTERVAL
        )
        if new_interval != self.refresh_interval:
            self.refresh_interval = new_interval
            self.notify(f"Refresh interval increased to {self.refresh_interval}s")
            self._status_bar.set_refresh_interval(self.refresh_interval)

    def action_decrease_refresh(self) -> None:
        """Decrease the refresh interval."""
        new_interval = max(
            MIN_REFRESH_INTERVAL, self.refresh_interval - STEP_REFRESH_INTERVAL
        )
        if new_interval != self.refresh_interval:
            self.refresh_interval = new_interval
            self.notify(f"Refresh interval decreased to {self.refresh_interval}s")
            self._status_bar.set_refresh_interval(self.refresh_interval)

    async def auto_refreshing(self) -> None:
        """Background task for auto-refreshing functionality."""
        while True:
            try:
                if self.auto_refresh:
                    self.refresh_operations()
                await asyncio.sleep(self.refresh_interval)
            except Exception as e:
                logger.error(f"Auto-refresh error: {e}", exc_info=True)
                await asyncio.sleep(self.refresh_interval)

    @work(exclusive=True)
    async def refresh_operations(self) -> None:
        """Refresh the operations table with current data."""
        if not self.mongodb:
            self.operations_view.loading = False
            return

        # Clear selected operations before refreshing.
        # This is needed to avoid issues with deselection after refreshing.
        self.operations_view.selected_ops.clear()

        start_time = time.monotonic()
        try:
            self.operations_view.loading = True
            ops = await self.mongodb.get_operations(self.operations_view.filters)

            # Store the operations data in the view
            self.operations_view.current_ops = ops

            # Clear the operations table
            self.operations_view.clear()

            # Sort operations by running time if needed
            if hasattr(self.operations_view, "sort_running_time_asc"):
                ops.sort(
                    key=lambda x: float(str(x.get("secs_running", 0)).rstrip("s")),
                    reverse=not self.operations_view.sort_running_time_asc,
                )

            for op in ops:
                # Get client info
                client_info = op.get("client_s") or op.get("client", "N/A")
                client_metadata = op.get("clientMetadata", {})
                mongos_info = client_metadata.get("mongos", {})
                mongos_host = mongos_info.get("host", "")

                if mongos_host:
                    client_info = f"{client_info} ({mongos_host.split('.', 1)[0]})"

                # Get effective users
                effective_users = op.get("effectiveUsers", [])
                users_str = (
                    ", ".join(u.get("user", "") for u in effective_users)
                    if effective_users
                    else "N/A"
                )

                row = (
                    "☐",
                    str(op["opid"]),
                    op.get("type", ""),
                    op.get("op", ""),
                    f"{op.get('secs_running', 0)}s",
                    client_info,
                    op.get("desc", "N/A"),
                    users_str,
                )
                self.operations_view.add_row(*row, key=str(op["opid"]))

            # Calculate load duration and emit event
            duration = time.monotonic() - start_time
            self.operations_view.post_message(
                OperationsLoaded(count=len(ops), duration=duration)
            )

        except Exception as e:
            self.notify(f"Failed to refresh: {e}", severity="error")

        finally:
            self.operations_view.loading = False

    def action_refresh(self) -> None:
        """Handle refresh action."""
        self.refresh_operations()

    def action_toggle_refresh(self) -> None:
        """Toggle auto-refresh."""
        self.auto_refresh = not self.auto_refresh
        self._status_bar.set_refresh_status(self.auto_refresh)
        status = "enabled" if self.auto_refresh else "paused"
        self.notify(f"Auto-refresh {status}")

    def action_deselect_all(self) -> None:
        """Deselect all selected operations."""
        if not self.operations_view.selected_ops:
            return

        # Remember selected ops before clearing
        count = len(self.operations_view.selected_ops)

        # Clear the selected operations set
        self.operations_view.selected_ops.clear()

        self.refresh_operations()

        # Show notification
        self.notify(f"Deselected {count} operations")

    def action_select_all(self) -> None:
        """Select all operations in the view."""
        # Clear any existing selections first
        self.operations_view.selected_ops.clear()

        # Add all row keys to selected_ops and update checkboxes
        for idx, key in enumerate(self.operations_view.rows.keys()):
            # Convert RowKey to string value
            row_key = str(getattr(key, "value", key))
            self.operations_view.selected_ops.add(row_key)
            coord = Coordinate(idx, 0)
            self.operations_view.update_cell_at(coord, "☒")

        # Show notification
        count = len(self.operations_view.selected_ops)
        if count > 0:
            self.notify(f"Selected {count} operations")

    # FIXME: When refreshing the table after killing an operation
    # the selected row is keep selected and the checkbox is not unchecked.
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection."""
        try:
            # Get the row key value directly
            row_key = str(event.row_key.value)
            coord = Coordinate(event.cursor_row, 0)  # Get checkbox cell coordinate

            if row_key in self.operations_view.selected_ops:
                self.operations_view.selected_ops.remove(row_key)
                self.operations_view.update_cell_at(coord, "☐")
            else:
                self.operations_view.selected_ops.add(row_key)
                self.operations_view.update_cell_at(coord, "☒")

        except Exception as e:
            logger.error(f"Error handling row selection: {e}", exc_info=True)
            self.notify("Error selecting row", severity="error")

    async def action_kill_selected(self) -> None:
        """Kill selected operations with confirmation."""
        if not self.operations_view.selected_ops:
            self.notify("No operations selected")
            return

        async def handle_confirmation(confirmed: bool | None) -> None:
            if not confirmed or not self.mongodb:
                return

            # Get operation details before killing
            current_ops = await self.mongodb.get_operations()
            selected_ops = [
                op
                for op in current_ops
                if str(op["opid"]) in self.operations_view.selected_ops
            ]

            for op in selected_ops:
                command = op.get("command", {})
                query_info = {
                    "find": command.get("find"),
                    "filter": command.get("filter"),
                    "ns": op.get("ns"),
                    "client": op.get("client"),
                }
                logger.info(
                    f"Preparing to kill operation {op['opid']}. Query details: {query_info}"
                )

            success_count = 0
            error_count = 0

            for opid in list(self.operations_view.selected_ops):
                try:
                    if await self.mongodb.kill_operation(opid):
                        success_count += 1
                    else:
                        error_count += 1
                        logger.error(
                            f"Failed to kill operation {opid}: Operation not found"
                        )
                except Exception as e:
                    error_count += 1
                    self.notify(
                        f"Failed to kill operation {opid}: {str(e)}", severity="error"
                    )
                    logger.error(f"Failed to kill operation {opid}: {e}", exc_info=True)

            # Clear selections after all operations are processed
            self.operations_view.clear_selections()
            self.operations_view.selected_ops.clear()

            # Refresh the view
            self.refresh_operations()

            # Show summary
            if success_count > 0:
                self.notify(
                    f"Successfully killed {success_count} operation(s)",
                    severity="information",
                )
            if error_count > 0:
                self.notify(
                    f"Failed to kill {error_count} operation(s)", severity="error"
                )

        await self.push_screen(
            KillConfirmation(list(self.operations_view.selected_ops)),
            callback=handle_confirmation,
        )

    async def on_filter_changed(self, event: FilterChanged) -> None:
        """Handle filter changes."""
        self.operations_view.filters = event.filters
        self.refresh_operations()

    def action_sort_by_time(self) -> None:
        """Sort operations by running time."""
        self.operations_view.sort_running_time_asc = not getattr(
            self.operations_view, "sort_running_time_asc", True
        )
        direction = (
            "ascending" if self.operations_view.sort_running_time_asc else "descending"
        )
        self.notify(f"Sorted by running time ({direction})")
        self.refresh_operations()

    def on_operations_loaded(self, event: OperationsLoaded) -> None:
        """Handle operations loaded event."""
        logger.info(f"Loaded {event.count} operations in {event.duration:.2f} seconds")


def main() -> None:
    parser = argparse.ArgumentParser(description="Close MongoDB Operations Manager")
    parser.add_argument(
        "--host",
        default=os.environ.get("MONGODB_HOST", "localhost"),
        type=str,
        help="MongoDB host",
    )
    parser.add_argument(
        "--port",
        default=os.environ.get("MONGODB_PORT", "27017"),
        type=str,
        help="MongoDB port",
    )
    parser.add_argument(
        "--username",
        default=os.environ.get("MONGODB_USERNAME"),
        type=str,
        help="MongoDB username",
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("MONGODB_PASSWORD"),
        type=str,
        help="MongoDB password",
    )
    parser.add_argument(
        "--namespace", help="MongoDB namespace to monitor", type=str, default=".*"
    )
    parser.add_argument(
        "--refresh-interval",
        type=int,
        default=int(
            os.environ.get("MONGODB_REFRESH_INTERVAL", str(DEFAULT_REFRESH_INTERVAL))
        ),
        help=f"Refresh interval in seconds (min: {MIN_REFRESH_INTERVAL}, max: {MAX_REFRESH_INTERVAL})",
    )
    parser.add_argument(
        "--show-system-ops",
        action="store_true",
        help="Show system operations (disabled by default)",
    )

    args = parser.parse_args()

    # Build connection string
    username = args.username or os.environ.get("MONGODB_USERNAME")
    password = args.password or os.environ.get("MONGODB_PASSWORD")
    host = args.host or os.environ.get("MONGODB_HOST", "localhost")
    port = args.port or os.environ.get("MONGODB_PORT", "27017")

    try:
        # Build connection string based on authentication settings
        if username and password:
            # Use authenticated connection
            username = quote_plus(username)
            password = quote_plus(password)
            connection_string = f"mongodb://{username}:{password}@{host}:{port}/"
        else:
            # Use unauthenticated connection
            connection_string = f"mongodb://{host}:{port}/"
            logger.info("Using unauthenticated connection")

        # Validate refresh interval
        refresh_interval = max(
            MIN_REFRESH_INTERVAL, min(args.refresh_interval, MAX_REFRESH_INTERVAL)
        )
        if refresh_interval != args.refresh_interval:
            if args.refresh_interval < MIN_REFRESH_INTERVAL:
                logger.warning(
                    f"Refresh interval too low, setting to minimum ({MIN_REFRESH_INTERVAL} seconds)"
                )
            else:
                logger.warning(
                    f"Refresh interval too high, setting to maximum ({MAX_REFRESH_INTERVAL} seconds)"
                )

        # Start the application
        app = MongoOpsManager(
            connection_string=connection_string,
            refresh_interval=refresh_interval,
            namespace=args.namespace,
            hide_system_ops=not args.show_system_ops,
        )
        app.run()

    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)
        print(f"\nError: {e}")
        print(f"Please check {LOG_FILE} for details")
        sys.exit(1)


if __name__ == "__main__":
    main()
