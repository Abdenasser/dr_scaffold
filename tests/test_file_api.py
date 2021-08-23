import os
import pytest  
import tempfile  
from os import path
from dr_scaffold import file_api
from unittest import TestCase

class TestFileApi(TestCase):
    tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")

    def setUp(self):
        with open(self.tmpfilepath, "x") as f:
            f.write("Delete me!")
        
    def tearDown(self):
        os.remove(self.tmpfilepath)           
         
    def test_create_file(self):
        file_api.create_file('file.txt')
        assert  path.exists("file.txt") == True
        os.remove("file.txt")  

    def test_wipe_file_content(self):
        file_api.wipe_file_content(self.tmpfilepath)
        with open(self.tmpfilepath, 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert body != "Delete me!"
        assert len(body) == 0
        
    def test_get_file_content(self):
        body = file_api.get_file_content(self.tmpfilepath)
        assert body == "Delete me!"

    def test_set_file_content(self):
        file_api.set_file_content(self.tmpfilepath, "new content")
        with open(self.tmpfilepath, 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert body == "new content"

    def test_prepend_file_content(self):
        file_api.prepend_file_content(self.tmpfilepath, "new content")
        with open(self.tmpfilepath, 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert body == "new contentDelete me!"

    def test_append_file_content(self):
        file_api.append_file_content(self.tmpfilepath, "new content")
        with open(self.tmpfilepath, 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert body == "Delete me!new content"

    def test_wrap_file_content(self):
        file_api.wrap_file_content(self.tmpfilepath, "head", "tail")
        with open(self.tmpfilepath, 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert body == "headDelete me!tail"

    def test_replace_file_chunk(self):
        file_api.replace_file_chunk(self.tmpfilepath, "Delete", "Remove")
        with open(self.tmpfilepath, 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert body == "Remove me!"

    def test_is_present_in_file(self):
        assert file_api.is_present_in_file(self.tmpfilepath, "Delete") == True
        assert file_api.is_present_in_file(self.tmpfilepath, "Remove") == False