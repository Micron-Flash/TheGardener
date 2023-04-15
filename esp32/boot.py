import os, machine
os.mount(machine.SDCard(slot=2,freq=10000), "/lib")

import wifi
import json
import mip
import machine
import gc
from os import listdir, mkdir


# In boot we check if any files or dependencies need to be downloaded from the internet
# If it can't connect to the internet there's really nothing to do in boot so it will continue to main.py
def main(config):
    
    gc.collect()
    gc.enable()
    
    print('Booting')
    print('Connecting...')
    if wifi.connect(config):
        print('Downloading Dependencies...')
        download_dependencies()
        if config['check_for_updates']:
            print('Checking for updates...')
            check_for_updates(config)
    else:
        print("Cant Connect skipping stuff that might be needed")
    wifi.disconnect()

def check_for_updates(config):
    import senko # type: ignore
    auth_header = { "Authorization": 'token ' + config['GitHubAuthToken'] }
    OTA = senko.Senko(
        user = config['ota_git_user'],
        repo = config['ota_git_repo'],
        branch = config['ota_branch'],
        working_dir = config['ota_working_dir'],
        files = config['ota_remote_files'],
        headers = auth_header
        )
    if OTA.fetch():
        print("A newer version is available!")
        if config['run_update']:
            if OTA.update():
                print("Updated to the latest version! Rebooting...")
                machine.reset()
    else:
        print("Up to date!")
        
def download_dependencies():
    config = load_json('pyckage.json')
    try: 
        mkdir('lib') 
        print("Created lib folder")  
    except OSError: 
        print("not creating lib folder, already exists")  
    lib_dir = listdir('lib')
    for lib in config['external_dependencies']:
        if lib['name'] in lib_dir:
            if config['force_external_dependencies_update']:
                print(lib['name'] + ' exist, force update enabled... downloading from the internet')
                mip.install(lib['url'], version = lib['branch_or_tag'])
            else:
                print(lib['name'] + ' exists, skipping')
        else:
            print(lib['name'] + ' missing, downloading from the internet')
            mip.install(lib['url'], version = lib['branch_or_tag'])
    machine.reset()    
    
def load_json(file_string):
    file = open(file_string)
    config = json.load(file)
    return config


if __name__ == "__main__":
    config = load_json('config.json')
    main(config)
    os.unmount('/lib')