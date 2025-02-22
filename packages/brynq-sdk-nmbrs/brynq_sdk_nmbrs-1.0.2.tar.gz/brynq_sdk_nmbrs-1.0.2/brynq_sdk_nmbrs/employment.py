import math
import pandas as pd
import requests


class Employment:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs

    def get(self,
            company_id: str,
            changed_from: str = None,
            created_from: str = None,
            employee_id: str = None) -> pd.DataFrame:
        params = {}
        if created_from:
            params['createdFrom'] = created_from
        if employee_id:
            params['changedFrom'] = changed_from
        if employee_id:
            params['employeeId'] = employee_id
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/employments",
                                   params=params)
        data = self.nmbrs.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='employments',
            meta=['employeeId']
        )
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df

    def create(self,
               employee_id: str,
               data: dict):

        required_fields = ["start_date_employment"]
        allowed_fields = {
            "pension_date": "seniorityDate"
        }
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "startDate": data["start_date_employment"]
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/employment",
                                       json=payload)
        return resp

    def update(self,
               employee_id: str,
               data: dict):

        required_fields = ["employment_id"]
        allowed_fields = {
            "pension_date": "seniorityDate",
            "termination_date": "endOfServiceDate",
            "termination_reason": "endOfContractReason",
        }
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "employment_id": data["employment_id"]
        }

        for field in (allowed_fields.keys() & data.keys()):
            payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/employment",
                                      json=payload)
        return resp
