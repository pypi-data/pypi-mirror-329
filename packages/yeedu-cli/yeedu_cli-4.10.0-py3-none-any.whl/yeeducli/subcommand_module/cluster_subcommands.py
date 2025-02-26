from yeeducli.openapi.cluster.cluster_configuration import ClusterConfiguration
from yeeducli.openapi.cluster.cluster_instance import ClusterInstance
from yeeducli.openapi.cluster.download_cluster_instance_logs import DownloadClusterInstanceLogs
from yeeducli.openapi.cluster.cluster_workspace_mapping import ClusterWorkspaceMapping
from yeeducli.utility.json_utils import *
from yeeducli.utility.logger_utils import Logger
import sys
import json

logger = Logger.get_logger(__name__, True)


# Engine Cluster Configuration
def create_cluster_config(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = ClusterConfiguration.add_cluster_config(
            json_data
        )

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_cluster_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterConfiguration.get_cluster_config_by_id_or_name(
            json_data.get('cluster_conf_id'),
            json_data.get('cluster_conf_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_cluster_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterConfiguration.list_cluster_config(
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider'),
            json_data.get('compute_type')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_cluster_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterConfiguration.search_cluster_config(
            json_data.get("cluster_conf_name"),
            json_data.get("page_number"),
            json_data.get("limit"),
            json_data.get('cloud_provider'),
            json_data.get('compute_type')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_cluster_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = process_null_values(remove_output(args))

        if json_data.get('cluster_conf_id'):
            del json_data["cluster_conf_id"]
        if json_data.get('cluster_conf_name'):
            del json_data["cluster_conf_name"]

        response_json = ClusterConfiguration.edit_cluster_config(
            json.dumps(json_data),
            trim_json_data.get('cluster_conf_id'),
            trim_json_data.get('cluster_conf_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_cluster_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterConfiguration.delete_cluster_config_by_id_or_name(
            json_data.get('cluster_conf_id'),
            json_data.get('cluster_conf_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Cluster Instance
def create_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        json_data = process_cluster_spark_config_arguments(process_cluster_arguments(
            remove_output(args)))

        response_json = ClusterInstance.add_cluster_instance(
            json_data
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_instance(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.list_cluster_instance(
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('enable'),
            json_data.get('cluster_conf_id'),
            json_data.get('cluster_conf_name'),
            json_data.get('cluster_status'),
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_instance(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.search_cluster_instance_by_name(
            json_data.get('cluster_name'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('enable'),
            json_data.get('cluster_conf_id'),
            json_data.get('cluster_conf_name'),
            json_data.get('cluster_status'),
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_instance(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.get_cluster_instance_by_id_or_name(
            json_data.get('cluster_id'),
            json_data.get('cluster_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = process_null_values(process_cluster_spark_config_arguments(
            process_cluster_arguments(remove_output(args))))

        if json_data.get('cluster_id'):
            del json_data["cluster_id"]
        if json_data.get('cluster_name'):
            del json_data["cluster_name"]

        response_json = ClusterInstance.edit_cluster_instance(
            json.dumps(json_data),
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def destroy_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.destroy_cluster_instance_by_id_or_name(
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def enable_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.enable_cluster_instance_by_id_or_name(
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def disable_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.disable_cluster_instance_by_id_or_name(
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def start_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.start_cluster_instance_by_id_or_name(
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def stop_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.stop_cluster_instance_by_id_or_name(
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name'),
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_instance_status(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.list_cluster_status_by_cluster_instance_id_or_name(
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('cluster_id'),
            json_data.get('cluster_name')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def stop_all_jobs_on_cluster_instance(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.stop_all_jobs_on_cluster_instance(
            json_data.get('cluster_id')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_instance_errors(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.list_cluster_errors_by_cluster_instance_id(
            json_data.get('cluster_id'),
            json_data.get('cluster_status_id'),
            json_data.get('page_number'),
            json_data.get('limit')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Download Cluster Instance Log Files
def download_cluster_instance_log_records(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = DownloadClusterInstanceLogs.get_cluster_instance_log_records(
            json_data.get('log_type'),
            json_data.get('cluster_id'),
            json_data.get('cluster_name'),
            json_data.get('cluster_status_id')
        )
        if (response_json is not True):
            confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Get Spark Job Statistics of an Cluster Instance
def get_instance_job_stats(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterInstance.get_job_stats_by_cluster_instance_id_or_name(
            json_data.get('cluster_id'),
            json_data.get('cluster_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Cluster Workspace Mapping
def associate_workspace(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterWorkspaceMapping.associate_workspace(
            json_data.get('workspace_id'),
            json_data.get('cluster_id')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def dissociate_workspace(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterWorkspaceMapping.dissociate_workspace(
            json_data.get('workspace_id'),
            json_data.get('cluster_id')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_cluster_workspaces(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterWorkspaceMapping.list_cluster_workspaces(
            json_data.get('cluster_id'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_cluster_workspaces(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterWorkspaceMapping.search_cluster_workspaces(
            json_data.get('cluster_id'),
            json_data.get('workspace_name'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_clusters(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterWorkspaceMapping.list_workspace_clusters(
            json_data.get('workspace_id'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('cluster_status'),
            json_data.get('job_type'),
            json_data.get('enable')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace_clusters(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = ClusterWorkspaceMapping.search_workspace_clusters(
            json_data.get('workspace_id'),
            json_data.get('cluster_name'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('cluster_status'),
            json_data.get('job_type'),
            json_data.get('enable')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
