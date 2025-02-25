import sys
import os
from .cpra import CPRA
from .sequence import SeqFunction
from .class_bam import BAM
from .Fasta import FASTA
__version__ = "1.0.1rc1"

# 指定from ngstoolkits import * 时导入的内容
__all__ = ["CPRA", "SeqFunction", "BAM", "FASTA"]

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover
