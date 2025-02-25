# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import pytest
from pydantic import BaseModel

from llama_stack.providers.tests.test_cases.test_case import TestCase

PROVIDER_TOOL_PROMPT_FORMAT = {
    "remote::ollama": "json",
    "remote::together": "json",
    "remote::fireworks": "json",
    "remote::vllm": "json",
}

PROVIDER_LOGPROBS_TOP_K = {"remote::together", "remote::fireworks", "remote::vllm"}


@pytest.fixture(scope="session")
def provider_tool_format(inference_provider_type):
    return (
        PROVIDER_TOOL_PROMPT_FORMAT[inference_provider_type]
        if inference_provider_type in PROVIDER_TOOL_PROMPT_FORMAT
        else None
    )


@pytest.fixture
def get_weather_tool_definition():
    return {
        "tool_name": "get_weather",
        "description": "Get the current weather",
        "parameters": {
            "location": {
                "param_type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
        },
    }


def test_text_completion_non_streaming(client_with_models, text_model_id):
    response = client_with_models.inference.completion(
        content="Complete the sentence using one word: Roses are red, violets are ",
        stream=False,
        model_id=text_model_id,
        sampling_params={
            "max_tokens": 50,
        },
    )
    assert len(response.content) > 10
    # assert "blue" in response.content.lower().strip()


def test_text_completion_streaming(client_with_models, text_model_id):
    response = client_with_models.inference.completion(
        content="Complete the sentence using one word: Roses are red, violets are ",
        stream=True,
        model_id=text_model_id,
        sampling_params={
            "max_tokens": 50,
        },
    )
    streamed_content = [chunk.delta for chunk in response]
    content_str = "".join(streamed_content).lower().strip()
    # assert "blue" in content_str
    assert len(content_str) > 10


def test_completion_log_probs_non_streaming(client_with_models, text_model_id, inference_provider_type):
    if inference_provider_type not in PROVIDER_LOGPROBS_TOP_K:
        pytest.xfail(f"{inference_provider_type} doesn't support log probs yet")

    response = client_with_models.inference.completion(
        content="Complete the sentence: Micheael Jordan is born in ",
        stream=False,
        model_id=text_model_id,
        sampling_params={
            "max_tokens": 5,
        },
        logprobs={
            "top_k": 1,
        },
    )
    assert response.logprobs, "Logprobs should not be empty"
    assert 1 <= len(response.logprobs) <= 5  # each token has 1 logprob and here max_tokens=5
    assert all(len(logprob.logprobs_by_token) == 1 for logprob in response.logprobs)


def test_completion_log_probs_streaming(client_with_models, text_model_id, inference_provider_type):
    if inference_provider_type not in PROVIDER_LOGPROBS_TOP_K:
        pytest.xfail(f"{inference_provider_type} doesn't support log probs yet")

    response = client_with_models.inference.completion(
        content="Complete the sentence: Micheael Jordan is born in ",
        stream=True,
        model_id=text_model_id,
        sampling_params={
            "max_tokens": 5,
        },
        logprobs={
            "top_k": 1,
        },
    )
    streamed_content = [chunk for chunk in response]
    for chunk in streamed_content:
        if chunk.delta:  # if there's a token, we expect logprobs
            assert chunk.logprobs, "Logprobs should not be empty"
            assert all(len(logprob.logprobs_by_token) == 1 for logprob in chunk.logprobs)
        else:  # no token, no logprobs
            assert not chunk.logprobs, "Logprobs should be empty"


@pytest.mark.parametrize("test_case", ["completion-01"])
def test_text_completion_structured_output(client_with_models, text_model_id, test_case):
    class AnswerFormat(BaseModel):
        name: str
        year_born: str
        year_retired: str

    tc = TestCase(test_case)

    user_input = tc["user_input"]
    response = client_with_models.inference.completion(
        model_id=text_model_id,
        content=user_input,
        stream=False,
        sampling_params={
            "max_tokens": 50,
        },
        response_format={
            "type": "json_schema",
            "json_schema": AnswerFormat.model_json_schema(),
        },
    )
    answer = AnswerFormat.model_validate_json(response.content)
    expected = tc["expected"]
    assert answer.name == expected["name"]
    assert answer.year_born == expected["year_born"]
    assert answer.year_retired == expected["year_retired"]


@pytest.mark.parametrize(
    "question,expected",
    [
        ("Which planet do humans live on?", "Earth"),
        (
            "Which planet has rings around it with a name starting with letter S?",
            "Saturn",
        ),
    ],
)
def test_text_chat_completion_non_streaming(client_with_models, text_model_id, question, expected):
    response = client_with_models.inference.chat_completion(
        model_id=text_model_id,
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        stream=False,
    )
    message_content = response.completion_message.content.lower().strip()
    assert len(message_content) > 0
    assert expected.lower() in message_content


@pytest.mark.parametrize(
    "question,expected",
    [
        ("What's the name of the Sun in latin?", "Sol"),
        ("What is the name of the US captial?", "Washington"),
    ],
)
def test_text_chat_completion_streaming(client_with_models, text_model_id, question, expected):
    response = client_with_models.inference.chat_completion(
        model_id=text_model_id,
        messages=[{"role": "user", "content": question}],
        stream=True,
    )
    streamed_content = [str(chunk.event.delta.text.lower().strip()) for chunk in response]
    assert len(streamed_content) > 0
    assert expected.lower() in "".join(streamed_content)


def test_text_chat_completion_with_tool_calling_and_non_streaming(
    client_with_models, text_model_id, get_weather_tool_definition, provider_tool_format
):
    response = client_with_models.inference.chat_completion(
        model_id=text_model_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's the weather like in San Francisco?"},
        ],
        tools=[get_weather_tool_definition],
        tool_choice="auto",
        tool_prompt_format=provider_tool_format,
        stream=False,
    )
    # No content is returned for the system message since we expect the
    # response to be a tool call
    assert response.completion_message.content == ""
    assert response.completion_message.role == "assistant"

    assert len(response.completion_message.tool_calls) == 1
    assert response.completion_message.tool_calls[0].tool_name == "get_weather"
    assert response.completion_message.tool_calls[0].arguments == {"location": "San Francisco, CA"}


