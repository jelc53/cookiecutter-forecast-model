"""BaseSchema class."""

from enum import Enum
from typing import Dict, List

import numpy as np
import pandas as pd
import pandera as pa


class BaseSchema(pa.SchemaModel):
    """Abstract Schema class defining the mandatory attributes and methods."""

    _label: str = "base"

    @classmethod
    def primary_key(cls):
        """."""
        return []
 
    @classmethod
    def enum(cls):
        """."""
        return {}

    @classmethod
    def get_label(cls):
        """Get class label attribute."""
        return cls._label

    @classmethod
    def get(cls, item: str):
        """Get class label attribute."""
        return getattr(cls, item)

    @classmethod
    def get_primary_key(cls):
        """Get primary key column list."""
        return cls.primary_key()

    @classmethod
    def get_enum(cls):
        """Get enum values dict."""
        return cls.enum()

    @classmethod
    def get_columns(cls) -> Dict[str, pa.Field]:
        """Return expanded column dictonary."""
        return {k: v.dtype.type for k, v in cls.to_schema().columns.items()}

    @classmethod
    def get_column_names(cls) -> List[str]:
        """Get list of physical column names."""
        return [name for name in cls.get_columns()]

    @classmethod
    def get_column_types(cls) -> List[str]:
        """Get list of column target types."""
        return [v for _, v in cls.get_columns().items()]

    @classmethod
    def cast(cls, data: pd.DataFrame) -> pd.DataFrame:
        """Cast columns to target column types defined in Column class."""
        data = data.copy()
        for name, type in cls.get_columns().items():
            col = name
            col_type = type
            if col in data.columns:
                if col_type == str:
                    data[col] = (
                        data[col]
                        .replace({np.nan: None})
                        .astype(col_type)
                        .replace({"None": None})
                    )
                elif col_type == int:
                    # Using Int64Dtype to handle null values
                    # and avoid conversion to float
                    data[col] = np.floor(
                        pd.to_numeric(data[col], errors="coerce")
                    ).astype(pd.Int64Dtype())
                elif col_type == float:
                    data[col] = pd.to_numeric(data[col], errors="coerce").astype(
                        pd.Float64Dtype()
                    )
                elif (col_type == bool) and (data[col].dtypes == object):
                    data[col] = (
                        data[col].fillna("False").astype(str).str.lower() == "true"
                    )
                else:
                    data[col] = data[col].astype(col_type)
        return data

    @classmethod
    def validate(cls, data: pd.DataFrame, **kwargs) -> None:
        """Apply all the data quality checks."""
        super().validate(data, **kwargs)
        cls.check_primary_key(data)
        cls.check_enum_values(data)
 
    @classmethod
    def check_primary_key(cls, data: pd.DataFrame) -> None:
        """Check if primary constraint is verified."""
        if cls.primary_key():
            is_unique = not data.duplicated(cls.get_primary_key()).sum()
            if not is_unique:
                raise PrimaryKeyError(
                    f"{cls._label} - Primary key: {cls.get_primary_key()} is not unique"
                )

    @classmethod
    def check_enum_values(cls, data: pd.DataFrame) -> None:
        """Check authorized values constraint is verified."""
        for k, v in cls.enum().items():
            col_values = set(data[k].unique())
            col_values = col_values.difference([None, "None", np.nan])

            if not col_values.issubset(set(v)):
                raise ValueError(
                    f"{cls._label} - Invalid values for column"
                    + f"{k}: {col_values.difference(set(v))}"
                )

class EnumSchema(str, Enum):
    """Base EnumSchema class."""

    @classmethod
    def get_values_aslist(cls):
        """Return attributes as list."""
        return [attr.value for attr in cls]

    def __str__(self) -> str:
        """Simplifies attributes' access for EnumSchema.

        Instead of doing EnumSchema.attr.value
        User can do EnumSchema.attr
        """
        return str.__str__(self)

"""Custom exceptions related to schemas."""
class PrimaryKeyError(Exception):
    """Primary key constraint can't be verified."""
    pass
