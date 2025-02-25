"""
    Dummy conftest.py for ngstools.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

# import pytest
import sys
sys.path.append('../src')
import pytest
from ngstoolkits import Seq
from ngstoolkits import CPRA
CPRA.loadBam("test_data/pancancer689__DX2083_sijuan_20S12590085_20B12590085__Cancer.realign.bam")
CPRA.loadReference("test_data/hg19.fa")


def test_single_mutation():
    sitea=CPRA("chr2","21230379","C","T")
    siteb=CPRA("chr1",65332550,"","T")
    sitec=CPRA("chr1",8074099,"AG","")
    sitec.get_suppot()
    assert sitec.pos_fit == 8074100
    sited=CPRA("chr1",8074100,"AG","")
    assert siteb.muttype=="INS"
    assert sited.muttype=="DEL"
    assert sitea.muttype=="SNV"

def test_Seq():
    assert Seq.reverse_complement("ATGC")=="GCAT"