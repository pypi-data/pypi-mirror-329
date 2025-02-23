import io
import uuid
import smbclient
import pandas as pd
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open
from smbprotocol.file_info import FileInformationClass


def smb_copy_file_local_to_remote(username, password, server_name, share_name, local_file_path, remote_file_path, port=445):
    """ This function is used to copy local file to public folder

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        local_file_path(str): This is the local file path
        remote_file_path(str): This is the public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
    """
    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)

    try:
        with open(local_file_path, 'rb') as local_file:
            with smbclient.open_file(fr'{server_name}/{share_name}/{remote_file_path}', mode='wb') as remote_file:
                remote_file.write(local_file.read())

        print("Copy successfully!")

    except Exception as e:
        print(f"Ops, error is: {e}")
    finally:
        smbclient.reset_connection_cache()


def smb_store_remote_file_by_obj(username, password, server_name, share_name, remote_file_path, file_obj, port=445):
    """ This function is used to store file to public folder

    Args:
        file_obj(io.BytesIO): This is the file object
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_file_path(str): This is the public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
    """
    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)

    try:
        with smbclient.open_file(fr'{server_name}/{share_name}/{remote_file_path}', mode='wb') as remote_file:
            file_obj.seek(0)
            remote_file.write(file_obj.read())

        print("File is saved successfully!")

    except Exception as e:
        print(f"Ops, error is: {e}")

    finally:
        smbclient.reset_connection_cache()

def smb_check_file_exist(username, password, server_name, share_name, remote_file_path, port=445):
    """ This function is used to check whether remote file is existed

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_file_path(str): This is the public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
    """
    is_file_exist = False
    file_obj = io.BytesIO()
    full_remote_file_path = f'{server_name}/{share_name}/{remote_file_path}'

    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)
    try:
        smbclient.stat(full_remote_file_path)
        is_file_exist = True

        with smbclient.open_file(full_remote_file_path, 'rb') as remote_file:
            file_obj.write(remote_file.read())
            file_obj.seek(0)
        print(f"File {remote_file_path} exist.")

    except Exception as e:
        print(f'Ops, error is {e}')
        print('File with current path does not exist!')
    finally:
        smbclient.reset_connection_cache()

    return is_file_exist, file_obj


def smb_check_folder_exist(username, password, server_name, share_name, remote_folder_path, port=445):
    """ This function is used to check whether remote folder is existed

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_folder_path(str): This is the public folder path that folder will be saved under share name folder
        port(int): This is the port number of the server name
    """
    is_folder_exist = False
    full_remote_folder_path = f'{server_name}/{share_name}/{remote_folder_path}'

    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)
    try:
        # Check if the directory exists
        dir_info = smbclient.stat(full_remote_folder_path)
        if dir_info.st_file_attributes & 0x10:
            is_folder_exist = True
            print("Directory exists.")
        else:
            print("The path exists, but it is not a directory.")

    except Exception as e:
        print(e)
        print('Folder with current path does not exist!')

    finally:
        # Reset connection cache
        smbclient.reset_connection_cache()

    return is_folder_exist


