from os.path import join
from dotenv import load_dotenv
import logging
import os
import sys

load_dotenv()

HOME = os.path.expanduser('~')

YEEDU_HIDDEN_DIR = join(HOME, '.yeedu')

DEFAULT_CLI_LOG_PATH = join(join(YEEDU_HIDDEN_DIR, 'cli'), 'logs')

if os.getenv('YEEDU_RESTAPI_TOKEN_FILE_PATH') is not None:

    if os.path.isdir(os.getenv('YEEDU_RESTAPI_TOKEN_FILE_PATH')):
        logging.error(
            f"Provided environment variable: 'YEEDU_RESTAPI_TOKEN_FILE_PATH: {os.getenv('YEEDU_RESTAPI_TOKEN_FILE_PATH')}' doesnot contain filename or directory not found.")
        sys.exit(-1)
    else:
        CONFIG_FILE_PATH = os.getenv('YEEDU_RESTAPI_TOKEN_FILE_PATH')
else:
    CONFIG_FILE_PATH = join(YEEDU_HIDDEN_DIR, 'yeedu_cli.config')


def check_environment_variable_int(variable_name, default_value):
    value = os.getenv(variable_name)
    if value is None:
        return default_value

    try:
        int_value = int(value)
    except ValueError:
        raise ValueError(
            f"Environment variable: {variable_name} must include only integers but found: {value}")

    return int_value


try:
    YEEDU_CLI_MAX_LOG_FILES = check_environment_variable_int(
        "YEEDU_CLI_MAX_LOG_FILES", 5)
    YEEDU_CLI_MAX_LOG_FILE_SIZE = check_environment_variable_int(
        "YEEDU_CLI_MAX_LOG_FILE_SIZE", 30)

except ValueError as e:
    logging.error(f"Error: {e}")
    sys.exit(-1)

CREDENTIALS_FILE_PATH = join(YEEDU_HIDDEN_DIR, 'yeedu_credentials.config')

# CLOUD PROVIDERS
CLOUD_PROVIDERS_LIST = ['GCP', 'AWS', 'Azure']

# COMPUTE TYPES
COMPUTE_TYPES_LIST = ['compute_optimized', 'memory_optimized',
                      'general_purpose', 'gpu_accelerated', 'custom_compute', 'storage_optimized']

# CLUSTER TYPEs
CLUSTER_TYPE_LIST = ['YEEDU', 'STANDALONE', 'CLUSTER']

NOTEBOOK_LANGUAGE_LIST = ['python3', 'scala']

# JOB TYPE lang used for Spark Job conf
CREATE_JOB_TYPE_LANG = ['RAW_SCALA', 'Jar', 'Python3', 'SQL', 'THRIFT_SQL', 'YEEDU_FUNCTIONS']

SPARK_JOB_TYPE_LANG_FOR_CONF = ['RAW_SCALA', 'Jar', 'Python3', 'SQL']

# JOB TYPE lang
JOB_TYPE_LANG = ['RAW_SCALA', 'Jar', 'Python3', 'Scala', 'SQL']

NOTEBOOK_LANG = ['Python3', 'Scala']

SPARK_JOB_TYPE = ['SPARK_JOB', 'SPARK_SQL', 'NOTEBOOK', 'THRIFT_SQL', 'YEEDU_FUNCTIONS']

SPARK_JOB_TYPE_FOR_CONF = ['SPARK_JOB', 'SPARK_SQL', 'THRIFT_SQL', 'YEEDU_FUNCTIONS']

# SPARK JOB STATUS
SPARK_JOB_STATUS = ['submitted', 'running', 'done',
                    'error', 'terminated', 'stopping', 'stopped']

# RESOURCE SUBCOMMANDS LIST
RESOURCE_LIST = ['list-providers', 'list-disk-machine-types', 'list-credential-types', 'list-engine-cluster-instance-status', 'get-provider', 'list-provider-availability-zones', 'get-provider-availability-zone', 'list-provider-machine-types', 'get-provider-machine-type', 'list-spark-compute-types', 'list-spark-infra-versions', 'list-spark-job-status', 'list-workflow-execution-states', 'list-workflow-types', 'create-volume-conf', 'get-volume-conf', 'list-volume-confs', 'search-volume-confs', 'edit-volume-conf', 'delete-volume-conf', 'create-network-conf', 'list-network-confs', 'search-network-confs', 'get-network-conf', 'edit-network-conf', 'delete-network-conf', 'create-boot-disk-image-conf', 'list-boot-disk-image-confs', 'search-boot-disk-image-confs', 'get-boot-disk-image-conf', 'edit-boot-disk-image-conf', 'delete-boot-disk-image-conf',
                 'create-cloud-env', 'list-cloud-envs', 'search-cloud-envs', 'get-cloud-env', 'edit-cloud-env', 'delete-cloud-env', 'create-object-storage-manager', 'get-object-storage-manager', 'list-object-storage-managers', 'search-object-storage-managers', 'edit-object-storage-manager', 'delete-object-storage-manager', 'create-object-storage-manager-file', 'get-object-storage-manager-file', 'list-object-storage-manager-files', 'search-object-storage-manager-files', 'delete-object-storage-manager-file', 'download-object-storage-manager-file', 'create-hive-metastore-conf', 'list-hive-metastore-confs', 'search-hive-metastore-confs', 'get-hive-metastore-conf', 'edit-hive-metastore-conf', 'delete-hive-metastore-conf', 'create-credential-conf', 'list-credential-confs', 'search-credential-confs', 'get-credential-conf', 'edit-credential-conf', 'delete-credential-conf', 'list-linux-distros']

