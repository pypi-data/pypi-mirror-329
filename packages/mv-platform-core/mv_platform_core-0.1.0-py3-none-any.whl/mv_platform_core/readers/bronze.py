from typing import Union
from pyspark.sql import SparkSession, DataFrame

from .base import DataReader


class BronzeReader(DataReader):
    spark: SparkSession

    def __init__(self, tables: dict):
        self.tables = tables

    def read(self, spark: SparkSession) -> Union[DataFrame | dict]:
        self.spark = spark
        for _ in self._create_temp_views():
            pass
        return "success"

    def _create_temp_views(self):
        for table_name, table_info in self.tables.items():
            temp_view_name = f"temp_{table_name}"
            bronze_table_name = table_info['table_name']
            separated_primary_keys = ", ".join(table_info['primary_keys'])
            filter_column = table_info['filter_column']
            filter_condition = table_info['filter_condition']

            yield self._create_view_by_column(
                temp_view_name,
                bronze_table_name,
                separated_primary_keys,
                filter_column,
                filter_condition
            )

    def _create_view_by_column(self,
                               temp_view_name,
                               bronze_table_name,
                               separated_primary_keys,
                               filter_column,
                               filter_condition):
        latest_data_query = f"""SELECT * FROM (SELECT *,
                        RANK() OVER (PARTITION BY {separated_primary_keys} ORDER BY {filter_column} DESC) as rnum
                        FROM {bronze_table_name} WHERE {filter_condition}) t
                        WHERE rnum = 1"""
        self.spark.sql(latest_data_query).createOrReplaceTempView(temp_view_name)
