# here we will enter what output we want from data_ingestion_config

from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
