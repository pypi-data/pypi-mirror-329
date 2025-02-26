import hashlib
from urllib.parse import urlparse
from typing import List, Optional
import hashlib
import logging
from typing import Optional, Dict, Any
from pydantic import ValidationError
from dhisana.schemas.sales import MessageItem
from dhisana.utils.cache_output_tools import (
    retrieve_output,
    cache_output
)
from dhisana.utils.field_validators import normalize_linkedin_url, normalize_salesnav_url
from dhisana.utils.parse_linkedin_messages_txt import parse_conversation
logger = logging.getLogger(__name__)



async def add_mapping_tool(mapping: dict) -> dict:
    """
    Create a two-way (forward & reverse) cache mapping between:
       - user_linkedin_url (normalized)
       - user_linkedin_salesnav_url (normalized)
    AND store single-direction entries for easy lookup:
       - LN→SN   (key: "mapping_ln:<sha_of_ln>")
       - SN→LN   (key: "mapping_sn:<sha_of_sn>")

    The cache content has the actual (raw) user-provided URLs,
    only the keys are lowercased/hashed.

    Returns a dict with status, message, and data.

    Example 'mapping':
    {
        "user_linkedin_url": "linkedin.com/in/some-user/",
        "user_linkedin_salesnav_url": "https://www.linkedin.com/sales/lead/123456,NAME_SEARCH"
    }
    """
    user_linkedin_url = mapping.get("user_linkedin_url", "").strip()
    user_linkedin_salesnav_url = mapping.get("user_linkedin_salesnav_url", "").strip()

    if not user_linkedin_url or not user_linkedin_salesnav_url:
        return {
            "status": "ERROR",
            "message": "Both user_linkedin_url and user_linkedin_salesnav_url must be provided."
        }

    # Normalize
    ln_url_norm = normalize_linkedin_url(user_linkedin_url)
    sn_url_norm = normalize_salesnav_url(user_linkedin_salesnav_url)

    # Forward & reverse combined keys (to check if identical mapping was previously stored)
    forward_str = f"{ln_url_norm}→{sn_url_norm}"
    reverse_str = f"{sn_url_norm}→{ln_url_norm}"
    forward_key = "mapping:" + hashlib.sha256(forward_str.encode("utf-8")).hexdigest()
    reverse_key = "mapping:" + hashlib.sha256(reverse_str.encode("utf-8")).hexdigest()

    # Check forward mapping
    forward_cached = retrieve_output("tool_mappings", forward_key)
    if forward_cached:
        if (
            forward_cached.get("user_linkedin_url") == ln_url_norm
            and forward_cached.get("user_linkedin_salesnav_url") == sn_url_norm
        ):
            return {
                "status": "SUCCESS",
                "message": "Mapping already exists (forward).",
                "data": forward_cached
            }

    # Check reverse mapping
    reverse_cached = retrieve_output("tool_mappings", reverse_key)
    if reverse_cached:
        if (
            reverse_cached.get("user_linkedin_url") == ln_url_norm
            and reverse_cached.get("user_linkedin_salesnav_url") == sn_url_norm
        ):
            return {
                "status": "SUCCESS",
                "message": "Mapping already exists (reverse).",
                "data": reverse_cached
            }

    # Create object for storing in forward & reverse
    serialized_results = {
        "user_linkedin_url": ln_url_norm,
        "user_linkedin_salesnav_url": sn_url_norm
    }

    # Store them
    cache_output("tool_mappings", forward_key, serialized_results)
    cache_output("tool_mappings", reverse_key, serialized_results)

    # ------------------------------------------------------------------------
    # Additional single-direction keys to enable easy lookups (raw usage):
    #   LN key: "mapping_ln:<sha_of_normalized_ln.lower()>"
    #   SN key: "mapping_sn:<sha_of_normalized_sn.lower()>"
    # And store the *raw* original user URLs as requested
    # ------------------------------------------------------------------------
    ln_lower = ln_url_norm.lower()
    sn_lower = sn_url_norm.lower()

    ln_key = "mapping_ln:" + hashlib.sha256(ln_lower.encode("utf-8")).hexdigest()
    sn_key = "mapping_sn:" + hashlib.sha256(sn_lower.encode("utf-8")).hexdigest()

    # Cache the raw user-provided URLs
    single_direction_data = {
        "raw_linkedin_url": user_linkedin_url,            # no lowercasing
        "raw_salesnav_url": user_linkedin_salesnav_url,   # no lowercasing
    }

    cache_output("tool_mappings", ln_key, single_direction_data)
    cache_output("tool_mappings", sn_key, single_direction_data)

    return {
        "status": "SUCCESS",
        "message": "Mapping saved successfully in both directions.",
        "data": serialized_results
    }


