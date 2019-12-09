import json
import requests
import os

LIFERAY_CLOUD_USERNAME = os.environ['LIFERAY_CLOUD_USERNAME']
LIFERAY_CLOUD_PASSWORD = os.environ['LIFERAY_CLOUD_PASSWORD']

# GITHUB_USERNAME = os.environ['GITHUB_USERNAME']
# GITHUB_PASSWORD = os.environ['GITHUB_PASSWORD']
# GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']


TARGET_DOMAIN='api.liferay.cloud'
# TARGET_DOMAIN='api.liferaycloud.dev'
# TARGET_DOMAIN='api.liferay.st'
# TARGET_DOMAIN='api.liferay.sh'


# List of API endpoints
# https://github.com/liferaycloud/api/tree/develop#table-of-contents

def get_url(url):
    response = requests.get(url, auth=(LIFERAY_CLOUD_USERNAME, LIFERAY_CLOUD_PASSWORD))

    return json.loads(response.text)

def get_master_token(projectId):
    url = 'https://{}}/projects/{}/masterToken'.format(TARGET_DOMAIN, projectId)

    response = get_url(url)

    master_token = response['masterToken']
    return master_token

def get_metadata(projectId):

    url = 'https://{}}/projects/{}'.format(TARGET_DOMAIN, projectId)

    response = get_url(url)

    metadata = response['metadata']
    return metadata


print(get_metadata('lfrspencerwoo'))