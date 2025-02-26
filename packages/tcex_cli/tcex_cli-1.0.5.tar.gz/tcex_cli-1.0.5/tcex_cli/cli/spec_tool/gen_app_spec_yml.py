"""TcEx Framework Module"""

# standard library
import json
from pathlib import Path

# third-party
from semantic_version import Version

# first-party
from tcex_cli.app.config import AppSpecYml
from tcex_cli.app.config.model import AppSpecYmlModel
from tcex_cli.cli.cli_abc import CliABC


class GenAppSpecYml(CliABC):
    """Generate App Config File"""

    def __init__(self):
        """Initialize instance properties."""
        super().__init__()

        # properties
        self.filename = 'app_spec.yml'
        self.asy = AppSpecYml(logger=self.log)

    def _add_standard_fields(self, app_spec_yml_data: dict):
        """Add field that apply to ALL App types."""
        app_spec_yml_data.update(
            {
                'allowOnDemand': self.app.ij.model.allow_on_demand,
                'apiUserTokenParam': self.app.ij.model.api_user_token_param,
                'appId': str(self.app.ij.model.app_id),
                'category': self.app.ij.model.category,
                'deprecatesApps': self.app.ij.model.deprecates_apps,
                'displayName': self.app.ij.model.display_name,
                'features': self.app.ij.model.features,
                'labels': self.app.ij.model.labels,
                'languageVersion': self.app.ij.model.language_version,
                'listDelimiter': self.app.ij.model.list_delimiter,
                'minServerVersion': str(self.app.ij.model.min_server_version),
                'note': self.app.ij.model.note,
                'packageName': self.app.tj.model.package.app_name,
                'programLanguage': self.app.ij.model.program_language,
                'programMain': self.app.ij.model.program_main,
                'programVersion': str(self.app.ij.model.program_version),
                'runtimeLevel': self.app.ij.model.runtime_level,
                'schemaVersion': '1.1.0',
                'sdkVersion': self.app.ij.model.sdk_version,
            }
        )

    def _add_category(self, app_spec_yml_data: dict):
        """Add category."""
        _category = ''
        if any([self.app.ij.model.is_playbook_app, self.app.ij.model.is_trigger_app]):
            _category = ''
            if self.app.ij.model.playbook and self.app.ij.model.playbook.type:
                _category = self.app.ij.model.playbook.type
        app_spec_yml_data['category'] = _category

    def _add_feeds(self, app_spec_yml_data: dict):
        """Add organization feeds section."""
        if not self.app.ij.model.is_feed_app:
            return

        feeds = []
        for feed in self.app.ij.model.feeds or []:
            feed_job_file = Path(feed.job_file)
            if not feed_job_file.is_file():
                self.log.error(
                    f'feature=app-spec-yml, exception=failed-reading-file, filename={feed.job_file}'
                )
                continue
            with feed_job_file.open(encoding='utf-8') as f:
                job = json.load(f)
            feed_dict = feed.dict(by_alias=True)
            feed_dict['job'] = job
            feeds.append(feed_dict)
        app_spec_yml_data.setdefault('organization', {})
        app_spec_yml_data['organization']['feeds'] = feeds

    def _add_note_per_action(self, app_spec_yml_data: dict):
        """Add note per action."""
        _notes_per_action = []
        param = self.app.ij.model.get_param('tc_action')
        if param and param.valid_values:
            for action in param.valid_values:
                _notes_per_action.append({'action': action, 'note': ''})

            app_spec_yml_data['notesPerAction'] = _notes_per_action

    def _add_organization(self, app_spec_yml_data: dict):
        """Add asy.organization."""
        if self.app.ij.model.is_organization_app:
            app_spec_yml_data.setdefault('organization', {})
            if self.app.ij.model.publish_out_files:
                app_spec_yml_data['organization']['publishOutFiles'] = (
                    self.app.ij.model.publish_out_files
                )
            if self.app.ij.model.repeating_minutes:
                app_spec_yml_data['organization']['repeatingMinutes'] = (
                    self.app.ij.model.repeating_minutes
                )

    def _add_output_data(self, app_spec_yml_data: dict):
        """Add asy.outputData."""
        if any([self.app.ij.model.is_playbook_app, self.app.ij.model.is_trigger_app]):
            # build outputs based on display value
            _output_data_temp = {}
            if self.app.lj.has_layout:
                # layout based Apps could will have a display clause for each output
                for o in self.app.ij.model.playbook_outputs.values():
                    ljo = self.app.lj.model.get_output(o.name)
                    if ljo.display is not None and ljo.name is not None:
                        _output_data_temp.setdefault(ljo.display or '1', []).append(o.name)
                    else:
                        _output_data_temp.setdefault('1', []).append(o.name)
            else:
                for _, o in self.app.ij.model.playbook_outputs.items():
                    _output_data_temp.setdefault('1', []).append(o.name)

            _output_data = []
            for display, names in _output_data_temp.items():
                _output_variables = []
                for name in names:
                    if not self._is_advanced_request_output(name):
                        output_variable_model = self.app.ij.model.get_output(name)
                        if output_variable_model is not None:
                            _output_variables.append(output_variable_model.dict(by_alias=True))

                _output_data.append({'display': display, 'outputVariables': _output_variables})

            app_spec_yml_data['outputData'] = _output_data

    def _add_output_prefix(self, app_spec_yml_data: dict):
        """Add asy.outputData."""
        if (
            self.app.ij.model.is_playbook_app
            and self.app.ij.model.playbook
            and self.app.ij.model.playbook.output_prefix
        ):
            app_spec_yml_data['outputPrefix'] = self.app.ij.model.playbook.output_prefix

    def _add_playbook(self, app_spec_yml_data: dict):
        """Add asy.playbook."""
        if any([self.app.ij.model.is_playbook_app, self.app.ij.model.is_trigger_app]):
            app_spec_yml_data.setdefault('playbook', {})
            if self.app.ij.model.playbook and self.app.ij.model.playbook.retry:
                app_spec_yml_data['playbook']['retry'] = self.app.ij.model.playbook.retry

    @staticmethod
    def _add_release_notes(app_spec_yml_data: dict):
        """Add release_notes."""
        app_spec_yml_data['releaseNotes'] = [
            {
                'notes': ['Initial Release'],
                'version': '1.0.0',
            }
        ]

    def _add_sections(self, app_spec_yml_data: dict):
        """Return params from ij and lj formatted for app_spec."""
        sections = []
        for section in self._current_data:
            _section_data = {'sectionName': section.get('title'), 'params': []}
            for p in section.get('parameters') or []:
                if not self._is_advanced_request_input(p['name']):
                    param = self.app.ij.model.get_param(p['name'])
                    if param is not None:
                        param = param.dict(by_alias=True)
                        param['display'] = p.get('display')
                        _section_data['params'].append(param)
            sections.append(_section_data)
        app_spec_yml_data['sections'] = sections

    @property
    def _current_data(self):
        """Retrieve the appropriate data regardless of if its a layout based app."""
        if self.app.lj.has_layout:
            # handle layout based Apps
            _current_data = [i.dict(by_alias=True) for i in self.app.lj.model.inputs]

            # add hidden inputs from install.json (hidden inputs are not in layouts.json)
            _current_data.append(
                {
                    'parameters': [
                        p.dict(by_alias=True) for p in self.app.ij.model.params if p.hidden is True
                    ],
                    'title': 'Hidden Inputs',
                }
            )
        else:
            # handle non-layout based Apps
            _current_data = [
                {
                    'parameters': [p.dict(by_alias=True) for p in self.app.ij.model.params],
                    'title': 'Inputs',
                }
            ]
        return _current_data

    def _is_64_min_version(self) -> bool:
        """Return params from ij and lj formatted for app_spec."""

        for section in self._current_data:
            for p in section.get('parameters', []):
                param = self.app.ij.model.get_param(p['name'])
                if param is not None and param.type.lower() == 'editchoice':
                    return True
        return False

    @staticmethod
    def _is_advanced_request_input(name: str) -> bool:
        """Return true if input is an Advanced Request input."""
        return name in [
            'tc_adv_req_path',
            'tc_adv_req_http_method',
            'tc_adv_req_params',
            'tc_adv_req_exclude_null_params',
            'tc_adv_req_headers',
            'tc_adv_req_body',
            'tc_adv_req_urlencode_body',
            'tc_adv_req_fail_on_error',
        ]

    def _is_advanced_request_output(self, name: str) -> bool:
        """Return true if input is an Advanced Request input."""
        for pattern in [
            'request.content',
            'request.content.binary',
            'request.headers',
            'request.ok',
            'request.reason',
            'request.status_code',
            'request.url',
        ]:
            if (
                self.app.ij.model.playbook is not None
                and f'{self.app.ij.model.playbook.output_prefix}.{pattern}' == name
            ):
                return True
        return False

    def _add_min_tc_version(self, app_spec_yml_data: dict):
        """Add the correct min TC server version."""

        if self._is_64_min_version() and self.app.ij.model.min_server_version < Version('6.4.0'):
            app_spec_yml_data['minServerVersion'] = '6.4.0'

    def generate(self):
        """Generate the layout.json file data."""
        app_spec_yml_data = {}

        # add feeds
        self._add_feeds(app_spec_yml_data)

        # add release notes
        self._add_release_notes(app_spec_yml_data)

        # add standard fields
        self._add_standard_fields(app_spec_yml_data)

        # add category
        self._add_category(app_spec_yml_data)

        # add note per action
        self._add_note_per_action(app_spec_yml_data)

        # add organization (feed, jobs, etc)
        self._add_organization(app_spec_yml_data)

        # add playbook (retry)
        self._add_playbook(app_spec_yml_data)

        # add playbook output prefix
        self._add_output_prefix(app_spec_yml_data)

        # add sections
        self._add_sections(app_spec_yml_data)

        # add output data
        self._add_output_data(app_spec_yml_data)

        asy_data = json.loads(
            AppSpecYmlModel(**app_spec_yml_data).json(
                by_alias=True,
                exclude_defaults=True,
                exclude_none=True,
                exclude_unset=True,
                sort_keys=False,
            )
        )

        # force order of keys
        return self.asy.dict_to_yaml(asy_data)
