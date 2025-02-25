import json
import logging
import time
from decimal import Decimal

from celery import shared_task
from django.conf import settings
from marketing_bot.models import User

from .models import Inference
from .utils import call_agents, create_linkedin_post

logger = logging.getLogger("marketing_bot")


@shared_task(
    bind=True,
    rate_limit="10/m",
    autoretry_for=(Exception,),
    retry_backoff=60,  # 60, 120, 240
    retry_kwargs={"max_retries": 3},
    retry_jitter=True,  # this means actual delay will be sampled at random from (0, retry_backoff) interval
)
def run_agent_inference(_, user_id: int) -> dict:
    user = None

    # if the user id was provived, try to get the user
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.warning(f"User with ID {user_id} does not exist.")

    try:
        with open(
            settings.BASE_DIR / "ai/resources/company_data.json", "r", encoding="utf-8"
        ) as f:
            detailed_instructions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load detailed instructions: {e}")
        raise ValueError("Invalid or missing detailed instructions")

    if not detailed_instructions:
        raise ValueError("detailed_instructions is empty")

    try:
        with open(
            settings.BASE_DIR / "ai/resources/general_rules.md", "r", encoding="utf-8"
        ) as f:
            general_rules = f.read()
    except FileNotFoundError as e:
        logger.error(f"Failed to load general rules: {e}")
        raise ValueError("Invalid or missing general rules")

    if not general_rules:
        raise ValueError("general_rules is empty")

    t0 = time.perf_counter()
    try:
        response, model_alias = call_agents(detailed_instructions, general_rules)
    except TypeError as e:
        logger.error(f"Error calling agents: {e}")
        return {"error": "Agent execution failed"}

    runtime = Decimal(f"{time.perf_counter() - t0:.2f}")
    logger.info(f"Got a response in {runtime} seconds...")

    post_response = create_linkedin_post(response)
    if post_response.status_code == 201:
        message = post_response.data.get("message")
    else:
        message = post_response.data.get("error")

    # check if the response needs to be converted
    try:
        if isinstance(response, (list, dict)):
            response_json = json.dumps(response)
        elif isinstance(response, str):
            response_json = response
        else:
            raise ValueError(f"Unsupported response type: {type(response)}")
    except Exception as e:
        logger.error(f"Failed to serialize response: {e}")
        response_json = json.dumps({"error": "Serialization failed", "details": str(e)})

    inference = Inference.objects.create(
        user=user,
        detailed_instructions=detailed_instructions,
        model_alias=model_alias,
        response=response_json,
        runtime=runtime,
    )

    return {"inference_id": inference.id, "message": message}
