import asyncio
import hashlib
import json
import os
import re
import time
import logging
import uuid
from typing import Any, Dict, List, Optional, Tuple

from fastapi import HTTPException
from openai import AsyncOpenAI, OpenAI, OpenAIError, LengthFinishReasonError
from pydantic import BaseModel, TypeAdapter

from dhisana.utils import cache_output_tools
from dhisana.utils.openai_assistant_and_file_utils import (
    add_user_message,
    create_and_retrieve_run,
    create_assistant,
    create_thread,
    delete_assistant,
    get_first_message_content,
    get_run_status,
)
from dhisana.utils.openai_helpers import get_openai_access_token

async def get_vector_store_object(vector_store_id: str, tool_config: Optional[List[Dict]] = None) -> Dict:
    """
    Retrieve the vector store object (dict) via the SDK.
    """
    OPENAI_KEY = get_openai_access_token(tool_config)
    client_async = AsyncOpenAI(api_key=OPENAI_KEY)
    return await client_async.beta.vector_stores.retrieve(vector_store_id=vector_store_id)

async def list_vector_store_files(
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
) -> List:
    """
    Retrieve the list of files (VectorStoreFile objects) for a given vector store.
    """
    OPENAI_KEY = get_openai_access_token(tool_config)
    client_async = AsyncOpenAI(api_key=OPENAI_KEY)
    page = await client_async.beta.vector_stores.files.list(vector_store_id=vector_store_id)
    return page.data  # 'data' is the list of VectorStoreFile objects

async def get_structured_output_internal(
    prompt: str,
    response_format,
    effort="medium",
    tool_config: Optional[List[Dict]] = None
):
    """
    Makes a direct call to the internal structured output approach,
    bypassing vector store or other chain-of-thought tools.
    """
    try:
        response_type_str = response_format.__name__
        message_hash = hashlib.md5(prompt.encode('utf-8')).hexdigest()
        response_type_hash = hashlib.md5(response_type_str.encode('utf-8')).hexdigest()
        cache_key = f"{message_hash}:{response_type_hash}"
        cached_response = cache_output_tools.retrieve_output("get_structured_output_internal", cache_key)
        if cached_response is not None:
            parsed_cached_response = response_format.parse_raw(cached_response)
            return parsed_cached_response, 'SUCCESS'

        OPENAI_KEY = get_openai_access_token(tool_config)
        client_async = AsyncOpenAI(api_key=OPENAI_KEY)
        completion = await client_async.beta.chat.completions.parse(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "Extract structured content from input. Output is in JSON Format."},
                {"role": "user", "content": prompt},
            ],
            response_format=response_format,
            reasoning_effort=effort
        )
        response = completion.choices[0].message
        if response.parsed:
            cache_output_tools.cache_output(
                "get_structured_output_internal",
                cache_key,
                response.parsed.json()
            )
            return response.parsed, 'SUCCESS'
        elif response.refusal:
            logging.warning("ERROR: Refusal response: %s", response.refusal)
            return response.refusal, 'FAIL'

    except LengthFinishReasonError as e:
        logging.error(f"Too many tokens: {e}")
        raise HTTPException(status_code=502, detail="The request exceeded the maximum token limit.")
    except OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=502, detail="Error communicating with the OpenAI API.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your request."
        )

async def get_structured_output_with_assistant_and_vector_store(
    prompt: str,
    response_format,
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    If the vector store has NO files, call get_structured_output_internal directly.
    Otherwise, proceed with the assistant flow.
    """
    assistant = None
    try:
        # 1. Retrieve the vector store object (to verify it exists or get usage).
        _ = await get_vector_store_object(vector_store_id, tool_config)

        # 2. Check if the vector store contains any files.
        files = await list_vector_store_files(vector_store_id, tool_config)
        if not files:
            # If no files, just call our internal structured output function.
            return await get_structured_output_internal(prompt, response_format, tool_config)

        # 3. If there are files, proceed with the assistant-based approach.
        response_type_str = response_format.__name__
        message_hash = hashlib.md5(prompt.encode('utf-8')).hexdigest()
        response_type_hash = hashlib.md5(response_type_str.encode('utf-8')).hexdigest()
        cache_key = f"{message_hash}:{response_type_hash}"
        cached_response = cache_output_tools.retrieve_output(
            "get_structured_output_with_assistant_and_vector_store",
            cache_key
        )
        if cached_response is not None:
            parsed_cached_response = response_format.parse_raw(cached_response)
            return parsed_cached_response, 'SUCCESS'

        assistant_name = f"assistant_{uuid.uuid4().hex}"
        instructions = "Hi, You are a helpful AI Assistant. Help the users with the given instructions."
        tools = []
        assistant, vector_store_id = await create_assistant(
            assistant_name,
            instructions,
            tools,
            vector_store_id,
            tool_config
        )

        metadata = {"assistant_id": assistant.id, "assistant_name": assistant_name}
        thread = await create_thread(metadata, vector_store_id=vector_store_id, tool_config=tool_config)
        await add_user_message(prompt, thread, tool_config)

        run = await create_and_retrieve_run(
            thread.id,
            assistant.id,
            instructions,
            tools,
            response_format,
            tool_config
        )

        MAX_WAIT_TIME = 180  # 3 minutes
        start_time = time.time()
        while run.status not in ["completed", "failed"]:
            if time.time() - start_time > MAX_WAIT_TIME:
                logging.error("Run did not complete within the maximum wait time of 3 minutes.")
                break
            await asyncio.sleep(3)
            run = await get_run_status(thread.id, run.id, tool_config)

        if run.status == 'completed':
            response_text = await get_first_message_content(thread.id, tool_config)
            pattern = r'【\d+:\d+†[^】]+】'
            response_text = re.sub(pattern, '', response_text)
            if response_text:
                response = TypeAdapter(response_format).validate_json(response_text)
                cache_output_tools.cache_output(
                    "get_structured_output_with_assistant_and_vector_store",
                    cache_key,
                    json.dumps(response.model_dump())
                )
            else:
                logging.error(f"Too many tokens: {run}")
                raise HTTPException(status_code=502, detail="No response from the assistant.")
            return response, 'SUCCESS'
        else:
            raise HTTPException(
                status_code=502,
                detail=f"Run failed with status: {run.status}"
            )

    except LengthFinishReasonError as e:
        logging.error(f"Too many tokens: {e}")
        raise HTTPException(status_code=502, detail="The request exceeded the maximum token limit.")
    except OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=502, detail="Error communicating with the OpenAI API.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your request."
        )
    finally:
        if assistant:
            await delete_assistant(assistant.id, tool_config)
