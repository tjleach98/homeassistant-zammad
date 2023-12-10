# Zammad Home Assistant Integration
This is a basic Home Assistant integration for Zammad. It uses the `zammad_py` library available [here](https://github.com/joeirimpan/zammad_py)

**Warning** This is my first attempt at Home Assistant/Zammad development. There _will_ be issues but feel free to create an issue or PR!

## Influence
The source code for this project is heavily based on the [SmartRent](https://github.com/ZacheryThomas/homeassistant-smartrent) and [Nextcloud](https://github.com/home-assistant/core/tree/dev/homeassistant/components/nextcloud) integrations.

## Installation
### Manual
Place the entire `custom_components/zammad` folder in this repo inside the `config/custom_components/` folder of your Home Assistant instance. 

If `custom_components` doesn't exist, create it. Click [here](https://developers.home-assistant.io/docs/creating_integration_file_structure/#where-home-assistant-looks-for-integrations) for more details.

Once the files are in place, restart Home Assistant and the integration should be available.

### HACS
TO-DO

## Setup
Go to Settings -> Devices & services -> Add Integration. Select Zammad and enter your login details.

**Warning** 2FA and token authentication not yet available

## Currently Available Sensors
### Binary Sensor
- User Verified
- User Out Of Office
- User Active
- User VIP

### Sensor
- User ID
- Organization ID
- User Login
- Last Login
- Number of Logins Failed
- User Updated At
- Number of Unread Notifications