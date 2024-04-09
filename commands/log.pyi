from .base_command import ICommand
from typing import Optional

class Log(ICommand):
    def __init__(self, username: str, path: str = "C:/", extension: str = '.log', user_data: Optional[list] = None,
                 clean: bool = True):

        self.path = None
        self.extension = None
        self.__tempdir = None
        self.today = Optional[str]
        self.user_data = Optional[list]
        self.clean = clean

    def __del__(self):
        pass

    def create_tempfile(self) -> Optional[str]:
        pass

    def edit_tempfile(self, command: str = None):
        pass

    def has_tempfile_edited(self, file_path, last_checked_time) -> bool:
        pass

    def create_log_file(self, path, extension) -> Optional[str]:
        pass

    def clean_tempfiles(self):
        pass

    def generate_id(self):
        pass

    def format_log(self, content: str):
        pass

    def execute(self) -> Optional[str]:
        pass
