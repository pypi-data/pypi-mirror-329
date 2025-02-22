import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions


class SalarySchema(pa.DataFrameModel):
    employee_id: Series[String] = pa.Field(coerce=True)
    salary_id: Series[String] = pa.Field(coerce=True)
    start_date: Series[DateTime] = pa.Field(coerce=True)
    type: Series[String] = pa.Field(coerce=True, isin=["grossFulltimeSalary", "grossParttimeSalary", "grossHourlyWage", "netParttimeSalaryInclWageComp", "netParttimeSalaryExclWageComp",
                                                       "netHourlyWageExclWageComp", "netHourlyWageInclWageComp", "employerCosts"])
    value: Series[Float] = pa.Field(coerce=True, nullable=True)
    created_at: Series[DateTime] = pa.Field(coerce=True)
    # todo: implement salary tables
    # created_at: Series[DateTime] = pa.Field(coerce=True, nullable=True)
    # company_id: Series[String] = pa.Field(coerce=True)
