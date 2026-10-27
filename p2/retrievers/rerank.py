"""Listwise reranking: Claude reorders hybrid's top 20, as rerank_one() in the 13 lab.

The top 20 go to Claude as numbered passages, and the reply is forced into {"order": [20 numbers]},
each between 1 and 20. A reply that is not each number once keeps hybrid's order. The reranked
documents score 20, 19, ... so the run file keeps Claude's order; the rest of hybrid's list follows.
"""

from p2 import claude, retrievers

NEEDS_CLAUDE = True
FIRST_STAGE = "hybrid"
CANDIDATES = 20
PASSAGE_CHARS = 2000

PROMPT = """Below are {n} passages from the US federal regulations, numbered 1 to {n}, and a search query.
Order the passages from the most useful for answering the query to the least useful.
A passage is useful if it states the requirement the query asks about; one that only refers to it elsewhere is less useful.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


def schema(n):
    items = {"type": "integer", "minimum": 1, "maximum": n}
    return {"type": "object", "properties": {"order": {"type": "array", "items": items, "minItems": n, "maxItems": n}}, "required": ["order"]}


class Rerank:
    def __init__(self, corpus, cfg):
        self.cfg = cfg
        self.first = retrievers.build(FIRST_STAGE, corpus, cfg)
        self.doc_text = {d.docid: d.text for d in corpus.docs}
        self.chunk_text = {c.id: c.text for c in self.first.parts[0].chunks}

    def rerank(self, text, ranked, texts, k):
        candidates = [item for item, _ in ranked[:CANDIDATES]]
        n = len(candidates)
        passages = "\n\n".join(f"[{i}] {texts[c][:PASSAGE_CHARS]}" for i, c in enumerate(candidates, 1))
        reply = claude.call(PROMPT.format(n=n, query=text, passages=passages), schema(n), model=self.cfg.model, cache_dir=claude.cache_folder(self.cfg))
        got = (reply.output or {}).get("order")
        if isinstance(got, list) and sorted(got) == list(range(1, n + 1)):
            candidates = [candidates[i - 1] for i in got]
        rest = [item for item, _ in ranked[CANDIDATES:]]
        return [(item, float(len(candidates) + len(rest) - i)) for i, item in enumerate(candidates + rest)][:k]

    def search(self, text, k):
        return self.rerank(text, self.first.search(text, max(k, CANDIDATES)), self.doc_text, k)

    def search_chunks(self, text, k):
        return self.rerank(text, self.first.search_chunks(text, max(k, CANDIDATES)), self.chunk_text, k)


def build(corpus, cfg):
    return Rerank(corpus, cfg)
