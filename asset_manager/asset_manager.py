import hou
import os
import json
import shutil
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
  destpath = '/' + asset_name + '/' + asset_name + '.' + ext
  
  # copy into local library
  shutil.copyfile(asset_path, '_assets' + destpath)

  # upload into cloud library
  man = DropboxUtils()
  asset = man.uploadAsset(destpath, overwrite=True)
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
