# -*- coding: utf-8 -*-

"""Top-level package for hypothesis-bio."""

__author__ = "Benjamin D. Lee"
__email__ = "benjamindlee@me.com"

MAX_ASCII = 126

from .__version__ import __version__
from .blast6 import *
from .fasta import *
from .fastq import *
from .sequence_identifiers import *
from .sequences import *
from .gff import *
