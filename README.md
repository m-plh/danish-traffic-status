# Danish Traffic Status for Home Assistant

This project provides a Home Assistant custom component that monitors Danish train and metro lines and sends notifications when there are changes or disruptions. It's designed to work with Home Assistant's notification system to keep you informed about your commute.

## Overview

The Danish Traffic Status integration:

- Monitors Danish S-train lines (DSB)
- Monitors Copenhagen Metro lines
- Sends notifications through Home Assistant when there are changes or disruptions
- Allows configuration of which lines to monitor
- Provides sensors that can be used in automations and dashboards

## Installation

### Prerequisites

- A running Home Assistant instance (version 2021.12 or newer recommended)
- Network access to the DSB and Metro APIs from your Home Assistant instance

### Installation Methods

#### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Go to HACS > Integrations
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add the URL of this repository and select "Integration" as the category
5. Click "Add"
6. Search for "Danish Traffic Status" in the integrations tab
7. Click "Install"
8. Restart Home Assistant

#### Manual Installation

1. Copy the `custom_components/danish_traffic_status` directory to your Home Assistant configuration directory
2. Restart Home Assistant

## Configuration

After installation, add the integration through the Home Assistant UI:

1. Go to Configuration > Integrations
2. Click the "+" button to add a new integration
3. Search for "Danish Traffic Status"
4. Follow the configuration steps

### Configuration Options

- **Name**: A name for the integration (default: "Danish Traffic Status")
- **Scan Interval**: How often to check for updates in minutes (default: 15 minutes)
- **Train Lines**: Comma-separated list of train lines to monitor (default: "C")
- **Metro Lines**: Comma-separated list of metro lines to monitor (default: "M1/M2")

## Usage

See the [component README](custom_components/danish_traffic_status/README.md) for detailed usage instructions, including:

- Sensor states and attributes
- Notification setup
- Automation examples
- Troubleshooting tips

## How It Works

This integration:

1. Periodically fetches status information from the DSB and Metro APIs
2. Compares the current status with the previous status
3. Creates sensor entities for each monitored line
4. Sends notifications through Home Assistant when changes are detected

## Credits

This project was inspired by the TrafficStatusService project and uses the same data sources:
- DSB API for train status
- Metro API for Copenhagen metro status

## License

This project is licensed under the MIT License - see the LICENSE file for details.