def smb_traverse_remote_folder(username, password, server_name, share_name, remote_folder_path, port=445):
    """ This function is list all files or folders within remote folder

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_folder_path(str): This is the public folder path that folder will be saved under share name folder
        port(int): This is the port number of the server name
    """

    traverse_result_list = []
    client_guid = uuid.uuid4()
    connection = Connection(guid=client_guid, server_name=server_name, port=port)
    connection.connect()

    session = Session(connection, username, password)
    session.connect()

    tree = TreeConnect(session, f"\\\\{server_name}\\{share_name}")
    tree.connect()

    folder_open = Open(tree, remote_folder_path)
    folder_open.create(impersonation_level=0,
                       desired_access=0x00000001,  # read only
                       file_attributes=0,
                       share_access=0x00000001,  # allow other process
                       create_disposition=1,  # OPEN_EXISTING
                       create_options=0
                       )
    try:
        pattern = "*"  # match all
        file_information_class = FileInformationClass.FILE_DIRECTORY_INFORMATION
        file_info = folder_open.query_directory(pattern, file_information_class)
        for item in file_info:
            item_name = item.fields.get('file_name').value.decode('utf-16')
            if item_name not in ['.', '..']:
                creation_time = item.fields.get('creation_time').value
                last_access_time = item.fields.get('last_access_time').value
                last_write_time = item.fields.get('last_write_time').value
                change_time = item.fields.get('change_time').value

                if item.fields.get('file_attributes').value & 0x10:  # check whether item is folder
                    traverse_result_list.append({'name': item_name,
                                                 'is_folder': True, 'is_file': False, 'creation_time': creation_time, 'last_access_time': last_access_time,
                                                 'last_write_time': last_write_time, 'change_time': change_time})
                else:
                    traverse_result_list.append({'name': item_name,
                                                 'is_folder': False, 'is_file': True, 'creation_time': creation_time, 'last_access_time': last_access_time,
                                                 'last_write_time': last_write_time, 'change_time': change_time})
    finally:
        connection.disconnect()
        session.disconnect()
        tree.disconnect()

    return traverse_result_list


def smb_copy_file_remote_to_local(username, password, server_name, share_name, local_file_path, remote_file_path, port=445):
    """ This function is used to copy local file to public folder

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        local_file_path(str): This is the local file path
        remote_file_path(str): This is the public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
    """
    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)

    try:
        with smbclient.open_file(fr'{server_name}/{share_name}/{remote_file_path}', 'rb') as remote_file:
            with open(local_file_path, mode='wb') as local_file:
                local_file.write(remote_file.read())

        print("Copy successfully!")

    except Exception as e:
        print(f"Ops, error is: {e}")
    finally:
        smbclient.reset_connection_cache()


def smb_load_file_obj(username, password, server_name, share_name, remote_file_path, port=445):
    """ This function is used to get file object from public folder

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_file_path(str): This is the public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
    """
    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)

    file_obj = io.BytesIO()
    try:
        with smbclient.open_file(fr'{server_name}/{share_name}/{remote_file_path}', mode='rb') as remote_file:
            file_obj.write(remote_file.read())
            file_obj.seek(0)
        print("Load successfully!")
    except Exception as e:
        print(f"Ops, error is: {e}")
    finally:
        smbclient.reset_connection_cache()

    return file_obj


def smb_delete_file(username, password, server_name, share_name, remote_file_path, port=445):
    """ This function is used to copy local file to public folder

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_file_path(str): This is the public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
    """
    # Register session with SMB server
    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)

    try:
        # Delete the specified remote file
        smbclient.remove(fr'//{server_name}/{share_name}/{remote_file_path}')
        print("File deleted successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Reset connection cache
        smbclient.reset_connection_cache()


def smb_create_folder(username, password, server_name, share_name, remote_folder_path, port=445):
    """ This function is used to copy local file to public folder

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_folder_path(str): This is the public folder path that folder will be created under share name folder
        port(int): This is the port number of the server name
    """
    # Register session with SMB server
    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)

    try:
        # Create the specified remote directory
        smbclient.mkdir(fr'//{server_name}/{share_name}/{remote_folder_path}')
        print("Directory created successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Reset connection cache
        smbclient.reset_connection_cache()


def smb_delete_folder(username, password, server_name, share_name, remote_folder_path, port=445):
    """ This function is used to delete remote folder

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_folder_path(str): This is the public folder path that folder will be created under share name folder
        port(int): This is the port number of the server name
    """
    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)
    try:
        # Iterate over the folder contents
        remote_folder_path=f'{server_name}/{share_name}/{remote_folder_path}'
        for entry in smbclient.scandir(remote_folder_path):
            entry_path = f"{remote_folder_path}/{entry.name}"
            if entry.is_dir():
                # Recursively delete subfolders
                smb_delete_folder(username, password, server_name, share_name, entry_path)
            else:
                # Delete files
                smbclient.remove(entry_path)

        # Remove the now-empty folder
        smbclient.rmdir(remote_folder_path)
        print(f"Folder {remote_folder_path} and its contents have been successfully deleted.")
    except FileNotFoundError:
        print(f"Folder {remote_folder_path} does not exist.")
    except OSError as e:
        print(f"Failed to delete folder {remote_folder_path}: {e}")


