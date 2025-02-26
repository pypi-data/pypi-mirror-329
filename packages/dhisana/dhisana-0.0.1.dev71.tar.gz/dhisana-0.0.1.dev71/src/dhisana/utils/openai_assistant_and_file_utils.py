# Helper functions for OpenAI Assistants API & File uploads
import json
import logging
import re
import traceback
from typing import AsyncIterable, Dict, List, Optional

import openai
from fastapi import HTTPException
from openai import AsyncAssistantEventHandler, AsyncOpenAI
from openai.types.beta import Thread
from typing_extensions import override
from pydantic import BaseModel
from dhisana.utils.openai_helpers import get_openai_access_token

MAX_RUN_ITERATIONS = 10


class AgentToolObject(BaseModel):
    """
    A tool provided as input to a Neo.
    """
    name: str
    description: str
    lookup_id: str


async def get_assistant(assistant_id: str, tool_config: Optional[List[Dict]] = None):
    """
    Retrieve an existing assistant by its ID.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    try:
        assistant = await client.beta.assistants.retrieve(assistant_id=assistant_id)
    except openai.NotFoundError as e:
        logging.error(
            f"Error retrieving assistant with ID {assistant_id}. "
            f"Error: {e}\n{traceback.format_exc()}"
        )
        return None
    return assistant


async def list_assistants(tool_config: Optional[List[Dict]] = None):
    """
    List available assistants (max 50).
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    assistants = await client.beta.assistants.list(limit=50)
    return assistants


async def delete_assistant(assistant_id: str, tool_config: Optional[List[Dict]] = None):
    """
    Delete an assistant by ID. If not found, return success since it's effectively deleted.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    try:
        response = await client.beta.assistants.delete(assistant_id=assistant_id)
    except openai.NotFoundError as e:
        logging.error(
            f"Error deleting assistant with ID {assistant_id}. "
            f"Error: {e}\n{traceback.format_exc()}"
        )
        return {
            "status": "success",
            "message": "Assistant not found, considered as deleted",
        }
    return response


async def create_vector_store(
    vector_store_name: str,
    tool_config: Optional[List[Dict]] = None
):
    normalized_name = vector_store_name.lower()
    normalized_name = re.sub(r'[^a-z0-9_]+', '_', normalized_name)
    normalized_name = normalized_name[:64]
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    vector_store = await client.beta.vector_stores.create(name=normalized_name)
    return vector_store


async def delete_vector_store(
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Delete a vector store by ID.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    await client.beta.vector_stores.delete(vector_store_id=vector_store_id)
    return



async def create_assistant(
    assistant_name: str,
    instructions: str,
    tools: list,
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
):
    assistant_name = assistant_name.lower()
    assistant_name = re.sub(r'[^a-z0-9_]+', '_', assistant_name)
    assistant_name = assistant_name[:64]

    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    if not vector_store_id:
        vector_store = await client.beta.vector_stores.create(name=assistant_name)
        vector_store_id = vector_store.id
    default_tools = [{"type": "file_search"}]
    if tools and len(tools) > 0:
        all_tools = default_tools + tools
    else:
        all_tools = default_tools
    assistant = await client.beta.assistants.create(
        name=assistant_name,
        instructions=instructions,
        tools=all_tools,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        model="o3-mini",
    )
    return assistant, vector_store_id


async def update_assistant(
    assistant_id: str,
    vector_store_id: str,
    assistant_name: str,
    instructions: str,
    tools: list,
    files: list,
    tool_config: Optional[List[Dict]] = None
):
    assistant_name = assistant_name.lower()
    assistant_name = re.sub(r'[^a-z0-9_]+', '_', assistant_name)
    assistant_name = assistant_name[:64]

    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)

    assistant = await client.beta.assistants.update(
        assistant_id=assistant_id,
        name=assistant_name,
        instructions=instructions,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        model="o3-mini",
    )
    return assistant


async def create_thread(
    metadata: dict,
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Create a new thread with optional vector store IDs attached to the file_search tool.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    if not vector_store_id:
        thread = await client.beta.threads.create(metadata=metadata)
    else:
        thread = await client.beta.threads.create(
            metadata=metadata,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )
    return thread


async def update_thread(
    thread_id: str,
    metadata: dict,
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Update an existing thread's metadata and vector store references.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    thread = await client.beta.threads.update(
        thread_id=thread_id,
        metadata=metadata,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )
    return thread


async def add_user_message(
    prompt: str,
    thread: Thread,
    tool_config: Optional[List[Dict]] = None
):
    """
    Add a user role message to the specified thread.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    message = await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )
    return message


