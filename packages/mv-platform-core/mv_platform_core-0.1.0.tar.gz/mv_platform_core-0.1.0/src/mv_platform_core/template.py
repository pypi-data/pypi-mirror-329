from abc import ABC, abstractmethod
from pyspark.sql import DataFrame, SparkSession

from mv_platform_core import DataReader, DataWriter


class DataProcessingTemplate(ABC):

    def __init__(self,
                 reader: DataReader,
                 writer: DataWriter,
                 spark: SparkSession = None,
                 ):
        self.spark = spark if spark else SparkSession.builder.getOrCreate()
        self.reader = reader
        self.writer = writer

    def execute_pipeline(self):
        input = self.read_data()
        processed_df = self.transform(input)
        cleaned_df = self.reject(processed_df)
        self.write_output(cleaned_df)

    def read_data(self):
        return self.reader.read(self.spark)

    @abstractmethod
    def transform(self, input) -> DataFrame:
        pass

    def reject(self, df: DataFrame) -> DataFrame:
        return df

    def write_output(self, df: DataFrame) -> None:
        self.writer.write(df)