def smb_move_remote_file(username, password, from_server_name, from_share_name, from_remote_file_path, to_server_name, to_share_name, to_remote_file_path, port=445):
    """ This function is used to move remote file to another folder

    Args:
        username(str): This is the username
        password(str): This is the password
        from_server_name(str):This is the source server name (url), e.g. szh0fs06.apac.bosch.com
        from_share_name(str): This is the source share_name of public folder, e.g. GS_ACC_CN$
        from_remote_file_path(str): This is the source public file path that file will be saved under share name folder
        to_server_name(str):This is the destination server name (url), e.g. szh0fs06.apac.bosch.com
        to_share_name(str): This is the  destination share_name of public folder, e.g. GS_ACC_CN$
        to_remote_file_path(str): This is the destination new public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
    """

    is_from_file_exist, file_obj = smb_check_file_exist(username, password, from_server_name, from_share_name, from_remote_file_path, port=port)
    if is_from_file_exist:
        smb_store_remote_file_by_obj(username, password, to_server_name, to_share_name, to_remote_file_path, file_obj, port=port)
        smb_delete_file(username, password, from_server_name, from_share_name, from_remote_file_path, port=port)
        print("Move successfully!")
    else:
        print("Source file does not exist!")


def smb_move_remote_folder(username, password, from_server_name, from_share_name, from_remote_folder_path, to_server_name, to_share_name, to_remote_folder_path, port=445):
    """ This function is used to move remote folder to another folder

    Args:
        username(str): This is the username
        password(str): This is the password
        from_server_name(str):This is the source server name (url), e.g. szh0fs06.apac.bosch.com
        from_share_name(str): This is the source share_name of public folder, e.g. GS_ACC_CN$
        from_remote_folder_path(str): This is the source public folder path that folder will be saved under share name folder
        to_server_name(str):This is the destination server name (url), e.g. szh0fs06.apac.bosch.com
        to_share_name(str): This is the  destination share_name of public folder, e.g. GS_ACC_CN$
        to_remote_folder_path(str): This is the destination new public folder path that folder will be saved under share name folder
        port(int): This is the port number of the server name
    """
    is_from_folder_exist = smb_check_folder_exist(username, password, from_server_name, from_share_name, from_remote_folder_path, port=port)
    if is_from_folder_exist:
        smb_create_folder(username, password, to_server_name, to_share_name, to_remote_folder_path, port=port)
        for item in smb_traverse_remote_folder(username, password, from_server_name, from_share_name, from_remote_folder_path, port=port):
            if item['is_folder']:
                smb_move_remote_folder(username, password, from_server_name, from_share_name, f"{from_remote_folder_path}/{item['name']}", to_server_name, to_share_name,
                                       f"{to_remote_folder_path}/{item['name']}", port=port)
            else:
                smb_move_remote_file(username, password, from_server_name, from_share_name, f"{from_remote_folder_path}/{item['name']}", to_server_name, to_share_name,
                                     f"{to_remote_folder_path}/{item['name']}", port=port)
        smb_delete_folder(username, password, from_server_name, from_share_name, from_remote_folder_path, port=port)
        print("Move successfully!")
    else:
        print("Source folder does not exist!")


