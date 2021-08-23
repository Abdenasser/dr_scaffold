import pytest
from os import path
from dr_scaffold import file_api

def test_create_file():
  file_api.create_file('file.txt')
  assert  path.exists("guru99.txt") == True