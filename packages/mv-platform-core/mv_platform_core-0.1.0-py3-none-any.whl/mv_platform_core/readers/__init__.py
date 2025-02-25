from .bronze import BronzeReader
from .base import DataReader
class ReaderFactory:
    _strategies = {
        "bronze": BronzeReader
    }

    @classmethod
    def create_reader(cls, reader_type: str, **kwargs) -> DataReader:
        return cls._strategies[reader_type](**kwargs)
