import math
import pandas as pd
import requests


class Contract:
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
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/contracts",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='contracts',
            meta=['employeeId']
        )
        # df_normalized = pd.json_normalize(df['contracts'].explode())
        # df = pd.concat([df['employee_id'], df_normalized], axis=1)

        df['company_id'] = company_id
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)
        # df = df[df['employee_id'].notna()]
        # df = df.reset_index(drop=True)

        return df

    def create(self,
               employee_id: str,
               data: dict):

        required_fields = ["start_date_contract", "indefinite_contract"]
        allowed_fields = {
            "probation_period": "trialPeriod",
            "end_date_contract": "endDate",
            "written_contract": "writtenContract",
            "weekly_hours": "hoursPerWeek"
        }
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "startDate": data["start_date_contract"],
            "indefinite": data["indefinite_contract"]
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/contract",
                                       json=payload)
        return resp

    def update(self,
               employee_id: str,
               data: dict):

        required_fields = ["contract_id", "start_date_contract", "indefinite_contract"]
        allowed_fields = {
            "probation_period": "trialPeriod",
            "end_date_contract": "endDate",
            "written_contract": "writtenContract",
            "weekly_hours": "hoursPerWeek"
        }
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "contractId": data["contract_id"],
            "startDate": data["start_date_contract"],
            "indefinite": data["indefinite_contract"]
        }

        for field in (allowed_fields.keys() & data.keys()):
            payload.update({allowed_fields[field]: data[field]})

        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/contract",
                                      json=payload)
        return resp
