from pathlib import Path
from yeeducli.utility.logger_utils import Logger
from requests.structures import CaseInsensitiveDict
import json
import os
import sys

logger = Logger.get_logger(__name__, True)


class FileUtils:

    def checkFilePathExists(file_path, argument, check_extension=False, extension=None, check_dir=False):
        try:
            if file_path == None:
                logger.error("Please provide a local file path\n")
                sys.exit(-1)
            else:
                if check_dir:
                    if file_path is not None and not os.path.isdir(file_path):
                        file_error = {
                            "error": f"The directory '{file_path}' cannot be found for the argument --{argument}"}
                        logger.error(json.dumps(file_error, indent=2))
                        sys.exit(-1)
                    else:
                        return file_path
                else:

                    if (file_path is not None and os.path.isfile(file_path)):

                        # checking if the file extension is of provided exxtension

                        if check_extension and extension is not None and os.path.splitext(file_path)[1] != extension:
                            extension_error = {
                                "error": f"The file at the provided path '{file_path}' must have the extension '{extension}'."
                            }
                            logger.error(json.dumps(extension_error, indent=2))
                            sys.exit(-1)
                        else:
                            return file_path
                    else:
                        file_error = {
                            "error": f"The file cannot be found at '{file_path}' for the argument --{argument}"}
                        logger.error(json.dumps(file_error, indent=2))
                        sys.exit(-1)
        except Exception as e:
            logger.error(f"Failed to check file path exists due to: {e}")
            sys.exit(-1)

    def readFileContent(file_path, validate_json=False):
        try:
            # 'with' statement automatically closes the file after the block is done
            with open(file_path, 'r') as f:
                file_content = f.read()

            if validate_json:
                try:
                    json_content = json.loads(file_content)
                    return json_content
                except json.JSONDecodeError as json_err:
                    logger.error(
                        f"Failed to read JSON file content from '{file_path}' due to: {json_err}")
                    sys.exit(-1)
            else:
                return file_content

        except Exception as e:
            logger.error(
                f"Failed to read file content from '{file_path}' due to: {e}")
            sys.exit(-1)

    def writeFileContent(file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)

            return {
                "message": f"Export successful and stored at location: {file_path}"
            }

        except Exception as e:
            logger.error(
                f"Failed to read file content from {file_path} due to: {e}")
            sys.exit(-1)

    def read_file_in_chunks(local_file_path, chunk_size):
        """
        Reads a file in chunks and yields each chunk for processing.

        Args:
            local_file_path (str): Path to the local file or a directory.
            chunk_size (int): Size of each chunk in bytes.

        Yields:
            bytes: A chunk of the file.

        Notes:
            This function helps process large files efficiently without loading them fully into memory.
        """
        try:
            if Path(local_file_path).is_file():
                with open(local_file_path, 'rb') as file:
                    while True:
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk

            elif Path(local_file_path).is_dir():
                # Yielding an empty byte string to simulate an empty chunk for creating a directory
                yield b''

            else:
                logger.error(json.dumps(
                    {"error": "The local_file_path must point to an existing file or directory."}, indent=2))
                sys.exit(-1)

        except Exception as e:
            logger.exception(f"Error occurred: {e}")
            sys.exit(-1)

    def generate_upload_request_params(local_file_path, base_params, recursive):
        """
        Prepares request parameters for uploading files and directories.

        Args:
            local_file_path (str): The path to the local file or directory being uploaded.
            base_params (dict): The base parameters to be used in the upload request.
            recursive (bool): Indicates whether the upload should process directories recursively.

        Returns:
            list[dict]: List of request parameters for each file or directory.
        """
        try:
            if base_params['target_dir'] is not None:
                target_dir = base_params['target_dir']

                target_dir_path = Path(target_dir)

                if not target_dir_path.is_absolute():
                    logger.error(json.dumps(
                        {"error": f"The provided root_output_dir: '{target_dir}' is not an absolute path."}, indent=2))
                    sys.exit(-1)

                invalid_parts = [
                    part for part in target_dir_path.parts if '\\' in part or not part.isprintable()]

                if invalid_parts:
                    logger.error(json.dumps(
                        {"error": f"The provided root_output_dir: '{target_dir}' contains invalid characters."}, indent=2))
                    sys.exit(-1)

            local_file_path = Path(local_file_path)

            # Ensure the path is valid and absolute
            if not local_file_path.exists():
                logger.error(json.dumps(
                    {"error": f"The provided local_file_path: {local_file_path} must point to an existing file or directory."}, indent=2))
                sys.exit(-1)

            if not local_file_path.is_absolute():
                logger.error(json.dumps(
                    {"error": f"The provided path '{local_file_path}' must be an absolute path."}, indent=2))
                sys.exit(-1)

            params = []

            if local_file_path.is_file():
                params.append({
                    **base_params,
                    "local_file_path": str(local_file_path),
                    "path": f"/{local_file_path.name}",
                    "is_dir": "false"
                })
                return params

            if local_file_path.is_dir():

                # Get the root directory to calculate relative paths
                root_path = local_file_path.parent

                # Add the current directory itself
                params.append({
                    **base_params,
                    "local_file_path": str(local_file_path),
                    "path": f"/{local_file_path.relative_to(root_path)}",
                    "is_dir": "true"
                })

                # Traverse the directory
                for dirpath, dirnames, filenames in os.walk(local_file_path):
                    # Combine directories and files into a single loop
                    for name in dirnames + filenames:
                        item_path = Path(dirpath) / name
                        relative_path = f"/{item_path.relative_to(root_path)}"
                        params.append({
                            **base_params,
                            "local_file_path": str(item_path),
                            "path": relative_path,
                            "is_dir": "true" if item_path.is_dir() else "false"
                        })

                    # If not recursive, stop processing after the first depth level
                    if not eval(recursive.capitalize()):
                        break

                return params

            logger.error(
                f"The path '{local_file_path}' is neither a file nor a directory.")

        except Exception as e:
            logger.exception(
                f"Error occurred while preparing request parameters for file upload: {e}")
            sys.exit(-1)

    def process_file_response(response, save_to_disk=False):
        """
        Process the file response by either saving it locally or streaming/logging its content.

        Args:
            response (requests.Response): The HTTP response object.
            save_to_disk (bool): Flag to indicate if the file should be saved to disk.

        Returns:
            dict or bool: JSON response if saved locally, else True for successful streaming.
        """
        try:
            from yeeducli.utility.json_utils import response_validator

            content_disposition = CaseInsensitiveDict(
                response.headers).get('Content-Disposition')

            if response.status_code == 200 and content_disposition:
                if save_to_disk:
                    # Extract filename
                    filename = None
                    for part in content_disposition.split(';'):
                        if 'filename' in part:
                            filename = part.split('=')[1].strip().strip('"')
                            break

                    if filename:
                        # Save the file to disk
                        with open(filename, 'wb') as file:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    file.write(chunk)

                        return {"message": f"File : {filename} saved successfully"}
                    else:
                        logger.error(
                            "Filename not found in Content-Disposition header.")
                        return {"error": "Filename not found in Content-Disposition header"}
                else:
                    for line in response.iter_lines(decode_unicode=True):
                        if line:
                            logger.info(line)
                    return True
            else:
                return response_validator(response)

        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            sys.exit(-1)
