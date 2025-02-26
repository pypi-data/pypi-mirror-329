from yeeducli.subcommand_module.resource_subcommands import *
from yeeducli.subcommand_module.cluster_subcommands import *
from yeeducli.subcommand_module.workspace_subcommands import *
from yeeducli.subcommand_module.job_subcommands import *
from yeeducli.subcommand_module.notebook_subcommands import *
from yeeducli.subcommand_module.iam_subcommands import list_tenants as listTenants, search_tenants as searchTenants, associate_tenant, get_user_info, get_user_roles as getUserRoles, sync_user, sync_group, list_groups, list_users, list_resources, describe_resource, list_permissions, describe_permission, list_roles, describe_role, list_rules, describe_rule, search_users, match_user, search_groups, match_group, list_workspace_permissions, get_workspace_permission
from yeeducli.subcommand_module.common_platform_and_admin_subcommands import *
from yeeducli.subcommand_module.platform_admin_subcommands import *
from yeeducli.subcommand_module.configure_subcommands import *
from yeeducli.subcommand_module.billing_subcommands import *
from yeeducli.utility.logger_utils import Logger
import sys

logger = Logger.get_logger(__name__, True)


class ServiceSubcommand:
    def call_configure_service_subcommand(args):
        try:
            if args.yeedu == 'configure':
                configure_user(args)
            elif args.yeedu == 'logout':
                user_logout(args)
        except Exception as e:
            logger.exception(e)
            sys.exit(-1)

    def call_resource_service_subcommand(args):
        try:
            if args.subcommand == 'get-provider':
                describe_provider(args)
            elif args.subcommand == 'list-providers':
                list_providers(args)
            elif args.subcommand == 'list-disk-machine-types':
                list_disk_machine_types(args)
            elif args.subcommand == 'list-credential-types':
                list_credential_types(args)
            elif args.subcommand == 'list-engine-cluster-instance-status':
                list_lookup_engine_cluster_instance_status(args)
            elif args.subcommand == 'list-provider-availability-zones':
                list_az_by_provider_id(args)
            elif args.subcommand == 'get-provider-availability-zone':
                describe_az_by_provider_id_and_zone_id(args)
            elif args.subcommand == 'list-provider-machine-types':
                list_machine_type_by_provider_id(args)
            elif args.subcommand == 'get-provider-machine-type':
                describe_machine_type_by_provider_id_and_machine_type_id(args)
            elif args.subcommand == 'list-spark-compute-types':
                list_lookup_spark_compute_type(args)
            elif args.subcommand == 'list-spark-infra-versions':
                list_lookup_spark_infra_version(args)
            elif args.subcommand == 'list-spark-job-status':
                list_lookup_spark_job_status(args)
            elif args.subcommand == 'list-workflow-execution-states':
                list_lookup_workflow_execution_state(args)
            elif args.subcommand == 'list-workflow-types':
                list_lookup_workflow_type(args)
            elif args.subcommand == 'list-linux-distros':
                list_lookup_linux_distros(args)
            elif args.subcommand == 'create-volume-conf':
                create_volume(args)
            elif args.subcommand == 'list-volume-confs':
                list_volume(args)
            elif args.subcommand == 'search-volume-confs':
                search_volume(args)
            elif args.subcommand == 'get-volume-conf':
                describe_volume(args)
            elif args.subcommand == 'edit-volume-conf':
                edit_volume(args)
            elif args.subcommand == 'delete-volume-conf':
                delete_volume(args)
            elif args.subcommand == 'create-network-conf':
                create_network(args)
            elif args.subcommand == 'list-network-confs':
                list_network(args)
            elif args.subcommand == 'search-network-confs':
                search_network(args)
            elif args.subcommand == 'get-network-conf':
                describe_network(args)
            elif args.subcommand == 'edit-network-conf':
                edit_network(args)
            elif args.subcommand == 'delete-network-conf':
                delete_network(args)
            elif args.subcommand == 'create-boot-disk-image-conf':
                create_boot_disk_image_config(args)
            elif args.subcommand == 'list-boot-disk-image-confs':
                list_boot_disk_image_config(args)
            elif args.subcommand == 'search-boot-disk-image-confs':
                search_boot_disk_image_config(args)
            elif args.subcommand == 'get-boot-disk-image-conf':
                describe_boot_disk_image_config(args)
            elif args.subcommand == 'edit-boot-disk-image-conf':
                edit_boot_disk_image_config(args)
            elif args.subcommand == 'delete-boot-disk-image-conf':
                delete_boot_disk_image_config(args)
            elif args.subcommand == 'create-credential-conf':
                create_credential(args)
            elif args.subcommand == 'list-credential-confs':
                list_credentials(args)
            elif args.subcommand == 'search-credential-confs':
                search_credentials(args)
            elif args.subcommand == 'get-credential-conf':
                describe_credential(args)
            elif args.subcommand == 'edit-credential-conf':
                edit_credential(args)
            elif args.subcommand == 'delete-credential-conf':
                delete_credential(args)
            elif args.subcommand == 'create-cloud-env':
                create_cloud_env(args)
            elif args.subcommand == 'list-cloud-envs':
                list_cloud_envs(args)
            elif args.subcommand == 'search-cloud-envs':
                search_cloud_envs(args)
            elif args.subcommand == 'get-cloud-env':
                get_cloud_env(args)
            elif args.subcommand == 'edit-cloud-env':
                edit_cloud_env(args)
            elif args.subcommand == 'delete-cloud-env':
                delete_cloud_env(args)
            elif args.subcommand == 'create-object-storage-manager':
                create_object_storage_manager(args)
            elif args.subcommand == 'list-object-storage-managers':
                list_object_storage_manager(args)
            elif args.subcommand == 'search-object-storage-managers':
                search_object_storage_manager(args)
            elif args.subcommand == 'get-object-storage-manager':
                get_object_storage_manager(args)
            elif args.subcommand == 'edit-object-storage-manager':
                edit_object_storage_manager(args)
            elif args.subcommand == 'delete-object-storage-manager':
                delete_object_storage_manager(args)
            elif args.subcommand == 'create-object-storage-manager-file':
                create_object_storage_manager_files(args)
            elif args.subcommand == 'get-object-storage-manager-file':
                get_object_storage_manager_files(args)
            elif args.subcommand == 'list-object-storage-manager-files':
                list_object_storage_manager_files(args)
            elif args.subcommand == 'search-object-storage-manager-files':
                search_object_storage_manager_files(args)
            elif args.subcommand == 'delete-object-storage-manager-file':
                delete_object_storage_manager_files(args)
            elif args.subcommand == 'download-object-storage-manager-file':
                download_object_storage_manager_files(args)
            elif args.subcommand == 'create-hive-metastore-conf':
                create_hive_metastore_config(args)
            elif args.subcommand == 'list-hive-metastore-confs':
                list_hive_metastore_config(args)
            elif args.subcommand == 'search-hive-metastore-confs':
                search_hive_metastore_config(args)
            elif args.subcommand == 'get-hive-metastore-conf':
                describe_hive_metastore_config(args)
            elif args.subcommand == 'edit-hive-metastore-conf':
                edit_hive_metastore_config(args)
            elif args.subcommand == 'delete-hive-metastore-conf':
                delete_hive_metastore_config(args)
            else:
                logger.error("\nInternal resource subcommand handling error\n")
                sys.exit(-1)
        except Exception as e:
            logger.exception(e)
            sys.exit(-1)

    def call_cluster_service_subcommand(args):
        try:
            if args.subcommand == 'create-conf':
                create_cluster_config(args)
            elif args.subcommand == 'list-confs':
                list_cluster_config(args)
            elif args.subcommand == 'search-confs':
                search_cluster_config(args)
            elif args.subcommand == 'get-conf':
                get_cluster_config(args)
            elif args.subcommand == 'edit-conf':
                edit_cluster_config(args)
            elif args.subcommand == 'delete-conf':
                delete_cluster_config(args)
            elif args.subcommand == 'create':
                create_instance(args)
            elif args.subcommand == 'list':
                list_instance(args)
            elif args.subcommand == 'search':
                search_instance(args)
            elif args.subcommand == 'get':
                get_instance(args)
            elif args.subcommand == 'edit':
                edit_instance(args)
            elif args.subcommand == 'destroy':
                destroy_instance(args)
            elif args.subcommand == 'enable':
                enable_instance(args)
            elif args.subcommand == 'disable':
                disable_instance(args)
            elif args.subcommand == 'start':
                start_instance(args)
            elif args.subcommand == 'stop':
                stop_instance(args)
            elif args.subcommand == 'list-status':
                list_instance_status(args)
            elif args.subcommand == 'stop-all-jobs':
                stop_all_jobs_on_cluster_instance(args)
            elif args.subcommand == 'list-errors':
                list_instance_errors(args)
            elif args.subcommand == 'logs':
                download_cluster_instance_log_records(args)
            elif args.subcommand == 'get-stats':
                get_instance_job_stats(args)
            elif args.subcommand == 'associate-workspace':
                associate_workspace(args)
            elif args.subcommand == 'dissociate-workspace':
                dissociate_workspace(args)
            elif args.subcommand == 'list-workspaces':
                list_cluster_workspaces(args)
            elif args.subcommand == 'search-workspaces':
                search_cluster_workspaces(args)
            elif args.subcommand == 'list-workspace-clusters':
                list_workspace_clusters(args)
            elif args.subcommand == 'search-workspace-clusters':
                search_workspace_clusters(args)
            else:
                logger.error("\nInternal cluster subcommand handling error\n")
                sys.exit(-1)
        except Exception as e:
            logger.exception(e)
            sys.exit(-1)

    def call_workspace_service_subcommand(args):
        try:
            if args.subcommand == 'create':
                create_workspace(args)
            elif args.subcommand == 'list':
                list_workspaces(args)
            elif args.subcommand == 'search':
                search_workspace(args)
            elif args.subcommand == 'get':
                get_workspace(args)
            elif args.subcommand == 'get-stats':
                get_workspace_stats(args)
            elif args.subcommand == 'edit':
                edit_workspace(args)
            elif args.subcommand == 'enable':
                enable_workspace(args)
            elif args.subcommand == 'disable':
                disable_workspace(args)
            elif args.subcommand == 'export':
                export_workspace(args)
            elif args.subcommand == 'import':
                import_workspace(args)
            elif args.subcommand == 'create-workspace-file':
                create_workspace_files(args)
            elif args.subcommand == 'get-workspace-file':
                get_workspace_files(args)
            elif args.subcommand == 'list-workspace-files':
                list_workspace_files(args)
            elif args.subcommand == 'search-workspace-files':
                search_workspace_files(args)
            elif args.subcommand == 'delete-workspace-file':
                delete_workspace_files(args)
            elif args.subcommand == 'download-workspace-file':
                download_workspace_files(args)
            elif args.subcommand == 'get-workspace-files-usage':
                get_workspace_files_usage(args)
            elif args.subcommand == 'rename-workspace-file':
                rename_workspace_file(args)
            elif args.subcommand == 'create-user-access':
                create_workspace_user_access(args)
            elif args.subcommand == 'create-group-access':
                create_workspace_group_access(args)
            elif args.subcommand == 'delete-user-access':
                delete_workspace_user_access(args)
            elif args.subcommand == 'delete-group-access':
                delete_workspace_group_access(args)
            elif args.subcommand == 'list-users':
                list_workspace_users(args)
            elif args.subcommand == 'list-users-access':
                list_workspace_users_access(args)
            elif args.subcommand == 'search-users-access':
                search_workspace_users_access(args)
            elif args.subcommand == 'search-users':
                search_workspace_users(args)
            elif args.subcommand == 'match-user':
                match_workspace_user(args)
            elif args.subcommand == 'list-groups':
                list_workspace_groups(args)
            elif args.subcommand == 'list-groups-access':
                list_workspace_groups_access(args)
            elif args.subcommand == 'search-groups-access':
                search_workspace_groups_access(args)
            elif args.subcommand == 'search-groups':
                search_workspace_groups(args)
            elif args.subcommand == 'match-group':
                match_workspace_group(args)
            elif args.subcommand == 'get-user-access':
                get_workspace_user_access(args)
            elif args.subcommand == 'get-group-access':
                get_workspace_group_access(args)
            else:
                logger.error(
                    "\nInternal workspace subcommand handling error\n")
                sys.exit(-1)
        except Exception as e:
            logger.exception(e)
            sys.exit(-1)

    def call_job_service_subcommand(args):
        try:
            if args.subcommand == 'create-conf':
                create_spark_job_config(args)
            elif args.subcommand == 'list-confs':
                list_spark_job_config(args)
            elif args.subcommand == 'search-confs':
                search_spark_job_configs(args)
            elif args.subcommand == 'get-conf':
                describe_spark_job_config(args)
            elif args.subcommand == 'edit-conf':
                edit_spark_job_config(args)
            elif args.subcommand == 'enable-conf':  # delete-conf
                enable_spark_job_config(args)
            elif args.subcommand == 'disable-conf':
                disable_spark_job_config(args)
            elif args.subcommand == 'export':
                export_spark_job_config(args)
            elif args.subcommand == 'start':
                start_spark_job_run(args)
            elif args.subcommand == 'list':
                list_spark_job_inst(args)
            elif args.subcommand == 'search':
                search_spark_job_inst(args)
            elif args.subcommand == 'get':
                describe_spark_job_inst(args)
            elif args.subcommand == 'stop':
                stop_spark_job_inst(args)
            elif args.subcommand == 'logs':
                download_job_instance_log_records(args)
            elif args.subcommand == 'get-workflow-job-instance':
                get_workflow_job_instance_details(args)
            elif args.subcommand == 'get-status':
                get_spark_job_inst_status(args)
            else:
                logger.error("\nInternal job subcommand handling error\n")
                sys.exit(-1)
        except Exception as e:
            logger.exception(e)
            sys.exit(-1)

    def call_notebook_service_subcommand(args):
        try:
            if args.subcommand == 'create-conf':
                create_notebook_config(args)
            elif args.subcommand == 'list-confs':
                list_notebook_configs(args)
            elif args.subcommand == 'search-confs':
                search_notebook_configs(args)
            elif args.subcommand == 'get-conf':
                get_notebook_config(args)
            elif args.subcommand == 'edit-conf':
                edit_notebook_config(args)
            elif args.subcommand == 'enable-conf':
                enable_notebook_config(args)
            elif args.subcommand == 'disable-conf':
                disable_notebook_config(args)
            elif args.subcommand == 'export':
                export_notebook_config(args)
            elif args.subcommand == 'start':
                start_notebook_run(args)
            elif args.subcommand == 'kernel-start':
                notebook_kernel_start(args)
            elif args.subcommand == 'kernel-status':
                notebook_kernel_status(args)
            elif args.subcommand == 'kernel-interrupt':
                notebook_kernel_interrupt(args)
            elif args.subcommand == 'kernel-restart':
                notebook_kernel_restart(args)
            elif args.subcommand == 'list':
                list_notebook_instances(args)
            elif args.subcommand == 'search':
                search_notebook_instances(args)
            elif args.subcommand == 'get':
                get_notebook_instance(args)
            elif args.subcommand == 'stop':
                stop_notebook_instance(args)
            elif args.subcommand == 'logs':
                download_notebook_instance_log_records(args)
            else:
                logger.error("\nInternal notebook subcommand handling error\n")
                sys.exit(-1)
        except Exception as e:
            logger.exception(e)
            sys.exit(-1)

    def call_billing_service_subcommand(args):
        try:
            if args.subcommand == 'tenants':
                list_billed_tenants(args)
            elif args.subcommand == 'date-range':
                list_billed_date_range(args)
            elif args.subcommand == 'clusters':
                list_billed_clusters(args)
            elif args.subcommand == 'machine-types':
                list_billed_machine_types(args)
            elif args.subcommand == 'labels':
                list_billed_labels(args)
            elif args.subcommand == 'usage':
                list_billed_usage(args)
            elif args.subcommand == 'invoice':
                list_billed_invoice(args)
            else:
                logger.error("\nInternal billing subcommand handling error\n")
                sys.exit(-1)
        except Exception as e:
            logger.exception(e)
            sys.exit(-1)

    def call_iam_service_subcommand(args):
        try:
            if args.subcommand == 'list-tenants':
                listTenants(args)
            elif args.subcommand == 'search-tenants':
                searchTenants(args)
            elif args.subcommand == 'associate-tenant':
                associate_tenant(args)
            elif args.subcommand == 'get-user-info':
                get_user_info(args)
            elif args.subcommand == 'get-user-roles':
                getUserRoles(args)
            elif args.subcommand == 'sync-user':
                sync_user(args)
            elif args.subcommand == 'sync-group':
                sync_group(args)
            elif args.subcommand == 'list-users' or args.subcommand == 'list-group-users':
                list_users(args)
            elif args.subcommand == 'search-users':
                search_users(args)
            elif args.subcommand == 'match-user':
                match_user(args)
            elif args.subcommand == 'list-groups' or args.subcommand == 'list-user-groups':
                list_groups(args)
            elif args.subcommand == 'search-groups':
                search_groups(args)
            elif args.subcommand == 'match-group':
                match_group(args)
            elif args.subcommand == 'list-resources':
                list_resources(args)
            elif args.subcommand == 'get-resource':
                describe_resource(args)
            elif args.subcommand == 'list-permissions':
                list_permissions(args)
            elif args.subcommand == 'get-permission':
                describe_permission(args)
            elif args.subcommand == 'list-workspace-permissions':
                list_workspace_permissions(args)
            elif args.subcommand == 'get-workspace-permission':
                get_workspace_permission(args)
            elif args.subcommand == 'list-roles':
                list_roles(args)
            elif args.subcommand == 'get-role':
                describe_role(args)
            elif args.subcommand == 'list-rules':
                list_rules(args)
            elif args.subcommand == 'get-rule':
                describe_rule(args)
            else:
                logger.error("\nInternal iam subcommand handling error\n")
                sys.exit(-1)
        except Exception as e:
            logger.exception(e)
            sys.exit(-1)

    def call_common_platform_and_admin_service_subcommand(args):
        try:
            if args.subcommand == 'list-tenants':
                list_tenants(args)
            elif args.subcommand == 'create-tenant':
                create_tenant(args)
            elif args.subcommand == 'get-tenant':
                get_tenant(args)
            elif args.subcommand == 'edit-tenant':
                edit_tenant(args)
            elif args.subcommand == 'delete-tenant':
                delete_tenant(args)
            elif args.subcommand == 'search-tenants':
                search_tenants(args)
            elif args.subcommand == 'list-users' or args.subcommand == 'list-tenant-users':
                list_tenant_users(args)
            elif args.subcommand == 'search-users' or args.subcommand == 'search-tenant-users':
                search_tenant_users(args)
            elif args.subcommand == 'get-user' or args.subcommand == 'get-tenant-user':
                get_tenant_user(args)
            elif args.subcommand == 'get-user-roles':
                get_user_roles(args)
            elif args.subcommand == 'list-users-roles':
                list_user_roles(args)
            elif args.subcommand == 'get-role-users':
                get_role_users(args)
            elif args.subcommand == 'list-groups' or args.subcommand == 'list-tenant-groups':
                list_tenant_groups(args)
            elif args.subcommand == 'search-groups' or args.subcommand == 'search-tenant-groups':
                search_tenant_groups(args)
            elif args.subcommand == 'get-group' or args.subcommand == 'get-tenant-group':
                get_tenant_group(args)
            elif args.subcommand == 'get-group-roles':
                get_group_roles(args)
            elif args.subcommand == 'list-groups-roles':
                list_group_roles(args)
            elif args.subcommand == 'get-role-groups':
                get_role_groups(args)
            elif args.subcommand == 'create-user-role':
                create_user_role(args)
            elif args.subcommand == 'delete-user-role':
                delete_user_role(args)
            elif args.subcommand == 'create-group-role':
                create_group_role(args)
            elif args.subcommand == 'delete-group-role':
                delete_group_role(args)
            elif args.subcommand == 'list-user-tenants':
                list_user_tenants(args)
            else:
                logger.error(
                    "\nInternal common platform admin and admin subcommand handling error\n")
                sys.exit(-1)
        except Exception as e:
            logger.exception(e)
            sys.exit(-1)