# Will extract streamed text and separate it from tool invocation content
# The returned tool inovcation content will be a string so it's easy to comapare with expected value
# e.g. "[get_weather, {'location': 'San Francisco, CA'}]"
def extract_tool_invocation_content(response):
    tool_invocation_content: str = ""
    for chunk in response:
        delta = chunk.event.delta
        if delta.type == "tool_call" and delta.parse_status == "succeeded":
            call = delta.tool_call
            tool_invocation_content += f"[{call.tool_name}, {call.arguments}]"
    return tool_invocation_content


def test_text_chat_completion_with_tool_calling_and_streaming(
    client_with_models, text_model_id, get_weather_tool_definition, provider_tool_format
):
    response = client_with_models.inference.chat_completion(
        model_id=text_model_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's the weather like in San Francisco?"},
        ],
        tools=[get_weather_tool_definition],
        tool_choice="auto",
        tool_prompt_format=provider_tool_format,
        stream=True,
    )
    tool_invocation_content = extract_tool_invocation_content(response)
    assert tool_invocation_content == "[get_weather, {'location': 'San Francisco, CA'}]"


def test_text_chat_completion_with_tool_choice_required(
    client_with_models,
    text_model_id,
    get_weather_tool_definition,
    provider_tool_format,
):
    response = client_with_models.inference.chat_completion(
        model_id=text_model_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's the weather like in San Francisco?"},
        ],
        tools=[get_weather_tool_definition],
        tool_config={
            "tool_choice": "required",
            "tool_prompt_format": provider_tool_format,
        },
        stream=True,
    )
    tool_invocation_content = extract_tool_invocation_content(response)
    assert tool_invocation_content == "[get_weather, {'location': 'San Francisco, CA'}]"


def test_text_chat_completion_with_tool_choice_none(
    client_with_models, text_model_id, get_weather_tool_definition, provider_tool_format
):
    response = client_with_models.inference.chat_completion(
        model_id=text_model_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's the weather like in San Francisco?"},
        ],
        tools=[get_weather_tool_definition],
        tool_config={"tool_choice": "none", "tool_prompt_format": provider_tool_format},
        stream=True,
    )
    tool_invocation_content = extract_tool_invocation_content(response)
    assert tool_invocation_content == ""


@pytest.mark.parametrize("test_case", ["chat_completion-01"])
def test_text_chat_completion_structured_output(client_with_models, text_model_id, test_case):
    class AnswerFormat(BaseModel):
        first_name: str
        last_name: str
        year_of_birth: int
        num_seasons_in_nba: int

    tc = TestCase(test_case)

    response = client_with_models.inference.chat_completion(
        model_id=text_model_id,
        messages=tc["messages"],
        response_format={
            "type": "json_schema",
            "json_schema": AnswerFormat.model_json_schema(),
        },
        stream=False,
    )
    answer = AnswerFormat.model_validate_json(response.completion_message.content)
    expected = tc["expected"]
    assert answer.first_name == expected["first_name"]
    assert answer.last_name == expected["last_name"]
    assert answer.year_of_birth == expected["year_of_birth"]
    assert answer.num_seasons_in_nba == expected["num_seasons_in_nba"]


@pytest.mark.parametrize(
    "streaming",
    [
        True,
        False,
    ],
)
def test_text_chat_completion_tool_calling_tools_not_in_request(client_with_models, text_model_id, streaming):
    # TODO: more dynamic lookup on tool_prompt_format for model family
    tool_prompt_format = "json" if "3.1" in text_model_id else "python_list"
    request = {
        "model_id": text_model_id,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "What pods are in the namespace openshift-lightspeed?",
            },
            {
                "role": "assistant",
                "content": "",
                "stop_reason": "end_of_turn",
                "tool_calls": [
                    {
                        "call_id": "1",
                        "tool_name": "get_object_namespace_list",
                        "arguments": {
                            "kind": "pod",
                            "namespace": "openshift-lightspeed",
                        },
                    }
                ],
            },
            {
                "role": "tool",
                "call_id": "1",
                "tool_name": "get_object_namespace_list",
                "content": "the objects are pod1, pod2, pod3",
            },
        ],
        "tools": [
            {
                "tool_name": "get_object_namespace_list",
                "description": "Get the list of objects in a namespace",
                "parameters": {
                    "kind": {
                        "param_type": "string",
                        "description": "the type of object",
                        "required": True,
                    },
                    "namespace": {
                        "param_type": "string",
                        "description": "the name of the namespace",
                        "required": True,
                    },
                },
            }
        ],
        "tool_choice": "auto",
        "tool_prompt_format": tool_prompt_format,
        "stream": streaming,
    }

    response = client_with_models.inference.chat_completion(**request)

    if streaming:
        for chunk in response:
            delta = chunk.event.delta
            if delta.type == "tool_call" and delta.parse_status == "succeeded":
                assert delta.tool_call.tool_name == "get_object_namespace_list"
            if delta.type == "tool_call" and delta.parse_status == "failed":
                # expect raw message that failed to parse in tool_call
                assert type(delta.tool_call) == str
                assert len(delta.tool_call) > 0
    else:
        for tc in response.completion_message.tool_calls:
            assert tc.tool_name == "get_object_namespace_list"
