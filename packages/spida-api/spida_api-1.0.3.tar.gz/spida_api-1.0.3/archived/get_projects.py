import json
from dataclasses import dataclass
from typing import List
import os
import requests
from requests import Response, Session
from dotenv import load_dotenv
import logging

# from utils.ssh import json_to_dataclass
#
# from utils.json_to_dataclass import json_to_dataclass
# from constants_and_classes.spida_getproject_dataclasses import Projects

load_dotenv()

spida_user = os.getenv('SPIDA_USERNAME')
spida_pass = os.getenv('SPIDA_PASSWORD')
spida_token = os.getenv('SPIDA_API_TOKEN')
spida_company = int(os.getenv('SPIDA_COMPANY'))

# For debugging, uncomment this line
logging.basicConfig(level=logging.DEBUG)

def saveJsonFile(response: Response, jsonFileName: str):
    try:
        with open(f'{jsonFileName}.json', 'w') as f:
            json.dump(response.json(), f)
    except Exception as e:
        print(f'Could not save {jsonFileName}: ' + str(e))


# ------------ ProjectAPI Functions Ref ------------
# https://github.com/spidasoftware/schema/blob/master/doc/apis/projectAPI.md

def getAllProjectsInCompany(company_id:int, include_finished:bool = False) -> Response:
    url = 'https://techserv.spidastudio.com/projectmanager/projectAPI/getAllProjectsInCompany'
    params = {
        'company_id': company_id,
        'include_finished': str(include_finished).lower(),
        'apiToken': str(spida_token)
    }
    logging.debug(params)
    return session.get(url, params=params)


def getFlows() -> Response:
    url = 'https://techserv.spidastudio.com/projectmanager/projectAPI/getFlows'
    params = {
        'include_viewable': 'true',
        'apiToken': str(spida_token)
    }
    logging.debug(params)
    return session.get(url, params=params)


def getCompany(company_id:int) -> Response:
    url = 'https://techserv.spidastudio.com/usersmaster/companyAPI/getCompany'
    params = {
        'company_id': company_id,
        'apiToken': str(spida_token)
    }
    logging.debug(params)
    return session.get(url, params=params)





# ------ Starting SpidaDB API -------
# Ref: https://github.com/spidasoftware/schema/blob/master/doc/apis/spidadbAPI.md

def getProject(spidaDB_id:str) -> Response:
    url = f'https://techserv.spidastudio.com/spidadb/projects/{spidaDB_id}'
    params = {

        'apiToken': str(spida_token)
    }
    logging.debug(params)
    return session.get(url, params=params)

def getDBProjects(label:str=None, limit:int=None, skip:int=None) -> Response:
    '''

    :param label: Text in the Project Name to search for. Partial search, case insensitive
    :param limit: How many results to return before stopping
    :param skip: How many results to skip. Used for paganation
    :return:
    '''
    url = f'https://techserv.spidastudio.com/spidadb/projects.referenced'
    params = {
        'apiToken': str(spida_token)
    }
    if label:
        params['label'] = label
    if limit:
        params['limit'] = limit
    logging.debug(params)
    return session.get(url, params=params)

# ------ Functions Which I Could Not Get Results From -------
#
# def findDBProjects(label:str)-> Response:
#     '''
#         Could not get a good result
#     '''
#     url = 'https://techserv.spidastudio.com/projectmanager/projectAPI/findDBProjectsInDB?'
#     params = {
#         'label': label,
#         'apiToken': str(spida_token)
#     }
#     logging.debug(params)
#     return session.get(url, params=params)
#
# def getProjectsByDBIDd(db_ids: list, details: bool = False) -> Response:
#     '''
#         Could not get a good result
#     '''
#     url = 'https://techserv.spidastudio.com/projectmanager/projectAPI/getProjectsByDBId'
#     params = {
#         'db_ids': json.dumps(db_ids),
#         'details': str(details).lower(),
#         'apiToken': str(spida_token)
#     }
#     logging.debug(params)
#     return session.get(url, params=params)
#
# def getDBProjectByDBId(db_id: str, format: str = 'calc') -> Response:
#     '''
#         'you do not have permission to view this project: 0' yet I can see the project in Studio
#     '''
#     url = 'https://techserv.spidastudio.com/projectmanager/projectAPI/getDBProjectByDBId'
#     params = {
#         'db_id': db_id,
#         'format': str(format).lower(),
#         'apiToken': str(spida_token)
#     }
#     logging.debug(params)
#     return session.get(url, params=params)
#
# def getProjects(project_ids:list=[], project_code_values:list=[], details:bool=False) -> Response:
#     '''
#         Could not get a good result
#     '''
#     url = 'https://techserv.spidastudio.com/projectmanager/projectAPI/getProjects'
#     params = {
#         'project_ids': json.dumps(project_ids),
#         'project_code_values': json.dumps(project_code_values),
#         'details': str(details).lower(),
#         'apiToken': str(spida_token)
#     }
#     logging.debug(params)
#     return session.get(url, params=params)
#
# def getLogs(project_id:int ) -> Response:
#     '''
#         Could not get a good result
#     '''
#     url = 'https://techserv.spidastudio.com/projectmanager/projectAPI/getProjectLogs'
#     params = {
#         'project_id': project_id,
#         'apiToken': str(spida_token)
#     }
#     logging.debug(params)
#     return session.get(url, params=params)
#
# def getLocationByDBId(db_id:str, format:str = 'calc',detailed_results:bool = False) -> Response:
#     '''
#         Could not get a good result
#         Maybe need to use a stations' spida DB Id
#     '''
#     url = 'https://techserv.spidastudio.com/projectmanager/projectAPI/getDBLocationByDBId'
#     params = {
#         'db_id': db_id,
#         'format': format.lower(),
#         'detailed_results' : str(detailed_results).lower(),
#         'apiToken': str(spida_token)
#     }
#     logging.debug(params)
#     return session.get(url, params=params)
#
# def getDetailedResults(spidaDB_id:str) -> Response:
#     '''
#     Could not get good result. I think this is for a design with a spida calc result which I dont have an ID for
#     :param spidaDB_id:
#     :return:
#     '''
#     url = f'https://techserv.spidastudio.com/spidadb/results/{spidaDB_id}'
#     params = {
#         'apiToken': str(spida_token)
#     }
#     logging.debug(params)
#     return session.get(url, params=params)

if __name__ == '__main__':
    session = requests.session()

    # ------- Functions I could not get results from -------
    # response = findDBProjects('Name')
    # response = getProjectsByDBIDd(['65aff2a1cff47e000128295d'],True)
    # response = getProjects(project_ids=[673504],project_code_values=['id','value','companyId','type'])
    # response = getLogs(673504)
    # response = getLocationByDBId('65e7ded5cff47e0001286bc0')
    # response = getDBProjectByDBId('66c4a0b3cff47e000173b366')
    # response = getDetailedResults('66f70921cff47e0001b4d57a')

    # ------- Function Call Examples -------
    #
    responseAllProjects = getAllProjectsInCompany(145,False)
    responseFlows = getFlows()
    responseCompany = getCompany(2)
    responseProject = getProject('66c4a0b3cff47e000173b366')
    responseDBProjects = getDBProjects(label='TYL')

    saveJsonFile(responseAllProjects,'getAllProjectsInCompany')
    saveJsonFile(responseFlows,'getFlows')
    saveJsonFile(responseCompany,'getCompany')
    saveJsonFile(responseProject,'getProject')
    saveJsonFile(responseDBProjects,'getDBProjects')

    quit()