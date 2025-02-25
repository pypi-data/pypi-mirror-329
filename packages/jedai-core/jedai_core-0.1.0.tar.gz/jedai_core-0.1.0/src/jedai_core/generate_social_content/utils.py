import json
import logging
import os
import re
from typing import Any

import requests
from ai.agents import Agents
from django.conf import settings
from django.db.utils import OperationalError
from marketing_bot.utils import (
    download_image,
    get_linkedin_Authentication,
    upload_image_to_linkedin,
)
from rest_framework.response import Response

from .exceptions import LiveSettingsUnknownKey
from .models import LiveSettings

LINKEDIN_ORGANIZATION_URL = os.getenv("LINKEDIN_ORGANIZATION_URL")
LINKEDIN_API_REST = os.getenv("LINKEDIN_API_REST")

logger = logging.getLogger("marketing_bot")


def call_agents(detailed_instructions: dict, general_rules: str):
    """
    Initializes LLMs and performs information extraction on the document.

    Args:
        detailed_instructions (dict): JSON used como base.
        general_rules (str): General rules for the extraction.
        access_token (str): Acess token for the LinkedIn API.

    Returns:
        tuple: (extracted_information, model_alias)
    """
    try:
        model: str = ls("model")
        api_key: str = ls("api_key")
        config: dict = ls("config")
        temperature: float = float(config.get("temperature"))
        top_p: float = float(config.get("top_p"))

        agents = Agents(model, api_key, temperature, top_p)

        agents_results = agents.StrategyBriefingAgent(detailed_instructions)
        final_output = clean_agent_output(
            agents.Agents_Chain(
                company_strategy_briefing=agents_results, general_rules=general_rules
            )
        )

        if not isinstance(final_output, (list, dict, str)):
            raise ValueError("Invalid type returned from callAgents.")

        return final_output, model
    except Exception as e:
        logger.error(f"Error during information extraction: {e}")
        return None, "Error"


def create_linkedin_post(data: dict):
    """
    Create a LinkedIn post with an image.
    """
    # Get the access token from the LinkedIn Authentication
    access_token = get_linkedin_Authentication("access_token")
    if not access_token:
        return Response({"error": "Access token is required"}, status=400)

    content = data.get("content")
    image_url = data.get("image_url")

    if not content:
        return Response({"error": "Content is required"}, status=400)

    def escape_special_chars(content):
        return content.replace("(", "\\(").replace(")", "\\)")

    content = escape_special_chars(content)

    # Get the organization ID
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202501",
        "Content-Type": "application/json",
    }
    org_response = requests.get(LINKEDIN_ORGANIZATION_URL, headers=headers)

    if org_response.status_code == 200:
        org_data = org_response.json()
        elements = org_data.get("elements", [])
        if not elements:
            return Response(
                {"error": "No organizations found for this user."}, status=400
            )
        org_urn = elements[0]["organization"]
    else:
        return Response(
            {
                "error": "Failed to retrieve LinkedIn organizations",
                "details": org_response.json(),
            },
            status=org_response.status_code,
        )

    # Upload the image (if an image URL is provided)
    asset = None
    downloaded_image_path = None
    if image_url:
        # Download the image
        downloaded_image_path, download_error = download_image(image_url)
        if download_error:
            return Response(download_error, status=400)

        # Upload the downloaded image
        asset, upload_error = upload_image_to_linkedin(
            access_token, org_urn, downloaded_image_path
        )
        if upload_error:
            return Response(upload_error, status=400)

    # Create the post with or without the image
    payload = {
        "author": org_urn,
        "commentary": content,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    # If the image was successfully uploaded, include it in the payload
    if asset:
        payload["content"] = {
            "media": {
                "title": "Test",
                "id": asset,
            }
        }

    post_url = f"{LINKEDIN_API_REST}/posts"
    post_response = requests.post(post_url, json=payload, headers=headers)

    try:
        response_data = post_response.json()
    except ValueError:
        response_data = {
            "error": "Invalid JSON response",
            "raw_response": post_response.text,
        }

    if post_response.status_code == 201:
        if downloaded_image_path and os.path.exists(downloaded_image_path):
            os.remove(downloaded_image_path)

        return Response({"message": "Post created successfully!"}, status=201)
    else:
        return Response(
            {"error": response_data, "status_code": post_response.status_code},
            status=post_response.status_code,
        )


def clean_agent_output(value):
    pattern = r"```json\s*([\s\S]+?)```"
    match = re.search(pattern, value)

    if match:
        json_str = match.group(1).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format", "content": value})


def save_strategy_briefing(
    strategy_briefing_result, output_filename="company_strategy_briefing.json"
):
    try:
        os.makedirs("company_data", exist_ok=True)
        file_path = os.path.join(settings.BASE_DIR, "company_data", output_filename)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(strategy_briefing_result, file, ensure_ascii=False, indent=4)

    except Exception as e:
        logger.error(f"Error creating directory: {e}")


def get_specific_file_data(folder, file):
    try:
        file_path = os.path.join(folder, file)
        if not os.path.exists(file_path):
            return {}

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return content

    except Exception as e:
        logger.error(f"Error get directory data: {e}")
        return {}


def ls(key: str, *, default: Any = LiveSettingsUnknownKey) -> Any:
    """ls stands for live settings.
    It provides a quick way to pull settings from the database singleton that stores them.
    """

    def default_or_exception(err: Exception):
        if default is LiveSettingsUnknownKey:
            raise err from None

        return default

    try:
        live_settings = LiveSettings.objects.get()
        return getattr(live_settings, key)
    except (
        LiveSettings.DoesNotExist,
        LiveSettings.MultipleObjectsReturned,
        OperationalError,
    ) as err:
        logger.error(f"Live settings error: {err}", extra={"key": key})
        return default_or_exception(err)
