import pandera as pa
from pandera.typing import Series, String, Float, DateTime
import pandas as pd


class VariableHoursSchema(pa.DataFrameModel):
    hour_component_id: Series[String] = pa.Field(coerce=True)  # UUID
    hour_code: Series[pd.Int64Dtype] = pa.Field(coerce=True)
    hour_code_description: Series[String] = pa.Field(coerce=True, nullable=True)
    hours: Series[Float] = pa.Field(coerce=True)
    cost_center_id: Series[String] = pa.Field(coerce=True, nullable=True)  # UUID
    cost_unit_id: Series[String] = pa.Field(coerce=True, nullable=True)  # UUID
    comment: Series[String] = pa.Field(coerce=True, nullable=True)
    created_at: Series[DateTime] = pa.Field(coerce=True)
    employee_id: Series[String] = pa.Field(coerce=True)  # Added for tracking

    class Config:
        coerce = True


class FixedHoursSchema(pa.DataFrameModel):
    hour_component_id: Series[String] = pa.Field(coerce=True)
    hour_code: Series[pd.Int64Dtype] = pa.Field(coerce=True)
    hour_code_description: Series[String] = pa.Field(nullable=True, coerce=True)
    hours: Series[Float] = pa.Field(coerce=True)
    cost_center_id: Series[String] = pa.Field(nullable=True, coerce=True)
    cost_unit_id: Series[String] = pa.Field(nullable=True, coerce=True)
    comment: Series[String] = pa.Field(nullable=True, coerce=True)
    end_year: Series[pd.Int64Dtype] = pa.Field(nullable=True, coerce=True)
    end_period: Series[pd.Int64Dtype] = pa.Field(nullable=True, coerce=True)
    created_at: Series[String] = pa.Field(coerce=True)

    class Config:
        coerce = True
