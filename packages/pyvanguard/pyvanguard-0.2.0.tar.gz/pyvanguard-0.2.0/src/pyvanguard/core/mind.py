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

import uuid
import json
from typing import Dict, Any, List
from datetime import datetime
from pyvanguard.module.database import Database
from pyvanguard.module.qdrant import Qdrant
from pyvanguard.module.openai import OpenAIClient
from pyvanguard.module.pagerduty import PagerdutyClient
from pyvanguard.module.logger import Logger
from pyvanguard.module.file_system import FileSystem


class Mind:
    """
    Core Functionality of PyVanguard
    """

    def __init__(
        self,
        database_client: Database,
        qdrant_client: Qdrant,
        openai_client: OpenAIClient,
        pagerduty_client: PagerdutyClient,
        logger: Logger,
        file_system: FileSystem,
    ):
        """
        Initialize the Mind class with the necessary clients and logger.

        Args:
            database_client (Database): An instance of the Database client for database operations.
            qdrant_client (Qdrant): An instance of the Qdrant client for vector database operations.
            openai_client (OpenAIClient): An instance of the OpenAI client for generating embeddings.
            pagerduty_client (PagerdutyClient): An instance of the PagerDuty client for alert management.
            logger (Logger): An instance of the Logger for logging operations.
            file_system (FileSystem): An instance of the FileSystem for reading documents from disk.
        """
        self._database_client = database_client
        self._qdrant_client = qdrant_client
        self._openai_client = openai_client
        self._pagerduty_client = pagerduty_client
        self._logger = logger
        self._file_system = file_system

    def setup(self):
        """
        Setup dependencies by connecting to the database and ensuring the Qdrant collection exists.

        This method should be called before performing any other operations to ensure that all
        necessary connections are established and collections are available.
        """
        self._database_client.connect()
        self._database_client.migrate()
        self._qdrant_client.create_collection_if_not_exist("pyvanguard")

    def store_documents(self, path: str, team: str, meta: Dict[str, Any]) -> bool:
        """
        Store documents from a specified directory into the database and Qdrant.

        Args:
            path (str): The path to the directory containing documents to store.
            team (str): The team associated with the documents.
            meta (Dict[str, Any]): Metadata associated with the documents.

        Returns:
            bool: True if documents were stored successfully; False otherwise.

        This method reads documents from the specified directory, generates embeddings for their
        content using OpenAI, and stores both the documents and their embeddings in the database
        and Qdrant respectively.
        """
        documents = self._file_system.read_documents_from_directory(
            path, [".txt", ".md"]
        )
        ids = []
        embeddings = []
        metas = []
        for document in documents:
            if document.get("id") and document.get("content") != "":
                self._database_client.insert_document(
                    {
                        "id": document.get("id"),
                        "content": document.get("content"),
                        "meta": json.dumps({"checksum": document.get("checksum")}),
                        "team": team,
                    }
                )
                ids.append(document.get("id"))
                response = self._openai_client.create_embedding(
                    [document.get("content")]
                )
                embeddings.append(response.data[0].embedding)
                metas.append({"team": team, "kind": "team_document"})

        self._qdrant_client.insert("pyvanguard", embeddings, ids, metas)

        return True

    def trigger_alert(self, summary: str, team: str, meta: Dict[str, Any]) -> str:
        """
        Trigger an alert in PagerDuty and store it in the local database.

        Args:
            summary (str): A brief summary of the alert.
            team (str): The team associated with this alert.
            meta (Dict[str, Any]): Additional metadata related to the alert.

        Returns:
            str: A message indicating whether the alert was triggered successfully.

        This method sends an alert to PagerDuty and stores its details in both
        the local database and Qdrant. It generates a unique ID for each alert
        if not provided and constructs a payload with relevant metadata.
        """

        id = str(uuid.uuid4())

        # Send to PagerDuty
        response = self._pagerduty_client.trigger_alert(
            summary,
            meta.get("severity", "error"),
            meta.get("source", "pyvanguard"),
            meta.get("component", "#"),
            meta.get(
                "links",
                [
                    {
                        "href": f"https://example.com/alert/{id}",
                        "text": "OnCall AI Assistant",
                    }
                ],
            ),
            meta.get("custom_details", {"vid": id}),
        )

        # Store in the local database
        self._database_client.insert_alert(
            {
                "id": id,
                "team": team,
                "summary": summary,
                "meta": json.dumps(
                    {
                        "dedup_key": response["dedup_key"],
                        "severity": meta.get("severity", "error"),
                        "source": meta.get("source", "pyvanguard"),
                        "component": meta.get("component", "#"),
                        "links": meta.get(
                            "links",
                            [
                                {
                                    "href": f"https://example.com/alert/{id}",
                                    "text": "OnCall AI Assistant",
                                }
                            ],
                        ),
                        "custom_details": meta.get("custom_details", {"vid": id}),
                        "notes": [],
                    }
                ),
            }
        )

        # Store in Vector DB (Qdrant)
        data = json.dumps(
            {
                "id": id,
                "team": team,
                "summary": summary,
                "severity": meta.get("severity", "error"),
                "source": meta.get("source", "pyvanguard"),
                "component": meta.get("component", "#"),
                "dedup_key": response["dedup_key"],
                "custom_details": meta.get("custom_details", {"vid": id}),
                "assistant_page": f"https://example.com/alert/{id}",
                "created_at_in_utc": datetime.utcnow().isoformat(),
            }
        )

        response = self._openai_client.create_embedding([f"pagerduty alert {data}"])

        self._qdrant_client.insert(
            "pyvanguard",
            [response.data[0].embedding],
            [id],
            [{"team": team, "kind": "pagerduty_alert"}],
        )

        return f"Alert with ID {id} got triggered successfully!"

    def get_alert(self, id: str) -> Dict[str, Any]:
        """
        Retrieve an alert by its ID from the database.

        Args:
            id (str): The ID of the alert to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing alert details or None if not found.

        This method fetches an alert's details from the local database using its ID.
        """
        return self._database_client.get_alert_by_id(id)

    def get_document(self, id: str) -> Dict[str, Any]:
        """
        Retrieve a document by its ID from the database.

        Args:
           id (str): The ID of the document to retrieve.

        Returns:
           Dict[str, Any]: A dictionary containing document details or None if not found.

        This method fetches a document's details from the local database using its ID.
        """
        return self._database_client.get_document_by_id(id)

    def get_documents_by_team(self, team: str) -> List[Dict[str, Any]]:
        """
        Retrieve all documents associated with a specific team from the database.

        Args:
            team (str): The name of the team whose documents are to be retrieved.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing document details.

        This method fetches all documents related to a specified team from
        the local database.
        """
        return self._database_client.get_documents_by_team(team)

    def get_alerts_by_team(self, team: str) -> List[Dict[str, Any]]:
        """
        Retrieve all alerts associated with a specific team from the database.

        Args:
            team (str): The name of the team whose alerts are to be retrieved.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing alert details.

        This method fetches all alerts related to a specified team from
        the local database.
        """
        return self._database_client.get_alerts_by_team(team)

    def get_relevant_data(
        self, text: str, kind: str, team: str, limit: int
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant data based on input text.

        Args:
           text (str): Input text for which relevant data is to be retrieved.

        Returns:
           str: Relevant data as a string or an empty string if no data is found.

        This method should implement logic to find relevant data based on
        input text using Qdrant or other means. Currently not implemented.
        """
        response = self._openai_client.create_embedding(text)

        if kind == "" or kind is None:
            metadata = {"team": team}
        else:
            metadata = {"team": team, "kind": kind}

        result = self._qdrant_client.search(
            "pyvanguard", response.data[0].embedding, metadata, limit
        )

        output = []

        for item in result:
            document = self._database_client.get_document_by_id(item.get("id"))
            alert = self._database_client.get_alert_by_id(item.get("id"))

            if document is not None:
                output.append(
                    {
                        "id": item.get("id"),
                        "score": item.get("score"),
                        "data": document,
                        "kind": "team_document",
                    }
                )

            if alert is not None:
                output.append(
                    {
                        "id": item.get("id"),
                        "score": item.get("score"),
                        "data": alert,
                        "kind": "pagerduty_alert",
                    }
                )

        return output

    def summarize_relevant_data(self, prompt: str, data: str) -> str:
        """
        Summarize relevant data using OpenAI's API based on a given prompt.

        Args:
            prompt (str): The prompt guiding how to summarize data.
            data (str): The data that needs summarization.

        Returns:
            str: The summarized version of the provided data or an empty string if an error occurs.

        This method should implement logic to summarize relevant data using
        OpenAI's API. Currently not implemented.
        """
        pass


def get_mind(
    database_client: Database,
    qdrant_client: Qdrant,
    openai_client: OpenAIClient,
    pagerduty_client: PagerdutyClient,
    logger: Logger,
    file_system: FileSystem,
) -> Mind:
    """
    Get Mind Class Instance
    """
    return Mind(
        database_client,
        qdrant_client,
        openai_client,
        pagerduty_client,
        logger,
        file_system,
    )
