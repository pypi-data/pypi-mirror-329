from typing import List, Union, Optional

import pydantic.dataclasses as pyd_dc

@pyd_dc.dataclass
class DataForm:
    title: str
    fields: dict


@pyd_dc.dataclass
class Status:
    current: str
    possible: Optional[List[str]] = None

    def __repr__(self):
        return f'{self.current} (current)'

@pyd_dc.dataclass
class Station:
    id: int
    display: str
    geometry: dict
    source: Optional[str] = None
    stationId: Optional[str] = None
    dataForms: Optional[List[DataForm]] = None


@pyd_dc.dataclass
class Project:
    id: int
    name: str
    companyId: int
    flowName: str
    stations: Optional[List[Station]] = None
    status: Optional[Status] = None
    dataForms: Optional[List[DataForm]] = None

    def __post_init__(self):
        self._set_dataform_mapping()

    def get_dataform(self, key: str) -> Union[DataForm, None]:
        return self.dataform_mapping[key] if key in self.dataform_mapping else None

    def _set_dataform_mapping(self) -> None:
        self.dataform_mapping = {}
        for dataForm in self.dataForms:
            title = dataForm.title
            self.dataform_mapping[title] = dataForm


@pyd_dc.dataclass
class ProjectCode:
    id: int
    value: str
    companyId: int
    type: str


@pyd_dc.dataclass
class CompanyProject:
    id: int
    status: Status
    projectCodes: List[ProjectCode]


@pyd_dc.dataclass
class CompanyProjects:
    projects: List[CompanyProject]


@pyd_dc.dataclass
class Projects:
    projects: List[Project]

@pyd_dc.dataclass
class CompanyProjects:
    projects: List[CompanyProject]


@pyd_dc.dataclass
class Log:
    message: str
    id: int
    trigger: str
    date: int
    success: bool
    eventId: Optional[int] = None
    eventName: Optional[str] = None

    def __post_init_post_parse__(self):
        self.source_node = None
        self.current_node = None
        self.target_nodes = []


# Logs is treated a bit differently as it comes in as a stand-alone array and not an object
@pyd_dc.dataclass
class Logs:
    logs: List[Log]

    def __post_init__(self):
        self.logs = sorted(self.logs, key=lambda x: x.date)

    def __getitem__(self, item):
        return self.logs[item]

    def get_log_event_names(self, filter_by_trigger: Optional[str] = None) -> "Logs":
        if filter_by_trigger:
            return Logs([log for log in self.logs if log.trigger == filter_by_trigger])
        return self