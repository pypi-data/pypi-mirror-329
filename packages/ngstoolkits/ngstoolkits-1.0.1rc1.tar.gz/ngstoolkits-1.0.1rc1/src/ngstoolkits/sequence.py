from typing import List

class SeqFunction:
    """序列处理相关的静态方法集合。
    
    提供DNA序列的基本操作功能，如反向互补、GC含量计算等。
    
    Examples:
        >>> SeqFunction.reverse_complement("ATGC")
        'GCAT'
        >>> SeqFunction.GC_content("ATGC")
        0.5
    """
    
    @staticmethod
    def base_count(seq: str) -> List[int]:
        """计算序列中各碱基的数量。
        
        Args:
            seq: DNA序列字符串
            
        Returns:
            包含4个整数的列表 [A数量, C数量, G数量, T数量]
            
        Examples:
            >>> SeqFunction.base_count("ATGC")
            [1, 1, 1, 1]
        """
        seq = seq.upper()
        counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0, 'N': 0}
        for nucleotide in seq:
            if nucleotide in counts:
                counts[nucleotide] += 1
        # 返回计数结果组成的列表
        base_list=[counts['A'], counts['C'], counts['G'], counts['T']]
        #return max(base_list)/(sum(base_list)+0.00001)
        return base_list

    @staticmethod
    def reverse_complement(seq: str) -> str:
        """获取序列的反向互补序列。
        
        Args:
            seq: DNA序列字符串
            
        Returns:
            反向互补序列
            
        Examples:
            >>> SeqFunction.reverse_complement("ATGC")
            'GCAT'
        """
        seq = seq[::-1].upper()
        return seq.replace('A', 't').\
                    replace('C', 'g').\
                    replace('T', 'a').\
                    replace('G', 'c').upper()
    @staticmethod
    def GC_content(seq: str) -> float:
        """计算序列的GC含量。
        
        Args:
            seq: DNA序列字符串
            
        Returns:
            GC含量(0-1之间的浮点数)
            
        Examples:
            >>> SeqFunction.GC_content("ATGC")
            0.5
        """
        seq = seq.upper()
        return (seq.count('G') + seq.count('C')) / len(seq)
    @staticmethod
    def GC_skew(seq):
        """
        param DNA sequence: eg ATAG
        return GC skew : 0.5
        method : (G-C)/(G+C)
        """
        return (seq.count('G') - seq.count('C')) /  (seq.count('G') + seq.count('C'))



acid_info = {
    'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D',
    'Cys': 'C', 'Gln': 'Q', 'Glu': 'E', 'Gly': 'G',
    'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K',
    'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'Ser': 'S',
    'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V',
    'Ter': '*'
}
#@function_timer
def get_oneletter_hgvsp(hgvsp):
    '''获取单字母的hgvsp结果
    '''
    for acid in acid_info:
        if acid in hgvsp:
            hgvsp = hgvsp.replace(acid, acid_info[acid])
    return hgvsp
