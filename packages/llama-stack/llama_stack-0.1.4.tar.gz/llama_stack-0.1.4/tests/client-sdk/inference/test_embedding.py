# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.


#
# Test plan:
#
#  Types of input:
#   - array of a string
#   - array of a image (ImageContentItem, either URL or base64 string)
#   - array of a text (TextContentItem)
#  Types of output:
#   - list of list of floats
#
# Todo:
#  - negative tests
#    - empty
#      - empty list
#      - empty string
#      - empty text
#      - empty image
#    - long
#      - long string
#      - long text
#      - large image
#      - appropriate combinations
#    - batch size
#      - many inputs
#    - invalid
#      - invalid URL
#      - invalid base64
#
# Notes:
#  - use llama_stack_client fixture
#  - use pytest.mark.parametrize when possible
#  - no accuracy tests: only check the type of output, not the content
#

import pytest
from llama_stack_client.types import EmbeddingsResponse
from llama_stack_client.types.shared.interleaved_content import (
    ImageContentItem,
    ImageContentItemImage,
    ImageContentItemImageURL,
    TextContentItem,
)

DUMMY_STRING = "hello"
DUMMY_STRING2 = "world"
DUMMY_TEXT = TextContentItem(text=DUMMY_STRING, type="text")
DUMMY_TEXT2 = TextContentItem(text=DUMMY_STRING2, type="text")
# TODO(mf): add a real image URL and base64 string
DUMMY_IMAGE_URL = ImageContentItem(
    image=ImageContentItemImage(url=ImageContentItemImageURL(uri="https://example.com/image.jpg")), type="image"
)
DUMMY_IMAGE_BASE64 = ImageContentItem(image=ImageContentItemImage(data="base64string"), type="image")


@pytest.mark.parametrize(
    "contents",
    [
        [DUMMY_STRING, DUMMY_STRING2],
        [DUMMY_TEXT, DUMMY_TEXT2],
    ],
    ids=[
        "list[string]",
        "list[text]",
    ],
)
def test_embedding_text(llama_stack_client, embedding_model_id, contents):
    response = llama_stack_client.inference.embeddings(model_id=embedding_model_id, contents=contents)
    assert isinstance(response, EmbeddingsResponse)
    assert len(response.embeddings) == sum(len(content) if isinstance(content, list) else 1 for content in contents)
    assert isinstance(response.embeddings[0], list)
    assert isinstance(response.embeddings[0][0], float)


@pytest.mark.parametrize(
    "contents",
    [
        [DUMMY_IMAGE_URL, DUMMY_IMAGE_BASE64],
        [DUMMY_IMAGE_URL, DUMMY_STRING, DUMMY_IMAGE_BASE64, DUMMY_TEXT],
    ],
    ids=[
        "list[url,base64]",
        "list[url,string,base64,text]",
    ],
)
@pytest.mark.skip(reason="Media is not supported")
def test_embedding_image(llama_stack_client, embedding_model_id, contents):
    response = llama_stack_client.inference.embeddings(model_id=embedding_model_id, contents=contents)
    assert isinstance(response, EmbeddingsResponse)
    assert len(response.embeddings) == sum(len(content) if isinstance(content, list) else 1 for content in contents)
    assert isinstance(response.embeddings[0], list)
    assert isinstance(response.embeddings[0][0], float)
