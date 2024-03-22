from .base_command import ICommand
from typing import Optional
import string
import random
import os
import subprocess
import time
import tempfile
import datetime


class Log(ICommand):

    def __init__(self, username: str, path: str = "C:/", extension: str = '.log'):
        self.username = username
        self.path = path
        self.extension = extension

    def __del__(self):
        pass

    def create_tempfile(self) -> Optional[str]:
        tempdir_path = tempfile.gettempdir()
        self.__tempdir = os.path.join(tempdir_path, "xz-log")

        # Create the temporary directory if it doesn't exist
        if not os.path.exists(self.__tempdir):
            os.makedirs(self.__tempdir)

        # Create a temporary file inside the temporary directory
        with tempfile.TemporaryFile(dir=self.__tempdir, prefix='log_', delete=False, suffix='.tmp') as temp_file:
            return temp_file.name

    def edit_tempfile(self, command: str = None):
        try:
            __temp_file = self.create_tempfile() if self.create_tempfile() is not None else None
            print(__temp_file)
            # Checking if user prefers special editor
            command = command if command is not None else "start"
            subprocess.run([command, __temp_file], shell=True)
            last_checked_time = time.time()
            # Check if tempfile has been updated
            while True:
                if self.has_tempfile_edited(__temp_file, last_checked_time):
                    print("File has been updated")
                    break
                print("File has NOT been updated")
                time.sleep(1)

            time.sleep(0.2)
            # The file has been updated

            with open(__temp_file, "r") as f:
                content = f.read()
            return content
        except Exception as e:
            print("edit_tempfile error")
            print(e)
            return None

    def has_tempfile_edited(self, file_path, last_checked_time) -> bool:
        try:
            if not os.path.exists(file_path):
                raise Exception(f"File {file_path} does not exist")
            return os.path.getmtime(file_path) > last_checked_time
        except:
            print("has_tempfile_edited error")
            pass

    def create_log_file(self, path, extension) -> Optional[str]:
        # Get everyday date
        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        log_dir = os.path.join(path, 'logs')
        # Create the logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        try:
            log_file = os.path.join(log_dir, f'{today}{extension}')
            # Create a log file with the content from tempfile
            _content = self.edit_tempfile()
            print(_content)
            with open(log_file, 'w') as f:
                f.write(_content)
            return log_file
        except Exception as e:
            print(e)
            return None

    def clean_tempfiles(self):
        try:
            __tempfiles: list = os.listdir(self.__tempdir)
            # Remove all files in the temporary directory
            if os.path.exists(self.__tempdir) and not len(__tempfiles) == 0:
                for file in __tempfiles:
                    os.remove(os.path.join(self.__tempdir, file))
        except:
            pass

    def format_log(self):
        pass

    def execute(self) -> Optional[str]:
        log_file: Optional[str] = self.create_log_file(self.path, self.extension)
        self.clean_tempfiles()
        return log_file