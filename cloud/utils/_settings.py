import os

# ==== USAGE ====
# Set FUNCTION to a method
# Set ARGS with parameters

FUNCTION='get_metadata'
ARGS=['lfrspencerwoo', 'api.liferay.cloud']

# FUNCTION='valid_functions'
# ARGS=[]

# ==== CONFIGURATION ====

PRINT_OUTPUT=True
WRITE_OUTPUT=True
WRITE_FILE='output.json'

LIFERAY_CLOUD_USERNAME = os.environ['LIFERAY_CLOUD_USERNAME']
LIFERAY_CLOUD_PASSWORD = os.environ['LIFERAY_CLOUD_PASSWORD']

# GITHUB_USERNAME = os.environ['GITHUB_USERNAME']
# GITHUB_PASSWORD = os.environ['GITHUB_PASSWORD']
# GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']

TARGET_DOMAIN='api.liferay.cloud'
# TARGET_DOMAIN='api.liferaycloud.dev'
# TARGET_DOMAIN='api.liferay.st'
# TARGET_DOMAIN='api.liferay.sh'

ALTERNATE_DOMAIN='api.liferay.sh'

PROTOCOL='https'