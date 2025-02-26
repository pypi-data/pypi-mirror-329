from difflib import SequenceMatcher
from yeeducli.utility.file_utils import FileUtils
from yeeducli.utility.logger_utils import Logger
from argparse import ArgumentTypeError
from yeeducli.constants import *
import json
import yaml
import sys

logger = Logger.get_logger(__name__, True)


def change_output(json_data_payload):
    try:
        for k, v in dict(json_data_payload).items():
            if type(v) == list and k not in VARCHAR_ARRAY_COLUMN_FULL_LIST:
                json_data_payload[k] = json_data_payload.pop(k)[0]

                if str(v[0]).lower() == 'true':
                    json_data_payload[k] = True
                elif str(v[0]).lower() == 'false':
                    json_data_payload[k] = False
    except Exception as e:
        logger.error(e)
        sys.exit(-1)
    return json_data_payload


def trim_namespace_json(args):
    try:
        json_data = vars(args)

        if json_data["yeedu"] in ['configure', 'logout']:
            del json_data["yeedu"]
            return json_data

        del json_data["yeedu"]
        del json_data["subcommand"]

        return json_data
    except Exception as e:
        logger.error(e)
        sys.exit(-1)


def get_similar_subcommand(args_subcommand, list_of_subcommand):
    try:
        if args_subcommand is not None:
            list_of_similar_subcommand = []
            splitted_args_command = args_subcommand.split('-')
            for subcommand in list_of_subcommand:
                splitted_subcommand = subcommand.split('-')
                i = 0
                percentage_match = 0
                for each_splitted_args_command in splitted_args_command:
                    if i >= 0 and i < len(splitted_subcommand):
                        percentage_match += similar(
                            splitted_subcommand[i], each_splitted_args_command)
                        i += 1
                if percentage_match >= 1.21:
                    list_of_similar_subcommand.append(subcommand)
            if len(list_of_similar_subcommand) > 0:
                return f"Did you mean? {list_of_similar_subcommand}"
            else:
                return f"Cannot find the provided subcommand: {args_subcommand}"
        else:
            return list_of_subcommand
    except Exception as e:
        logger.error(e)
        sys.exit(-1)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def remove_output(args, subcommand=None):
    try:
        json_data = vars(args)

        json_payload = json_data.copy()

        del json_payload["json_output"]
        del json_payload["yaml_output"]

        for k, v in dict(json_payload).items():
            if v is None:
                del json_payload[k]

        for k, v in dict(json_payload).items():

            if str(k) in VARCHAR_ARRAY_COLUMN_LIST and len(str(v).split(",")) >= 1:
                json_payload[k] = [item.strip() for item in str(
                    v).split(",")] if str(v).lower() != "null" else str(v).lower()

            if str(k) in ["conf"] and subcommand in ['create-conf', 'edit-conf', 'start']:
                json_payload[k] = set_labels_or_conf_or_env_var(
                    argument=k, conf=v, delimiter='=', expectedResult=[])
            elif str(k) in ["labels"] and subcommand in ['usage', 'invoice']:
                json_payload[k] = set_labels_or_conf_or_env_var(
                    argument=k, conf=v, delimiter='=', expectedResult={})

            if str(k) == "network_tags":
                if v == []:
                    pass
                else:
                    json_payload[k] = tags_validator(v)

            if str(k) == 'base64_encoded_credentials':
                credentials_json = {"encoded": str(v)}
                json_payload[k] = credentials_json

            if str(v).lower() == 'true':
                json_payload[k] = True
            elif str(v).lower() == 'false':
                json_payload[k] = False

        return json_payload
    except Exception as error:
        logger.exception(f"Error while preparing payload: {error}")
        sys.exit(-1)


def process_cluster_arguments(json_payload):
    try:
        for k, v in dict(json_payload).items():
            if str(k) == "cluster_type":
                json_payload[k] = str(v).upper()

            # if str(k) in VARCHAR_ARRAY_COLUMN_LIST and len(str(v).split(",")) >= 1:
            #     json_payload[k] = str(v).split(",")

            if str(k) in ['conf', 'conf_secret', 'env_var_secret', 'env_var', 'labels', 'packages', 'repositories', 'jars', 'archives', 'files', 'py_files']:
                json_payload[k] = set_labels_or_conf_or_env_var(
                    argument=k,
                    conf=v,
                    delimiter='=' if (
                        str(k) in ['env_var_secret', 'env_var', 'labels']) else ' ',
                    expectedResult={} if (
                        str(k) in ['conf_secret', 'env_var_secret', 'labels']) else []
                )

            if str(k) == 'bootstrap_shell_script_file_path':
                if str(v).lower() != "null":
                    bootstrap_shell_script_file_path = FileUtils.checkFilePathExists(
                        file_path=v,
                        argument='bootstrap_shell_script_file_path'
                    )
                    json_payload["bootstrap_shell_script"] = FileUtils.readFileContent(
                        bootstrap_shell_script_file_path
                    )
                else:
                    json_payload["bootstrap_shell_script"] = str(v).lower()

                del json_payload["bootstrap_shell_script_file_path"]

            engine_cluster_spark_config_keys = [
                'max_parallel_spark_job_execution_per_instance', 'num_of_workers']

            engine_cluster_spark_config = {'engine_cluster_spark_config': {}}

            for key in engine_cluster_spark_config_keys:
                if key in json_payload:
                    engine_cluster_spark_config['engine_cluster_spark_config'][key] = int(
                        json_payload[key])
                    del json_payload[key]

            if engine_cluster_spark_config['engine_cluster_spark_config']:
                json_payload.update(engine_cluster_spark_config)

        return json_payload

    except Exception as error:
        logger.exception(f"Error while preparing cluster payload: {error}")
        sys.exit(-1)


