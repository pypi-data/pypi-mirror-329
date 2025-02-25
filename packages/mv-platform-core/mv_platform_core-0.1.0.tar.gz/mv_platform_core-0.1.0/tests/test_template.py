import unittest
from unittest.mock import Mock, patch

from pyspark.sql import DataFrame, SparkSession

from libs.core.src.mv_platform_core.template import DataProcessingTemplate
from libs.core.src.mv_platform_core.readers.base import DataReader
from libs.core.src.mv_platform_core.writers.base import DataWriter


class TestTemplatePipeline(unittest.TestCase):

    class DummyPipeline(DataProcessingTemplate):

        def transform(self, input) -> DataFrame:
            return self.spark.createDataFrame(input.get("views"))

    def test_dummy(self):
        #if
        mock_reader = Mock(spec=DataReader)
        mock_reader.read.return_value = {"views": ["transactions", "clients"]}
        mock_writer = Mock(spec=DataWriter)
        mock_spark = Mock(spec=SparkSession)

        #when
        with patch.object(SparkSession, 'builder', Mock()):
            dummy_pipeline = TestTemplatePipeline.DummyPipeline(reader=mock_reader, writer=mock_writer)
            dummy_pipeline.spark = mock_spark

            dummy_pipeline.execute_pipeline()
            mock_spark.createDataFrame.assert_called_once()
            mock_reader.read.assert_called_once()
            mock_writer.write.assert_called_once()
