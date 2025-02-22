import pandas as pd
import pandera as pa
from pandera.typing import Series, String, Float


class FixedWageComponentSchema(pa.DataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    fixed_wage_component_id: Series[String] = pa.Field(coerce=True)
    code: Series[String] = pa.Field(coerce=True)
    value: Series[Float] = pa.Field(coerce=True)
    end_year: Series[pd.Int64Dtype] = pa.Field(nullable=True, coerce=True)
    end_period: Series[pd.Int64Dtype] = pa.Field(nullable=True, coerce=True)
    comment: Series[String] = pa.Field(nullable=True, coerce=True)
    cost_center_id: Series[String] = pa.Field(nullable=True, coerce=True)
    cost_unit_id: Series[String] = pa.Field(nullable=True, coerce=True)

    class Config:
        coerce = True

class VariableWageComponentSchema(pa.DataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    variable_wage_component_id: Series[String] = pa.Field(coerce=True)
    code: Series[String] = pa.Field(coerce=True)
    value: Series[Float] = pa.Field(coerce=True)
    comment: Series[String] = pa.Field(nullable=True, coerce=True)
    cost_center_id: Series[String] = pa.Field(nullable=True, coerce=True)
    cost_unit_id: Series[String] = pa.Field(nullable=True, coerce=True)

    class Config:
        coerce = True