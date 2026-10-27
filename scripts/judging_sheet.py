"""Write a judging sheet for the own gold set: for each query, the pooled candidates from several systems.

Usage: uv run python scripts/judging_sheet.py > ../p2-raw/judging.md
Candidates are the union of the top 10 of bm25, dense and hybrid, so the pool is not one system's view.
Each candidate shows its title, which systems found it, and its chunk that best matches the query
(hybrid's chunk ranking), so most decisions can be made from the sheet.
The sheet only finds candidates; the relevance decision is made by reading the document.
"""

from p2 import config, corpus, retrievers
from p2.runfile import read_queries

SYSTEMS = ("bm25", "dense", "hybrid")

cfg = config.load()
own = corpus.load(cfg.root, "own")
queries, _ = read_queries(cfg.root / "eval/own/queries.tsv", require_origin=True)
built = {name: retrievers.build(name, own, cfg) for name in SYSTEMS}

n_chunks = len(built["bm25"].chunks)
chunk_text = {c.id: c.text for c in built["bm25"].chunks}

for q in queries:
    best = {}
    for chunk_id, _ in built["hybrid"].search_chunks(q.text, n_chunks):
        best.setdefault(corpus.docid_of(chunk_id), chunk_id)
    found = {}
    for name, system in built.items():
        for rank, (docid, _) in enumerate(system.search(q.text, 10), 1):
            found.setdefault(docid, []).append(f"{name}#{rank}")
    print(f"\n## {q.qid} ({q.cls}, {q.origin}): {q.text}\n")
    for docid, hits in sorted(found.items(), key=lambda kv: -len(kv[1])):
        body = " ".join(chunk_text[best[docid]].split()[:90])
        print(f"- [ ] `{docid}` {own.docs[docid].title} ({', '.join(hits)}; best chunk {best[docid]})\n      {body}...")
