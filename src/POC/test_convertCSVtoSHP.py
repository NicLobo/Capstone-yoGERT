import pytest
from convertCSVtoSHP import readDir, convertCSVtoSHP
import os
import subprocess


def test_readDir(tmpdir):
    expectedoutput = ['testfile.txt', 'testfile1.txt']
    for i in expectedoutput:
        filename = tmpdir.join(i)
        filename.write("this is a test stub")
    output = readDir(tmpdir)
    assert 'testfile1.txt' in output[0]
    assert 'testfile.txt' in output[1] 

def test_convertCSVtoSHP(tmpdir):
    csvfiles = readDir("../test/csvdata")
    convertCSVtoSHP(csvfiles)
    outputpath = readDir("../SHPfiles/")
    assert "travelepisode0" in outputpath[0]
    subprocess.run(["rm", "-r", "../SHPfiles/"])