def smb_copy_remote_file(username, password, from_server_name, from_share_name, from_remote_file_path, to_server_name, to_share_name, to_remote_file_path, port=445):
    """ This function is used to copy remote file to another folder

    Args:
        username(str): This is the username
        password(str): This is the password
        from_server_name(str):This is the source server name (url), e.g. szh0fs06.apac.bosch.com
        from_share_name(str): This is the source share_name of public folder, e.g. GS_ACC_CN$
        from_remote_file_path(str): This is the source public file path that file will be saved under share name folder
        to_server_name(str):This is the destination server name (url), e.g. szh0fs06.apac.bosch.com
        to_share_name(str): This is the  destination share_name of public folder, e.g. GS_ACC_CN$
        to_remote_file_path(str): This is the destination new public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
    """

    is_from_file_exist, file_obj = smb_check_file_exist(username, password, from_server_name, from_share_name, from_remote_file_path, port=port)
    if is_from_file_exist:
        smb_store_remote_file_by_obj(username, password, to_server_name, to_share_name, to_remote_file_path, file_obj, port=port)
        print("Copy successfully!")
    else:
        print("Source file does not exist!")


def smb_copy_remote_folder(username, password, from_server_name, from_share_name, from_remote_folder_path, to_server_name, to_share_name, to_remote_folder_path, port=445):
    """ This function is used to copy remote folder to another folder

    Args:
        username(str): This is the username
        password(str): This is the password
        from_server_name(str):This is the source server name (url), e.g. szh0fs06.apac.bosch.com
        from_share_name(str): This is the source share_name of public folder, e.g. GS_ACC_CN$
        from_remote_folder_path(str): This is the source public folder path that folder will be saved under share name folder
        to_server_name(str):This is the destination server name (url), e.g. szh0fs06.apac.bosch.com
        to_share_name(str): This is the  destination share_name of public folder, e.g. GS_ACC_CN$
        to_remote_folder_path(str): This is the destination new public folder path that folder will be saved under share name folder
        port(int): This is the port number of the server name
    """
    is_from_folder_exist = smb_check_folder_exist(username, password, from_server_name, from_share_name, from_remote_folder_path, port=port)
    if is_from_folder_exist:
        smb_create_folder(username, password, to_server_name, to_share_name, to_remote_folder_path, port=port)
        for item in smb_traverse_remote_folder(username, password, from_server_name, from_share_name, from_remote_folder_path, port=port):
            if item['is_folder']:
                smb_copy_remote_folder(username, password, from_server_name, from_share_name, f"{from_remote_folder_path}/{item['name']}", to_server_name, to_share_name,
                                       f"{to_remote_folder_path}/{item['name']}", port=port)
            else:
                smb_copy_remote_file(username, password, from_server_name, from_share_name, f"{from_remote_folder_path}/{item['name']}", to_server_name, to_share_name,
                                     f"{to_remote_folder_path}/{item['name']}", port=port)
        print("Copy successfully!")
    else:
        print("Source folder does not exist!")


def smb_rename_remote_file(username, password, server_name, share_name, remote_file_path, new_remote_file_path, port=445):
    """ This function is used to rename remote file

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_file_path(str): This is the public file path that file will be saved under share name folder
        new_remote_file_path(str): This is the new public file path that file will be saved under share name folder
        port(int): This is the port number of the server name
    """
    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)

    try:
        # Rename the specified remote file
        smbclient.rename(fr'//{server_name}/{share_name}/{remote_file_path}', fr'//{server_name}/{share_name}/{new_remote_file_path}')
        print("File renamed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Reset connection cache
        smbclient.reset_connection_cache()


def smb_rename_remote_folder(username, password, server_name, share_name, remote_folder_path, new_remote_folder_path, port=445):
    """ This function is used to rename remote folder

    Args:
        username(str): This is the username
        password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        remote_folder_path(str): This is the public folder path that folder will be saved under share name folder
        new_remote_folder_path(str): This is the new public folder path that folder will be saved under share name folder
        port(int): This is the port number of the server name
    """
    smbclient.register_session(server_name, username=username, password=password, port=port, encrypt=True)

    try:
        # Rename the specified remote directory
        smbclient.rename(fr'//{server_name}/{share_name}/{remote_folder_path}', fr'//{server_name}/{share_name}/{new_remote_folder_path}')
        print("Folder renamed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Reset connection cache
        smbclient.reset_connection_cache()