async def get_salesnav_url_for_linkedin_url(raw_ln_url: str) -> Optional[str]:
    """
    Given a LinkedIn URL, normalize it and look up the corresponding
    *raw* sales nav URL from the single-direction cache.
    Return None if not found in cache.
    """
    # Normalize & lower-case for key
    ln_norm = normalize_linkedin_url(raw_ln_url)
    ln_key = "mapping_ln:" + hashlib.sha256(ln_norm.lower().encode("utf-8")).hexdigest()

    record = retrieve_output("tool_mappings", ln_key)
    if not record:
        return None

    # record["raw_salesnav_url"] is the original user_linkedin_salesnav_url
    return record.get("raw_salesnav_url")


async def get_linkedin_url_for_salesnav_url(raw_sn_url: str) -> Optional[str]:
    """
    Given a Sales Navigator URL, normalize it and look up the corresponding
    *raw* LinkedIn URL from the single-direction cache.
    Return None if not found in cache.
    """
    # Normalize & lower-case for key
    sn_norm = normalize_salesnav_url(raw_sn_url)
    sn_key = "mapping_sn:" + hashlib.sha256(sn_norm.lower().encode("utf-8")).hexdigest()

    record = retrieve_output("tool_mappings", sn_key)
    if not record:
        return None

    # record["raw_linkedin_url"] is the original user_linkedin_url
    return record.get("raw_linkedin_url")


async def cache_enriched_lead_info_from_salesnav(lead_info: dict, agent_id: str) -> Dict[str, Any]:
    """
    Cache lead information using the old SHA-256 approach if and only if:
      - command_name is "get_current_messages" or "send_linkedin_message"
      - user_linkedin_url is present
    Then store a *parsed/serialized* version of the conversation data under:
      "salesnav_lead_messages_raw:<sha256(normalized_url + agent_id)>".
    For other commands, do nothing (ignore).
    """
    if not lead_info:
        return {"status": "ERROR", "message": "No lead_info provided."}

    command_name = lead_info.get("command_name", "")
    if command_name not in ["get_current_messages", "send_linkedin_message"]:
        return {"status": "IGNORED", "message": f"No caching for command_name={command_name}"}

    user_linkedin_url = lead_info.get("user_linkedin_url", "").strip()
    if not user_linkedin_url:
        return {
            "status": "ERROR",
            "message": "Missing user_linkedin_url for caching messages."
        }

    data_to_store = lead_info.get("data", "")
    if not isinstance(data_to_store, str):
        return {
            "status": "ERROR",
            "message": "Invalid data format; must be raw text for parsing."
        }

    try:
        parsed_messages = parse_conversation(data_to_store)
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Failed to parse conversation: {e}"
        }

    sn_norm = normalize_linkedin_url(user_linkedin_url)
    sn_key = "salesnav_lead_messages_raw:" + hashlib.sha256(
        (sn_norm.lower() + agent_id).encode("utf-8")
    ).hexdigest()

    list_of_dicts = [m.dict() for m in parsed_messages]
    cache_output("lead_linkedin_messages_", sn_key, list_of_dicts)

    return {
        "status": "SUCCESS",
        "message": f"Cached parsed messages for command={command_name}, url={user_linkedin_url}",
        "parsed_count": len(list_of_dicts),
        "data": list_of_dicts
    }

async def retrieve_enriched_lead_info_from_salesnav(user_linkedin_url: str, agent_id: str) -> Optional[dict]:
    """
    Retrieve the data previously cached for "get_current_messages" or
    "send_linkedin_message" under the key:
      "salesnav_lead_messages_raw:<sha256(normalized_url + agent_id)>".
    Returns None if not found.
    """
    if not user_linkedin_url:
        return None

    sn_norm = normalize_linkedin_url(user_linkedin_url)
    sn_key = "salesnav_lead_messages_raw:" + hashlib.sha256(
        (sn_norm.lower() + agent_id).encode("utf-8")
    ).hexdigest()

    return retrieve_output("tool_mappings", sn_key)

