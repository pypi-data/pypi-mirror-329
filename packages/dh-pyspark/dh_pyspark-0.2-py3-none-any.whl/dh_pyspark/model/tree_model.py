from dataclasses import dataclass, field
from enum import IntEnum
from typing import Union, Dict, Any, Iterable, Optional, TypeVar

from dataheroes.data.common import DataParams
from dataheroes.services.common import CoresetParams
from dataheroes.services.coreset._base import CoresetT
from pyspark.sql import DataFrame


@dataclass
class LevelDataFrame:
    """
    Represents a level in a tree structure with associated DataFrame and metadata.
    """

    def __init__(self, level=0, level_df=None, level_metadata=None):
        """
        Initialize LevelDataFrame.

        Parameters:
            level (int): The level in the tree.
            level_df (DataFrame): The DataFrame associated with the level.
            level_metadata (dict): Metadata associated with the level.
        """
        if level_metadata is None:
            level_metadata = {}
        self.level = level
        self.level_df = level_df
        self.level_metadata = level_metadata

    level: int
    level_df: DataFrame
    level_metadata: dict = field(default_factory=dict)

    class MetaDataParams:
        PARTITIONS_TO_SAVE = "partitions_to_save"
        ROOT_CORESET_PARTITION = "root_coreset_partition"


class SaveOrig(IntEnum):
    """
    Enumeration of data column save modes.
    """
    NONE = 1
    PREPROCESSING_ONLY = 2
    PREPROCESSING_AND_BUILD = 3


CoresetParamsT = TypeVar('CoresetParamsT', bound=CoresetParams)


@dataclass
class TreeParams:
    """
       A class to hold parameters for configuring of the coreset tree this is a private class which holds the state of the tree in the Coreset srtvice.
       please do not add to here spark object like a session or dataframe because of serialization issues this claas will only be available on the driver.
    """

    coreset: Optional[CoresetT] = None
    coreset_params: Optional[CoresetParamsT] = None
    dhspark_path: str = None
    chunk_size: int = None
    coreset_size: Union[float, int] = None
    chunk_sample_ratio: float = None
    n_instances: int = None
    n_instances_exact: bool = None
    leaf_factor: int = 2
    first_level_max_chunk: int = None
    first_level_last_max_chunk: int = None  # max chunk before partial tree build
    partial_build_starting_index: int = None
    partial_build_ending_chunk_by: str = None
    categorical_columns: [] = None
    numeric_columns: [] = None
    calc_column_names: [] = None
    ohe_arr_size_diff: {} = None
    target_column: str = None
    data_params: DataParams = None
    index_column: str = None
    chunk_by: str = None
    stop_level_max_chunk: int = None
    stop_level: int = None
    stop_tree_size: int = None
    class_size: Dict[Any, int] = None
    sample_all: Iterable[Any] = None
    model_class: str = None
    chunk_by_tree: [] = None
    temp_metadata_pd_df = None
    save_orig: SaveOrig = SaveOrig.NONE
    trace_mode: str = None


@dataclass
class TreeDataFrame:
    """
    Represents a tree structure with associated DataFrames and parameters.   """

    validation_ldf: LevelDataFrame = None
    chunk_data_no_coreset_ldf: LevelDataFrame = None
    tree_ldf: list[LevelDataFrame] = field(default_factory=list)
    tree_params: TreeParams = None

    def addUpdateLevel(self, level: int, df: DataFrame = None) -> LevelDataFrame:
        """
        Add or update a level in the tree with the specified DataFrame.

        Parameters:
            level (int): The level in the tree.
            df (DataFrame): The DataFrame associated with the level.

        Returns:
            LevelDataFrame: The LevelDataFrame object.
        """
        if self.levelInTree(level):
            self.setLevelDF(level, df)
        else:
            self.tree_ldf.append(LevelDataFrame(level, df))
        return self.getLevel(level)

    def addValidation(self, df: DataFrame):
        """
        Add validation DataFrame.

        Parameters:
            df (DataFrame): The DataFrame for validation.
        """
        self.validation_ldf = LevelDataFrame(0, df)

    def levelInTree(self, level) -> bool:
        """
        Check if a level is present in the tree.

        Parameters:
            level: The level to check.

        Returns:
            bool: True if the level is present, False otherwise.
        """
        ldf_ = level < len(self.tree_ldf)
        return ldf_

    def getLevel(self, level) -> LevelDataFrame:
        return self.tree_ldf[level]

    def getLevelDF(self, level) -> DataFrame:
        return self.getLevel(level).level_df

    def setLevelDF(self, level, df: DataFrame):
        self.tree_ldf[level].level_df = df

    def getValidation(self) -> LevelDataFrame:
        return self.validation_ldf

    def getValidationDF(self) -> Union[DataFrame, None]:
        if self.getValidation() is not None:
            return self.getValidation().level_df
        else:
            return None

    def setValidationDF(self, df: DataFrame, metadata: dict):
        self.validation_ldf = LevelDataFrame(level_df=df, level_metadata=metadata)

    def getChunkDataNoCoreset(self) -> LevelDataFrame:
        return self.chunk_data_no_coreset_ldf

    def getChunkDataNoCoresetDF(self) -> DataFrame:
        return self.getChunkDataNoCoreset().level_df

    def setChunkDataNoCoresetDF(self, df: DataFrame, metadata: dict = None):
        self.chunk_data_no_coreset_ldf = LevelDataFrame(level_df=df, level_metadata=metadata)

    def getTreeSize(self):
        if self.tree_ldf is not None:
            return len(self.tree_ldf)
        else:
            return None
