"""TcEx Framework Module"""

# standard library
import hashlib
import json
import os
from collections.abc import Generator
from pathlib import Path

# third-party
import yaml
from pydantic import ValidationError
from requests import Response, Session
from requests.auth import HTTPBasicAuth
from tinydb import Query, TinyDB

# first-party
from tcex_cli.cli.cli_abc import CliABC
from tcex_cli.cli.model.file_metadata_model import FileMetadataModel
from tcex_cli.cli.template.model.template_config_model import TemplateConfigModel
from tcex_cli.pleb.cached_property import cached_property
from tcex_cli.pleb.proxies import proxies
from tcex_cli.render.render import Render


class TemplateCli(CliABC):
    """CLI command for initializing, listing, and updating template files."""

    def __init__(
        self,
        proxy_host,
        proxy_port,
        proxy_user,
        proxy_pass,
    ):
        """Initialize instance properties."""
        super().__init__()

        # properties
        _default_github_user = 'ThreatConnect-Inc'
        _github_user = os.getenv('TCEX_TEMPLATE_GITHUB_USER', _default_github_user)
        self.accent = 'dark_orange'
        self.base_url = f'https://api.github.com/repos/{_github_user}/tcex-app-templates'
        self.base_raw_url = f'https://raw.githubusercontent.com/{_github_user}/tcex-app-templates'
        self.errors = False
        self.gh_password = os.getenv('GITHUB_PAT')
        self.gh_username = os.getenv('GITHUB_USER')
        self.template_configs = {}
        self.template_data: dict[str, list[TemplateConfigModel]] = {}
        self.template_manifest = {}
        self.template_manifest_fqfn = Path('.template_manifest.json')
        self.proxy_host = self._process_proxy_host(proxy_host)
        self.proxy_port = self._process_proxy_port(proxy_port)
        self.proxy_user = self._process_proxy_user(proxy_user)
        self.proxy_pass = self._process_proxy_pass(proxy_pass)

        # load current template manifest
        self.load_template_manifest()

        # log current github user, if not the default
        if _github_user != _default_github_user:
            Render.panel.info(f'Using GitHub user: [{self.accent}]{_github_user}')

    def _log_validation_error(self, ex: ValidationError):
        """Log model validation errors."""
        for error in json.loads(ex.json()):
            location = [str(location) for location in error.get('loc')]
            self.log.error(
                """Schema validation failed for template.yaml. """
                f"""({error.get('msg')}: {' -> '.join(location)})"""
            )
            self.errors = True

    @cached_property
    def cache_valid(self) -> bool:
        """Return true if cache is valid."""
        if self.project_sha is None:
            return False

        # retrieve stored sha
        stored_sha = self.db_get_sha(self.project_sha)

        # upsert sha if values don't match and then return False
        if stored_sha != self.project_sha:
            self.db_add_sha(self.project_sha)
            return False

        return True

    def clear(self):
        """Clear the stored template cache."""
        Render.panel.info('Clearing template cache.')
        (self.cli_out_path / 'tcex.json').unlink(missing_ok=True)

    @cached_property
    def db(self) -> TinyDB:
        """Return db instance."""
        db_file = self.cli_out_path / 'tcex.json'
        try:
            return TinyDB(db_file)
        except Exception:
            self.log.exception(f'action=get-db, file={db_file}')
            Render.panel.failure('Failed to open database.')

    def db_add_config(self, config: TemplateConfigModel):
        """Add a config to the DB."""
        config_query = Query()
        try:
            if config.name == '_app_common':
                config.type = '_app_common'
            self.db.upsert(
                json.loads(config.json()),
                (config_query.type == config.type) & (config_query.name == config.name),
            )
        except Exception:
            self.log.exception('Failed inserting config in db.')
            self.errors = True

    def db_add_sha(self, sha: str):
        """Add a config to the DB."""
        sha_query = Query()
        try:
            self.db.upsert({'sha': sha}, sha_query.sha.exists())
        except Exception:
            self.log.exception('Failed inserting config in db.')
            self.errors = True

    def db_get_config(self, template_type: str, template: str) -> TemplateConfigModel | None:
        """Get a config from the DB."""
        config = Query()
        try:
            if template == '_app_common':
                template_type = '_app_common'
            config = self.db.search((config.type == template_type) & (config.name == template))

            if config:
                return TemplateConfigModel(**config[0])
        except Exception:
            self.log.exception('Failed retrieving config from db.')
            self.errors = True
            return None
        else:
            return None

    def db_get_sha(self, sha: str) -> str | None:
        """Get repo SHA from the DB."""
        sha_query = Query()
        try:
            data = self.db.search(sha_query.sha == sha)
            if data:
                return data[0].get('sha')
        except Exception:
            self.log.exception(f'action=db-get-sha, sha={sha}')
            self.errors = True
            return None
        else:
            return None

    def download_template_file(self, item: FileMetadataModel):
        """Download the provided source file to the provided destination."""
        # directories do not have a download_url, skip when value is null
        if item.download_url is None:
            return

        # neither of the following options seem to work, but leaving here for future reference:
        # - headers={'Cache-Control': 'no-cache'}
        # - headers={'Cache-Control': 'max-age=0'}
        r = self.session.get(
            item.download_url, allow_redirects=True, headers={'Cache-Control': 'max-age=0'}
        )
        if not r.ok:
            self.log.error(
                f'action=download-template-file, url={r.request.url}, '
                f'status_code={r.status_code}, headers={r.headers}, '
                f'response={r.text or r.reason}'
            )
            ex_msg = (
                f'action=get-template-config, url={r.request.url}, status_code='
                f'{r.status_code}, reason={r.reason}'
            )
            raise RuntimeError(ex_msg)

        # get the relative path to the file and create the parent directory if it does not exist
        destination = item.relative_path
        if destination.parent.exists() is False:
            destination.parent.mkdir(parents=True, exist_ok=True)
        destination.open(mode='wb').write(r.content)
        self.log.info(f'action=download-template-file, file={destination}')

        # update manifest, using the path as the key for uniqueness
        self.template_manifest[item.path]['md5'] = self.file_hash(destination)

    @staticmethod
    def file_hash(fqfn: Path) -> str:
        """Return the file hash."""
        with fqfn.open(mode='rb') as fh:
            md5 = hashlib.md5()  # nosec
            while True:
                chunk = fh.read(8192)
                if not chunk:
                    break
                md5.update(chunk)
        return md5.hexdigest()

    def file_metadata_contents(
        self,
        branch: str,
        template_type: str,
        template_path: str | None = None,
        app_builder: bool = False,
    ) -> Generator[dict, None, None]:
        """Yield template contents."""
        url = self.file_metadata_url(template_type, template_path)
        params = {'ref': branch}
        r: Response = self.session.get(url, params=params)
        if not r.ok:
            self.log.error(
                f'action=get-contents, url={r.request.url}, '
                f'status_code={r.status_code}, headers={r.headers}, '
                f'response={r.text or r.reason}'
            )
            self.errors = True
        else:
            for content in r.json():
                # exclusion - this file is only needed for building App Builder templates
                if content.get('name') == '.appbuilderconfig' and app_builder is False:
                    continue

                # exclusions - files that should not be part of the App
                if content.get('name') in ['.gitignore', 'template.yaml']:
                    continue

                # rename gitignore to .gitignore
                if content.get('name') == 'gitignore':
                    content['name'] = '.gitignore'
                    content['path'] = '_app_common/.gitignore'

                yield content

    def file_metadata_model(
        self,
        branch: str,
        template_name: str,
        template_path: str,
        template_type: str,
        app_builder: bool = False,
    ) -> Generator[FileMetadataModel, None, None]:
        """Yield template contents."""
        for content in self.file_metadata_contents(
            branch, template_type, template_path, app_builder
        ):
            # add additional local metadata
            content['template_name'] = template_name or template_path
            content['template_type'] = template_type

            fmm = FileMetadataModel(**content)

            # set relative path, after all metadata has been added
            fmm.relative_path = self.item_relative_path(fmm)

            yield fmm

    def file_metadata_url(self, template_type: str, template_path: str | None = None) -> str:
        """Return the content url."""
        match template_path:
            case None:
                return f'{self.base_url}/contents/{template_type}'

            case '_app_common':
                return f'{self.base_url}/contents/{template_path}'

            case _:
                return f'{self.base_url}/contents/{template_type}/{template_path}'

    def get_template_config(
        self, template_name: str, template_type: str, branch: str = 'v2'
    ) -> TemplateConfigModel | None:
        """Return the data from the template.yaml file.

        This method will first check the cache for the template.yaml data. If the data is not in the
        cache, the template.yaml file will be downloaded from GitHub and the data will be cached.

        Failure to download the template.yaml file will result in a None return value to allow
        continued execution.
        """
        # special case for _app_common
        template_type = '_app_common' if template_name == '_app_common' else template_type

        self.log.info(
            f'action=get-template-config, type={template_type}, '
            f'template={template_name}, cache-valid={self.cache_valid}, branch={branch}'
        )

        # check cache
        if self.cache_valid is True:
            config = self.db_get_config(template_type, template_name)
            if config is not None:
                return config

        # download template.yaml contents
        url = self.get_template_config_url(branch, template_name, template_type)
        r = self.get_template_config_contents(branch, url)

        # process template.yaml contents
        try:
            template_config_data = yaml.safe_load(r.text)
            template_config_data.update({'name': template_name, 'type': template_type})
            config = TemplateConfigModel(**template_config_data)

            # upsert db
            self.db_add_config(config)
            self.log.debug(f'action=get-template-config, config={config}')
        except ValidationError as ex:
            self.log.exception(f'action=get-template-config, url={url}')
            Render.panel.warning(f'Could not parse template config file (url={url}).')

            self._log_validation_error(ex)
            return None
        else:
            return config

    def get_template_config_contents(self, branch: str, url: str) -> Response:
        """Return the contents of the template."""
        params = {}
        if branch:
            params['ref'] = branch

        r = self.session.get(url)
        self.log.debug(f'action=get-template-config, url={url}, status-code={r.status_code}')

        if not r.ok:
            self.log.error(
                f'action=get-template-config, url={r.request.url}, '
                f'status_code={r.status_code}, headers={r.headers}, '
                f'response={r.text or r.reason}'
            )
            self.errors = True
            Render.panel.failure(f'Failed to download template config file (url={url}).')

        return r

    def get_template_config_url(self, branch: str, template_name: str, template_type: str) -> str:
        """Return the URL for the template.yml file."""
        match template_name:
            case '_app_common':
                return f'{self.base_raw_url}/{branch}/_app_common/template.yaml'

            case _:
                return f'{self.base_raw_url}/{branch}/{template_type}/{template_name}/template.yaml'

    def get_template_contents(
        self,
        branch: str,
        data: dict[str, FileMetadataModel],  # recursively update data dict
        template_name: str,  # preserve the template name for recursion
        template_path: str,
        template_type: str,
        app_builder: bool,
    ) -> dict[str, FileMetadataModel]:
        """Get the contents of a template and allow recursion."""
        for item in self.file_metadata_model(
            branch, template_name, template_path, template_type, app_builder
        ):
            # process any files and recurse into any directories
            if item.type == 'file':
                # templates are hierarchical, overwrite previous values with new
                # values using relative path for as the identifier for the file
                data[str(item.relative_path)] = item

                # update manifest data, this will be used during
                # updates to determine if the file has changed
                self.template_manifest.setdefault(item.path, {})
                self.template_manifest[item.path]['sha'] = item.sha
            elif item.type == 'dir':
                nested_path = f"""{template_path}/{item.name}"""
                self.get_template_contents(
                    branch, data, template_name, nested_path, template_type, app_builder
                )

        return data

    def init(
        self, branch: str, template_name: str, template_type: str, app_builder: bool
    ) -> list[FileMetadataModel]:
        """Initialize an App with template files."""
        data = {}
        for template_parent_name in self.template_parents(template_name, template_type, branch):
            # template_parent_name is both the name and the path
            self.get_template_contents(
                branch, data, template_parent_name, template_parent_name, template_type, app_builder
            )
        return list(data.values())

    def item_relative_path(self, item: FileMetadataModel) -> Path:
        """Return the relative path to the item."""
        template_path = self.item_template_path(item)

        # handle nested files by stripping the type/template values from the path, the
        # remaining part is the relative path to the file to be used for read/write.
        _path = item.name
        if item.path.startswith(template_path):
            _path = item.path.replace(template_path, '')

        return Path(_path)

    @staticmethod
    def item_template_path(item: FileMetadataModel) -> str:
        """Return the template path."""
        if item.template_name == '_app_common':
            return f'{item.template_name}/'
        return f'{item.template_type}/{item.template_name}/'

    def list_(self, branch: str, template_type: str | None = None):
        """List template types."""
        template_types = self.template_types
        if template_type is not None:
            if template_type not in self.template_types:
                ex_msg = f'Invalid Types: {template_type}'
                raise ValueError(ex_msg)
            template_types = [template_type]

        for selected_type in template_types:
            for meta in self.file_metadata_contents(branch, selected_type):
                if meta['type'] == 'dir':
                    template_config = self.get_template_config(meta['name'], selected_type, branch)
                    if template_config is not None:
                        self.template_data.setdefault(selected_type, [])
                        self.template_data[selected_type].append(template_config)

    def load_template_manifest(self):
        """Write the template manifest file."""
        if self.template_manifest_fqfn.is_file():
            with self.template_manifest_fqfn.open(encoding='utf-8') as fh:
                try:
                    self.template_manifest = json.load(fh)
                except json.JSONDecodeError:
                    self.log.exception(
                        f'Failed loading template manifest: {self.template_manifest_fqfn}'
                    )
                    Render.panel.failure(
                        f'Failed loading template manifest: {self.template_manifest_fqfn}'
                    )

    @cached_property
    def project_sha(self) -> str | None:
        """Return the current commit sha for the tcex-app-templates project."""
        params = {'perPage': '1'}
        r: Response = self.session.get(f'{self.base_url}/commits', params=params)
        if not r.ok:
            self.log.error(
                f'action=get-project-sha, url={r.request.url}, '
                f'status_code={r.status_code}, headers={r.headers}, '
                f'response={r.text or r.reason}'
            )
            self.errors = True
            ex_msg = (
                f'action=get-template-config, url={r.request.url}, status_code='
                f'{r.status_code}, reason={r.reason}'
            )
            raise RuntimeError(ex_msg)

        try:
            commits_data = r.json()
        except Exception:
            return None

        # get current sha
        return commits_data[0].get('sha')

    @cached_property
    def session(self) -> Session:
        """Return session object"""
        session = Session()
        session.headers.update({'Cache-Control': 'no-cache'})
        session.proxies = proxies(
            proxy_host=self.proxy_host,
            proxy_port=self.proxy_port,
            proxy_user=self.proxy_user,
            proxy_pass=self.proxy_pass,
        )

        # add auth if set (typically not require since default site is public)
        if self.gh_username is not None and self.gh_password is not None:
            session.auth = HTTPBasicAuth(self.gh_username, self.gh_password)

        return session

    # @property
    # def template_manifest(self) -> dict:
    #     """Write the template manifest file."""
    #     if self.template_manifest_fqfn.is_file():
    #         with self.template_manifest_fqfn.open(encoding='utf-8') as fh:
    #             try:
    #                 return json.load(fh)
    #             except json.JSONDecodeError:
    #                 self.log.error(
    #                     f'Failed loading template manifest: {self.template_manifest_fqfn}'
    #                 )
    #                 Render.panel.failure(
    #                     f'Failed loading template manifest: {self.template_manifest_fqfn}'
    #                 )
    #     return {}

    def template_manifest_write(self):
        """Write the template manifest file."""
        with self.template_manifest_fqfn.open(mode='w', encoding='utf-8') as fh:
            fh.write(json.dumps(self.template_manifest, indent=2, sort_keys=True))
            fh.write('\n')

    def template_parents(
        self, template_name: str, template_type: str, branch: str = 'v2'
    ) -> list[str]:
        """Return all parents for the provided template."""
        # get the config for the requested template
        template_config = self.get_template_config(template_name, template_type, branch)

        # fail if template config can't be found
        if template_config is None:
            self.log.error(
                f'template-type={template_type}, template-name={template_name}, '
                f'template-config={template_config}'
            )
            Render.panel.failure(
                'Failed retrieving template.yaml: \n'
                f'template-type={template_type}, template-name={template_name}'
                '\n\nTry running "tcex list" to get valid template types and names.'
            )

        app_templates = []
        # iterate over each parent template
        for parent in template_config.template_parents or []:
            parent_config = self.get_template_config(parent, template_type, branch)
            if parent_config is None:
                continue

            # update templates
            app_templates.extend(
                [t for t in parent_config.template_parents if t not in app_templates]
            )

            # add parent after parent->parents have been added
            app_templates.extend(
                [t for t in template_config.template_parents if t not in app_templates]
            )

        # add this current template last
        app_templates.append(template_name)

        return app_templates

    @property
    def template_to_prefix_map(self) -> dict[str, str]:
        """Return the defined template types."""
        return {
            'api_service': 'tcva',
            'feed_api_service': 'tcvf',
            'organization': 'tc',
            'playbook': 'tcpb',
            'trigger_service': 'tcvc',
            'web_api_service': 'tcvp',
            'webhook_trigger_service': 'tcvw',
        }

    @property
    def template_types(self) -> list[str]:
        """Return the defined template types."""
        return [
            'api_service',
            'external',
            'feed_api_service',
            'organization',
            'playbook',
            'trigger_service',
            # 'web_api_service',
            'webhook_trigger_service',
        ]

    def update(
        self,
        branch: str,
        template_name: str | None = None,
        template_type: str | None = None,
        ignore_hash=False,
    ) -> list[FileMetadataModel]:
        """Initialize an App with template files."""
        # update tcex.json model
        if template_name is not None:
            self.app.tj.model.template_name = template_name
        if template_type is not None:
            self.app.tj.model.template_type = template_type

        # retrieve ALL template contents
        data: dict[str, FileMetadataModel] = {}

        # for App builder, both template_name and template_type were made optional in the
        # model, but in reality these fields are required.  This is a temporary fix to
        # allow App Builder to work with older Apps that do not have these fields set.
        for template_parent_name in self.template_parents(
            self.app.tj.model.template_name,  # type: ignore
            self.app.tj.model.template_type,  # type: ignore
            branch,  # type: ignore
        ):
            # template_parent_name is both the name and the path
            self.get_template_contents(
                branch,
                data,
                template_parent_name,
                template_parent_name,
                self.app.tj.model.template_type,  # type: ignore
                app_builder=False,
            )

        # determine which files should be downloaded
        downloads = []
        for item in data.values():
            # skip files if it has not changed
            if (
                item.relative_path.is_file()
                and ignore_hash is False
                and self.update_item_check_hash(item.relative_path, item) is False
            ):
                continue

            # is the file a template file and dev says overwrite
            if self.update_item_prompt(branch, item) and item.relative_path.is_file() is True:
                response = Render.prompt.input(
                    f'Overwrite existing [{self.accent}]{item.relative_path}[/{self.accent}] file?',
                    prompt_default=f' (Default: [{self.accent}]no[/{self.accent}])',
                )
                if response != 'yes':
                    continue

            downloads.append(item)
            self.template_manifest.setdefault(item.path, {})
            self.template_manifest[item.path]['sha'] = item.sha

        return downloads

    def update_item_check_hash(self, fqfn: Path, item: FileMetadataModel) -> bool:
        """Check if the file hash has changed since init or last update."""
        file_hash = self.file_hash(fqfn)
        if self.template_manifest.get(item.path, {}).get('md5') != file_hash:
            self.log.debug(
                f"""action=update-check-hash, template-file={item.name}, """
                'check=hash-check, result=hash-has-not-changed'
            )
            return True
        return False

    def update_item_prompt(self, branch: str, item: FileMetadataModel) -> bool:
        """Update the prompt value for the provided item."""
        template_config = self.get_template_config(
            item.template_name,
            self.app.tj.model.template_type,  # type: ignore
            branch,  # type: ignore
        )

        # enforce prompt if template config can't be found
        if template_config is None:
            return True

        # determine if file requires user prompt
        return str(item.relative_path) not in (template_config.template_files or [])

    def update_tcex_json(self):
        """Update the tcex.json file."""
        self.app.tj.model.template_repo_hash = self.project_sha
        self.app.tj.write()
