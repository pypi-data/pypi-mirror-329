import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions


class EmploymentSchema(pa.DataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    employment_id: Series[String] = pa.Field(coerce=True)
    start_date: Series[DateTime] = pa.Field(coerce=True)
    end_date: Series[DateTime] = pa.Field(coerce=True, nullable=True)
    end_contract_reason: Series[String] = pa.Field(coerce=True, nullable=True)
    # created_at: Series[DateTime] = pa.Field(coerce=True)
    # todo: implement salary tables
    # created_at: Series[DateTime] = pa.Field(coerce=True, nullable=True)
    # company_id: Series[String] = pa.Field(coerce=True)
