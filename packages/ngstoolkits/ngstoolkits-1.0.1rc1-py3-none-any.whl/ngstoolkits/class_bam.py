from typing import List, Tuple
import pysam

class BAM:
    """BAM文件处理类，提供对BAM文件的常用分析功能。
    
    Attributes:
        Bam (pysam.AlignmentFile): BAM文件对象
        
    Examples:
        >>> import pysam
        >>> bam = BAM(pysam.AlignmentFile("sample.bam"))
        >>> # 使用0-based坐标
        >>> counts = bam.get_base_count_per_position("chr1", 999)  # 获取chr1:1000位点信息
        >>> # 使用1-based坐标
        >>> counts = bam.get_base_count_per_position("chr1", 1000, base=1)  # 获取相同位点
    """
    
    def __init__(self, Bam: pysam.AlignmentFile) -> None:
        self.Bam = Bam
        
    def get_base_count_per_position(self, chr: str, pos: int, base: int = 0) -> List[int]:
        """获取指定位置的碱基计数。
        
        Args:
            chr: 染色体名称
            pos: 基因组位置
            base: 位置计数方式，0表示0-based(默认)，1表示1-based
            
        Returns:
            包含5个整数的列表 [A数量, C数量, G数量, T数量, 总数量]
            
        Examples:
            >>> # 0-based坐标
            >>> counts = bam.get_base_count_per_position("chr1", 999)  # chr1:1000
            >>> # 1-based坐标
            >>> counts = bam.get_base_count_per_position("chr1", 1000, base=1)  # chr1:1000
        """
        pos_0base = pos - base  # 转换为0-based坐标
        count = self.Bam.count_coverage(chr, pos_0base, pos_0base + 1, quality_threshold=0)
        return [count[0][0], count[1][0], count[2][0], count[3][0], 
                count[0][0]+count[1][0]+count[2][0]+count[3][0]]

    def get_region_depth(self, chr: str, start: int, end: int = 0, flank: int = 10, base: int = 0) -> Tuple[float, List[List[int]]]:
        """获取指定区域的平均深度和每个位置的碱基计数。
        
        Args:
            chr: 染色体名称
            start: 起始位置
            end: 终止位置，如果为0则使用start±flank
            flank: 当end为0时使用的侧翼长度
            base: 位置计数方式，0表示0-based(默认)，1表示1-based
            
        Returns:
            Tuple包含:
                - float: 区域平均深度
                - List[List[int]]: 每个位置的碱基计数列表
                
        Examples:
            >>> # 0-based坐标
            >>> depth, details = bam.get_region_depth("chr1", 999, 1999)  # chr1:1000-2000
            >>> # 1-based坐标
            >>> depth, details = bam.get_region_depth("chr1", 1000, 2000, base=1)  # chr1:1000-2000
        """
        # 转换为0-based坐标
        start_0base = start - base
        if end == 0:
            print(f"Warning: end is not set, use flank: {flank}")
            end_0base = start_0base + flank
            start_0base = start_0base - flank
        else:
            end_0base = end - base
            if start_0base > end_0base:
                print("Warning: start is larger than end, change start and end")
                start_0base, end_0base = end_0base, start_0base
            
        region_site_num = 0
        region_cover_base = 0
        region_detail = []
        
        for position in range(start_0base, end_0base):
            region_site_num += 1
            base_counts = self.get_base_count_per_position(chr, position, base=0)  # 已经是0-based了
            region_cover_base += base_counts[4]
            region_detail.append(base_counts)
            
        region_average_depth = region_cover_base / region_site_num
        return region_average_depth, region_detail
