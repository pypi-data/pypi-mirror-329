from yeeducli.openapi.resource.boot_disk_image_configuration import BootDiskImageConfiguration
from yeeducli.openapi.resource.volume_configuration import VolumeConfiguration
from yeeducli.openapi.resource.network_configuration import NetworkConfiguration
from yeeducli.openapi.resource.cloud_environment import CloudEnvironment
from yeeducli.openapi.resource.credentials_config import CredentialsConfig
from yeeducli.openapi.resource.object_storage_manager import ObjectStorageManager
from yeeducli.openapi.resource.object_storage_manager_files import ObjectStorageManagerFiles
from yeeducli.openapi.resource.hive_metastore_configuration import HiveMetastoreConfiguration
from yeeducli.openapi.resource.lookup import Lookup
from yeeducli.utility.json_utils import *
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.file_utils import FileUtils
import json
import sys
import re

logger = Logger.get_logger(__name__, True)


# Cloud Provider
def list_providers(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_providers()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_provider(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_provider_by_id(
            json_data.get('cloud_provider_id')[0])
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_az_by_provider_id(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = Lookup.get_az_by_provider_id(
            json_data.get('cloud_provider_id'),
            json_data.get('limit'),
            json_data.get('page_number')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_az_by_provider_id_and_zone_id(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = Lookup.get_az_by_provider_id_and_zone_id(
            json_data.get('cloud_provider_id')[0], json_data.get('availability_zone_id')[0])
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_machine_type_by_provider_id(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = Lookup.get_machine_type_by_provider_id(
            json_data.get('cloud_provider_id'),
            json_data.get('limit'),
            json_data.get('page_number')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_machine_type_by_provider_id_and_machine_type_id(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = Lookup.get_machine_type_by_provider_id_and_machine_type_id(
            json_data.get('cloud_provider_id')[0], json_data.get("machine_type_id")[0])
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_disk_machine_types(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_disk_machine_type()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_credential_types(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_credential_type(
            json_data.get('cloud_provider'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_engine_cluster_instance_status(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_lookup_engine_cluster_instance_status()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_spark_compute_type(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_lookup_spark_compute_type()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_spark_infra_version(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_lookup_spark_infra_version()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_spark_job_status(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_lookup_spark_job_status()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_workflow_execution_state(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_lookup_workflow_execution_state()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_workflow_type(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_lookup_workflow_type()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_linux_distros(args):
    try:
        json_data = trim_namespace_json(args)
        response_json = Lookup.get_lookup_linux_distros()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Volume Configuration
def create_volume(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = VolumeConfiguration.add_volume_config(
            json_data)
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_volume(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = VolumeConfiguration.list_volume_config(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_volume(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = VolumeConfiguration.search_volume_config(
            json_data.get('volume_conf_name'),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_volume(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = VolumeConfiguration.get_volume_config_by_id_or_name(
            json_data.get('volume_conf_id'),
            json_data.get('volume_conf_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_volume(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        json_data = process_null_values(remove_output(args))

        if json_data.get('volume_conf_id') is not None:
            del json_data['volume_conf_id']
        if json_data.get('volume_conf_name') is not None:
            del json_data['volume_conf_name']

        response_json = VolumeConfiguration.edit_volume_config_by_id_or_name(
            json.dumps(json_data),
            trim_json_data.get('volume_conf_id'),
            trim_json_data.get('volume_conf_name'))
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_volume(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = VolumeConfiguration.delete_volume_config_by_id_or_name(
            json_data.get('volume_conf_id'),
            json_data.get('volume_conf_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Network Configuration
def create_network(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = NetworkConfiguration.add_network_config_by_cp_id(
            json_data
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_network(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = NetworkConfiguration.list_network_config_by_cp_id(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider'))

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_network(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = NetworkConfiguration.search_network_config_by_cp_id(
            json_data.get("network_conf_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider'))

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_network(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = NetworkConfiguration.get_network_config_by_id_or_name(
            json_data.get('network_conf_id'),
            json_data.get('network_conf_name'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_network(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = process_null_values(remove_output(args))

        if json_data.get('network_conf_id') is not None:
            del json_data['network_conf_id']
        if json_data.get('network_conf_name') is not None:
            del json_data['network_conf_name']

        response_json = NetworkConfiguration.edit_network_config_by_id_or_name(
            json.dumps(json_data),
            trim_json_data.get('network_conf_id'),
            trim_json_data.get('network_conf_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_network(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = NetworkConfiguration.delete_network_config_by_id_or_name(
            json_data.get('network_conf_id'),
            json_data.get('network_conf_name'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Boot Disk Image Configuration
def create_boot_disk_image_config(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = BootDiskImageConfiguration.add_boot_disk_image_config(
            json_data
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_boot_disk_image_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = BootDiskImageConfiguration.list_boot_disk_image_config(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_boot_disk_image_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = BootDiskImageConfiguration.search_boot_disk_image_config(
            json_data.get("boot_disk_image_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_boot_disk_image_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = BootDiskImageConfiguration.get_boot_disk_image_config(
            json_data.get('boot_disk_image_id'),
            json_data.get('boot_disk_image_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_boot_disk_image_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = process_null_values(remove_output(args))

        if json_data.get('boot_disk_image_id') is not None:
            del json_data['boot_disk_image_id']
        if json_data.get('boot_disk_image_name') is not None:
            del json_data['boot_disk_image_name']

        response_json = BootDiskImageConfiguration.edit_boot_disk_image_config(
            json.dumps(json_data),
            trim_json_data.get('boot_disk_image_id'),
            trim_json_data.get('boot_disk_image_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_boot_disk_image_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = BootDiskImageConfiguration.delete_boot_disk_image_config(
            json_data.get('boot_disk_image_id'),
            json_data.get('boot_disk_image_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Credentials Configuration
def create_credential(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = remove_output(args)

        response_json = CredentialsConfig.add_credentials_config(
            json_data)
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_credentials(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = CredentialsConfig.list_credentials_config(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_credentials(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = CredentialsConfig.search_credentials_config(
            json_data.get("credentials_conf_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_credential(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = CredentialsConfig.get_credentials_config_by_id_or_name(
            json_data.get('credentials_conf_id'),
            json_data.get('credentials_conf_name'),
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_credential(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = process_null_values(remove_output(args))

        if json_data.get("credentials_conf_id"):
            del json_data["credentials_conf_id"]
        if json_data.get("credentials_conf_name"):
            del json_data["credentials_conf_name"]

        response_json = CredentialsConfig.edit_credentials_config_by_id_or_name(
            json.dumps(json_data),
            trim_json_data.get('credentials_conf_id'),
            trim_json_data.get('credentials_conf_name')
        )
        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_credential(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = CredentialsConfig.delete_credentials_config_by_id_or_name(
            json_data.get('credentials_conf_id'),
            json_data.get('credentials_conf_name'),
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Cloud Environment
def create_cloud_env(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = CloudEnvironment.add_cloud_env(
            json_data
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_cloud_envs(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = CloudEnvironment.list_cloud_env(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_cloud_envs(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = CloudEnvironment.search_cloud_env(
            json_data.get("cloud_env_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_cloud_env(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = CloudEnvironment.get_cloud_env(
            json_data.get('cloud_env_id'),
            json_data.get('cloud_env_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_cloud_env(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = process_null_values(remove_output(args))

        if json_data.get('cloud_env_id') is not None:
            del json_data['cloud_env_id']
        if json_data.get('cloud_env_name') is not None:
            del json_data['cloud_env_name']

        response_json = CloudEnvironment.edit_cloud_env(
            json.dumps(json_data),
            trim_json_data.get('cloud_env_id'),
            trim_json_data.get('cloud_env_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_cloud_env(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = CloudEnvironment.delete_cloud_env(
            json_data.get('cloud_env_id'),
            json_data.get('cloud_env_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Object Storage Manager Configuration
def create_object_storage_manager(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = ObjectStorageManager.add_object_storage_manager(
            json_data)
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_object_storage_manager(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ObjectStorageManager.list_object_storage_manager(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_object_storage_manager(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ObjectStorageManager.search_object_storage_manager(
            json_data.get("object_storage_manager_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get("cloud_provider")
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_object_storage_manager(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ObjectStorageManager.get_object_storage_manager_by_id_or_name(
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_object_storage_manager(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = process_null_values(remove_output(args))

        if json_data.get('object_storage_manager_id') is not None:
            del json_data['object_storage_manager_id']
        if json_data.get('object_storage_manager_name') is not None:
            del json_data['object_storage_manager_name']

        response_json = ObjectStorageManager.edit_object_storage_manager_by_id_or_name(
            json.dumps(json_data),
            trim_json_data.get('object_storage_manager_id'),
            trim_json_data.get('object_storage_manager_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_object_storage_manager(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = ObjectStorageManager.delete_object_storage_manager_by_id_or_name(
            trim_json_data.get('object_storage_manager_id'),
            trim_json_data.get('object_storage_manager_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Object Storage Manager Files Configuration
def create_object_storage_manager_files(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        base_params = {
            "object_storage_manager_id": trim_json_data.get('object_storage_manager_id'),
            "object_storage_manager_name": trim_json_data.get('object_storage_manager_name'),
            "overwrite": trim_json_data.get('overwrite'),
            "target_dir": trim_json_data.get('root_output_dir')
        }

        params = FileUtils.generate_upload_request_params(
            trim_json_data.get('local_file_path'),
            base_params,
            trim_json_data.get('recursive')
        )

        for param in params:

            response_json = ObjectStorageManagerFiles.add_object_storage_manager_files(
                param['local_file_path'],
                param['path'],
                param['overwrite'],
                param['object_storage_manager_id'],
                param['object_storage_manager_name'],
                param['is_dir'],
                param['target_dir']
            )
            confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_object_storage_manager_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ObjectStorageManagerFiles.get_object_storage_manager_files_by_id_or_name(
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )

        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_object_storage_manager_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ObjectStorageManagerFiles.list_object_storage_manager_files_by_id_or_name(
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('recursive'),
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_object_storage_manager_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ObjectStorageManagerFiles.search_object_storage_manager_files_by_id_or_name_and_file_name(
            json_data.get('file_name'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('recursive'),
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_object_storage_manager_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ObjectStorageManagerFiles.delete_object_storage_manager_file_by_id_or_name(
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def download_object_storage_manager_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ObjectStorageManagerFiles.download_object_storage_manager_files(
            json_data.get('object_storage_manager_id'),
            json_data.get('object_storage_manager_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

# Hive Metastore Configuration
def create_hive_metastore_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        json_data = createOrUpdateHiveMetastoreConfig(
            change_output(remove_output(args)))

        response_json = HiveMetastoreConfiguration.add_hive_metastore_configuration(
            json_data)

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_hive_metastore_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = HiveMetastoreConfiguration.list_hive_metastore_config(
            json_data.get('page_number'),
            json_data.get('limit'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_hive_metastore_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = HiveMetastoreConfiguration.search_hive_metastore_config(
            json_data.get('hive_metastore_conf_name'),
            json_data.get('page_number'),
            json_data.get('limit'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_hive_metastore_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = HiveMetastoreConfiguration.get_hive_metastore_config_by_id_or_name(
            json_data.get('hive_metastore_conf_id'),
            json_data.get('hive_metastore_conf_name'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_hive_metastore_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        json_data = process_null_values(
            createOrUpdateHiveMetastoreConfig(remove_output(args)))

        if json_data.get('hive_metastore_conf_id') is not None:
            del json_data['hive_metastore_conf_id']
        if json_data.get('hive_metastore_conf_name') is not None:
            del json_data['hive_metastore_conf_name']

        response_json = HiveMetastoreConfiguration.edit_hive_metastore_config(
            json.dumps(json_data),
            trim_json_data.get('hive_metastore_conf_id'),
            trim_json_data.get('hive_metastore_conf_name'))

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_hive_metastore_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = HiveMetastoreConfiguration.delete_hive_metastore_config_by_id(
            trim_json_data.get('hive_metastore_conf_id'),
            trim_json_data.get('hive_metastore_conf_name'))

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
