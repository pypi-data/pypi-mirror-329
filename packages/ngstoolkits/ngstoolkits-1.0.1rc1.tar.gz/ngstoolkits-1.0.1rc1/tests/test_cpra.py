import pytest
import pysam
from ngstoolkits import CPRA

def test_cpra_coordinate_systems():
    """测试CPRA类的坐标系统"""
    # 1-based坐标初始化
    mut1 = CPRA("chr1", 1000, "A", "T", base=1)
    assert mut1.pos_1based == 1000
    assert mut1.pos_0based == 999
    
    # 0-based坐标初始化
    mut0 = CPRA("chr1", 999, "A", "T", base=0)
    assert mut0.pos_1based == 1000
    assert mut0.pos_0based == 999
    
    # 验证两种方式初始化的对象表示相同位置
    assert mut1.pos_1based == mut0.pos_1based
    assert mut1.pos_0based == mut0.pos_0based

def test_cpra_position_conversion():
    """测试位置转换功能"""
    mut = CPRA("chr1", 1000, "A", "T", base=1)
    assert mut._get_pos_in_base(0) == 999  # 转换为0-based
    assert mut._get_pos_in_base(1) == 1000  # 转换为1-based
    assert mut._get_pos_in_base() == 1000  # 使用默认base 