async def create_and_retrieve_run(
    thread_id: str,
    assistant_id: str,
    prompt: str,
    openai_tools: list,
    response_format: BaseModel,
    tool_config: Optional[List[Dict]] = None
):
    """
    Create a new run and immediately retrieve it from a thread.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    response_format_schema = {
        'type': 'json_schema',
        'json_schema': {
            "name": response_format.__name__,
            "schema": response_format.model_json_schema()
        }
    }
    default_tools = [{"type": "file_search"}]
    all_tools = []
    if openai_tools and len(openai_tools) > 0:
        all_tools = default_tools + openai_tools
    else:
        all_tools = default_tools
    run = await client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=prompt,
        response_format=response_format_schema,
        tools=all_tools,
        tool_choice={"type": "file_search"}
    )
    return await client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

async def get_run_status(thread_id:str, run_id:str, tool_config: Optional[List[Dict]] = None):
    """
    Get the status of a run by its ID.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    run = await client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run

def get_response(tool_run_id: str, parsed_output: dict):
    """
    Prepare a structured response message based on the parsed output from a tool call.
    """
    status_code = parsed_output.get("status_code")
    output = json.dumps(parsed_output.get("text"))
    status_messages = {
        200: output,
        201: f"operation successful {output} {parsed_output.get('reason')}",
        204: f"operation successful {output} {parsed_output.get('reason')}",
    }
    return {"tool_call_id": tool_run_id, "output": status_messages.get(status_code, "")}


def get_error_message(run):
    """
    Generate a string error message based on the run's last known status or error.
    """
    return (
        f"There was error processing the request."
        f"Status: {run.status} {run.last_error if run.last_error else ''}"
    )


async def get_first_message_content(thread_id: str, tool_config: Optional[List[Dict]] = None):
    """
    Fetch the text content of the first message in a thread, if any.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    messages = await client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value if messages.data else ""


async def upload_file_openai_and_vector_store(
    file_content,
    file_name: str,
    mime_type: str,
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Upload a file to OpenAI for use with an assistant or vector store.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    purpose = "assistants"
    if mime_type in ["image/jpeg", "image/png"]:
        purpose = "vision"

    file = await client.files.create(
        file=(file_name, file_content, mime_type),
        purpose=purpose
    )

    if purpose == "assistants" and vector_store_id:
        # Add the file to the specified vector store
        await client.beta.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file.id
        )

    return file

async def upload_file_openai(
    file_content,
    file_name: str,
    mime_type: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Upload a file to OpenAI for use with an assistant or vector store.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    purpose = "assistants"
    if mime_type in ["image/jpeg", "image/png"]:
        purpose = "vision"

    file = await client.files.create(
        file=(file_name, file_content, mime_type),
        purpose=purpose
    )
    return file

async def attach_file_to_vector_store(
    file_id: str,
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Upload a file to OpenAI for use with an assistant or vector store.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)

    # Add the file to the specified vector store
    response = await client.beta.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=file_id
    )
    return response

async def delete_assistant_files(
    assistant_id: str,
    file_id: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Remove a specific file from an assistant. 
    If not found, consider it as deleted.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    try:
        response = await client.beta.assistants.files.delete(
            assistant_id=assistant_id,
            file_id=file_id
        )
    except openai.NotFoundError as e:
        logging.error(
            f"Error deleting file with ID {file_id} from assistant {assistant_id}. "
            f"Error: {e}\n{traceback.format_exc()}"
        )
        return {
            "status": "success",
            "message": "Assistant file not found, considered as deleted",
        }
    return response


async def delete_files(
    file_ids: List[str],
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Delete multiple files from a vector store and from OpenAI's file storage.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    response = None
    for file_id in file_ids:
        try:
            await client.beta.vector_stores.files.delete(
                vector_store_id=vector_store_id,
                file_id=file_id
            )
            response = await client.files.delete(file_id=file_id)
        except openai.NotFoundError as e:
            logging.error(
                f"Error deleting file with ID {file_id}. Error: {e}\n{traceback.format_exc()}"
            )
    return response


async def delete_assistant_file(
    file_id: str,
    vector_store_id: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Delete a single file from vector store and OpenAI's file storage if it exists.
    """
    if not file_id:
        return None

    try:
        openai_key = get_openai_access_token(tool_config)
        client = AsyncOpenAI(api_key=openai_key)
        if vector_store_id:
            await client.beta.vector_stores.files.delete(
                vector_store_id=vector_store_id,
                file_id=file_id
            )
        response = await client.files.delete(file_id=file_id)
        return response
    except openai.NotFoundError:
        print("File not found in store")
        return None


