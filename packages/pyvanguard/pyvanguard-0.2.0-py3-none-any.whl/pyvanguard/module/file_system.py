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

import os
import hashlib
import uuid
from typing import List, Dict, Any


class FileSystem:
    """
    A utility class for handling file system operations, specifically for reading
    documents from a directory with specified file extensions.
    """

    def read_documents_from_directory(
        self, directory_path: str, extensions: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Reads documents from files with specified extensions in a given directory.

        Args:
            directory_path (str): The path to the directory to read from.
            extensions (List[str]): A list of file extensions to consider (e.g., ['.txt', '.md']).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, where each dictionary contains:
                - 'file_path' (str): The full path to the file.
                - 'content' (str): The content of the file, or None if an error occurred.
                - 'checksum' (str): The MD5 checksum of the file content.
        """
        documents = []
        for filename in os.listdir(directory_path):
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(
                    file_path
                ):  # Ensure it's a file and not a subdirectory
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            checksum = self._calculate_md5(content)
                        documents.append(
                            {
                                "id": str(uuid.uuid4()),
                                "file_path": file_path,
                                "content": content,
                                "checksum": checksum,
                            }
                        )
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
                        documents.append(
                            {
                                "file_path": file_path,
                                "content": None,
                                "checksum": None,
                                "id": None,
                            }
                        )

        return documents

    def _calculate_md5(self, content: str) -> str:
        """
        Calculates the MD5 checksum of a given string content.

        Args:
            content (str): The content to calculate the checksum for.

        Returns:
            str: The MD5 checksum as a hexadecimal string.
        """
        md5_hash = hashlib.md5()
        md5_hash.update(content.encode("utf-8"))  # Encode the string to bytes
        return md5_hash.hexdigest()


def get_file_system() -> FileSystem:
    return FileSystem()


if __name__ == "__main__":
    fs = FileSystem()
    print(
        fs.read_documents_from_directory(
            "/Users/ahmetwal/space/personal/pyvanguard/testdocs", [".md"]
        )
    )
