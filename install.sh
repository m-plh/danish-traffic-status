#!/bin/bash

# Danish Traffic Status for Home Assistant - Installation Script
# This script helps install the Danish Traffic Status component manually

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Danish Traffic Status for Home Assistant - Installation Script${NC}"
echo ""

# Check if HASS_CONFIG_DIR is set, otherwise use default
if [ -z "$HASS_CONFIG_DIR" ]; then
    echo -e "${YELLOW}Home Assistant configuration directory not specified.${NC}"
    echo -e "Please enter your Home Assistant configuration directory path:"
    echo -e "(Default: ~/.homeassistant or ~/homeassistant)"
    read -p "> " HASS_CONFIG_DIR
    
    # If still empty, use default
    if [ -z "$HASS_CONFIG_DIR" ]; then
        if [ -d ~/.homeassistant ]; then
            HASS_CONFIG_DIR=~/.homeassistant
        elif [ -d ~/homeassistant ]; then
            HASS_CONFIG_DIR=~/homeassistant
        else
            echo -e "${RED}Could not find Home Assistant configuration directory.${NC}"
            echo -e "Please run this script again and specify the correct path."
            exit 1
        fi
    fi
fi

# Expand tilde to home directory
HASS_CONFIG_DIR="${HASS_CONFIG_DIR/#\~/$HOME}"

echo -e "Using configuration directory: ${GREEN}$HASS_CONFIG_DIR${NC}"

# Check if the directory exists
if [ ! -d "$HASS_CONFIG_DIR" ]; then
    echo -e "${RED}Error: The specified directory does not exist.${NC}"
    exit 1
fi

# Create custom_components directory if it doesn't exist
CUSTOM_COMPONENTS_DIR="$HASS_CONFIG_DIR/custom_components"
if [ ! -d "$CUSTOM_COMPONENTS_DIR" ]; then
    echo -e "Creating custom_components directory..."
    mkdir -p "$CUSTOM_COMPONENTS_DIR"
fi

# Create component directory
COMPONENT_DIR="$CUSTOM_COMPONENTS_DIR/danish_traffic_status"
if [ -d "$COMPONENT_DIR" ]; then
    echo -e "${YELLOW}The danish_traffic_status directory already exists.${NC}"
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Installation aborted.${NC}"
        exit 1
    fi
    rm -rf "$COMPONENT_DIR"
fi

echo -e "Creating component directory..."
mkdir -p "$COMPONENT_DIR"
mkdir -p "$COMPONENT_DIR/translations"

# Copy files
echo -e "Copying component files..."
cp -r custom_components/danish_traffic_status/* "$COMPONENT_DIR/"

echo -e "${GREEN}Installation completed successfully!${NC}"
echo -e "Please restart Home Assistant to complete the installation."
echo -e "After restarting, you can add the integration through the UI:"
echo -e "Configuration > Integrations > Add Integration > Danish Traffic Status"
