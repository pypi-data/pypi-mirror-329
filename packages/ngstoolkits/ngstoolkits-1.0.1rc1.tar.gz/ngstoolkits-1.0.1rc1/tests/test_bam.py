import pytest
import pysam
from ngstoolkits import BAM

@pytest.fixture
def bam_file(tmp_path):
    """创建测试用的BAM文件"""
    bam_path = tmp_path / "test.bam"
    header = {'HD': {'VN': '1.0'},
              'SQ': [{'LN': 1000, 'SN': 'chr1'}]}
    
    with pysam.AlignmentFile(bam_path, "wb", header=header) as outf:
        # 创建一些测试数据
        a = pysam.AlignedSegment()
        a.query_name = "read1"
        a.query_sequence = "AGTC"
        a.reference_id = 0
        a.reference_start = 100  # 0-based position
        a.mapping_quality = 20
        a.cigar = [(0, 4)]
        outf.write(a)
    
    pysam.index(str(bam_path))
    return str(bam_path)

def test_bam_init(bam_file):
    """测试BAM类的初始化"""
    bam = BAM(pysam.AlignmentFile(bam_file))
    assert isinstance(bam.Bam, pysam.AlignmentFile)

def test_get_base_count_per_position_0base(bam_file):
    """测试获取位点碱基计数(0-based)"""
    bam = BAM(pysam.AlignmentFile(bam_file))
    counts = bam.get_base_count_per_position("chr1", 100)  # 0-based
    assert len(counts) == 5
    assert isinstance(counts[0], int)
    assert sum(counts[:4]) == counts[4]

def test_get_base_count_per_position_1base(bam_file):
    """测试获取位点碱基计数(1-based)"""
    bam = BAM(pysam.AlignmentFile(bam_file))
    counts = bam.get_base_count_per_position("chr1", 101, base=1)  # 1-based
    assert len(counts) == 5
    assert isinstance(counts[0], int)
    assert sum(counts[:4]) == counts[4]

def test_get_region_depth_0base(bam_file):
    """测试获取区域深度(0-based)"""
    bam = BAM(pysam.AlignmentFile(bam_file))
    depth, details = bam.get_region_depth("chr1", 100, 104)  # 0-based
    assert isinstance(depth, float)
    assert isinstance(details, list)
    assert len(details) == 4
    assert all(len(x) == 5 for x in details)

def test_get_region_depth_1base(bam_file):
    """测试获取区域深度(1-based)"""
    bam = BAM(pysam.AlignmentFile(bam_file))
    depth, details = bam.get_region_depth("chr1", 101, 105, base=1)  # 1-based
    assert isinstance(depth, float)
    assert isinstance(details, list)
    assert len(details) == 4
    assert all(len(x) == 5 for x in details)

def test_coordinate_conversion(bam_file):
    """测试0-based和1-based坐标是否返回相同结果"""
    bam = BAM(pysam.AlignmentFile(bam_file))
    counts_0base = bam.get_base_count_per_position("chr1", 100)  # 0-based
    counts_1base = bam.get_base_count_per_position("chr1", 101, base=1)  # 1-based
    assert counts_0base == counts_1base 