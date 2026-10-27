"""Dense retrieval: embed every chunk once, embed the query, rank chunks by cosine similarity.

The embedder is bge-small-en-v1.5 by default (the stronger of the two the 12 lab measured);
set [dense] model = "..." in p2.toml to try another. Vectors are unit length, so a dot product is the cosine.
"""

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        self.model = cfg.table("dense").get("model", embed.BGE)
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)

    def score_chunks(self, text):
        return self.vectors @ self.embedder.encode([text])[0]


def build(corpus, cfg):
    return Dense(corpus, cfg)
