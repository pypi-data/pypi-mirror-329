import pytest
from ngstoolkits import SeqFunction

def test_base_count():
    """测试碱基计数功能"""
    assert SeqFunction.base_count("ATGC") == [1, 1, 1, 1]
    assert SeqFunction.base_count("AAAA") == [4, 0, 0, 0]
    assert SeqFunction.base_count("atgc") == [1, 1, 1, 1]  # 测试小写

def test_reverse_complement():
    """测试反向互补功能"""
    assert SeqFunction.reverse_complement("ATGC") == "GCAT"
    assert SeqFunction.reverse_complement("AAAA") == "TTTT"
    assert SeqFunction.reverse_complement("atgc") == "GCAT"  # 测试小写

def test_gc_content():
    """测试GC含量计算"""
    assert SeqFunction.GC_content("ATGC") == 0.5
    assert SeqFunction.GC_content("AAAA") == 0.0
    assert SeqFunction.GC_content("CCGG") == 1.0
    assert SeqFunction.GC_content("atgc") == 0.5  # 测试小写

def test_invalid_input():
    """测试无效输入的处理"""
    with pytest.raises(ZeroDivisionError):
        SeqFunction.GC_content("")
    
    # 测试含有非法字符的序列
    result = SeqFunction.base_count("ATG-C")
    assert sum(result) == 4  # 应该只计数ATGC 