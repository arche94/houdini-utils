import os
import dropbox
import yaml
import requests
import webbrowser

class DropboxUtils:
  def __init__(self):
    with open("config.yaml", "r") as config_file:
      try:
        config = yaml.safe_load(config_file)
      except yaml.YAMLError as e:
        print(e)
    
    self.__app_key = config['dropbox']['app_key']
    self.__app_secret = config['dropbox']['app_secret']
    self.__refresh_token = config['dropbox']['refresh_token'] if 'refresh_token' in config['dropbox'] else None
    self.__session = None

    if not self.__refresh_token:
      self.__getRefreshToken()
    self.__getSession()

  def getFileList(self, location=''):
    return self.__session.files_list_folder(location)
  
  def getUsername(self):
    user = self.__session.users_get_current_account()
    return user.name.display_name

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
      with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
      
      config['dropbox']['refresh_token'] = self.__refresh_token

      with open('config.yaml', 'w') as config_file:
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
  dbx = DropboxUtils()
  print(dbx.getUsername())
  for e in dbx.getFileList().entries:
    print(e.name)
  