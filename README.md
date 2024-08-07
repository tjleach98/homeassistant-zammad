[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/tjleach98/homeassistant-zammad/.github%2Fworkflows%2Fvalidate.yml?style=flat-square&label=validate)](https://github.com/tjleach98/homeassistant-zammad/actions/workflows/validate.yml)
[![GitHub Release](https://img.shields.io/github/release/tjleach98/homeassistant-zammad.svg?style=flat-square)](https://github.com/tjleach98/homeassistant-zammad/releases)
[![GitHub](https://img.shields.io/github/license/tjleach98/homeassistant-zammad.svg?style=flat-square)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Downloads](https://img.shields.io/github/downloads/tjleach98/homeassistant-zammad/total?style=flat-square)](https://github.com/tjleach98/homeassistant-zammad/releases)

# Zammad Home Assistant Integration
This is a basic Home Assistant integration for Zammad. It uses the `zammad_py` library available [here](https://github.com/joeirimpan/zammad_py)

## Influence
The source code for this project is heavily based on the [SmartRent](https://github.com/ZacheryThomas/homeassistant-smartrent) and [Nextcloud](https://github.com/home-assistant/core/tree/dev/homeassistant/components/nextcloud) integrations.

## Installation
### Manual
Place the entire `custom_components/zammad` folder in this repo inside the `config/custom_components/` folder of your Home Assistant instance. 

If `custom_components` doesn't exist, create it. Click [here](https://developers.home-assistant.io/docs/creating_integration_file_structure/#where-home-assistant-looks-for-integrations) for more details.

Once the files are in place, restart Home Assistant and the integration should be available.

### HACS
Add this repository to HACS as a custom repository. Details for this can be found [here](https://hacs.xyz/docs/faq/custom_repositories).

## Setup
Go to Settings -> Devices & services -> Add Integration. Select Zammad and enter your login details.

**Warning** 2FA and token authentication not yet available

## Currently Available Sensors
### Button
- Mark All Notificatons Read

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
