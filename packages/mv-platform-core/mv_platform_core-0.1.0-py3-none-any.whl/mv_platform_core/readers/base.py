from abc import ABC, abstractmethod
from typing import Union

from pyspark.sql import SparkSession, DataFrame

class DataReader(ABC):
    @abstractmethod
    def read(self, spark: SparkSession) -> Union[DataFrame | dict]:
        pass


