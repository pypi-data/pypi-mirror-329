import math
import pandas as pd
import requests


class Salaries:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            company_id: str,
            created_from: str = None,
            employee_id: str = None) -> pd.DataFrame:
        params = {}
        if created_from:
            params['createdFrom'] = created_from
        if employee_id:
            params['employeeId'] = employee_id
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/salaries",
                                   params=params)
        data = self.nmbrs.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='salaries',
            meta=['employeeId']
        )
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df

    def get_salary_tables(self,
            salary_table_id: str) -> pd.DataFrame:
        params = {}
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}salarytable/{salary_table_id}",
                                   params=params)
        data = self.nmbrs.get_paginated_result(request)
        df = self.nmbrs._rename_camel_columns_to_snake_case(data)

        return df

    def create(self,
               employee_id: str,
               data: dict):

        required_fields = ["start_date_salary"]
        allowed_fields = {
            "salary_amount": "value",
            "salary_type": "type"
        }
        allowed_fields_salary_table = {
            "salary_table_id": "salaryTableId",
            "scale_id": "scaleId",
            "step_id": "stepId",
            "increase_step_period": "period",
            "increase_step_year": "year"
        }
        allowed_fields = allowed_fields | allowed_fields_salary_table
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "startDate": data["start_date_salary"]
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        salary_table_payload = {
            "salaryTable": {
            }
        }
        for field in (allowed_fields_salary_table.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                salary_table_payload["salaryTable"].update({allowed_fields_salary_table[field]: data[field]})
        if len(salary_table_payload["salaryTable"]) > 0:
            payload.update(salary_table_payload)

        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/salary",
                                       json=payload)

        return resp
