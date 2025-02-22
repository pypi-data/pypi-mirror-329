import math
import pandas as pd
import requests

from brynq_sdk_nmbrs.brynq_sdk_nmbrs.document import Payslip
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.address import Address
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.contract import Contract
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.costcenter import EmployeeCostcenter
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.department import EmployeeDepartment
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.employment import Employment
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.function import EmployeeFunction
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.hours import VariableHours, FixedHours
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.schedules import Schedule
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.salaries import Salaries
from brynq_sdk_nmbrs.brynq_sdk_nmbrs.wagecomponents import EmployeeVariableWageComponents, EmployeeFixedWageComponents


class Employees:
    def __init__(self, nmbrs):
        self.nmbrs = nmbrs
        self.address = Address(nmbrs)
        self.function = EmployeeFunction(nmbrs)
        self.contract = Contract(nmbrs)
        self.department = EmployeeDepartment(nmbrs)
        self.costcenter = EmployeeCostcenter(nmbrs)
        self.schedule = Schedule(nmbrs)
        self.employment = Employment(nmbrs)
        self.variable_hours = VariableHours(nmbrs)
        self.fixed_hours = FixedHours(nmbrs)
        self.salaries = Salaries(nmbrs)
        self.variable_wagecomponents = EmployeeVariableWageComponents(nmbrs)
        self.fixed_wagecomponents = EmployeeFixedWageComponents(nmbrs)
        self.payslips = Payslip(nmbrs)

    def get(self,
            company_id: str,
            employee_type: str = None) -> pd.DataFrame:
        params = {} if employee_type is None else {'employeeType': employee_type}
        request = requests.Request(method='GET',
                                   url=f"{self.nmbrs.base_url}companies/{company_id}/employees/personalinfo",
                                   params=params)

        data = self.nmbrs.get_paginated_result(request)
        # df_normalized = pd.json_normalize(df['info'].explode())
        # df = pd.concat([df['employee_id'], df_normalized], axis=1)
        df = pd.json_normalize(
            data,
            record_path='info',
            meta=['employeeId']
        )
        df['company_id'] = company_id

        df['createdAt'] = pd.to_datetime(df['createdAt'])
        df = df.loc[df.groupby('employeeId')['createdAt'].idxmax()]
        df = df.reset_index(drop=True)
        df = self.nmbrs._rename_camel_columns_to_snake_case(df)

        return df

    def create(self,
               company_id: str,
               data: dict) -> requests.Response:
        allowed_fields_basic_info = {
            'first_name': "firstName",
            'initials': "initials",
            "prefix": "prefix",
            "full_name": "firstNameInFull"
        }
        allowed_fields_birth_info = {
            'birth_date': "birthDate",
            'nationality': "nationalityCodeISO",
            "country_of_birth": "birthCountryCodeISO",
            "date_deceased": "deceasedOn"
        }
        allowed_fields_contact_info = {
            'email_private': "privateEmail",
            'email_work': "businessEmail",
            "phone_work": "businessPhone",
            "mobile_work": "businessMobilePhone",
            "phone_private": "privatePhone",
            "mobile_private": "privateMobilePhone",
            "phone_other": "otherPhone"
        }
        allowed_fields_partner_info = {
            'prefix_partner_name': "partnerPrefix",
            'partner_name': "partnerName",
            "ascription": "ascriptionCode",
        }
        required_fields = ['last_name', "year", "period", "in_service_date", "employee_id", "gender", "employee_type"]
        allowed_fields = allowed_fields_partner_info | allowed_fields_basic_info | allowed_fields_contact_info | allowed_fields_birth_info
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "PersonalInfo": {
                # "personalInfoId": "0039b188-b5f5-49a6-a3d5-0448ce4042ee",
                "basicInfo": {
                    "employeeNumber": data["employee_id"],
                    "lastName": data["last_name"],
                    "employeeType": data["employee_type"]
                },
                "birthInfo": {
                    "gender": data["gender"]
                },
                "contactInfo": {
                },
                "partnerInfo": {
                },
                "period": {
                    "year": data["year"],
                    "period": data["period"],
                },
            },
            "AdditionalEmployeeInfo": {
                "inServiceDate": data["in_service_date"]
            }
        }
        for field in (allowed_fields_basic_info.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload['PersonalInfo']['basicInfo'].update({allowed_fields_basic_info[field]: data[field]})

        for field in (allowed_fields_birth_info.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload['PersonalInfo']['birthInfo'].update({allowed_fields_birth_info[field]: data[field]})

        for field in (allowed_fields_contact_info.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload['PersonalInfo']['contactInfo'].update({allowed_fields_contact_info[field]: data[field]})

        for field in (allowed_fields_partner_info.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload['PersonalInfo']['partnerInfo'].update({allowed_fields_partner_info[field]: data[field]})

        resp = self.nmbrs.session.post(url=f"{self.nmbrs.base_url}companies/{company_id}/employees",
                                       json=payload)
        return resp

    def update(self, employee_id: str, data: dict):
        allowed_fields_basic_info = {
            'first_name': "firstName",
            'initials': "initials",
            "prefix": "prefix",
            "full_name": "firstNameInFull",
            "last_name": "lastName",
            "employee_type": "employeeType"
        }
        allowed_fields_birth_info = {
            'birth_date': "birthDate",
            'nationality': "nationalityCodeISO",
            "country_of_birth": "birthCountryCodeISO",
            "date_deceased": "deceasedOn",
            "gender": "gender"
        }
        allowed_fields_contact_info = {
            'email_private': "privateEmail",
            'email_work': "businessEmail",
            "phone_work": "businessPhone",
            "mobile_work": "businessMobilePhone",
            "phone_private": "privatePhone",
            "mobile_private": "privateMobilePhone",
            "phone_other": "otherPhone"
        }
        allowed_fields_partner_info = {
            'prefix_partner_name': "partnerPrefix",
            'partner_name': "partnerName",
            "ascription": "ascriptionCode",
        }
        required_fields = ["year", "period", "employee_id"]
        allowed_fields = allowed_fields_partner_info | allowed_fields_basic_info | allowed_fields_contact_info | allowed_fields_birth_info
        self.nmbrs.check_fields(data=data, required_fields=required_fields, allowed_fields=list(allowed_fields.keys()))

        payload = {
            "basicInfo": {
                "employeeNumber": data["employee_id"]
            },
            "birthInfo": {
            },
            "contactInfo": {
            },
            "partnerInfo": {
            },
            "period": {
                "year": data["year"],
                "period": data["period"],
            }
        }
        for field in (allowed_fields_basic_info.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload['basicInfo'].update({allowed_fields_basic_info[field]: data[field]})

        for field in (allowed_fields_birth_info.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload['birthInfo'].update({allowed_fields_birth_info[field]: data[field]})

        for field in (allowed_fields_contact_info.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload['contactInfo'].update({allowed_fields_contact_info[field]: data[field]})

        for field in (allowed_fields_partner_info.keys() & data.keys()):
            if not isinstance(data[field], float) or not math.isnan(data[field]):
                payload['partnerInfo'].update({allowed_fields_partner_info[field]: data[field]})

        resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/personalInfo",
                                      json=payload)
        if 'social_security_number' in data.keys():
            resp = self.nmbrs.session.put(url=f"{self.nmbrs.base_url}employees/{employee_id}/social_security_number",
                                          json=payload)

        return resp
