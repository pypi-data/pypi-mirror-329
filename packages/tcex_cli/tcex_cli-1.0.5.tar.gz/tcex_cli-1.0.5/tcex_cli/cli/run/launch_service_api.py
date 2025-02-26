"""TcEx Framework Module"""

# standard library
import datetime
import json
from pathlib import Path
from threading import Thread

# third-party
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

# first-party
from tcex_cli.cli.run.launch_service_common_abc import LaunchServiceCommonABC
from tcex_cli.cli.run.model.app_api_service_model import AppApiInputModel
from tcex_cli.cli.run.request_handler_api import RequestHandlerApi
from tcex_cli.cli.run.web_server import WebServer
from tcex_cli.pleb.cached_property import cached_property


class LaunchServiceApi(LaunchServiceCommonABC):
    """Launch an App"""

    def __init__(self, config_json: Path):
        """Initialize instance properties."""
        super().__init__(config_json)

        # properties
        self.request_data = []
        self.response_data = []

    def _format_key_value(self, key_value: list[dict]) -> str:
        """Return a formatted key value pair."""
        key_value_ = ''
        for kv in key_value:
            key_value_ += f'{kv.get("name")}: [{self.accent}]{kv.get("value")}[/]\n'
        return key_value_

    @cached_property
    def api_web_server(self) -> WebServer:
        """Return an instance of the API Web Server."""
        return WebServer(
            self.model.inputs,
            self.message_broker,
            self.publish,
            self.redis_client,
            RequestHandlerApi,
            self.tc_token,
        )

    @cached_property
    def model(self) -> AppApiInputModel:
        """Return the App inputs."""
        return AppApiInputModel(**self.construct_model_inputs())

    def live_data_display(self):
        """Display live data."""
        console = Console()
        layout = Layout()

        # Divide the "screen" in to three parts
        layout.split(
            Layout(self.live_data_header(), name='header', ratio=1, minimum_size=3),
            Layout(self.live_data_request(), name='request', ratio=8),
            Layout(self.live_data_response(), name='response', ratio=8),
            Layout(self.live_data_commands(), name='commands', ratio=4),
        )

        with Live(
            layout,
            console=console,
            refresh_per_second=4,
            screen=True,
            vertical_overflow='ellipsis',
        ) as _:
            while True:
                # if self.stop_server is True:
                #     # console.clear()
                #     break

                self.event.wait()
                self.log.trace('Updating live data table.')
                layout['header'].update(self.live_data_header())
                layout['request'].update(self.live_data_request())
                layout['response'].update(self.live_data_response())
                layout['commands'].update(self.live_data_commands())
                self.event.clear()

    def live_data_header(self) -> Panel:
        """Display live header."""
        return Panel(
            (
                f'Running server: [{self.accent}]http://{self.model.inputs.api_service_host}'
                f':{self.model.inputs.api_service_port}[/{self.accent}]'
            ),
            expand=True,
            title='[blue]HTTP Server[/blue]',
            title_align='left',
        )

    def live_data_request(self):
        """Display live data."""
        table = Table(expand=True, show_edge=False, show_lines=False)
        table.add_column('Request Datetime')
        table.add_column('Method')
        table.add_column('Path')
        table.add_column('Headers')
        table.add_column('Query Params')
        table.add_column('Request Key')

        try:
            for request in self.request_data[::-1]:
                table.add_row(
                    request.get('request_time'),
                    request.get('method'),
                    f'[{self.accent}]{request.get("path")}[/]',
                    self._format_key_value(request.get('headers') or []),
                    self._format_key_value(request.get('query_params') or []),
                    request.get('request_key'),
                )
        except Exception:
            self.log.exception('Error in live_data_table')

        return Panel(
            table,
            border_style='',
            title=f'[{self.panel_title}]Requests[/]',
            title_align='left',
        )

    def live_data_response(self):
        """Display live data."""
        table = Table(expand=True, show_edge=False, show_lines=False)
        table.add_column('Response Datetime')
        table.add_column('Status')
        table.add_column('Status Code')
        table.add_column('Headers')
        table.add_column('Request Key')

        try:
            for request in self.response_data[::-1]:
                table.add_row(
                    request.get('response_time'),
                    request.get('status'),
                    f'[{self.accent}]{request.get("status_code")}[/]',
                    self._format_key_value(request.get('headers') or []),
                    request.get('request_key'),
                )
        except Exception:
            self.log.exception('Error in live_data_table')

        return Panel(
            table,
            border_style='',
            title=f'[{self.panel_title}]Response[/]',
            title_align='left',
        )

    def process_client_channel(self, client, userdata, message):  # noqa: ARG002
        """Handle message broker on_message shutdown command events."""
        try:
            msg = json.loads(message.payload)
        except ValueError as ex:
            ex_msg = f'Could not parse API service response JSON. ({message})'
            raise RuntimeError(ex_msg) from ex

        command = msg.get('command').lower()
        self.message_data.append(
            {
                'channel': 'client',
                'command': command,
                'msg_time': datetime.datetime.now(datetime.UTC).isoformat(),
                'type': msg.get('type'),
            }
        )

        match command:
            case 'acknowledged':
                self.response_data.append(
                    {
                        'headers': msg.get('headers'),
                        'status': msg.get('status'),
                        'status_code': msg.get('statusCode'),
                        'request_key': msg.get('requestKey'),
                        'response_time': datetime.datetime.now(datetime.UTC).isoformat(),
                    }
                )

        self.event.set()

    def process_server_channel(self, client, userdata, message):  # noqa: ARG002
        """Handle message broker on_message shutdown command events."""
        try:
            msg = json.loads(message.payload)
        except ValueError as ex:
            ex_msg = f'Could not parse API service response JSON. ({message})'
            raise RuntimeError(ex_msg) from ex

        command = msg.get('command').lower()
        self.message_data.append(
            {
                'channel': 'server',
                'command': command,
                'msg_time': datetime.datetime.now(datetime.UTC).isoformat(),
                'type': msg.get('type'),
            }
        )

        match command:
            case 'runservice':
                self.request_data.append(
                    {
                        'headers': msg.get('headers'),
                        'method': msg.get('method'),
                        'path': msg.get('path'),
                        'query_params': msg.get('queryParams'),
                        'request_key': msg.get('requestKey'),
                        'request_time': datetime.datetime.now(datetime.UTC).isoformat(),
                    }
                )

            case 'shutdown':
                self.stop_server = True

        self.event.set()

    def setup(self, debug: bool = False):
        """Configure the API Web Server."""
        # setup web server
        self.api_web_server.setup()

        # start thread to listen for on connect
        self.message_broker_listen()

        # add call back to process server channel messages
        self.message_broker.add_on_message_callback(
            callback=self.process_client_channel,
            index=0,
            topics=[self.model.inputs.tc_svc_client_topic],
        )

        # add call back to process server channel messages
        self.message_broker.add_on_message_callback(
            callback=self.process_server_channel,
            index=0,
            topics=[self.model.inputs.tc_svc_server_topic],
        )

        # start live display
        if debug is False:
            self.display_thread = Thread(
                target=self.live_data_display, name='LiveDataDisplay', daemon=True
            )
            self.display_thread.start()
