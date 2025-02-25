import pysam
from collections import namedtuple
from functools import lru_cache
from enum import Enum,unique
import warnings
from .config import config

class CPRA():
    """
    descriptrion a mutation in cpra( eg: chr1, 100, A, T)
    and get some useful information with Bam or reference genome:
    """
    reference=None
    bam=None
    @classmethod
    def loadReference(cls,reference=None):
        """
        load reference genome
        param reference FilePath: eg: d:\Git_Repo\package_ngstools\data\hg19.fa
        """
        ref_path = reference or config.reference
        if ref_path is None:
            raise ValueError("No reference genome specified. Please either provide a path or set it in config.")
            
        if cls.reference is None:
            cls.reference = pysam.FastaFile(ref_path)
        else:
            cls.reference = pysam.FastaFile(ref_path)
            print("reference has been loaded & reloaded")

    @classmethod
    def loadBam(cls,Bam=None):
        """
        load bam file
        param Bam FilePath : eg: d:\Git_Repo\package_ngstools\data\test.bam
        """
        bam_path = Bam or config.bam
        if bam_path is None:
            raise ValueError("No BAM file specified. Please either provide a path or set it in config.")
            
        cls.bam = pysam.AlignmentFile(bam_path)

    def __init__(self,CHROM:str,POS:int,REF:str,ALT:str,base:int=1):
        """
        Init a mutation object,
        param chrom(str): eg: chr1
        param pos(int): eg: 100
        param REF(str):表示参考序列的字符串 eg: A
        param ALT(str):表示替代序列的字符串。 eg: T
        param base: 位置计数方式，0表示0-based，1表示1-based(默认)
        """
        self.chrom = CHROM
        self._pos_1base = POS + (1 - base)  # 转换为1-based并保存
        self.pos = self._pos_1base  # 对外接口保持1-based
        self.pos_fit = self._pos_1base  # 对外接口保持1-based
        self.ref = REF
        self.alt = ALT
        self._base = base  # 保存用户选择的坐标系统

        if not self._is_valid_nucleotide_sequence(REF):
            warnings.warn(f"Invalid REF sequence '{REF}'; using empty string instead.")
            self.ref = ""

        if not self._is_valid_nucleotide_sequence(ALT):
            warnings.warn(f"Invalid ALT sequence '{ALT}'; using empty string instead.")
            self.alt = ""
        if hasattr(self,'bam'):
            self.get_suppot()

    @staticmethod
    def _is_valid_nucleotide_sequence(sequence: str) -> bool:
        valid_nucleotides = set('ATCGatcg')
        return all(nucleotide in valid_nucleotides for nucleotide in sequence)

    def _get_pos_in_base(self, base: int = None) -> int:
        """获取指定坐标系统下的位置。
        
        Args:
            base: 目标坐标系统，0表示0-based，1表示1-based
                 如果为None，则使用初始化时的坐标系统
        
        Returns:
            int: 转换后的位置
        """
        if base is None:
            base = self._base
        return self._pos_1base - (1 - base)

    @property
    def pos_0based(self) -> int:
        """获取0-based位置"""
        return self._get_pos_in_base(0)

    @property
    def pos_1based(self) -> int:
        """获取1-based位置"""
        return self._get_pos_in_base(1)

    def _is_valid_ref_sequence(self)->int:
        try:
            pos_0based = self.pos_0based
            if self.reference.fetch(self.chrom, pos_0based, pos_0based + len(self.ref)) == self.ref:
                return 0
            elif self.reference.fetch(self.chrom, pos_0based + 1, pos_0based + 1 + len(self.ref))== self.ref:
                return 1
            else:
                raise ValueError("ref sequence do not match with the genome file, check your data")
        except AttributeError as e:
            raise e.add_note("reference genome is not set, set it with cpra.loadReference(referencePath)")

    @property
    def info(self):
        """
        return the information of the mutation
        """
        if hasattr(self,'_support_readsID_list'):
            return f"{self.chrom}\t{self.pos}\t{self.ref}\t{self.alt}\t{self.muttype}\t{self.supportReadNum}\t{self.CoverReadNum}\t{self.ratio}"
        else:
            return f"{self.chrom}\t{self.pos}\t{self.ref}\t{self.alt}\t*\t*\t*\t*"

    @property
    def muttype(self):
        if len(self.ref)>len(self.alt):
            return "DEL"
        elif len(self.ref)<len(self.alt):
            return "INS"
        else:
            return "SNV"

    @property
    def flank10(self, length:int=10) -> str:
        '''获取变异的侧翼10bp序列
        使用前需要通过loadReference(reference) 完成参考基因组的加载
        param length: 侧翼序列长度
        '''
        lbase = self.reference.fetch(self.chrom, self.pos-length,self.pos)
        rbase = self.reference.fetch(self.chrom, self.pos+len(self.ref), self.pos+len(self.ref)+length)
        return '..'.join((lbase, rbase))

    @property
    def CoverReadList(self):
        if hasattr(self,'_cover_readsID_list'):
            return self._cover_readsID_list
        else :
            self.get_suppot()
            return self._cover_readsID_list
    @property
    def CoverReadNum(self):
        return len(self.CoverReadList)

    @property
    def supportReads(self):
        if hasattr(self,'_support_reads'):
            return self._support_reads
        else :
            self.get_suppot()
            return self._support_reads
    def plot_support(self, savepath):
        """
        plot the support for the mutation
        param savepath: eg: d:\Git_Repo\package_ngstools\data\test.png
        """
        import matplotlib.pyplot as plt
        plot_y_range=len(self.supportReads)
        plt.figure(figsize=(410 / 96, plot_y_range / 96))  # 单位英寸，注意DPI转换

        for pos in range(52524252, 52524252 + 1):
            plt.axvline(x=self.pos, color="#ffb6c1", linewidth=2.8) # 标注关注的突变起始位置
            plt.axvline(x=self.pos+len(self.ref), color="#ffb6c1", linewidth=2.8) # 标注关注的突变终止位置
        plot_Read_index=0
        for aln in self.supportReads:
            plot_Read_index+=1
            plt.text(aln.reference_start,plot_Read_index, aln.query_sequence, fontsize=8)

        # 由于Python中没有直接对应于R的scale_colour_manual的简单转换，
        # 这里不直接展示图例设置，但可以通过plt.legend手动设置

        # 设置标题、坐标轴标签等
        plt.title(self.chrom+":"+str(self.pos)+"-"+self.ref+">"+self.alt, fontsize=20)
        plt.xlabel(None)  # 不显示x轴标签
        plt.ylabel("reads")
        plt.xlim(pos-200, pos + 200)
        plt.ylim(0,plot_y_range)
        plt.savefig(savepath)
        # 显示图形
        plt.show()

    @property
    def supportreadsIDlist(self):
        if hasattr(self,'_support_readsID_list'):
            return self._support_readsID_list
        else :
            self.get_suppot()
            return self._support_readsID_list

    @property
    def supportReadNum(self):
        return len(self.supportreadsIDlist)

    @property
    def ratio(self):
        return self.supportReadNum/self.CoverReadNum

    def flank(self, length:int):
        '''获取变异的任意长度侧翼序列
        使用前需要通过loadReference(reference) 完成参考基因组的加载
        param length: 侧翼序列长度
        '''
        lbase = self.reference.fetch(self.chrom, self.pos-length,self.pos)
        rbase = self.reference.fetch(self.chrom, self.pos+len(self.ref), self.pos+len(self.ref)+length)
        return '..'.join((lbase, rbase))

    def get_suppot(self,bam="",ref="",coverflank=5):
        """
        get support for the mutation with special Bam File &ref;
        param coverflank: only the reads cover the ±coverflank(5) bases will be considered
        get property: support_reads,support_readsID_list,cover_readsID_list
        """
        if(self.bam is None):
            if(bam is not None):
                self.loadBam(bam)
            else:
                raise ValueError("bam file is not set, set it with cpra.loadBam(bamPath)")
        if(self.reference is None):
            if(ref is not None):
                self.loadReference(ref)
            else:
                raise ValueError("reference genome is not set, set it with cpra.loadReference(referencePath)")
        self.pos_fit = self.pos+ self._is_valid_ref_sequence()
        self._support_reads = []
        self._support_readsID_list = []
        self._cover_readsID_list = []
        if self.muttype == "SNV":
            self._support_reads,self._support_readsID_list,self._cover_readsID_list = self._get_snv_support_reads(coverflank)
        elif self.muttype == "INS":
            self._support_reads,self._support_readsID_list,self._cover_readsID_list = self._get_ins_support_reads(coverflank)
        elif self.muttype == "DEL":
            self._support_reads,self._support_readsID_list,self._cover_readsID_list = self._get_del_support_reads(coverflank)

    @lru_cache
    def _get_snv_support_reads(self, coverflank=5, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
        Read = namedtuple('Read', ['read_name', 'pair', 'strand'])
        support_reads = []
        cover_reads = []
        start_reads = {}
        EndSite = self.pos_fit + len(self.ref)
        for pileup_column in self.bam.pileup(region=str(self.chrom) + ':' + str(self.pos_fit) + '-' + str(self.pos_fit),mapq=mapq , baseq = baseq,
                                            stepper=stepper, fastaFile=self.reference, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    read_name = aln.query_name
                    pair = 'pe1' if aln.is_read1 else 'pe2'
                    strand = '-' if aln.is_reverse else '+'
                    read = Read(read_name, pair, strand)
                    if pileup_read.is_del or pileup_read.is_refskip or (aln.flag > 1024) or (aln.mapping_quality < mapq) or \
                            aln.query_qualities[pileup_read.query_position] < baseq:
                        continue
                    start_reads[read] = [pileup_read.query_position, aln]
        for pileup_column in self.bam.pileup(region=str(self.chrom) + ':' + str(EndSite) + '-' + str(EndSite),
                                            stepper=stepper, fastaFile=self.reference, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    read_name = aln.query_name
                    pair = 'pe1' if aln.is_read1 else 'pe2'
                    strand = '-' if aln.is_reverse else '+'
                    read = Read(read_name, pair, strand)
                    if pileup_read.is_del or pileup_read.is_refskip:
                        continue
                    if read in start_reads:
                        start_query_position, start_aln = start_reads[read]
                        seq = start_aln.query_sequence[start_query_position:pileup_read.query_position]
                        cover_reads.append(aln)
                        if seq.upper() == self.alt.upper():
                            support_reads.append(aln)
        support_readIDs = []
        cover_readID_list = []
        for aln in cover_reads:
            cover_readID_list.append(aln.query_name)
        for aln in support_reads:
            support_readIDs.append(aln.query_name)
        return [support_reads,support_readIDs,cover_readID_list]

    @lru_cache
    def _get_ins_support_reads(self, coverflank=5, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
        support_reads = []
        cover_reads = []
        bam = {}
        EndSite = self.pos_fit + len(self.ref)
        CoverStart = self.pos_fit-coverflank
        CoverEnd = EndSite + coverflank
        insLength=len(self.alt)-len(self.ref)
        for pileup_column in self.bam.pileup(region=str(self.chrom) + ':' + str(self.pos_fit) + '-' + str(self.pos_fit), mapq=mapq, baseq=baseq, stepper=stepper, fastaFile=self.reference, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    bam[aln.query_name] = pileup_read
                    if (CoverStart in aln.positions) and (CoverEnd in aln.positions):
                        cover_reads.append(aln)
                        if pileup_read.query_position and aln.cigarstring.find("I") > 0:
                            start = pileup_read.query_position-1
                            altstop = pileup_read.query_position - 1 +len(self.alt)
                            refstop = pileup_read.query_position-1 + len(self.ref)
                            if aln.query_sequence[start:altstop].upper() == self.alt.upper() and \
                                    aln.get_reference_sequence()[start:refstop].upper() == self.ref.upper():
                                support_reads.append(aln)
                            elif aln.query_sequence[pileup_read.query_position-insLength:pileup_read.query_position -insLength+ len(self.alt)].upper() == self.alt.upper() and \
                                aln.get_reference_sequence()[pileup_read.query_position-insLength:pileup_read.query_position - insLength + len(self.ref)].upper() == self.ref.upper():
                                support_reads.append(aln)
                            elif aln.query_sequence[pileup_read.query_position:pileup_read.query_position + len(self.alt)].upper() == self.alt.upper() and \
                                aln.get_reference_sequence()[pileup_read.query_position:pileup_read.query_position + len(self.ref)].upper() == self.ref.upper():
                                support_reads.append(aln)
        support_readID_list = []
        cover_readID_list = []
        for aln in cover_reads:
            cover_readID_list.append(aln.query_name)
        for aln in support_reads:
            support_readID_list.append(aln.query_name)
        return [support_reads,support_readID_list,cover_readID_list]

    @lru_cache
    def _get_del_support_reads(self, coverflank=5, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
        support_reads = []
        cover_reads = []
        bam = {}
        EndSite = self.pos_fit + len(self.ref)
        CoverStart = self.pos_fit-coverflank
        CoverEnd = EndSite + coverflank
        for pileup_column in self.bam.pileup(region=str(self.chrom) + ':' + str(self.pos_fit) + '-' + str(EndSite), mapq=mapq , baseq = baseq,
                                            stepper=stepper, fastaFile=self.reference, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    bam[aln.query_name]=pileup_read
                    if (CoverStart in aln.positions) and (CoverEnd in aln.positions):
                        cover_reads.append(aln)
                        if pileup_read.query_position_or_next and aln.cigarstring.find("D") > 0:
                            start = pileup_read.query_position_or_next - 1
                            refstop = pileup_read.query_position_or_next + len(self.ref) - 1
                            altstop = pileup_read.query_position_or_next +len(self.alt) -1
                            if aln.get_reference_sequence()[start:refstop].upper() == self.ref.upper() and aln.query_sequence[start:altstop].upper() == self.alt.upper():
                                support_reads.append(aln)
                            elif aln.get_reference_sequence()[start+1:refstop+1].upper() == self.ref.upper() and aln.query_sequence[start+1:altstop+1].upper() == self.alt.upper():
                                support_reads.append(aln)
        support_readsID_list = []
        cover_readID_list = []
        for aln in cover_reads:
            cover_readID_list.append(aln.query_name)
        for aln in support_reads:
            support_readsID_list.append(aln.query_name)
        return [support_reads,support_readsID_list,cover_readID_list]

