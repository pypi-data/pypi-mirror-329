import pytest
import pysam
from ngstoolkits import FASTA

@pytest.fixture
def fasta_file(tmp_path):
    """创建测试用的FASTA文件"""
    fasta_path = tmp_path / "test.fa"
    with open(fasta_path, "w") as f:
        f.write(">chr1\n")
        f.write("ATGCATGCATGC\n")
    pysam.faidx(str(fasta_path))
    return str(fasta_path)

def test_fasta_coordinate_systems(fasta_file):
    """测试FASTA类的坐标系统"""
    # 1-based坐标
    fa1 = FASTA(fasta_file, base=1)
    gc1 = fa1.gc_rate_special_region("chr1", 1, 4)
    
    # 0-based坐标
    fa0 = FASTA(fasta_file, base=0)
    gc0 = fa0.gc_rate_special_region("chr1", 0, 3)
    
    # 两种方式应该得到相同结果
    assert gc1 == gc0 