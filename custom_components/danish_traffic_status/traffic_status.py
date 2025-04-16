"""Traffic status services for Danish Traffic Status integration."""
import logging
import json
import re
from datetime import datetime
import requests

_LOGGER = logging.getLogger(__name__)


class TrainStatusService:
    """Service to fetch train status from DSB API."""

    BASE_URL = "https://www.dsb.dk/api/travelplans/gettrafficinfolist?lang=da"

    def get_status(self, train_line):
        """Get status for a specific train line."""
        try:
            response = requests.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            
            train_status_messages = response.json()
            
            # Filter active messages for the specified line
            active_messages = [
                msg for msg in train_status_messages
                if msg.get("sender") == "S-tog" and
                self._is_message_active(msg) and
                self._is_message_for_line(msg, train_line)
            ]
            
            # Prioritize urgent messages
            urgent_messages = [msg for msg in active_messages if msg.get("urgent", False)]
            if urgent_messages:
                return self._format_message(urgent_messages[0])
            
            # Return first active message or None
            return self._format_message(active_messages[0]) if active_messages else None
            
        except Exception as err:
            _LOGGER.error("Error fetching train status: %s", err)
            return None
    
    def _is_message_active(self, message):
        """Check if a message is currently active."""
        now = datetime.now()
        valid_from = datetime.fromisoformat(message.get("validFromDate").replace("Z", "+00:00")) if message.get("validFromDate") else None
        valid_to = datetime.fromisoformat(message.get("validToDate").replace("Z", "+00:00")) if message.get("validToDate") else now + datetime.timedelta(hours=1)
        
        return valid_from and valid_from <= now and valid_to >= now
    
    def _is_message_for_line(self, message, train_line):
        """Check if a message is for the specified train line."""
        body = message.get("body", "").lower()
        train_line = train_line.lower()
        
        # Check if message mentions the line
        line_patterns = [
            f"linje {train_line}",
            f" {train_line},",
            f" {train_line} ",
            f" {train_line}."
        ]
        
        if any(pattern in body for pattern in line_patterns):
            return True
        
        # Check if message is for all S-trains
        geography = [g.lower() for g in message.get("geography", [])]
        return any("alle s-tog" in g for g in geography)
    
    def _format_message(self, message):
        """Format the message for Home Assistant."""
        if not message:
            return None
            
        return {
            "messageId": message.get("messageId"),
            "header": message.get("header"),
            "body": message.get("body"),
            "url": message.get("url"),
            "urgent": message.get("urgent", False),
            "validFrom": message.get("validFromDate"),
            "validTo": message.get("validToDate")
        }


class MetroStatusService:
    """Service to fetch metro status from Metro API."""

    BASE_URL = "https://metroselskabet.euwest01.umbraco.io/api/operationData/GetOperationData/"

    def get_status(self, metro_line):
        """Get status for a specific metro line."""
        try:
            response = requests.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            
            metro_status = response.json()
            
            # Find active message for the specified line
            active_messages = metro_status.get("activeMessages", [])
            for message in active_messages:
                line_setup = message.get("lineSetup", {})
                if line_setup.get("lineGroup", "").strip() == metro_line:
                    return self._format_message(message)
            
            return None
            
        except Exception as err:
            _LOGGER.error("Error fetching metro status: %s", err)
            return None
    
    def _format_message(self, message):
        """Format the message for Home Assistant."""
        if not message:
            return None
            
        return {
            "name": message.get("name"),
            "type": message.get("Type"),
            "icon": message.get("icon"),
            "published": message.get("published", False),
            "isClearMessage": message.get("isClearMessage", False),
            "lineGroup": message.get("lineSetup", {}).get("lineGroup")
        }


def clean_html(text):
    """Remove HTML tags from text."""
    if not text:
        return ""
        
    # Replace HTML entities
    text = re.sub(r"&AElig;", "Æ", text)
    text = re.sub(r"&Oslash;", "Ø", text)
    text = re.sub(r"&Aring;", "Å", text)
    text = re.sub(r"&aelig;", "æ", text)
    text = re.sub(r"&oslash;", "ø", text)
    text = re.sub(r"&aring;", "å", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&#230;", "æ", text)
    text = re.sub(r"&#248;", "ø", text)
    text = re.sub(r"&#229;", "å", text)
    text = re.sub(r"&#198;", "Æ", text)
    text = re.sub(r"&#216;", "Ø", text)
    text = re.sub(r"&#197;", "Å", text)
    
    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)
    
    return text
