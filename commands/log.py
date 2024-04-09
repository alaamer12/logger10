from .base_command import ICommand
from typing import Optional
# import string
# import random
import os
import subprocess
import time
import tempfile
import datetime
# from rich import table
# from rich.console import Console

today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')


class Log(ICommand):

    def __init__(self, path: str = "C:/", extension: str = '.log', user_data: Optional[list] = None,
                 date: str = today,
                 clean: bool = True,
                 override: bool = False
                 ):
        self.clean = clean
        self.user_data = user_data
        self.path = path
        self.extension = extension
        self.today = date
        self.__tempdir = None
        self.override = override

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

    @staticmethod
    def has_tempfile_edited(file_path, last_checked_time) -> bool:
        try:
            if not os.path.exists(file_path):
                raise Exception(f"File {file_path} does not exist")
            return os.path.getmtime(file_path) > last_checked_time
        except Exception as e:
            print("has_tempfile_edited error")
            print(e)

    def create_log_file(self, path, extension) -> Optional[str]:
        # Get everyday date
        log_dir = os.path.join(path, 'logs')
        # Create the logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        try:
            log_file = os.path.join(log_dir, f'{self.today}{extension}')
            # Create a log file with the content from tempfile
            _content = self.edit_tempfile()

            # Format the log content and write it to the log file
            _modified_content = self.format_log(_content)
            with open(log_file, 'w') as f:
                f.write(_modified_content)
            return log_file
        except Exception as e:
            raise e

    def clean_tempfiles(self):
        try:
            __tempfiles: list = os.listdir(self.__tempdir)
            # Remove all files in the temporary directory
            if os.path.exists(self.__tempdir) and not len(__tempfiles) == 0:
                for file in __tempfiles:
                    os.remove(os.path.join(self.__tempdir, file))
        except Exception as e:
            print(e)
            pass

    # def generate_id(self):
    #     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))[:2]

    # TODO:
    def format_log(self, content: str):
        the_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        # u = '-' * 100
        x = 'x' * 45 + (self.today or '') + 'x' * 45
        # w = '-' * 100
        # z = u + '\n' + x + '\n' + w
        user_data_parts = [part if part is not None else '' for part in self.user_data]
        userdata = "[" + the_time + "]\t" + "\t".join(user_data_parts)
        modified_content = userdata + "\n\n" + content + "\n\n" + x  # Or z
        return modified_content

    def execute(self) -> Optional[str]:
        log_file: Optional[str] = self.create_log_file(self.path, self.extension)
        if self.clean:
            self.clean_tempfiles()
        print(f"Log file created: {log_file}")
        return log_file