async def delete_thread(thread_id: str, tool_config: Optional[List[Dict]] = None):
    """
    Delete a thread by its ID.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    response = await client.beta.threads.delete(thread_id=thread_id)
    return response


async def get_thread(thread_id: str, tool_config: Optional[List[Dict]] = None):
    """
    Retrieve a thread by ID. Returns None if not found.
    """
    try:
        openai_key = get_openai_access_token(tool_config)
        client = AsyncOpenAI(api_key=openai_key)
        response = await client.beta.threads.retrieve(thread_id=thread_id)
    except openai.NotFoundError as e:
        logging.error(
            f"Error retrieving thread with ID {thread_id}. "
            f"Error: {e}\n{traceback.format_exc()}"
        )
        return None
    return response


async def list_thread_messages(thread_id: str, tool_config: Optional[List[Dict]] = None):
    """
    List all messages in a thread.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    message = await client.beta.threads.messages.list(thread_id=thread_id)
    messages = []
    for msg in message.data:
        messages.append(
            {
                "payload": msg.content[0].text.value if msg.content else "",
                "role": msg.role,
                "id": msg.id,
            }
        )
    return messages


async def delete_all_assistants_danger(tool_config: Optional[List[Dict]] = None):
    """
    Danger: Deletes all assistants in this workspace.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    assistants = await client.beta.assistants.list()
    for assistant in assistants.data:
        await client.beta.assistants.delete(assistant_id=assistant.id)
    return assistants


async def delete_all_files_danger(tool_config: Optional[List[Dict]] = None):
    """
    Danger: Deletes all files (with 'assistants' purpose) in this workspace.
    """
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    files = await client.files.list(purpose="assistants")
    for file in files.data:
        await client.files.delete(file_id=file.id)
    return files


async def run_function_callback(
    prompt: str,
    tools: list,
    tool_config: Optional[List[Dict]] = None
):
    """
    Run a single function call, returning its tool calls and the final message.
    """
    messages = [{"role": "user", "content": prompt}]
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    try:
        chat_response = await client.chat.completions.create(
            model="o3-mini",
            messages=messages,
            tools=tools,
            response_format={"type": "json_object"},
            temperature=0.0,
            max_tokens=2048,
        )

        response_message = chat_response.choices[0].message
        return response_message.tool_calls, chat_response.choices[0].message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


async def run_function_callback_multiple(
    prompt: str,
    tools: list,
    tool_config: Optional[List[Dict]] = None
):
    """
    Run multiple function calls, returning each in tool_calls if they exist,
    or parse them from 'tool_uses' in JSON content if needed.
    """
    messages = [{"role": "user", "content": prompt}]
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    try:
        chat_response = await client.chat.completions.create(
            model="o3-mini",
            messages=messages,
            tools=tools,
            response_format={"type": "json_object"},
            temperature=0.0,
            max_tokens=2048,
        )

        response_message = chat_response.choices[0].message
        if response_message.tool_calls is not None:
            tool_calls = [
                json.loads(tool_call.json())
                for tool_call in response_message.tool_calls
            ]
        else:
            response_message_json = json.loads(response_message.content)
            tool_uses = response_message_json.get("tool_uses", [])
            tool_calls = []
            for i, tool_use in enumerate(tool_uses):
                tool_call = {
                    "id": str(i),
                    "type": "function",
                    "function": {
                        "name": tool_use["recipient_name"],
                        "arguments": json.dumps(tool_use["parameters"])
                    }
                }
                tool_calls.append(tool_call)

        return tool_calls, response_message
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], "error"


async def run_chat_completion_text(
    prompt: str,
    max_tokens: int = 2048,
    tool_config: Optional[List[Dict]] = None
):
    """
    Run a standard chat completion request returning text content only.
    """
    messages = [{"role": "user", "content": prompt}]
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    chat_response = await client.chat.completions.create(
        model="o3-mini",
        messages=messages,
        temperature=0.0,
        max_tokens=max_tokens,
    )

    if chat_response.choices:
        response_message = chat_response.choices[0].message
        if response_message.content:
            return response_message.content, "success"
    return (
        "Please check your request. I don't have an answer for that currently.",
        "error",
    )


async def run_chat_completion(
    prompt: str,
    tools: list,
    function_name: str,
    tool_config: Optional[List[Dict]] = None
):
    """
    Run a chat completion with the possibility of function calls.
    """
    messages = [{"role": "user", "content": prompt}]
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    chat_response = await client.chat.completions.create(
        model="o3-mini",
        messages=messages,
        tools=tools,
        response_format={"type": "json_object"},
        temperature=0.0,
        max_tokens=1024,
    )

    response_message = chat_response.choices[0].message
    tool_calls = response_message.tool_calls

    # Step 2: Check if the model wanted to call a function
    if tool_calls:
        for tool_call in tool_calls:
            return tool_call.function.arguments, "success"

    if response_message.content:
        try:
            content = response_message.content
            if not content.endswith("}"):
                content += "}"
            json.loads(content)
            return content, "success"
        except json.JSONDecodeError:
            errmsg = (
                "Please check your request. I don't have an answer for that currently. "
                + response_message.content
            )
            print(errmsg)
            return errmsg, "error"
        except Exception as e:
            print(str(e))
            return str(e), "error"

    return (
        "Please check your request. I don't have an answer for that currently.",
        "error",
    )


async def run_chat_completion_json(
    prompt: str,
    max_tokens: int = 1024,
    tool_config: Optional[List[Dict]] = None
):
    """
    Run a chat completion expecting a JSON object as output.
    """
    messages = [{"role": "user", "content": prompt}]
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    chat_response = await client.chat.completions.create(
        model="o3-mini",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.0,
        max_tokens=max_tokens,
    )

    response_message = chat_response.choices[0].message
    if response_message.content:
        try:
            content = response_message.content
            if not content.endswith("}"):
                content += "}"
            json.loads(content)
            return content, "success"
        except json.JSONDecodeError:
            errmsg = (
                "Please check your request. I don't have an answer for that currently. "
                + response_message.content
            )
            print(errmsg)
            return errmsg, "error"
        except Exception as e:
            print(str(e))
            return str(e), "error"
    else:
        return (
            "Please check your request. I don't have an answer for that currently.",
            "error",
        )


async def run_chat_completion_structured_output(
    prompt: str,
    response_format: dict,
    max_tokens: int = 1024,
    tool_config: Optional[List[Dict]] = None
):
    """
    Run a chat completion returning parsed structured output (beta).
    """
    messages = [{"role": "user", "content": prompt}]
    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)
    chat_response = await client.beta.chat.completions.parse(
        model="o3-mini",
        messages=messages,
        response_format=response_format,
        temperature=0.0,
        max_tokens=max_tokens,
    )

    message = chat_response.choices[0].message
    if message.parsed:
        print(message.parsed)
        return message.parsed, "success"
    else:
        print(message.refusal)
        return message.refusal, "error"


async def invoke_tool(tool, function_name: str, arguments: dict):
    """
    Invoke a tool asynchronously, passing the function name and arguments.
    """
    return await tool.ainvoke(input={"input": arguments, "function_name": function_name})


def invoke_tool_sync(tool, function_name: str, arguments: dict):
    """
    Synchronous equivalent of invoking a tool with arguments.
    """
    return tool.invoke(input={"input": arguments, "function_name": function_name})


class EventHandler(AsyncAssistantEventHandler):
    """
    Custom event handler to manage tool calls and streaming output.
    """
    def __init__(self, openai_client, openai_tools, agent_tools, thread_id, callback):
        super().__init__()
        self.openai_client = openai_client
        self.openai_tools = openai_tools
        self.agent_tools = agent_tools
        self.thread_id = thread_id
        self.callback = callback

    @override
    async def on_event(self, event):
        if event.event == "thread.run.requires_action":
            await self.handle_requires_action(event.data)

    async def handle_requires_action(self, data):
        """
        Handle events requiring action: tool calls from the model.
        """
        tools_run = data.required_action.submit_tool_outputs.tool_calls
        tool_outputs = []

        for tool_run in tools_run:
            if "_" in tool_run.function.name:
                # Example function name: functionName_toolconf_configId
                function_name, config_id = tool_run.function.name.rsplit("_toolconf_", 1)
                config_id = "toolconf_" + config_id
                tool = next(
                    (
                        x for x in self.agent_tools
                        if x.properties["config_id"] == config_id
                    ),
                    None,
                )
                if tool:
                    parsed_output = await invoke_tool(
                        tool,
                        function_name,
                        tool_run.function.arguments
                    )

                    # Attempt to parse JSON from string
                    if isinstance(parsed_output, str):
                        try:
                            parsed_output = json.loads(parsed_output)
                        except json.JSONDecodeError as e:
                            print(f"Failed to parse JSON: {e}")
                            parsed_output = {"status_code": 400, "text": parsed_output}

                    if parsed_output.get("status_code") in [200, 201, 204]:
                        tool_outputs.append(get_response(tool_run.id, parsed_output))
                    else:
                        # Cancel the run if there's an error
                        await self.openai_client.beta.threads.runs.cancel(
                            run_id=self.current_run.id,
                            thread_id=self.current_run.thread_id,
                        )
                        raise HTTPException(400, get_error_message(parsed_output))

        # Fill in any leftover calls
        for remain in tools_run:
            if remain.id not in [x["tool_call_id"] for x in tool_outputs]:
                tool_outputs.append(
                    {
                        "tool_call_id": remain.id,
                        "output": "Operation completed successfully. No Output",
                    }
                )

        await self.submit_tool_outputs(tool_outputs)
        return tool_outputs

    async def submit_tool_outputs(self, tool_outputs):
        """
        Submit tool outputs back to the run, streaming the assistant's response.
        """
        accumulated_text = ""
        async with self.openai_client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(
                self.openai_client,
                self.openai_tools,
                self.agent_tools,
                self.thread_id,
                self.callback,
            ),
        ) as stream:
            async for text in stream.text_deltas:
                accumulated_text += text
            await stream.until_done()

        print("tools_submit>" + accumulated_text, end="", flush=True)
        self.callback(accumulated_text)

    @override
    async def on_text_created(self, text) -> None:
        print(f"assistant: {text}\n> ", flush=True)

    @override
    async def on_text_delta(self, delta, snapshot):
        # We could print incremental deltas if needed.
        pass

    async def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    async def on_tool_call_delta(self, delta, snapshot):
        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)


async def run_assistant(
    thread: Thread,
    prompt: str,
    instructions: str,
    assistant_id: str,
    file_ids: list = None,
    openai_tools: list = None,
    tools: List[AgentToolObject] = None
):
    """
    Non-streaming version that accumulates the text response from run_assistant_streaming.
    """
    if file_ids is None:
        file_ids = []
    if openai_tools is None:
        openai_tools = []
    if tools is None:
        tools = []

    text = ""
    async for result in run_assistant_streaming(
        thread=thread,
        prompt=prompt,
        instructions=instructions,
        assistant_id=assistant_id,
        openai_tools=openai_tools,
        agent_tools=tools,
        file_ids=file_ids,
    ):
        text += result
    return "", text, "success"


async def run_assistant_streaming(
    thread: Thread,
    prompt: str,
    instructions: str,
    assistant_id: str,
    openai_tools: list = None,
    agent_tools: List[AgentToolObject] = None,
    file_ids: list = None,
    image_ids: list = None,
    tool_config: Optional[List[Dict]] = None,
) -> AsyncIterable[str]:
    """
    Streaming version of run_assistant. Yields text deltas from the model as it generates.
    """
    if openai_tools is None:
        openai_tools = []
    if agent_tools is None:
        agent_tools = []
    if file_ids is None:
        file_ids = []
    if image_ids is None:
        image_ids = []

    openai_key = get_openai_access_token(tool_config)
    client = AsyncOpenAI(api_key=openai_key)

    # Cancel any existing run in the thread that is queued or in-progress
    runs = await client.beta.threads.runs.list(thread_id=thread.id)
    for run in runs.data:
        if run.status in ["queued", "in_progress", "requires_action"]:
            await client.beta.threads.runs.cancel(run_id=run.id, thread_id=thread.id)

    print(prompt[:128])  # Print the first 128 characters of the prompt
    print("\nprompt len:", len(prompt))  # Print the total length of the prompt

    # Handle empty prompt
    if not prompt:
        prompt = "Hi there!"

    # Attach up to 10 files
    attachments = []
    for file_id in file_ids[:10]:
        attachments.append({"file_id": file_id, "tools": [{"type": "file_search"}]})

    # Create the user message content
    content = [{"type": "text", "text": prompt}]
    for image_id in image_ids[:10]:
        content.append({
            "type": "image_file",
            "image_file": {
                "file_id": image_id,
                "detail": "low"  # or "high" depending on your needs
            },
        })

    # Add message to thread
    await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content,
        attachments=attachments,
    )

    # Extend the openai_tools with file_search
    openai_tools.extend([{"type": "file_search"}])
    accumulated_text = ""

    def my_callback_function(out: str):
        nonlocal accumulated_text
        print(f"Accumulated text: {out}")
        accumulated_text += "\n  " + out

    event_handler = EventHandler(
        openai_client=client,
        openai_tools=openai_tools,
        agent_tools=agent_tools,
        thread_id=thread.id,
        callback=my_callback_function,
    )

    try:
        async with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant_id,
            tools=openai_tools,
            event_handler=event_handler,
            max_prompt_tokens=8192,
            max_completion_tokens=1024,
            truncation_strategy={"type": "last_messages", "last_messages": 6},
            temperature=0.0,
            instructions=instructions,
            model="o3-mini",
        ) as stream:
            async for text in stream.text_deltas:
                yield text
            await stream.until_done()

            yield accumulated_text
            print("full" + accumulated_text, end="", flush=True)

    except Exception as e:
        logging.error(
            f"Error running assistant with ID {assistant_id}. "
            f"Error: {e}\n{traceback.format_exc()}"
        )
        yield "An error occurred while processing the request. Please try again later."