async def cache_lead_html_from_salesnav(lead_info: dict, agent_id: str) -> dict:
    """
    Cache enriched lead information from Sales Navigator for a given lead.
    The cache key is generated from the SHA-256 hash of: normalized(Sales Navigator URL) + agent_id.
    """
    if not lead_info or not lead_info.get("user_linkedin_url"):
        return {
            "status": "ERROR",
            "message": "Lead information or user_linkedin_url is missing."
        }

    user_linkedin_url = lead_info.get("user_linkedin_url", "").strip()
    sn_norm = normalize_linkedin_url(user_linkedin_url)
    sn_key = "lead_html_from_salesnav:" + hashlib.sha256(
        (sn_norm.lower() + agent_id).encode("utf-8")
    ).hexdigest()

    cache_output("tool_mappings", sn_key, lead_info)

    return {
        "status": "SUCCESS",
        "message": "Lead information cached successfully.",
        "data": lead_info
    }

async def retrieve_lead_html_from_salesnav(user_linkedin_url: str, agent_id: str) -> Optional[dict]:
    """
    Retrieve enriched lead information from Sales Navigator for a given user LinkedIn URL
    using the key: "lead_html_from_salesnav:<sha256(normalized_url + agent_id)>".
    """
    sn_norm = normalize_linkedin_url(user_linkedin_url)
    sn_key = "lead_html_from_salesnav:" + hashlib.sha256(
        (sn_norm.lower() + agent_id).encode("utf-8")
    ).hexdigest()

    return retrieve_output("tool_mappings", sn_key)


async def cache_touchpoint_status(
    lead_info: Dict[str, Any],
    agent_id: str,
    touchpoint_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Cache TouchPointStatus data for a given lead.
    The cache key is generated from the SHA-256 hash of the normalized LinkedIn URL
    and the sdr_user_id if available.
    """
    # ...existing code...
    if not lead_info or not lead_info.get("user_linkedin_url"):
        return {
            "status": "ERROR",
            "message": "Lead information or user_linkedin_url is missing."
        }

    user_linkedin_url = lead_info["user_linkedin_url"].strip()
    sn_norm = normalize_linkedin_url(user_linkedin_url)
    
    sn_key = "touchpoint_status:" + hashlib.sha256((sn_norm.lower() + agent_id).encode("utf-8")).hexdigest()

    cache_output("touchpoint_status", sn_key, touchpoint_data)

    return {
        "status": "SUCCESS",
        "message": "TouchPointStatus cached successfully.",
        "data": touchpoint_data
    }

async def retrieve_touchpoint_status(
    user_linkedin_url: str,
    agent_id: str
):
    """
    Retrieve TouchPointStatus data from the cache for a given user LinkedIn URL
    and sdr_user_id if available.
    """
    # ...existing code...
    sn_norm = normalize_linkedin_url(user_linkedin_url.strip())
    sn_key = "touchpoint_status:" + hashlib.sha256((sn_norm.lower() + agent_id).encode("utf-8")).hexdigest()

    cached_data = retrieve_output("touchpoint_status", sn_key)
    return cached_data

async def retrieve_connection_status(
    user_linkedin_url: str,
    agent_id: str
):
    # ...existing code...
    sn_norm = normalize_linkedin_url(user_linkedin_url.strip())
    sn_key = "touchpoint_status:" + hashlib.sha256((sn_norm.lower() + agent_id).encode("utf-8")).hexdigest()

    cached_data = retrieve_output("touchpoint_status", sn_key) or {}
    connection_degree = cached_data.get("connection_degree", "")
    connection_status = {
        "connection_degree": cached_data.get("connection_degree", ""),
        "connection_request_status": cached_data.get("connection_request_status", ""),
        "is_connected_on_linkedin": connection_degree == "1st"
    }
    return connection_status

async def get_lead_linkedin_messages(user_linkedin_url: str, agent_id: str) -> Optional[list]:
    """
    Retrieve parsed LinkedIn messages for a given user LinkedIn URL.
    The cache key includes agent_id in the SHA-256 hash.
    """
    sn_norm = normalize_linkedin_url(user_linkedin_url)
    sn_key = "salesnav_lead_messages_raw:" + hashlib.sha256((sn_norm + agent_id).encode("utf-8")).hexdigest()
    list_of_dicts = retrieve_output("lead_linkedin_messages_", sn_key)
    messages: List[MessageItem] = []

    for message in list_of_dicts:
        message_item = MessageItem(**message)
        messages.append(message_item)

    return messages
