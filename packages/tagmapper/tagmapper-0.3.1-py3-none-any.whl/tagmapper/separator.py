from typing import List
import pandas as pd

from tagmapper.attribute import Attribute
from tagmapper.connector_db import query


class Separator:
    """
    Separator class
    """

    _sep_attributes = pd.DataFrame()

    def __init__(self, usi):
        if isinstance(usi, str):
            # assume data is USI
            data = Separator.get_sep_attributes(usi)
        elif isinstance(usi, pd.DataFrame):
            data = usi

        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a dataframe")

        if data.empty:
            raise ValueError("Input data can not be empty")

        self.inst_code = data["STID_CODE"].iloc[0]
        self.object_name = data["OBJECT_NAME"].iloc[0]
        self.object_code = data["PDM.OBJECT_CODE"].iloc[0]
        self.usi = data["unique_separator_identifier"].iloc[0]

        self.attributes = []
        for _, r in data.iterrows():
            self.attributes.append(Attribute(r.to_dict()))

    @classmethod
    def get_all_separators(cls) -> List["Separator"]:
        usi = Separator.get_separator_names()
        sep = []

        for u in usi:
            sep.append(Separator(Separator.get_sep_attributes(u)))

        return sep

    @classmethod
    def get_separator(cls, inst_code: str, tag_no: str) -> "Separator":
        return Separator(Separator.get_sep_attributes(f"{inst_code}-{tag_no}"))

    @classmethod
    def get_sep_attributes(cls, usi: str = "") -> pd.DataFrame:
        if cls._sep_attributes.empty:
            cls._sep_attributes = query(
                "select * from [dbo].[separator_attribute_mapping]"
            )

        if usi:
            ind = cls._sep_attributes["unique_separator_identifier"] == usi
            return cls._sep_attributes.loc[ind, :]
        else:
            return cls._sep_attributes

    @staticmethod
    def get_separator_names() -> List[str]:
        d = Separator.get_sep_attributes()
        usi = list(d["unique_separator_identifier"].unique())
        usi.sort()
        return usi

    @staticmethod
    def get_usi() -> List[str]:
        return Separator.get_separator_names()
