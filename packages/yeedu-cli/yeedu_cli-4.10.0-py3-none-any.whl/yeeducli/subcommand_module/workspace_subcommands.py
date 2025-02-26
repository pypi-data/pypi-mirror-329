from yeeducli.openapi.workspace.workspace import Workspace
from yeeducli.openapi.workspace.workspace_files import WorkspaceFiles
from yeeducli.openapi.workspace.workspace_access_control import WorkspaceAccessControl
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.json_utils import *
import sys
import json

logger = Logger.get_logger(__name__, True)


# Workspace
def create_workspace(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json = Workspace.create_workspace(
            json_data)
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workspace(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = Workspace.get_workspace_by_id_or_name(
            json_data.get('workspace_id'),
            json_data.get('workspace_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workspace_stats(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = Workspace.get_workspace_stats(
            json_data.get('workspace_id'),
            json_data.get('workspace_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = Workspace.search_workspace_by_name(
            json_data.get('workspace_name'),
            json_data.get('enable'),
            json_data.get('page_number'),
            json_data.get('limit')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspaces(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = Workspace.list_workspaces(
            json_data.get('enable'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_workspace(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = process_null_values(remove_output(args))

        if json_data.get('workspace_id') is not None:
            del json_data["workspace_id"]
        if json_data.get('workspace_name') is not None:
            del json_data["workspace_name"]

        response_json = Workspace.edit_workspace_by_id_or_name(
            json.dumps(json_data),
            trim_json_data.get('workspace_id'),
            trim_json_data.get('workspace_name')
        )
        confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def enable_workspace(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = Workspace.enable_workspace_by_id_or_name(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('workspace_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def disable_workspace(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = Workspace.disable_workspace_by_id_or_name(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('workspace_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def export_workspace(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = Workspace.export_workspace(
            trim_json_data.get('enable'),
            trim_json_data.get('workspace_id'),
            trim_json_data.get('workspace_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def import_workspace(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        FileUtils.checkFilePathExists(
            file_path=trim_json_data.get('file_path'),
            argument='file_path',
            check_extension=True,
            extension='.yeedu'
        )

        trim_json_data['workspaceImport'] = FileUtils.readFileContent(
            trim_json_data.get('file_path'),
            validate_json=True
        )

        response_json = Workspace.import_workspace(
            trim_json_data.get('workspaceImport'),
            trim_json_data.get('permissive'),
            trim_json_data.get('overwrite'),
            trim_json_data.get('workspace_id'),
            trim_json_data.get('workspace_name'),
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Workspace Files
def create_workspace_files(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        base_params = {
            "workspace_id": trim_json_data.get('workspace_id'),
            "workspace_name": trim_json_data.get('workspace_name'),
            "overwrite": trim_json_data.get('overwrite'),
            "target_dir": trim_json_data.get('root_output_dir')
        }

        params = FileUtils.generate_upload_request_params(
            trim_json_data.get('local_file_path'),
            base_params,
            trim_json_data.get('recursive')
        )

        for param in params:

            response_json = WorkspaceFiles.add_workspace_files(
                param['local_file_path'],
                param['path'],
                param['overwrite'],
                param['workspace_id'],
                param['workspace_name'],
                param['is_dir'],
                param['target_dir']
            )
            confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workspace_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceFiles.get_workspace_files_by_id_or_name(
            json_data.get('workspace_id'),
            json_data.get('workspace_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )

        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceFiles.list_workspace_files_by_id_or_name(
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('recursive'),
            json_data.get('workspace_id'),
            json_data.get('workspace_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceFiles.search_workspace_files_by_id_or_name_and_file_name(
            json_data.get('file_name'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('recursive'),
            json_data.get('workspace_id'),
            json_data.get('workspace_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_workspace_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceFiles.delete_workspace_file_by_id_or_name(
            json_data.get('workspace_id'),
            json_data.get('workspace_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def download_workspace_files(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceFiles.download_workspace_files(
            json_data.get('workspace_id'),
            json_data.get('workspace_name'),
            json_data.get('file_id'),
            json_data.get('file_path')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

def get_workspace_files_usage(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceFiles.get_workspace_files_usage(
            json_data.get('workspace_id'),
            json_data.get('workspace_name')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
          
def rename_workspace_file(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceFiles.rename_workspace_file(
            json_data.get('workspace_id'),
            json_data.get('workspace_name'),
            json_data.get('file_id'),
            json_data.get('file_path'),
            json_data.get('file_name'),
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)

# Workspace Access Control
def create_workspace_user_access(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        del json_data["workspace_id"]

        response_json = WorkspaceAccessControl.create_workspace_user_access(
            trim_json_data.get('workspace_id')[0],
            json_data
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def create_workspace_group_access(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        del json_data["workspace_id"]

        response_json = WorkspaceAccessControl.create_workspace_group_access(
            trim_json_data.get('workspace_id')[0],
            json_data
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_workspace_user_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.delete_workspace_user_access(
            json_data.get('workspace_id'),
            json_data.get('user_id'),
            json_data.get('permission_id')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_workspace_group_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.delete_workspace_group_access(
            json_data.get('workspace_id'),
            json_data.get('group_id'),
            json_data.get('permission_id')
        )
        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_users(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.list_workspace_users(
            json_data.get('workspace_id'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_users_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.list_workspace_users_access(
            json_data.get('workspace_id'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('permission_id'),
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace_users_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.search_workspace_users_access(
            json_data.get('workspace_id'),
            json_data.get('username'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('permission_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace_users(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.search_workspace_users(
            json_data.get('workspace_id'),
            json_data.get('username'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def match_workspace_user(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.match_workspace_user(
            json_data.get('workspace_id'),
            json_data.get('username')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_groups(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.list_workspace_groups(
            json_data.get('workspace_id'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_groups_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.list_workspace_groups_access(
            json_data.get('workspace_id'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('permission_id'),
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace_groups_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.search_workspace_groups_access(
            json_data.get('workspace_id'),
            json_data.get('groupname'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('permission_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_workspace_groups(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.search_workspace_groups(
            json_data.get('workspace_id'),
            json_data.get('groupname'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def match_workspace_group(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.match_workspace_group(
            json_data.get('workspace_id'),
            json_data.get('groupname')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workspace_user_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.get_workspace_user_access(
            json_data.get('workspace_id'),
            json_data.get('user_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workspace_group_access(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = WorkspaceAccessControl.get_workspace_group_access(
            json_data.get('workspace_id'),
            json_data.get('group_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
