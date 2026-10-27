"""Ablation: bm25 with the 12 lab's plain [a-z0-9]+ tokenizer instead of "codes".

The one change is the tokenizer; k1, b and chunking stay as in p2.toml. "codes" keeps section
numbers such as 1926.1053 whole, so this variant tests how much identifier queries lean on that.
"""

from p2.retrievers.bm25 import BM25

NEEDS_CLAUDE = False
BASE = "bm25"


def build(corpus, cfg):
    return BM25(corpus, cfg.replace(tokenizer="lab"))
