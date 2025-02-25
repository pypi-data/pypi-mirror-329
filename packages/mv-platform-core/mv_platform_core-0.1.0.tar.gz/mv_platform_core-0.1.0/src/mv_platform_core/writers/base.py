from abc import ABC, abstractmethod
from pyspark.sql import DataFrame, SparkSession

class DataWriter(ABC):

    def __init__(self, spark: SparkSession):
        self.spark = spark

    @abstractmethod
    def write(self, df: DataFrame) -> None:
        pass
