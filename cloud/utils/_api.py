
from _settings import *
from _utils import *

# List of API endpoints
# https://github.com/liferaycloud/api/tree/develop#table-of-contents

# // Routes

# /projects

@log
def get_master_token(project_id: str):
    url = f'https://{TARGET_DOMAIN}/projects/{project_id}/masterToken'

    response = get_url(url)

    master_token = response['masterToken']
    return master_token

@log
def get_metadata(project_id: str, set_domain: str=''):
    url = f'https://{TARGET_DOMAIN}/projects/{project_id}'

    if set_domain:
        url = f'https://{set_domain}/projects/{project_id}'    

    response = get_url(url)

    return response
    # metadata = response['metadata']
    # return metadata

@log
def get_scale(project_id: str, service_id: str='liferay'):
    url = f'https://{TARGET_DOMAIN}/projects/{project_id}/services/{service_id}/scale'

    response = get_url(url)

    return response

@log
def list_project_service(project_id: str):
    url = f'https://{TARGET_DOMAIN}/projects/{project_id}/services'

    response = get_url(url)

    return response

@log
def get_project_service(project_id: str, service_id: str='liferay'):
    url = f'https://{TARGET_DOMAIN}/projects/{project_id}/services/{service_id}'

    response = get_url(url)

    return response

@log
def restart_project_service(project_id, service_id):
    url = f'https://{TARGET_DOMAIN}/projects/{project_id}/services/{service_id}/restart'
    data = ''

    response = post_url(url, data)

    return response

@log
def stop_project_service(project_id, service_id):
    url = f'https://{TARGET_DOMAIN}/projects/{project_id}/services/{service_id}/restart'
    data = ''

    response = post_url(url, data)

    return response

# @log
# def post_hook(project_id: str, provider: str='github'):
#     master_token = get_master_token(project_id)
#     url = f'https://{TARGET_DOMAIN}/hooks/providers/{provider}/build/{project_id}/{master_token}'

#     #repository

#     data = '${"ref": "refs/heads/master", "repository": {full_name: SpencerWoo/lfrspencerwoo}, }'

#     # response = requests.post('https://api.liferay.cloud/hooks/providers/github/build/lfrspencerwoo/856759bc-e05f-4f97-8641-1cf3a11fa959', headers=headers, data=data, auth=('user@domain.com', 'pass'))

#     # data = '{"ref": "refs/heads/master", "repository": {full_name: "SpencerWoo/lfrspencerwoo"}}'

#     # SpencerWoo/lfrspencerwoo
#     response = post_url(url, data)

#     return response

# @log
# def download_database_backup(id):
#     url = f''
#     # curl -X POST /backup/download/database/:id -H 'Content-Type: application/json' -H 'Authorization: Bearer USER_TOKEN' --output database.tgz

#     response = get_url(url, data)

#     return response

# @log
# def upload_backups(volume, other):
#     pass

# @log
# def download_backups(project_id):
#     pass

@log
def get_deployments(project_id: str, limit: bool=True):
    if limit:
        url = f'https://{TARGET_DOMAIN}/projects/{project_id}/deployments?limit=1'
    else:
        url = f'https://{TARGET_DOMAIN}/projects/{project_id}/deployments'

    response = get_url(url)

    return response

@log
def get_alerts(project_id:str, unread=False):
    url = f'https://{TARGET_DOMAIN}/alerts?projectId={project_id}'

    response = get_url(url)

    return response

@log
def get_user_plans():
    url = f'https://{TARGET_DOMAIN}/plans/user'

    response = get_url(url)

    return response

# /admin

@log
def get_plans():
    url = f'https://{TARGET_DOMAIN}/admin/plans'

    response = get_url(url)

    return response

@log
def get_user(user_id):
    # get_user('spencer.woo@liferay.cloud')
    url = f'https://{TARGET_DOMAIN}/admin/users/{user_id}'

    response = get_url(url)

    return response

@log
def get_builds(user_id):
    url = f'https://{TARGET_DOMAIN}/admin/builds/{user_id}'

    response = get_url(url)

    return response

# type, limit, offset, field, order

#admin utils
@log
def get_user_uid(user_id):
    response = get_user(user_id)

    return response['id']

@log
def _get_usages():
    url = f'https://{TARGET_DOMAIN}/admin/usage'

    response = get_url(url)

    return response

@log
def get_usage(user_uid):
    usages = get_usages()

    for usage in usages:

        if usage['userId'] == user_uid:
            return usage

    return response 


# ================

# CAUTION - DO NOT USE ON PRODUCTION

# These functions exist for alternate domains ONLY

@log
def _create_plan(
                    planId='test', description='test', 
                    projects=1, services=1, cpu=4, 
                    memory=1024, traffic=1024, customDomains=0, 
                    collaborators=0, canScale=True, instances=3, 
                    storage=1024, buildsPerDay=100, constraints=[], 
                    support=False, price=0
                    ):

    url = f'https://{ALTERNATE_DOMAIN}/plans'
    data = f'''{{
                    "planId": {planId}, "description": {description}, 
                    "projects": {projects}, "services": {services}, "cpu": {cpu}, 
                    "memory": {memory}, "traffic": {traffic}, "customDomains": {customDomains}, 
                    "collaborators": {collaborators}, "canScale": {canScale}, "instances": {instances}, 
                    "storage": {storage}, "buildsPerDay": {buildsPerDay}, "constraints": {constraints}, 
                    "support": {support}, "price": {price} 
                    }}'''

    response = post_url(url, data)

    return response

@log
def _set_production_type(project_id: str, set_type: str):
    metadata = get_metadata(project_id, ALTERNATE_DOMAIN)
    metadata['type'] = set_type

    return _set_metadata(project_id, metadata)

@log
def _set_metadata(project_id: str, metadata: str):
    master_token = get_master_token(project_id)
    url = f'https://{ALTERNATE_DOMAIN}/projects/{project_id}/{master_token}'
    
    data = f'{{"metadata": {metadata}}}'

    response = patch_url(url, data)

    return response

@log
def _set_scale(project_id: str, scale: int, enabled: bool, service_id='liferay'):
    url = f'https://{ALTERNATE_DOMAIN}/projects/{project_id}/services/{service_id}/scale'

    enabled = map_to_str(enabled, True)
    data = f'{{"scale": {scale}, "canAutoscale": {enabled} }}'

    response = patch_url(url, data)

    return response