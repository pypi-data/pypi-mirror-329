from yeeducli.openapi.iam.common_platform_and_admin import CommonPlatformAndAdmin
from yeeducli.utility.json_utils import *
from yeeducli.utility.logger_utils import Logger
import sys

logger = Logger.get_logger(__name__, True)


# Platform Admin and Admin common
def list_tenant_users(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.list_tenant_users(
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('tenant_id'))
        else:
            response_json = CommonPlatformAndAdmin.list_tenant_users(
                json_data.get('page_number'),
                json_data.get('limit')
            )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_tenant_users(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.search_tenant_users(
                json_data.get('username'),
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('tenant_id'))
        else:
            response_json = CommonPlatformAndAdmin.search_tenant_users(
                json_data.get('username'),
                json_data.get('page_number'),
                json_data.get('limit')
            )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_tenant_user(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.get_tenant_user(
                json_data.get('user_id'), json_data.get('tenant_id'))
        else:
            response_json = CommonPlatformAndAdmin.get_tenant_user(
                json_data.get('user_id'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_user_roles(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.get_user_roles(
                json_data.get('user_id'), json_data.get('tenant_id'))
        else:
            response_json = CommonPlatformAndAdmin.get_user_roles(
                json_data.get('user_id'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_user_roles(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.list_user_roles(
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('tenant_id')
            )
        else:
            response_json = CommonPlatformAndAdmin.list_user_roles(
                json_data.get('page_number'),
                json_data.get('limit')
            )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_role_users(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.get_role_users(
                json_data.get('role_id'),
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('tenant_id')
            )
        else:
            response_json = CommonPlatformAndAdmin.get_role_users(
                json_data.get('role_id'),
                json_data.get('page_number'),
                json_data.get('limit')
            )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_tenant_groups(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.list_tenant_groups(
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('tenant_id'))
        else:
            response_json = CommonPlatformAndAdmin.list_tenant_groups(
                json_data.get('page_number'),
                json_data.get('limit')
            )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_tenant_groups(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.search_tenant_groups(
                json_data.get('groupname'),
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('tenant_id'))
        else:
            response_json = CommonPlatformAndAdmin.search_tenant_groups(
                json_data.get('groupname'),
                json_data.get('page_number'),
                json_data.get('limit')
            )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_tenant_group(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.get_tenant_group(
                json_data.get('group_id'), json_data.get('tenant_id'))
        else:
            response_json = CommonPlatformAndAdmin.get_tenant_group(
                json_data.get('group_id'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_group_roles(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.get_group_roles(
                json_data.get('group_id'), json_data.get('tenant_id'))
        else:
            response_json = CommonPlatformAndAdmin.get_group_roles(
                json_data.get('group_id'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_group_roles(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.list_group_roles(
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('tenant_id')
            )
        else:
            response_json = CommonPlatformAndAdmin.list_group_roles(
                json_data.get('page_number'),
                json_data.get('limit')
            )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_role_groups(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('tenant_id'):
            response_json = CommonPlatformAndAdmin.get_role_groups(
                json_data.get('role_id'),
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('tenant_id')
            )
        else:
            response_json = CommonPlatformAndAdmin.get_role_groups(
                json_data.get('role_id'),
                json_data.get('page_number'),
                json_data.get('limit')
            )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def create_user_role(args):
    try:
        json_data = change_output(vars(args))

        if json_data.get('yeedu') == 'platform-admin':
            response_json = CommonPlatformAndAdmin.create_user_role(
                json_data.get('user_id'),
                json_data.get('role_id'),
                json_data.get('yeedu'),
                json_data.get('tenant_id')
            )
        else:
            response_json = CommonPlatformAndAdmin.create_user_role(
                json_data.get('user_id'),
                json_data.get('role_id'),
                json_data.get('yeedu')
            )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_user_role(args):
    try:
        json_data = change_output(vars(args))

        if json_data.get('yeedu') == 'platform-admin':
            response_json = CommonPlatformAndAdmin.delete_user_role(
                json_data.get('user_id'),
                json_data.get('role_id'),
                json_data.get('yeedu'),
                json_data.get('tenant_id')
            )
        else:
            response_json = CommonPlatformAndAdmin.delete_user_role(
                json_data.get('user_id'),
                json_data.get('role_id'),
                json_data.get('yeedu')
            )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def create_group_role(args):
    try:
        json_data = change_output(vars(args))

        if json_data.get('yeedu') == 'platform-admin':
            response_json = CommonPlatformAndAdmin.create_group_role(
                json_data.get('group_id'),
                json_data.get('role_id'),
                json_data.get('yeedu'),
                json_data.get('tenant_id')
            )
        else:
            response_json = CommonPlatformAndAdmin.create_group_role(
                json_data.get('group_id'),
                json_data.get('role_id'),
                json_data.get('yeedu')
            )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_group_role(args):
    try:
        json_data = change_output(vars(args))

        if json_data.get('yeedu') == 'platform-admin':
            response_json = CommonPlatformAndAdmin.delete_group_role(
                json_data.get('group_id'),
                json_data.get('role_id'),
                json_data.get('yeedu'),
                json_data.get('tenant_id')
            )
        else:
            response_json = CommonPlatformAndAdmin.delete_group_role(
                json_data.get('group_id'),
                json_data.get('role_id'),
                json_data.get('yeedu')
            )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
