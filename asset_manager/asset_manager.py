import hou
import os
import json
from DropboxUtil import DropboxUtils

def upload_asset(node):
  # find library path destination
  asset_path = node.parm('file').eval()
  asset_name = asset_path.split('/')[-1]
  ext = ''
  if 'bgeo.sc' in asset_name:
    asset_name = asset_name.replace('.bgeo.sc', '')
    ext = 'bgeo.sc'
  if 'vdb' in asset_name:
    asset_name = asset_name.replace('.vdb', '')
    ext = 'vdb'
  
  destpath = '/' + asset_name
  destfile = destpath + '/' + asset_name + '.' + ext
  
  # copy into local library
  with open(asset_path, 'rb') as asset_file:
    asset_data = asset_file.read()
  
  if not os.path.exists(destpath):
    os.makedirs(destpath)

  with open(destfile, 'wb') as dest_file:
    dest_file.write(asset_data)

  # upload into cloud library
  cloud_mod_path = os.path.join(hou.getenv('HU'), 'asset_manager').replace('\\', '/')
  man = DropboxUtils(module_basepath=cloud_mod_path)
  asset = man.uploadAsset(destfile, overwrite=True)
  asset_link = man.getSharedLink(destpath)

  # update asset info
  update_library(asset, asset_link)

def update_library(asset, asset_link):
  if not os.path.exists('assetlib.json') or os.path.getsize('assetlib.json') == 0:
    with open('assetlib.json', 'w') as lib_file:
      json.dump({}, lib_file, indent=2)

  with open('assetlib.json', 'r') as lib_file:
    asset_lib = json.load(lib_file)

  entry = {
    "name": asset.name,
    "path": f"{asset.path_display}",
    "shared_link": f"{asset_link.url}"
  }
  asset_lib[asset.id] = entry

  with open('assetlib.json', 'w') as lib_file:
    json.dump(asset_lib, lib_file, indent=2)
