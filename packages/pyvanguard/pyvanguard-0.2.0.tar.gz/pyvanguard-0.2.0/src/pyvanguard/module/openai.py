# MIT License
#
# Copyright (c) 2025 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from openai import OpenAI


class OpenAIClient:
    """
    A wrapper class for the OpenAI API client.

    This class provides a simplified interface for creating embeddings
    and accessing the underlying OpenAI client.

    Attributes:
        _client (OpenAI): The underlying OpenAI client instance.
    """

    def __init__(self, api_key: str):
        """
        Initialize the OpenAIClient with the given API key.

        Args:
            api_key (str): The OpenAI API key for authentication.
        """
        self._client = OpenAI(api_key=api_key)

    def create_embedding(self, texts: list, model="text-embedding-3-small"):
        """
        Create embeddings for the given texts using the specified model.

        Args:
            texts (list): A list of strings to create embeddings for.
            model (str, optional): The name of the embedding model to use.
                Defaults to "text-embedding-3-small".

        Returns:
            The response from the OpenAI API containing the created embeddings.
        """
        return self._client.embeddings.create(input=texts, model=model)

    def get_client(self):
        """
        Get the underlying OpenAI client instance.

        Returns:
            OpenAI: The OpenAI client instance.
        """
        return self._client


def get_openai_client(api_key: str) -> OpenAIClient:
    """
    Create and return an instance of OpenAIClient.

    Args:
        api_key (str): The OpenAI API key for authentication.

    Returns:
        OpenAIClient: An instance of the OpenAIClient class.
    """
    return OpenAIClient(api_key)
