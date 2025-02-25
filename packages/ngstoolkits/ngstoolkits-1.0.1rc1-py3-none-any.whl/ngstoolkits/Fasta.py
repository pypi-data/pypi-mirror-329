from typing import Union, Optional
import pysam
from .sequence import SeqFunction
from .config import config

class FASTA:
    """FASTA文件处理类。
    
    提供对FASTA文件的常用操作功能。
    
    Attributes:
        reference (pysam.FastaFile): FASTA文件对象
        
    Examples:
        >>> # 使用1-based坐标
        >>> fa = FASTA("reference.fa", base=1)
        >>> gc = fa.gc_rate_special_region("chr1", 1000, 2000)
        >>> # 使用0-based坐标
        >>> fa = FASTA("reference.fa", base=0)
        >>> gc = fa.gc_rate_special_region("chr1", 999, 1999)
    """
    
    def __init__(self, fasta: Optional[str] = None, base: int = 1):
        """初始化FASTA对象。
        
        Args:
            fasta: FASTA文件路径，如果为None则使用配置值
            base: 位置计数方式，0表示0-based，1表示1-based(默认)
        """
        fasta_path = fasta or config.reference
        if fasta_path is None:
            raise ValueError("No FASTA file specified. Please either provide a path or set it in config.")
            
        self.reference = pysam.FastaFile(fasta_path)
        self._base = base

    def _get_pos_in_0base(self, pos: int) -> int:
        """转换位置为0-based。"""
        return pos - self._base

    def gc_rate_special_region(self, chrom: str, start: int, end: int) -> float:
        """计算特定区域的GC含量。
        
        Args:
            chrom: 染色体名称
            start: 起始位置
            end: 终止位置
            
        Returns:
            float: GC含量(0-1之间的浮点数)
            
        Examples:
            >>> # 1-based坐标
            >>> gc = fa.gc_rate_special_region("chr1", 1000, 2000)
            >>> # 0-based坐标
            >>> gc = fa.gc_rate_special_region("chr1", 999, 1999)
        """
        start_0base = self._get_pos_in_0base(start)
        end_0base = self._get_pos_in_0base(end)
        seq = self.reference.fetch(chrom, start_0base, end_0base)
        return SeqFunction.GC_content(seq)
