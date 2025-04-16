# Danish Traffic Status for Home Assistant

This custom component for Home Assistant allows you to monitor the status of Danish trains and metro lines and receive notifications when there are disruptions or changes.

## Features

- Monitor status of Danish train lines (S-trains)
- Monitor status of Copenhagen Metro lines
- Receive notifications through Home Assistant when there are changes or disruptions
- Configure which train and metro lines to monitor
- Customize update frequency

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Go to HACS > Integrations
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add the URL of this repository and select "Integration" as the category
5. Click "Add"
6. Search for "Danish Traffic Status" in the integrations tab
7. Click "Install"
8. Restart Home Assistant

### Manual Installation

1. Download the `danish_traffic_status` folder from this repository
2. Copy the folder to your Home Assistant configuration directory under `custom_components/`
3. Restart Home Assistant

## Configuration

### Through the UI

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

After installation, the integration will create sensor entities for each configured train and metro line. These sensors will show the current status of the line and will update according to the configured scan interval.

### Sensor States

- **normal**: No disruptions or changes detected
- **disruption**: Disruptions or changes detected
- **unknown**: Unable to determine the status

### Sensor Attributes

Train sensors include:
- **line**: The train line identifier
- **message**: The message content if there's a disruption
- **url**: URL with more information (if available)
- **urgent**: Whether the message is marked as urgent
- **last_updated**: When the sensor was last updated

Metro sensors include:
- **line**: The metro line identifier
- **status**: The current status message
- **message**: The message type
- **icon**: Icon identifier from the metro service
- **last_updated**: When the sensor was last updated

## Notifications

The integration will automatically send notifications through Home Assistant's notification system when there are changes in the status of monitored lines. To receive these notifications:

1. Make sure you have a notification service set up in Home Assistant (e.g., mobile app, Telegram, etc.)
2. Configure this service as your default notification service or create an automation to forward notifications to your preferred service

## Automations

You can create your own automations based on the sensor states. For example:

```yaml
automation:
  - alias: "Train Line C Disruption"
    trigger:
      platform: state
      entity_id: sensor.train_line_c_status
      to: "disruption"
    action:
      - service: notify.mobile_app
        data:
          title: "Train Line C Disruption"
          message: "{{ state_attr('sensor.train_line_c_status', 'message') }}"
```

## Troubleshooting

If you encounter issues:

1. Check the Home Assistant logs for errors related to `danish_traffic_status`
2. Verify that the APIs are accessible from your Home Assistant instance
3. Try increasing the scan interval if you're experiencing timeouts
4. Make sure your notification services are properly configured

## Credits

This integration was inspired by the TrafficStatusService project and uses the same data sources:
- DSB API for train status
- Metro API for Copenhagen metro status