# CLUSTER SUBCOMMANDS LIST
CLUSTER_LIST = ['create-conf', 'list-confs', 'search-confs', 'get-conf', 'edit-conf', 'delete-conf', 'create', 'list', 'search', 'get', 'edit', 'destroy', 'enable', 'disable', 'start', 'stop', 'get-stats', 'list-status', 'logs',
                'stop-all-jobs', 'list-errors', 'associate-workspace', 'dissociate-workspace', 'list-workspaces', 'search-workspaces', 'list-workspace-clusters', 'search-workspace-clusters', 'get-user-access', 'get-group-access']

# WORKSPACE SUBCOMMANDS LIST

WORKSPACE_LIST = ['create', 'list', 'search', 'get', 'get-stats', 'edit', 'enable', 'disable', 'export', 'import', 'create-workspace-file', 'get-workspace-file', 'list-workspace-files', 'search-workspace-files', 'delete-workspace-file', 'download-workspace-file', 'rename-workspace-file', 'get-workspace-files-usage', 'create-user-access', 'create-group-access',
                  'delete-user-access', 'delete-group-access', 'list-users', 'list-users-access', 'search-users-access', 'search-users', 'match-user', 'list-groups', 'list-groups-access', 'search-groups-access', 'search-groups', 'match-group', 'get-user-access', 'get-group-access']

# JOB SUBCOMMANDS LIST
JOB_LIST = ['create-conf', 'get-conf', 'list-confs', 'search-confs', 'edit-conf', 'enable-conf', 'disable-conf',
            'export', 'start', 'get', 'search', 'list', 'stop', 'get-status', 'logs', 'get-workflow-job-instance']

# NOTEBOOK SUBCOMMANDS LIST
NOTEBOOK_LIST = ['create-conf', 'get-conf', 'list-confs', 'search-confs', 'edit-conf', 'enable-conf', 'disable-conf', 'export',
                 'start', 'kernel-start', 'kernel-status', 'kernel-interrupt', 'kernel-restart', 'get', 'search', 'list', 'stop', 'logs']

# BILLING SUBCOMMANDS LIST
BILLING_LIST = ['tenants', 'date-range', 'clusters',
                'machine-types', 'labels', 'usage', 'invoice']

# IAM SUBCOMMANDS LIST
IAM_LIST = ['list-tenants', 'search-tenants', 'associate-tenant', 'get-user-info', 'get-user-roles', 'sync-user', 'sync-group', 'list-user-groups', 'list-users', 'list-group-users', 'list-groups', 'list-resources', 'get-resource',            'list-permissions',
            'get-permission', 'list-roles', 'get-role', 'list-rules', 'get-rule', 'search-users',  'match-user', 'search-groups', 'match-group', 'list-workspace-permissions', 'get-workspace-permission']

# ADMIN SUBCOMMANDS LIST
ADMIN_LIST = ['list-users', 'search-users', 'get-user', 'get-user-roles', 'list-users-roles', 'get-role-users', 'list-groups', 'search-groups',
              'get-group', 'get-group-roles', 'list-groups-roles', 'get-role-groups', 'create-user-role', 'delete-user-role', 'create-group-role', 'delete-group-role']

# PLATFORM ADMIN SUBCOMMANDS LIST
PLATFORM_ADMIN_LIST = ['create-tenant', 'list-tenants', 'get-tenant', 'edit-tenant', 'delete-tenant', 'list-tenant-users', 'search-tenant-users', 'list-tenant-groups', 'search-tenant-groups', 'get-tenant-user', 'get-tenant-group',
                       'get-user-roles', 'get-group-roles', 'list-user-tenants', 'get-role-users', 'list-users-roles', 'list-groups-roles', 'get-role-groups', 'create-user-role', 'delete-user-role', 'create-group-role', 'delete-group-role', 'search-tenants']

COMMANDS_DICT = {
    'resource': RESOURCE_LIST,
    'cluster': CLUSTER_LIST,
    'workspace': WORKSPACE_LIST,
    'job': JOB_LIST,
    'notebook': NOTEBOOK_LIST,
    'billing': BILLING_LIST,
    'iam': IAM_LIST,
    'admin': ADMIN_LIST,
    'platform-admin': PLATFORM_ADMIN_LIST
}

# Columns list having data type as varchar array
VARCHAR_ARRAY_COLUMN_LIST = ['files', 'properties_file',
                             'packages', 'repositories', 'jars', 'archives', 'py_files']

VARCHAR_ARRAY_COLUMN_FULL_LIST = ['labels', 'conf', 'conf_secret', 'env_var', 'env_var_secret', 'network_tags', 'files', 'properties_file', 'packages', 'repositories', 'jars', 'archives',
                                  'py_files', 'cluster_ids', 'machine_type_ids', 'cloud_providers', 'job_type_langs', 'language', 'last_run_status', 'created_by_ids', 'modified_by_ids', 'job_type', 'job_status', 'job_conf_ids', 'notebook_status', 'notebook_conf_ids']

# TAG Samples used in network_tags_validator
VALID_NETWORK_TAG = 'key1,value1,key2,value2'

INVALID_NETWORK_TAG = 'key1,value1,key2'

CLOUD_PROVIDER_AVAILABILITY_ZONE_ORDER = [
    'availability_zone_id', 'cloud_provider', 'name', 'region', 'description', 'from_date', 'to_date']

CLOUD_PROVIDER_DISK_MACHINE_TYPE_ORDER = ['disk_type_id', 'cloud_provider',
                                          'name', 'has_fixed_size', 'min_size', 'max_size', 'from_date', 'to_date']

LOOKUP_AUTH_RULES_ORDER = ['rule_id', 'permission_type',
                           'resource', 'role', 'from_date', 'to_date']

LOOKUP_CREDENTIAL_TYPES_ORDER = [
    'credential_type_id', 'name', 'cloud_provider', 'from_date', 'to_date']