def process_cluster_spark_config_arguments(json_payload):
    try:
        spark_config_keys = ['conf', 'packages', 'repositories', 'jars', 'archives',
                             'env_var', 'conf_secret', 'env_var_secret', 'files', 'py_files']

        spark_config = {'spark_config': {}}

        for key in spark_config_keys:
            if key in json_payload:
                if key == 'py_files':
                    spark_config['spark_config']['py-files'] = json_payload[key]
                    del json_payload[key]
                else:
                    if key in ['conf_secret', 'env_var_secret']:
                        for k, v in json_payload[key].items():
                            if v.lower() == 'null':
                                json_payload[key][k] = None
                            else:
                                json_payload[key][k] = v

                    spark_config['spark_config'][key] = json_payload[key]
                    del json_payload[key]

        if spark_config['spark_config']:
            json_payload.update(spark_config)

        return json_payload

    except Exception as error:
        logger.exception(
            f"Error while preparing cluster spark config: {error}")
        sys.exit(-1)


def set_labels_or_conf_or_env_var(argument, conf, delimiter, expectedResult):
    try:
        result = expectedResult.copy()
        keys_set = set()

        if argument in ['packages', 'repositories', 'jars', 'archives', 'files', 'py_files']:
            return expectedResult if conf[0].lower() == 'null' else conf
        else:
            for item in conf:

                key_value = item[0].strip().split(delimiter, maxsplit=1)

                # check if any cluster spark config or secret we want to clear
                if len(key_value) == 1 and key_value[0].lower() == 'null':
                    return expectedResult

                # Check if multiple key value pairs are provided within a single label
                if len(item[0].split(",")) > 1 and argument == 'labels':
                    logger.error(
                        f"\nMultiple key=value pair detected in --labels='{item[0]}'.\n\nPlease provide a single key=value pair as --labels='key=value'")
                    sys.exit(-1)

                # Check if only key is provided without a value
                if len(key_value) != 2 or not key_value[0] or not key_value[1]:
                    logger.error(
                        f"Invalid input for '--{argument}'\n\nVALID\n --{argument}='key1{delimiter}value1'\n --{argument}='key2{delimiter}value2'\nINVALID\n --{argument}='{delimiter}value1'\n --{argument}='key2{delimiter}'")
                    sys.exit(-1)

                # Check for duplicate keys
                if key_value[0] in keys_set:
                    logger.error(
                        f"Duplicate key found in --{argument}: '{item[0]}'.")
                    sys.exit(-1)

                # Check if the key contains spaces
                if " " in key_value[0]:
                    logger.error(f"Invalid input for '--{argument}'.\n\nKeys cannot contain spaces. Detected in: '{key_value[0]}'."
                    )
                    sys.exit(-1)
                
                keys_set.add(key_value[0])

                if isinstance(expectedResult, list):
                    result.append(item[0])
                elif isinstance(expectedResult, dict):
                    result.update({key_value[0]: key_value[1]})

            return result

    except Exception as error:
        logger.error(f"Error while validating --{argument}: {error}")
        sys.exit(-1)


def tags_validator(tagsString):
    # if (len(tagsString.split(",")) % 2 == 0):
    tagsList = []
    uniquetagList = []
    duplicatetagList = []

    for tag in tagsString.split(","):
        tagsList.append(str(tag))

    for eachTag in tagsList:
        if eachTag not in uniquetagList:
            uniquetagList.append(eachTag)
        else:
            duplicatetagList.append(eachTag)
    if len(duplicatetagList) > 0:
        logger.error(
            f"The duplicate values for --tags are: {duplicatetagList}")
        sys.exit(-1)

    return tagsList
    # else:
    #     logger.error(
    #         f"Invalid input for '--network_tags'\n\nVALID\n --network_tags={VALID_NETWORK_TAG}\nINVALID\n --network_tags={INVALID_NETWORK_TAG}")
    #     sys.exit(-1)


