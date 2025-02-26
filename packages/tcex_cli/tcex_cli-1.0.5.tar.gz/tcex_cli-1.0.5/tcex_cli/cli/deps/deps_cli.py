"""TcEx Framework Module"""

# standard library
import contextlib
import logging
import os
import shutil
import subprocess  # nosec
import sys
from datetime import UTC, datetime
from functools import cached_property
from importlib.metadata import version as get_version
from pathlib import Path
from urllib.parse import quote

# third-party
from semantic_version import Version

# first-party
from tcex_cli.cli.cli_abc import CliABC
from tcex_cli.cli.model.key_value_model import KeyValueModel
from tcex_cli.render.render import Render

# get logger
_logger = logging.getLogger(__name__.split('.', maxsplit=1)[0])


class DepsCli(CliABC):
    """Dependencies Handling Module."""

    def __init__(
        self,
        app_builder: bool,
        branch: str,
        no_cache_dir: bool,
        pre: bool,
        proxy_host: str | None,
        proxy_port: int | None,
        proxy_user: str | None,
        proxy_pass: str | None,
    ):
        """Initialize instance properties."""
        super().__init__()
        self.app_builder = app_builder
        self.branch = branch
        self.no_cache_dir = no_cache_dir
        self.pre = pre
        self.proxy_host = self._process_proxy_host(proxy_host)
        self.proxy_port = self._process_proxy_port(proxy_port)
        self.proxy_user = self._process_proxy_user(proxy_user)
        self.proxy_pass = self._process_proxy_pass(proxy_pass)

        # properties
        self.deps_dir_tests = self.app_path / 'deps_tests'
        self.env = self._env
        self.latest_version = None
        self.log = _logger
        self.output: list[KeyValueModel] = []
        self.proxy_enabled = False
        self.requirements_fqfn_branch = None
        self.requirements_lock = self.app_path / 'requirements.lock'
        self.requirements_lock_tests = self.app_path / 'tests' / 'requirements.lock'
        self.requirements_txt = self.app_path / 'requirements.txt'
        self.requirements_txt_tests = self.app_path / 'tests' / 'requirements.txt'
        self.start_time = datetime.now(tz=UTC)

        # update tcex.json
        self.app.tj.update.multiple()

    def _build_command(self, deps_dir: Path, requirements_file: Path) -> list[str]:
        """Build the pip command for installing dependencies."""
        tool = 'pip'

        uv_executable = shutil.which('uv')
        if uv_executable and self.is_executable(Path(uv_executable)):
            tool = 'uv'
            exe_command = [
                uv_executable,
                'pip',
                'install',
            ]
        else:
            exe_command = [
                str(self.python_executable),
                '-m',
                'pip',
                'install',
                '--ignore-installed',
            ]

        exe_command.extend(
            [
                '-r',
                str(requirements_file),
                '--quiet',
                '--target',
                deps_dir.name,
            ]
        )

        if self.no_cache_dir:
            if tool == 'pip':
                exe_command.append('--no-cache-dir')
            elif tool == 'uv':
                exe_command.append('--no-cache')
            self.output.append(KeyValueModel(key='Allow cached-dir Release', value='False'))
        if self.pre:
            exe_command.append('--pre')
            self.output.append(KeyValueModel(key='Allow "pre" Release', value='True'))
        if self.proxy_enabled:
            # trust the pypi hosts to avoid ssl errors
            trusted_hosts = ['pypi.org', 'pypi.python.org', 'files.pythonhosted.org']

            for host in trusted_hosts:
                exe_command.append('--trusted-host')
                exe_command.append(host)

        return exe_command

    @property
    def _env(self):
        """Return the environment variables."""
        _env = os.environ.copy()

        # add ci env
        ci_token = os.getenv('CI_JOB_TOKEN')
        if ci_token:
            _env.update({'CI_JOB_TOKEN': ci_token})

        return _env

    @staticmethod
    def is_executable(executable: Path):
        """Check if a file exists and is executable, then attempts to run it."""
        if executable.is_file() and os.access(executable, os.X_OK):
            try:
                subprocess.run(  # nosec
                    [executable, '--help'],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                return False
            else:
                return True
        return False

    def _remove_previous(self, path: Path):
        """Remove previous deps directory recursively."""
        shutil.rmtree(str(path), ignore_errors=True)

    def configure_proxy(self):
        """Configure proxy settings using environment variables."""
        if os.getenv('HTTP_PROXY') or os.getenv('HTTPS_PROXY'):
            # don't change proxy settings if the OS already has them configured.
            return

        if self.proxy_host is not None and self.proxy_port is not None:
            # proxy url without auth
            proxy_pass_ = None
            if self.proxy_pass is not None and hasattr(self.proxy_pass, 'value'):
                proxy_pass_ = self.proxy_pass.value
            proxy_url = f'{self.proxy_host}:{self.proxy_port}'
            if self.proxy_user is not None and proxy_pass_ is not None:
                proxy_user = quote(self.proxy_user, safe='~')
                proxy_pass_ = quote(proxy_pass_, safe='~')

                # proxy url with auth
                proxy_url = f'{proxy_user}:{proxy_pass_}@{proxy_url}'

            # update proxy properties
            self.proxy_enabled = True
            self.env.update(
                {
                    'HTTP_PROXY': f'http://{proxy_url}',
                    'HTTPS_PROXY': f'http://{proxy_url}',
                }
            )

            # add proxy setting to output
            self.output.append(
                KeyValueModel(
                    key='Using Proxy Server', value=f'{self.proxy_host}:{self.proxy_port}'
                )
            )

    def create_requirements_lock(self, contents: str, requirements_file: Path):
        """Create the requirements.lock file."""
        with requirements_file.open(mode='w', encoding='utf-8') as fh:
            # add lock file creation to output
            relative_path = requirements_file.relative_to(self.app_path)
            relative_path = f'[{self.accent}]{relative_path}[/{self.accent}]'
            self.output.append(KeyValueModel(key='Lock File Created', value=str(relative_path)))
            fh.write(contents)
            fh.write('')

    def download_deps(self, exe_command: list[str]):
        """Download the dependencies (run pip)."""
        # recommended -> https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program
        p = subprocess.Popen(
            exe_command,
            shell=False,  # nosec
            # stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
        )
        _, err = p.communicate()

        if p.returncode != 0:
            # display error
            err = err.decode('utf-8')
            Render.panel.failure(f'Failure: {err}')

    def install_deps(self):
        """Install Required Libraries using pip."""
        error = False  # track if any errors have occurred and if so, don't create lock file.

        # check for requirements.txt
        if not self.requirements_fqfn.is_file():
            Render.panel.failure(f'A {self.requirements_fqfn} file is required to install modules.')

        # remove deps directory from previous runs
        self._remove_previous(self.deps_dir)

        # build the sub process command

        # support temp (branch) requirements.txt file
        exe_command = self._build_command(self.deps_dir, self.requirements_fqfn)

        # display command setting
        self.output.append(KeyValueModel(key='Pip Command', value=f'{" ".join(exe_command)}'))

        if self.app_builder is False:
            with Render.progress_bar_deps() as progress:
                progress.add_task('Downloading Dependencies', total=None)

                self.download_deps(exe_command)
        else:
            self.download_deps(exe_command)

        # if self.requirements_fqfn_branch:
        #     # remove temp requirements.txt file
        #     self.requirements_fqfn_branch.unlink()

        if self.requirements_lock.exists() is False:
            if error:
                Render.panel.warning('Not creating requirements.lock file due to errors.')
            else:
                contents = self.requirements_lock_contents(self.deps_dir)
                self.create_requirements_lock(contents, self.requirements_lock)

        if self.app_builder is True and self.app.ij.model.sdk_version < Version('4.0.0'):
            # the lib_version directory
            python_version = self.target_python_version or '3.6.15'
            lib_version = Path(f'lib_{python_version}')

            # remove previous build director
            if lib_version.is_symlink():
                lib_version.unlink()
            elif lib_version.is_dir():
                shutil.rmtree(lib_version)

            # create symlink: lib_latest -> lib_version
            lib_version.symlink_to(self.deps_dir, target_is_directory=True)

        # display tcex version
        with contextlib.suppress(Exception):
            self.output.append(KeyValueModel(key='App TcEx Version', value=get_version('tcex')))

    def install_deps_tests(self):
        """Install tests dependencies."""
        if self.requirements_txt_tests.exists():
            error = False  # track if any errors have occurred and if so, don't create lock file.

            # remove deps directory from previous runs
            self._remove_previous(self.deps_dir_tests)

            # build the sub process command
            exe_command = self._build_command(self.deps_dir_tests, self.requirements_fqfn_tests)

            # display command setting
            self.output.append(
                KeyValueModel(key='Tests Pip Command', value=f'{" ".join(exe_command)}')
            )

            if self.app_builder is False:
                with Render.progress_bar_deps() as progress:
                    progress.add_task('Downloading Tests Dependencies', total=None)

                    self.download_deps(exe_command)

            if self.requirements_lock_tests.exists() is False:
                if error:
                    Render.panel.warning(
                        f'Not creating {self.requirements_fqfn_tests} file due to errors.'
                    )
                else:
                    contents = self.requirements_lock_contents(self.deps_dir_tests)
                    self.create_requirements_lock(contents, self.requirements_lock_tests)

        runtime = datetime.now(tz=UTC) - self.start_time
        self.output.append(
            KeyValueModel(key='Total Runtime', value=f'{round(runtime.seconds, 2)}s')
        )

    @cached_property
    def python_executable(self) -> Path:
        """Return the python executable."""
        tcex_python_path = os.getenv('TCEX_PYTHON_PATH', None)
        return Path(tcex_python_path) / 'python' if tcex_python_path else Path(sys.executable)

    @cached_property
    def requirements_fqfn(self) -> Path:
        """Return the appropriate requirements.txt file."""
        if self.requirements_lock.exists():
            _requirements_file = self.requirements_lock
        else:
            _requirements_file = self.requirements_txt

        # add deps directory to output
        self.output.append(KeyValueModel(key='Dependencies Directory', value=self.deps_dir.name))

        # add requirements file to output
        relative_path = _requirements_file.relative_to(self.app_path)
        self.output.append(
            KeyValueModel(
                key='Requirement File',
                value=f'[{self.accent}]{relative_path}[/{self.accent}]',
            )
        )
        return _requirements_file

    @cached_property
    def requirements_fqfn_tests(self) -> Path:
        """Return the appropriate requirements.txt file."""
        if self.requirements_lock_tests.exists():
            _requirements_file_tests = self.requirements_lock_tests
        else:
            _requirements_file_tests = self.requirements_txt_tests

        # add deps directory to output
        self.output.append(
            KeyValueModel(key='Tests Dependencies Directory', value=self.deps_dir_tests.name)
        )

        # add requirements file to output
        relative_path = _requirements_file_tests.relative_to(self.app_path)
        self.output.append(
            KeyValueModel(
                key='Tests Requirement File',
                value=f'[{self.accent}]{relative_path}[/{self.accent}]',
            )
        )
        return _requirements_file_tests

    def requirements_lock_contents(self, deps_dir: Path) -> str:
        """Return the Python packages for the provided directory."""
        cmd = f'pip freeze --path "{deps_dir}"'
        self.log.debug(f'event=get-requirements-lock-data, cmd={cmd}')
        try:
            output = subprocess.run(  # noqa: PLW1510
                cmd,
                shell=True,
                capture_output=True,  # nosec
            )
        except Exception:
            self.log.exception('event=pip-freeze')
            Render.panel.failure('Failure: could not get requirements lock data.')

        if output.returncode != 0:
            self.log.error(f'event=pip-freeze, stderr="{output.stderr}"')

        return '\n'.join(sorted(output.stdout.decode('utf-8').splitlines()))

    @property
    def target_python_version(self) -> Version | None:
        """Return the python version that deps/pip will run with.

        On App builder this could be a different version than this CLI command is running with.
        """
        version = None
        try:
            p = subprocess.Popen(  # nosec
                [self.python_executable, '--version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, _ = p.communicate()

            if p.returncode == 0:
                output = stdout.decode('utf-8').strip().split(' ')[1]
                version = Version(output)
        except Exception:
            self.log.exception('event=get-python-version')

        return version

    def validate_python_version(self):
        """Validate the python version."""
        tpv = self.target_python_version
        if tpv is not None:
            target_major_minor = f'{tpv.major}.{tpv.minor}'

            # temp logic until all TC instances are on version 7.2
            language_major_minor = self.app.ij.model.language_version
            if isinstance(language_major_minor, Version):
                language_major_minor = f'{language_major_minor.major}.{language_major_minor.minor}'  # type: ignore

            if target_major_minor != language_major_minor:
                Render.panel.failure(
                    (
                        ' • The App languageVersion defined in the install.json '
                        'file does not match the current Python version.\n'
                        f' • defined-version={language_major_minor} '
                        f'!= current-version={target_major_minor}.'
                    ),
                )
