"""
Tests for management command
"""
import os
import tempfile
from os import path
from unittest import TestCase

from dr_scaffold import file_api


class TestFileApi(TestCase):
    """
    Tests for file api
    """

    tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")

    def setUp(self):
        """
        Tests for file api
        """
        with open(self.tmpfilepath, "x", encoding="utf8") as file:
            file.write("Delete me!")

    def tearDown(self):
        """
        Tests for file api
        """
        os.remove(self.tmpfilepath)
        if path.exists("file.txt"):
            os.remove("file.txt")

    @classmethod
    def test_create_file(cls):
        """
        Tests for file api
        """
        file_api.create_file("file.txt")
        assert path.exists("file.txt")

    def test_wipe_file_content(self):
        """
        Tests for file api
        """
        file_api.wipe_file_content(self.tmpfilepath)
        self._extracted_from_test_wipe_files_4()

    def test_get_file_content(self):
        """
        Tests for file api
        """
        body = file_api.get_file_content(self.tmpfilepath)
        assert body == "Delete me!"

    def test_set_file_content(self):
        """
        Tests for file api
        """
        file_api.set_file_content(self.tmpfilepath, "new content")
        with open(self.tmpfilepath, "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body == "new content"

    def test_prepend_file_content(self):
        """
        Tests for file api
        """
        file_api.prepend_file_content(self.tmpfilepath, "new content")
        with open(self.tmpfilepath, "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body == "new contentDelete me!"

    def test_append_file_content(self):
        """
        Tests for file api
        """
        file_api.append_file_content(self.tmpfilepath, "new content")
        with open(self.tmpfilepath, "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body == "Delete me!new content"

    def test_wrap_file_content(self):
        """
        Tests for file api
        """
        file_api.wrap_file_content(self.tmpfilepath, "head", "tail")
        with open(self.tmpfilepath, "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body == "headDelete me!tail"

    def test_replace_file_chunk(self):
        """
        Tests for file api
        """
        file_api.replace_file_chunk(self.tmpfilepath, "Delete", "Remove")
        with open(self.tmpfilepath, "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body == "Remove me!"

    def test_is_present_in_file(self):
        """
        Tests for file api
        """
        assert file_api.is_present_in_file(self.tmpfilepath, "Delete") is True
        assert file_api.is_present_in_file(self.tmpfilepath, "Remove") is False

    def test_wipe_files(self):
        """
        Tests for file api
        """
        file_api.wipe_files((self.tmpfilepath,))
        self._extracted_from_test_wipe_files_4()

    def _extracted_from_test_wipe_files_4(self):
        with open(self.tmpfilepath, "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body != "Delete me!"
        assert len(body) == 0

    @classmethod
    def test_create_files(cls):
        """
        Tests for file api
        """
        file_api.create_files(("file.txt",))
        assert path.exists("file.txt") is True
