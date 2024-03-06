# Houdini Utils
A collection of utilities for SideFX Houdini.

## Asset Manager
A tool that will allow to upload and publish assets on cloud services.

### Supported services
- Dropbox

### Configuration
In order to work properly, you will need to configure your cloud service in the `asset_manager/config.yaml` file.

#### Dropbox configuration
You will need your service's `<APP_KEY>` and `<APP_SECRET>` from your Dropbox App Console and edit the `dropbox` section of `config.yaml`.

```
dropbox:
  app_key: <APP_KEY>
  app_secret: <APP_SECRET>
```