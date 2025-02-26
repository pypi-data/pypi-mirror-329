from yeeducli.openapi.iam.iam_lookup import IamLookup
from yeeducli.openapi.iam.user import User
from yeeducli.openapi.iam.shared_platform_and_admin import SharedPlatformAndAdmin
from yeeducli.utility.json_utils import *
from yeeducli.utility.logger_utils import Logger
import sys

logger = Logger.get_logger(__name__, True)


# User
def list_tenants(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = User.list_tenants(
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_tenants(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = User.search_tenants(
            json_data.get('tenant_name'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def associate_tenant(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = User.associate_tenant(
            json_data.get('tenant_id')[0])
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_user_info(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = User.get_user_info()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_user_roles(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = User.get_user_roles(
            json_data.get('tenant_id')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Shared Platform Admin and Admin
def sync_user(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = SharedPlatformAndAdmin.sync_user(
            json_data.get('username')[0])
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def sync_group(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SharedPlatformAndAdmin.sync_group(
            json_data.get('groupname'))

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_users(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SharedPlatformAndAdmin.list_users(
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('group_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_users(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SharedPlatformAndAdmin.search_users(
            json_data.get('username'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('group_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def match_user(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SharedPlatformAndAdmin.match_user(
            json_data.get('username')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_groups(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SharedPlatformAndAdmin.list_groups(
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('user_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_groups(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SharedPlatformAndAdmin.search_groups(
            json_data.get('groupname'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('user_id')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def match_group(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SharedPlatformAndAdmin.match_group(
            json_data.get('groupname')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# IAM LOOKUP
def list_resources(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.list_resources()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_resource(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.describe_resource(
            json_data.get('resource_id')[0])
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_permissions(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.list_permissions()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_permission(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.describe_permission(
            json_data.get('permission_id')[0])
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_roles(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.list_roles()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_role(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.describe_role(
            json_data.get('role_id')[0])
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_rules(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.list_rules()
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_rule(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.describe_rule(
            json_data.get('rule_id')[0])
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_cluster_permissions(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.list_cluster_permissions()

        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_cluster_permission(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = IamLookup.get__cluster_permission(
            json_data.get('permission_id'))

        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_workspace_permissions(args):
    try:
        json_data = trim_namespace_json(args)

        response_json = IamLookup.list_workspace_permissions()

        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workspace_permission(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = IamLookup.get__workspace_permission(
            json_data.get('permission_id'))

        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
