import pytest
from convertCSVtoSHP import readDir, convertCSVtoSHP
import os


def test_readDir(tmpdir):
    expectedoutput = ['testfile.txt', 'testfile1.txt']

    for i in expectedoutput:
        filename = tmpdir.join(i)
        filename.write("this is a test stub")

    output = readDir(tmpdir)

    assert output[0] == 'testfile1.txt'
    assert output[1] == 'testfile.txt'

def test_convertCSVtoSHP(tmpdir):
    convertCSVtoSHP("test/csvdata")