def check_boolean(boolean):
    if boolean is not None:
        if (boolean.lower()) not in ['true', 'false']:
            raise ArgumentTypeError(
                f"invalid boolean value: '{boolean}' (choose from 'true', 'false')")
        else:
            return boolean.lower()


def confirm_output(response_json, json_data):

    if json_data["json_output"] == 'default':
        logger.info(response_json)

    elif json_data["yaml_output"] == 'true':
        logger.info(yaml.dump(
            data=response_json,
            indent=2,
            sort_keys=False,
            # added allow_unicode=True for strings like 'Intel®', 'Xeon®', and 'Epyc™'
            allow_unicode=True
        ))

    else:
        logger.info(json.dumps(
            obj=response_json,
            indent=2,
            # added ensure_ascii=False for strings like 'Intel®', 'Xeon®', and 'Epyc™'
            ensure_ascii=False
        ))


def response_validator(response):
    try:
        # Check if the response content type includes 'application/json'
        if 'application/json' in response.headers.get('Content-Type', ''):
            return response.json()
        else:
            logger.error(
                f"Received BAD RESPONSE : '{response.text}'\nwith status code : {response.status_code}")
            sys.exit(-1)
    except ValueError:
        logger.error(
            f"Response JSON Decoding failed as \nResponse is : '{response.text}'\nStatus code : {response.status_code}")
        sys.exit(-1)


def response_json_custom_order(response_json, custom_response_order):
    try:
        sorted_list = []
        json_length = len(response_json)
        if isinstance(response_json, dict):
            return {key: response_json[key] for key in custom_response_order}
        else:
            for i in range(json_length):
                sorted_list.append(
                    {key: response_json[i][key] for key in custom_response_order})
            return sorted_list
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def check_non_empty_string(value):
    if value is not None and value.strip() == "":
        raise ArgumentTypeError(
            f"string value cannot be empty: '{value}'")

    return value.strip()


def validate_array_of_intgers(value):
    try:
        if value is not None and value.strip() == "":
            raise ArgumentTypeError(
                f"Integer value cannot be empty: '{value}'")
        else:
            ids = [int(id) for id in value.split(',')]

            if not all(isinstance(id, int) for id in ids):
                raise ArgumentTypeError(
                    "Please provide a comma-separated list of integers.")
            return ids if len(ids) > 1 else ids.pop()
    except:
        raise ArgumentTypeError(
            f"Please provide a comma-separated list of integers: '{value}'")


def check_choices(values, choices):
    try:
        check_non_empty_string(values)

        list_of_values = [value.strip() for value in values.split(',')]

        if not all(value in choices for value in list_of_values):
            raise ArgumentTypeError(
                f"invalid choice: '{values}' (choose from {choices})")
        return list_of_values
    except ValueError:
        raise ArgumentTypeError(
            f"invalid choice: '{values}' (choose from {choices})")


def createOrUpdateHiveMetastoreConfig(config):
    try:
        requestBody = {}

        columnAlias = {
            'hive_site_xml_file_path': 'hiveSiteXml',
            'core_site_xml_file_path': 'coreSiteXml',
            'hdfs_site_xml_file_path': 'hdfsSiteXml',
            'krb5_conf_file_path': 'krb5Conf'
        }

        for key, value in config.items():
            if key in columnAlias.keys():
                if isinstance(value, str) and value.lower() != "null":
                    FileUtils.checkFilePathExists(
                        file_path=value, argument=key)
                    requestBody[columnAlias[key]
                                ] = FileUtils.readFileContent(value)

                if isinstance(value, str) and value.lower() == "null":
                    requestBody[columnAlias[key]] = value
            else:
                requestBody[key] = value

        return requestBody

    except Exception as e:
        logger.error(
            f"Failed to create or update Hive metastore configuration due to: {e}")
        sys.exit(-1)


def process_null_values(json_data):
    try:
        for key, value in json_data.items():
            if isinstance(value, str) and value.lower() == "null":
                json_data[key] = None

            elif isinstance(value, dict):
                json_data[key] = process_null_values(value)

        return json_data

    except Exception as e:
        logger.error(f"Failed to process null values due to error: {e}")


def validate_integer_and_null(value):
    try:
        if (isinstance(value, str) and value.lower() == "null"):
            return value.lower()

        return int(value)
    except (ValueError, TypeError):
        raise ArgumentTypeError(f"Invalid integer value: '{value}'")


def validate_string_and_null(value):
    if value is not None and value.strip() == "":
        raise ArgumentTypeError(
            f"string value cannot be empty: '{value}'")

    if (isinstance(value, str) and value.lower() == "null"):
        return value.lower()

    return value.strip()
