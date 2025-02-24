from abc import ABC, abstractmethod
from typing import IO


class BaseFSAccess(ABC):
    @abstractmethod
    def get_file_paths(self, directory: str, file_type: str) -> list[str]:
        pass

    @abstractmethod
    def open(self, path: str) -> IO:
        # needs to be a context manager (handle cleanup/closing of file after reading)
        pass
