import pandas as pd
import requests
import math


class Schedule:
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
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/schedules",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        df = self.nmbrs._rename_camel_columns_to_snake_case(pd.DataFrame(data))

        return df

    def create(self,
               employee_id: str,
               data: dict):

        required_fields = ["start_date_schedule"]
        allowed_fields = {
            "weekly_hours": "hoursPerWeek"
        }
        allowed_fields_schedule = {
            "hours_monday": "hoursMonday",
            "hours_tuesday": "hoursTuesday",
            "hours_wednesday": "hoursWednesday",
            "hours_thursday": "hoursThursday",
            "hours_friday": "hoursFriday",
            "hours_saturday": "hoursSaturday",
            "hours_sunday": "hoursSunday"
        }
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        allowed_fields = allowed_fields | allowed_fields_schedule
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "startDate": data["start_date_schedule"]
        }

        for field in (allowed_fields.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload.update({allowed_fields[field]: data[field]})

        payload_schedule = {
        }

        for field in (allowed_fields_schedule.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload_schedule.update({allowed_fields_schedule[field]: data[field]})
        if len(payload_schedule) > 0:
            payload.update(payload_schedule)

        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}employees/{employee_id}/schedule",
                                       json=payload)
        return resp
