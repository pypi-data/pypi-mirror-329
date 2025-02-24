from typing import Literal , Union
from urllib.parse import urljoin

import requests

from spida_api.spida_api_dataclasses import CompanyProjects, Projects, Logs, Log


class SpidaAPI:
    _LOGIN_ENDPOINT = 'usersmaster/login/auth'
    _SWITCH_COMPANY_ENDPOINT = 'projectmanager/switchcompany'
    _ALL_PROJECTS_IN_COMPANY_ENDPOINT = 'projectmanager/projectAPI/getAllProjectsInCompany'
    _GET_PROJECT_ENDPOINT = 'projectmanager/projectAPI/getProjects'
    _GET_PROJECT_LOGS_ENDPOINT = 'projectmanager/projectAPI/getProjectLogs'
    _PUT_FORM_ENDPOINT = '/projectmanager/rest/forms'
    # add more as needed

    def __init__(self, username: str, password: str, host: str) -> None:
        self._username = username
        self._password = password
        self._host = host

        self._base_url = f'https://{self._host}'

        self._create_session()
        self._login_to_spida()

    def get_projects_in_company(self, include_finished: bool = True) -> CompanyProjects:
        url = urljoin(self._base_url, self._ALL_PROJECTS_IN_COMPANY_ENDPOINT)

        params = {'include_finished': include_finished}

        response = self._session.get(url, params=params)

        response_json = response.json()
        response_json = response_json['result']

        dataclass = CompanyProjects(**response_json)
        return dataclass

    def get_project(self, project_id_or_project_code_input: Union[list, int, str],
                    project_id_or_project_code: Literal['project_ids', 'project_code_values'] = 'project_ids', details: bool = True) -> Projects:

        url = urljoin(self._base_url, self._GET_PROJECT_ENDPOINT)

        if project_id_or_project_code == 'project_ids':
            project_id_or_project_code_param = self._build_project_id_string(project_id_or_project_code_input)
        elif project_id_or_project_code == 'project_code_values':
            project_id_or_project_code_param = self._build_project_code_string(project_id_or_project_code_input)
        else:
            raise ValueError

        params = {
            project_id_or_project_code: project_id_or_project_code_param,
            'details': details
        }

        response = self._session.get(url, params=params)
        response_json = response.json()
        response_json = response_json['result']

        dataclass = Projects(**response_json)

        return dataclass

    def get_project_logs(self, project_id: Union[int, str]) -> Logs:
        url = urljoin(self._base_url, self._GET_PROJECT_LOGS_ENDPOINT)

        params = {
            'project_id': project_id,
            'details': True
        }
        response = self._session.get(url, params=params)
        response_json = response.json()

        dataclass = Logs(logs=[Log(**response) for response in response_json])
        return dataclass

    def get_form(self, form_id):
        url = f"{self._base_url}/projectmanager/rest/forms/{form_id}"

        return self._session.get(url).json()

    def update_form(self, form_id, form):
        url = f"{self._base_url}/projectmanager/rest/forms/{form_id}"
        print(url)

        return self._session.put(url, json=form).json()

    def switch_company(self, company_id: int) -> None:
        url = urljoin(self._base_url, self._SWITCH_COMPANY_ENDPOINT)

        params = {
            'coselect': company_id
        }

        self._session.get(url=url, params=params)

    def _create_session(self) -> None:
        session = requests.session()
        session.get(self._base_url)
        self._session = session

    def _login_to_spida(self) -> None:
        url = urljoin(self._base_url, self._LOGIN_ENDPOINT)

        params = {
            'j_username': self._username,
            'j_password': self._password,
            'login': 'Login'
        }
        self._session.post(url=url, params=params)

    @staticmethod
    def _build_project_id_string(project_ids: Union[list, int, str]) -> str:
        if isinstance(project_ids, list):
            project_ids = ','.join([str(item) for item in project_ids])
        return f'[{project_ids}]'

    @staticmethod
    def _build_project_code_string(project_codes: Union[list, str]) -> str:
        if isinstance(project_codes, list):
            project_codes = ','.join([f'"{code}"' for code in project_codes])
        else:
            project_codes = f'"{project_codes}"'
        return f'[{project_codes}]'