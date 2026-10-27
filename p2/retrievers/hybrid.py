"""Hybrid retrieval: reciprocal rank fusion (k = 60) of bm25 and dense, as rrf() in the 13 lab.

Each document scores the sum of 1 / (60 + rank) over the two full rankings, so a document that is
11th in both can still reach the fused top 10. search_chunks does the same over chunk rankings.
"""

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False
RRF_K = 60
PARTS = ("bm25", "dense")


def rrf(rankings, k=RRF_K):
    scores = {}
    for ranking in rankings:
        for rank, (item, _) in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1 / (k + rank)
    return order(scores.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        self.parts = [retrievers.build(name, corpus, cfg) for name in PARTS]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(self.parts[0].chunks)

    def search(self, text, k):
        return rrf([p.search(text, self.n_docs) for p in self.parts])[:k]

    def search_chunks(self, text, k):
        return rrf([p.search_chunks(text, self.n_chunks) for p in self.parts])[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
