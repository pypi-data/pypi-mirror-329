import enum
import gitlab
import logging
import os
import typing

from platformdirs import PlatformDirs

if typing.TYPE_CHECKING:
    from gitlab.v4.objects import Project

logger = logging.getLogger('typeinfo_parser.utils')


Dirs = PlatformDirs("SystemG3Visu", ensure_exists=True)


class AccessToken:

    @staticmethod
    def get() -> str:
        path = os.path.join(Dirs.user_data_dir, ".token")
        if not os.path.isfile(path):
            logger.warning('Token file was not found at "%s".', path)
            return ''
        with open(path, "r", encoding='utf-8') as file:
            return file.read().strip()

    @staticmethod
    def set(token: str) -> None:
        path = os.path.join(Dirs.user_data_dir, ".token")
        with open(path, "w", encoding='utf-8') as file:
            file.write(token)

    @staticmethod
    def is_valid(token: str) -> bool:
        try:
            with gitlab.Gitlab(SitesFileDownloader.BASE_URL, token) as gl:
                gl.projects.get(SitesFileDownloader.PROJECT_ID)
                return True
        except gitlab.GitlabAuthenticationError:
            return False
        except gitlab.GitlabGetError:  # project may be invisible
            return False               # without the correct access token


def prompt_token_until_valid() -> str:
    while True:
        try:
            token = input("Invalid token. Enter your Gitlab access token: ")
            if AccessToken.is_valid(token):
                break
        except KeyboardInterrupt:
            raise SystemExit(1)
        except Exception as exc:
            logger.error('Unexpected error occured: {%s}', exc)
    return token


def ensure_token_set() -> str:
    token = AccessToken.get()
    if not token or not AccessToken.is_valid(token):
        token = prompt_token_until_valid()
        AccessToken.set(token)
    return token


class SitesFilePaths(enum.StrEnum):
    """Relative paths to the files in the repository."""
    TYPE_INFO = "sites/_files/typeInfo.cpon"
    """Path to the `visu-types-g3.svg` file in the repository."""
    VISU_TYPES_G3 = "sites/_files/predefined-visu-types/visu-types-g3.svg"
    """Path to the `visu-types-g3.svg` file in the repository."""


class SitesFileDownloader:
    BASE_URL: str = "https://gitlab.com"
    """Base URL where the repository is hosted."""
    PROJECT_ID: int = 9492559
    """ID of the project repository on Gitlab."""

    @staticmethod
    def _get_contents(
        project: 'Project', file_path: str, branch: str, decode: bool
    ) -> str | bytes | None:
        """
        Retrieve the contents of a file from a project.

        Args:
            project (Project): Project object.
            file_path (str): Path to the file in the project repository.
            branch (str): Branch name.

        Returns:
            bytes: The contents of the file.
        """
        try:
            logger.info(f'Retrieving file from "{file_path}".')
            contents = project.files.raw(file_path=file_path, ref=branch)
            if not isinstance(contents, bytes):
                raise TypeError(
                    f'Unexpected file data type: "{type(contents).__name__}" '
                    f'(expected type "bytes")'
                    )
            if decode:
                return contents.decode()
            return contents
        except gitlab.GitlabGetError:
            logger.error('Failed to retrieve file data from "%s".', file_path)
        except gitlab.GitlabAuthenticationError:
            project_name = project.asdict().get("name", "UNKNOWN_PROJECT")
            logger.error('Authentication error to project "%s".', project_name)
        except Exception as exc:
            logger.error(
                'Unexpected error occured while retrieving file contents: '
                '{%s}', exc
                )
        return None

    @staticmethod
    def _extract_file_name(path: str) -> str:
        _, file_name = os.path.split(path)
        return file_name

    @staticmethod
    def _check_save_to_path(
        file_name: str, save_to: str, overwrite_if_exists: bool
    ) -> str:
        logger.info('Ensuring local path "%s" exists.', save_to)
        os.makedirs(save_to, exist_ok=True)
        file_path = os.path.join(save_to, file_name)
        if os.path.isfile(file_path):
            msg = f'File "{file_name}" already exists in "{save_to}"'
            if overwrite_if_exists:
                msg += ', but will be overwritten.'
                logger.warning(msg)
            else:
                msg += '.'
                raise FileExistsError(msg)
        return file_path

    def read(
        self,
        file_path: str,
        branch: str = 'master',
        access_token: str | None = None,
        decode: bool = True
    ) -> str | bytes | None:
        """Read the contents of a file from the repository.

        Args:
            file_path (str): Path to the file in the repository.
            branch (str, optional): Reference Branch name.
                Defaults to 'master'.
            access_token (str | None, optional): Gitlab access token.
            decode (bool, optional): Whether to decode the file contents from
                bytes to string. Defaults to True.

        Returns:
            str | bytes | None: File contents. If the file was not found or
                an error occured, None is returned.
        """
        access_token = access_token or AccessToken.get()
        logger.info(f'Initializing a Gitlab instance for "{self.BASE_URL}"')
        with gitlab.Gitlab(self.BASE_URL, access_token) as gl:
            logger.info(f"Retrieving the project with id={self.PROJECT_ID}")
            project = gl.projects.get(self.PROJECT_ID)
            contents = self._get_contents(project, file_path, branch, decode)
        return contents

    def download(
        self,
        file_path: str,
        branch: str = 'master',
        save_to: str = os.getcwd(),
        overwrite_if_exists: bool = False
    ) -> None:
        """Download a file from the repository.

        Args:
            file_path (str): Path to the file in the repository.
            branch (str, optional): Reference Branch name.
                Defaults to 'master'.
            save_to (str, optional): Local path to save the file to.
                Defaults to the current working directory.
            overwrite_if_exists (bool, optional): Whether to overwrite the file
                if it already exists in the save_to directory.
                Defaults to False.
        """
        file_name = self._extract_file_name(file_path)
        if not file_name:
            logger.error('File name cannot be empty.')
            return
        try:
            local_path = self._check_save_to_path(
                file_name, save_to, overwrite_if_exists
                )
        except FileExistsError as err:
            logger.error(err)
            return
        contents = self.read(file_path, branch, decode=False)
        if contents is None:
            logger.error('Failed to save file contents to "%s".', local_path)
            return
        try:
            logger.info('Saving file contents to "%s".', local_path)
            assert isinstance(contents, bytes)
            with open(local_path, 'wb') as file:
                file.write(contents)
        except Exception as exc:
            logger.error(
                'Failed to save file contents to "%s" (%s).', local_path, exc
                )
