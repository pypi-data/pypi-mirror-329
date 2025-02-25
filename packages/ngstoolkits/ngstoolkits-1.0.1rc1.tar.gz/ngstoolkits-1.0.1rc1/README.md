<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/ngstools.svg?branch=main)](https://cirrus-ci.com/github/<USER>/ngstools)
[![ReadTheDocs](https://readthedocs.org/projects/ngstools/badge/?version=latest)](https://ngstools.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/ngstools/main.svg)](https://coveralls.io/r/<USER>/ngstools)
[![PyPI-Server](https://img.shields.io/pypi/v/ngstools.svg)](https://pypi.org/project/ngstools/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/ngstools.svg)](https://anaconda.org/conda-forge/ngstools)
[![Monthly Downloads](https://pepy.tech/badge/ngstools/month)](https://pepy.tech/project/ngstools)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/ngstools)
-->

Author : Liubo <[Ben-unbelieveable](git@github.com:Ben-unbelieveable/package_ngstoolkits.git)>
# ngstoolkits

> NGS(下一代测序)数据分析工具包

## 主要功能类

### CPRA
用于表示和分析变异位点的类。支持加载参考基因组和BAM文件进行深入分析。

```python
from ngstoolkits import CPRA

# 初始化变异对象
mut = CPRA("chr6", 159188398, "C", "T")

# 加载必要文件
CPRA.loadBam("sample.bam")
CPRA.loadReference("reference.fa")

# 获取变异支持信息
mut.get_suppot()

# 访问分析结果
print(mut.supportReadNum)  # 支持该变异的reads数量
print(mut.CoverReadNum)    # 覆盖该位点的总reads数量
print(mut.ratio)           # 变异频率
```

### BAM
用于处理BAM文件的工具类。

```python
from ngstoolkits import BAM
import pysam

bam = BAM(pysam.AlignmentFile("sample.bam"))

# 获取特定位点的碱基统计
counts = bam.get_base_count_per_position("chr1", 1000)
print(counts)  # 返回 [A数量, C数量, G数量, T数量, 总数量]

# 获取区域平均深度
depth, details = bam.get_region_depth("chr1", 1000, 2000)
```

### SeqFunction
提供序列处理的静态方法。

```python
from ngstoolkits import SeqFunction

# 获取反向互补序列
rev_comp = SeqFunction.reverse_complement("ATGC")  # 返回 "GCAT"

# 计算GC含量
gc = SeqFunction.GC_content("ATGC")  # 返回 0.5
```

### FASTA
用于处理FASTA文件的工具类。

```python
from ngstoolkits import FASTA

fa = FASTA("reference.fa")
gc_rate = fa.gc_rate_special_region("chr1", 1000, 2000)
```

## 安装

```bash
pip install ngstoolkits
```

## 依赖

- Python >= 3.8
- pysam

## 许可证

MIT License

