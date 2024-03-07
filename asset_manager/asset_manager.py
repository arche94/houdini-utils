import os
import json
from DropboxUtil import DropboxUtils

def upload_asset(asset_path, asset_name, ext="bgeo.sc"):
  destpath = '/' + asset_name + '/' + asset_name + '.' + ext

  man = DropboxUtils()
  asset = man.uploadAsset(destpath, overwrite=True)
  asset_link = man.getSharedLink(destpath)

  updateLibrary(asset, asset_link)

def updateLibrary(asset, asset_link):
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
