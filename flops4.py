import ctypes.wintypes
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
import shutil
import sys
import usvfs

INI_NAME = 'flops4.ini'
INI_SECTION_NAME = 'general'

script_root = Path(sys.argv[0]).absolute().parent
ini_path = script_root / INI_NAME

docs_path_buffer = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, docs_path_buffer)
docs_path = Path(docs_path_buffer.value).absolute()
default_data_path = docs_path / 'Electronic Arts' / 'The Sims 4'

ini_defaults = {
    INI_SECTION_NAME: {
        'profiles_root': script_root,
        'data_path': default_data_path,
        'launch_command': '',
        'default_profile': 'default'
    }
}

config = ConfigParser()
config.read_dict(ini_defaults)
config.read(ini_path)

with open(ini_path, 'w') as ini_file:
    config.write(ini_file)

section_data = config[INI_SECTION_NAME]
profiles_root = Path(section_data.get('profiles_root'))
data_path = Path(section_data.get('data_path'))
launch_command = section_data.get('launch_command')
profile_name = section_data.get('default_profile')

if launch_command == '':
    print('Error: "launch_command" is not set.')
    print('Please check "' + str(ini_path) + '".')
    exit()

if data_path.exists():
    print('Warning: Data path "' + str(data_path) + '" exists.')
    backup_name = 'backup_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = profiles_root / backup_name
    print('Moving to "' + str(backup_path) + '". This may take time...', end=' ')
    shutil.move(data_path, backup_path)
    print('Done.')

profile_path = profiles_root / profile_name

if len(sys.argv) > 1:
    req_profile = Path(sys.argv[1])
    if req_profile.is_absolute():
        profile_path = req_profile
    else:
        profile_path = profiles_root / req_profile
    
if not profile_path.exists():
    profile_path.mkdir()

print('Using profile "' + str(profile_path) + '".')

vfs_mapping = usvfs.Mapping()
virtual_dir = usvfs.VirtualDirectory(profile_path, data_path)
virtual_dir.link_recursively = True
virtual_dir.redirect_create = True
virtual_dir.monitor_changes = True
vfs_mapping.link(virtual_dir)

vfs = usvfs.UserspaceVFS()
vfs.initialize()
vfs.set_mapping(vfs_mapping)

vfs.run_process(launch_command)
