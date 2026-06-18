# Remeha Home integration for Home Assistant
This integration lets you control your Remeha Home thermostats from Home Assistant.

> **Note :** This is a custom fork of [msvisser/remeha_home](https://github.com/msvisser/remeha_home) with additional sensors and a hot water comfort switch.

**Before using this integration, make sure you have set up your thermostat in the [Remeha Home](https://play.google.com/store/apps/details?id=com.bdrthermea.application.remeha) app.**
If you are unable to use the Remeha Home app for your thermostat, this integration will not work.

There have been reports by users that this intergration will also work for Baxi, De Dietrich, and Brötje systems (and possibly other BDR Thermea products).
You can simply log in using the credentials that you would use in the respective apps.

## Current features
- All climate zones are exposed as [climate](https://www.home-assistant.io/integrations/climate/) entities with:
    - The following modes:
        - Auto mode: the thermostat will follow the clock program.
        If the target temperature is changed, it will temporarily override the clock program until the next target temperature change in the schedule.
        - Heat mode: the thermostat will be set to manual mode and continuously hold the set temperature.
        - Off mode: the thermostat is disabled.
    - Three presets for the three clock programs available in the Remeha Home app.
    When a preset is selected, the integration will automatically switch the climate zone to auto mode to make sure the preset is applied.
- Each climate zone also exposes the following sensors/switches:
    - The next schedule setpoint
    - The time at which the next schedule setpoint gets activated
    - The current schedule setpoint
    - Switch to control fireplace mode
- Each hot water zone exposes the following sensors and switches:
    - The water temperature
    - **DHW Zone Mode** — current hot water mode (e.g. `Schedule`, `ContinuousComfort`)
    - **DHW Target Setpoint** — target hot water temperature (°C)
    - **Force Water Comfort** switch — turns on continuous comfort mode, turns off to revert to schedule
- Each appliance (CV-ketel) exposes the following sensors:
    - The water pressure
    - **Active Thermal Mode** — current thermal mode of the appliance

## Data polling
Data is refreshed every **120 seconds**.

## Installation

### Install with HACS (recommended)

1. In HACS, go to **Integrations** → ⋮ → **Custom repositories**
2. Add `https://github.com/daxharry/remeha_home` — category **Integration**
3. Search for **Remeha Home** and click `Download`
4. Restart Home Assistant
5. See [Setup](#setup)

### Install manually

1. Install this platform by creating a `custom_components` folder in the same folder as your configuration.yaml, if it doesn't already exist.
2. Create another folder `remeha_home` in the `custom_components` folder. Copy all files from `custom_components/remeha_home` into the `remeha_home` folder.

## Setup
1. In Home Assitant click on `Configuration`
1. Click on `Devices & Services`
1. Click on `+ Add integration`
1. Search for and select `Remeha Home`
1. Enter your email address and password
1. Click "Next"
1. Enjoy

## API documentation
For information on the Remeha Home API see [API documentation](documentation/api.md).
