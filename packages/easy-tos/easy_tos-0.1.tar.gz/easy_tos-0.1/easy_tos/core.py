import tos 
import os
def _valid_tos_path(path):
    """
    Check if the given path is a valid Terms of Service (TOS) file path.

    Args:
    path (str): The path to be checked.

    Returns:
    bool: True if the path is a valid TOS file path, False otherwise.
    """
    if not path.startswith("tos://"):
        raise ValueError(f"tos path should start with 'tos://'")
        
    if path.endswith("/"):
        raise ValueError(f"tos path should not end with '/'")
    return True

def _split_tospath(path):
    """
    Split the given TOS file path into its components.

    Args:
    path (str): The TOS file path to be split.

    Returns:
    tuple: A tuple containing the bucket name, prefix, and file name.
    """
    path = path.replace("tos://", "")
    path = path.split("/")
    bucket_name = path[0]
    prefix = "/".join(path[1:-1])
    file_name = path[-1]
    return bucket_name, prefix, file_name
    
def check_tos_file_exists(tos_filepath, config):
    """
    Check if the Terms of Service (TOS) file exists at the specified filepath.

    Args:
    tos_filepath (str): The filepath of the TOS file.
    config (dict): A dictionary containing configuration settings.

    Returns:
    bool: True if the file exists, False otherwise.

    Raises:
    ValueError: If the tos_filepath is empty or None.
    """
    _valid_tos_path(tos_filepath)
    bucket_name, prefix, file_name = _split_tospath(tos_filepath)
    client = tos.TosClientV2(config['ak'], config['sk'], config['endpoint'], config['region'])
    
    truncated = True
    continuation_token = ''
    while truncated:
        try:
            result = client.list_objects_type2(bucket_name, prefix=prefix, continuation_token=continuation_token, max_keys=1000)
        except tos.exceptions.TosServerError as e:
            print(f"Error listing objects: {e}")
            return False
        for item in result.contents:
            if item.key.endswith(file_name):
                return item.key
        truncated = result.is_truncated
        continuation_token = result.next_continuation_token
    return None
    # Check if the file exists
    

def save_dict_to_json(data, file_path):
    import json
    with open(file_path, 'w') as json_file:
        # Write the dictionary to the file as JSON
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Dict has been successfully saved to {file_path}")

def write_list_to_txt(uid_list, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(uid_list))
    print(f"List has been successfully saved to {file_path}")
    