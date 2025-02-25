from pyspark.sql import DataFrame, SparkSession

from mv_platform_core.writers import DataWriter


class ScdOneWriter(DataWriter):

    def __init__(self, as_of_date,destination, spark: SparkSession):
        super().__init__(spark)
        self.as_of_date = as_of_date
        self.destination = destination

    def write(self, df: DataFrame) -> None:
        self._write_as_delta(df, {"replaceWhere": f"as_of_date = '{self.as_of_date}'"}, destination=self.destination)

    def _write_as_delta(self,
            df: DataFrame,
            options: dict[str, str] = {},
            **kwargs
    ) -> None:
        destination = kwargs.get("destination")
        df.write.format("delta").mode("overwrite").options(**options).save(destination)
