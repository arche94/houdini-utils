import os
import dropbox
import yaml
import json
import requests
import webbrowser
import datetime
import time

class DropboxUtils:
  def __init__(self, module_basepath=''):
    self.__config_file = os.path.join(module_basepath, "config.yaml").replace('\\', '/')

    with open(self.__config_file, "r") as config_file:
      try:
        config = yaml.safe_load(config_file)
      except yaml.YAMLError as e:
        print(e)
    
    self.__local_basepath = config['assets']['basepath']

    self.__app_key = config['dropbox']['app_key']
    self.__app_secret = config['dropbox']['app_secret']
    self.__refresh_token = config['dropbox']['refresh_token'] if 'refresh_token' in config['dropbox'] else None
    self.__session = None

    if not self.__refresh_token:
      self.__getRefreshToken()
    self.__getSession()

  def getFileList(self, location='', list_subfolders=False):
    entries = self.__session.files_list_folder(location, recursive=list_subfolders).entries
    entries.sort(key=lambda e: e.path_display)
    return entries
  
  def getUsername(self):
    user = self.__session.users_get_current_account()
    return user.name.display_name

  def uploadAsset(self, filepath, overwrite=False):
    fullpath = os.path.abspath(os.path.join(self.__local_basepath, filepath)).replace("\\", "/")
    mode = dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add
    mtime = os.path.getmtime(fullpath)

    if not filepath.startswith('/'):
      filepath = '/' + filepath

    with open(fullpath, 'rb') as asset_file:
      asset_data = asset_file.read()

    try:
      res = self.__session.files_upload(
        asset_data, 
        filepath, 
        mode=mode, 
        client_modified=datetime.datetime(*time.gmtime(mtime)[:6])
      )      
    except dropbox.exceptions.ApiError as e:
      print(f"Error uploading {filepath} to Dropbox: {e}")
      return
    
    print(f"Successfully uploaded {res.name.encode('utf8')}")
    return res

  def downloadAsset(self, entry, overwrite=False):
    path = entry.path_display
    fullpath = os.path.abspath(os.path.join(self.__local_basepath, path[1:])).replace('\\', '/')

    if os.path.exists(fullpath) and not overwrite:
      print(f"The requested files already exists: {path}")
      return
    
    if len(path[1:].split('/')) > 1:
      try:     
        os.makedirs('/'.join(fullpath.split('/')[:-1]), exist_ok=True)
      except OSError as oe:
        print(f"Error creating folder {fullpath}: {oe}")
        return
    
    try:
      res = self.__session.files_download_to_file(fullpath, path)
    except dropbox.exceptions.ApiError as e:
      print(f"Error downloading asset {path} from Dropbox: {e}")
      return
    
    print(f"File successfully downloaded at {fullpath}")
    return res

  def getSharedLink(self, asset_path):
    if not asset_path.startswith('/'):
      asset_path = '/' + asset_path

    try:
      link = self.__session.sharing_create_shared_link(asset_path)
    except dropbox.exceptions.ApiError as e:
      print(f"Error getting shared link for {asset_path}: {e}")
      return None
    
    return link

  def __getRefreshToken(self):
    webbrowser.open(f"https://www.dropbox.com/oauth2/authorize?client_id={self.__app_key}&token_access_type=offline&response_type=code")
    auth_code = input('Paste here the authentication code from the browser: ')
    
    url = "https://api.dropboxapi.com/oauth2/token"
    data = {
      "grant_type": "authorization_code",
      "code": auth_code,
      "client_id": self.__app_key,
      "client_secret": self.__app_secret
    }
    
    res = requests.post(url, data=data)
    if res.status_code == 200:
      self.__refresh_token = res.json().get('refresh_token')
      with open(self.__config_file, 'r') as config_file:
        config = yaml.safe_load(config_file)
      
      config['dropbox']['refresh_token'] = self.__refresh_token

      with open(self.__config_file, 'w') as config_file:
        yaml.dump(config, config_file)
    else:
      print(f"Error getting refresh token: {res.text}")

  def __getSession(self):
    try:
      self.__session = dropbox.Dropbox(oauth2_refresh_token=self.__refresh_token, app_key=self.__app_key, app_secret=self.__app_secret)
    except:
      self.__getRefreshToken()
      self.__getSession()

if __name__ == "__main__":
  test_assets = [
    'test.txt',
    'subdir/test_nested.txt'
  ]

  dbx = DropboxUtils()
  print(dbx.getUsername())

  if not os.path.exists('testlib.json') or os.path.getsize('testlib.json') == 0:
    with open('testlib.json', 'w') as lib_file:
      json.dump({}, lib_file, indent=2)

  with open('testlib.json', 'r') as lib_file:
    test_lib = json.load(lib_file)

  for asset in test_assets:
    dbx_asset = dbx.uploadAsset(asset)
    dbx_shrlnk = dbx.getSharedLink(asset)
    entry = {
      "name": dbx_asset.name,
      "path": f"{dbx_asset.path_display}",
      "shared_link": f"{dbx_shrlnk.url}"
    }
    test_lib[dbx_asset.id] = entry

  with open('testlib.json', 'w') as lib_file:
    json.dump(test_lib, lib_file, indent=2)

  for e in dbx.getFileList(list_subfolders=True):
    if not isinstance(e, dropbox.files.FolderMetadata):
      if e.id in test_lib:
        print(f"File already exists: {e.path_display}")
      else:
        print(f"Downloading: {e.path_display} ...")
        dbx_asset = dbx.downloadAsset(e)
        dbx_shrlnk = dbx.getSharedLink(e.path_display)
        entry = {
          "name": dbx_asset.name,
          "path": f"{dbx_asset.path_display}",
          "shared_link": f"{dbx_shrlnk.url}"
        }
        test_lib[dbx_asset.id] = entry

  with open('testlib.json', 'w') as lib_file:
    json.dump(test_lib, lib_file, indent=2)
  