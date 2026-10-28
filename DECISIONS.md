# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

I selected OSHA's Safety and Health Regulations for Construction (29 CFR 1926), extracted from the official eCFR XML. Construction safety is a high-stakes, heavily regulated domain where finding the operative standard quickly and accurately directly prevents jobsite injuries and regulatory citations. The corpus comprises 307 documents that average 1,185 words—roughly seven times longer than the shared mine safety corpus (158 words)—with numerous interrelated subparts covering fall protection, scaffolding, excavation, electrical wiring, and toxic substances.

Before measuring, I expected `rerank` to win by a substantial margin. Construction regulations feature repetitive structural layouts with frequent look-alike provisions (e.g., general fall protection under 1926.501 vs. steel erection fall protection under 1926.760 vs. scaffolding fall protection under 1926.451). First-stage retrievers surface all of these based on shared vocabulary, but an LLM reranker inspecting all 20 candidates simultaneously has the context needed to distinguish the exact operative rule from definitions and exceptions. I expected `dense` to struggle on identifier queries because splitting citation numbers (e.g., 1926.1053) dilutes lexical exact matches, and `bm25` to struggle on conversational paraphrases due to vocabulary mismatch. I anticipated `hybrid` would fall between them, though with RRF its gains might be muted whenever one retriever ranked irrelevant sections near the top.

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

A key design choice was the BM25 tokenizer: `codes` versus the baseline `lab` tokenizer. In `p2.toml`, I selected `tokenizer = "codes"`, which preserves dotted citations, table identifiers, and hyphenated terms (e.g., `1926.1053`, `Table 1`, `part02`) as unified tokens while also indexing their constituent alphanumeric parts. The alternative was the simpler `[a-z0-9]+` regex tokenizer from lab 12 (`tokenizer = "lab"`), which splits every citation into generic numbers and words.

I measured both on the own gold set (32 judged queries). The default `bm25` (`codes`) achieved an MRR@10 of 0.624 and nDCG@10 of 0.682, whereas `bm25_lab` achieved an MRR@10 of 0.601 and nDCG@10 of 0.664 (a difference of -0.023 MRR@10 [-0.062, +0.000] and -0.018 nDCG@10 [-0.047, +0.000]). As shown in the `own-ablation-queries` table, the `codes` tokenizer protected reciprocal rank on identifier queries such as `c01` (1926.1053 portable ladders, RR dropped from 1.000 to 0.500 under `bm25_lab`) and `c07` (1926.1408 Table A, RR dropped from 0.500 to 0.250). What was given up by not choosing the simpler lab tokenizer was a slightly larger term dictionary and a custom tokenization pattern, but keeping codes whole is essential for legal and regulatory texts.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

When constructing the relevance judgments for hand-written query `h06` ("How do you store and move dynamite on a construction site?"), the pooled candidate sheet generated by `scripts/judging_sheet.py` contained 20 candidates from BM25, dense, and hybrid, but completely missed the two operative sections in Subpart U: `1926.904` (Storage of explosives and blasting agents) and `1926.902` (Surface transportation of explosives). The pool's top candidates were general underground construction (`1926.800`) and loading of explosives (`1926.905`).

I noticed this omission because the word "dynamite" is a common industry synonym that does not appear verbatim in the section titles of Subpart U (which use "explosives and blasting agents"). By checking `subparts.md` for Subpart U (Blasting and the Use of Explosives, 1926.900–1926.914) and searching the corpus text directly, I discovered § 1926.904 (mandating BATF-approved magazines for storage) and § 1926.902 (mandating DOT-compliant vehicles for surface transit). Instead of accepting the retrieval pool's candidates or marking the query unanswerable, I overruled the pool, read both sections, and explicitly added `1926.904` and `1926.902` as relevant documents in `eval/own/qrels.txt` and `p2-raw/judging.md`.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

I do not fully trust the 100% verified citation rate reported in Section 2 on the shared answers (`8 of 8 verified (100%) [0.676, 1.000]` on in-corpus questions, and `4 of 4 declined (100%) [0.510, 1.000]`). 

While 100% sounds flawless, with only 8 in-corpus and 4 out-of-corpus questions the 95% Wilson confidence intervals are very wide—a true reliability as low as 68% for answering or 51% for declining falls within the 95% interval. Furthermore, `p2 verify` only checks mechanical substring presence in the retrieved chunk; it does not verify semantic correctness or whether the cited sentence truly supports the assertion made in the generated answer. To trust this number, I would need a benchmark of at least 50–100 questions evaluated with claim-level human verification. To test it locally, I audited three answers (`a01`, `a02`, `a03`) by reading the cited chunks against the claims. While those three claims were indeed supported, relying on an automated 8-question substring check as proof of system faithfulness is unwarranted.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

In the own corpus, Subpart Y (Commercial Diving Operations, `1926.1071` through `1926.1091`) and Hazard Communication (`1926.59`) consist solely of short "incorporation by reference" notes stating that construction requirements are identical to general industry standards in 29 CFR 1910 (e.g., § 1910.424 for SCUBA and § 1910.1200 for HazCom). For query `c15` ("What should a worker carry or wear when diving underwater on a job?") and `h08` ("Hazard communication safety data sheets for chemicals on site"), the substantive regulatory text does not exist inside Part 1926. 

Anyone inspecting `corpora/own/docs/1926.1084.md` can see that the file is only four lines long. Consequently, first-stage keyword and dense retrievers struggle to match detailed queries against these placeholder sections, and answers cannot cite operative details. Next, I would enhance the corpus ingestion pipeline (`scripts/ecfr_to_md.py`) to resolve and inline cross-referenced 1910 subparts when a 1926 section is merely a stub note, and evaluate whether that lifts first-stage recall on queries `c15` and `h08`.
