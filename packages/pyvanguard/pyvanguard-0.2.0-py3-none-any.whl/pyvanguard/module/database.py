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
import sqlite3
from typing import List, Dict, Any


class Database:
    """A class to manage SQLite database operations."""

    def __init__(self, path: str):
        """Initialize the database with a file path.

        Args:
            path (str): Path to the SQLite database file.
        """
        self._path = path
        self._connection = None

    def connect(self) -> int:
        """Establish a connection to the SQLite database.

        Returns:
            int: The number of total changes to the database.
        """
        self._connection = sqlite3.connect(self._path)
        return self._connection.total_changes

    def migrate(self) -> None:
        """Create necessary tables if they don't exist."""
        cursor = self._connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS document (id TEXT, content TEXT, meta TEXT, team TEXT, createdAt TEXT, updatedAt TEXT)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS alert (id TEXT, summary TEXT, meta TEXT, team TEXT, createdAt TEXT, updatedAt TEXT)"
        )

        cursor.close()
        self._connection.commit()

    def insert_document(self, document: Dict[str, Any]) -> int:
        """Insert a new document

        Args:
            document (Dict): The document data

        Returns:
            The total rows inserted
        """
        cursor = self._connection.cursor()

        result = cursor.execute(
            "INSERT INTO document VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))",
            (
                document.get("id", str(uuid.uuid4())),
                document.get("content"),
                document.get("meta", "{}"),
                document.get("team"),
            ),
        )

        cursor.close()

        self._connection.commit()

        return result.rowcount

    def insert_alert(self, alert: Dict[str, Any]) -> int:
        """Insert a new alert

        Args:
            alert (Dict): The alert data

        Returns:
            The total rows inserted
        """
        cursor = self._connection.cursor()

        result = cursor.execute(
            "INSERT INTO alert VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))",
            (
                alert.get("id", str(uuid.uuid4())),
                alert.get("summary"),
                alert.get("meta", "{}"),
                alert.get("team"),
            ),
        )

        cursor.close()

        self._connection.commit()

        return result.rowcount

    def delete_document(self, id: str) -> None:
        """Delete a document by its ID.

        Args:
            id (str): The ID of the document to delete.
        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM document WHERE id = ?", (id,))
        cursor.close()
        self._connection.commit()

    def delete_alert(self, id: str) -> None:
        """Delete an alert by its ID.

        Args:
            id (str): The ID of the alert to delete.
        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM alert WHERE id = ?", (id,))
        cursor.close()
        self._connection.commit()

    def get_document_by_id(self, id: str) -> Dict[str, Any]:
        """Retrieve a document by its ID.

        Args:
            id (str): The ID of the document to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing the document details.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM document WHERE id = ?", (id,))
        result = cursor.fetchone()
        cursor.close()

        return (
            dict(
                zip(["id", "content", "meta", "team", "createdAt", "updatedAt"], result)
            )
            if result
            else None
        )

    def get_alert_by_id(self, id: str) -> Dict[str, Any]:
        """Retrieve an alert by its ID.

        Args:
            id (str): The ID of the alert to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing the alert details.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM alert WHERE id = ?", (id,))
        result = cursor.fetchone()
        cursor.close()

        return (
            dict(
                zip(["id", "summary", "meta", "team", "createdAt", "updatedAt"], result)
            )
            if result
            else None
        )

    def get_documents_by_team(self, team: str) -> List[Dict[str, Any]]:
        """Retrieve all documents for a specific team.

        Args:
            team (str): The team name.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing document details.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM document WHERE team = ?", (team,))
        results = cursor.fetchall()
        cursor.close()

        return [
            dict(zip(["id", "content", "meta", "team", "createdAt", "updatedAt"], row))
            for row in results
        ]

    def get_alerts_by_team(self, team: str) -> List[Dict[str, Any]]:
        """Retrieve all alerts for a specific team.

        Args:
            team (str): The team name.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing alert details.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM alert WHERE team = ?", (team,))
        results = cursor.fetchall()
        cursor.close()

        return [
            dict(zip(["id", "summary", "meta", "team", "createdAt", "updatedAt"], row))
            for row in results
        ]


def get_database_client(path: str) -> Database:
    """Create and return a Database instance.

    Args:
        path (str): SQLite database path.

    Returns:
        Database: Initialized Database client.
    """
    return Database(path)
