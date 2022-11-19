#Stub to test convertCSVtoSHP module
import pytest
#import tempfile
#import shutil
import convertCSVtoSHP


def test_readDir(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    output = readDir(d)[0]
    assert output == "hello.txt"

    
