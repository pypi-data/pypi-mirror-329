from .base import DataWriter
from .silver import ScdOneWriter


class WriterFactory:
    _strategies = {
        "scd_one": ScdOneWriter
    }

    @classmethod
    def create_writer(cls, writer_type: str, **kwargs) -> DataWriter:
        return cls._strategies[writer_type](**kwargs)
