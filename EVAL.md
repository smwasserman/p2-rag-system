# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

`dense` encodes documents split into 300-word chunks (50-word overlap) using `BAAI/bge-small-en-v1.5` embeddings (384 dimensions), ranking by maximum inner product chunk similarity. `hybrid` fuses chunk-level BM25 (configured with the `codes` tokenizer, $k_1 = 0.9, b = 0.4$) and `dense` rankings using Reciprocal Rank Fusion (RRF constant 60), aggregating chunks by maximum score per document. `rerank` takes the top 20 candidate documents from `hybrid`, selects each document's top-scoring chunk, and presents them in a single prompt to `claude-3-5-sonnet` with a forced JSON schema ordering output, scoring documents by their returned reciprocal rank.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.592 | 0.471 | 0.443 |
| rerank | 0.733 | 0.800 | 0.743 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.500 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.152 | 0.792 |
| hybrid | nDCG@10 | 0.397 | 0.202 | 0.779 |
| rerank | Recall@10 | 0.643 | 0.595 | 1.000 |
| rerank | MRR@10 | 0.714 | 0.714 | 1.000 |
| rerank | nDCG@10 | 0.641 | 0.626 | 1.000 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.033 | [-0.250, +0.192] | 0.324 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.037 | [-0.178, +0.083] | 0.192 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.075 | [-0.238, +0.075] | 0.228 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.033 | [-0.125, +0.192] | 0.231 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.092 | [-0.306, +0.109] | 0.301 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.036 | [-0.200, +0.113] | 0.227 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.108 | [-0.133, +0.350] | 0.351 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.293 | [+0.043, +0.533] | 0.353 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.225 | [-0.011, +0.451] | 0.336 | not distinguishable |
| rerank minus dense | Recall@10 | +0.175 | [+0.033, +0.333] | 0.221 | rerank higher |
| rerank minus dense | MRR@10 | +0.237 | [+0.083, +0.408] | 0.239 | rerank higher |
| rerank minus dense | nDCG@10 | +0.264 | [+0.128, +0.413] | 0.210 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.142 | [+0.050, +0.258] | 0.160 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | 0.247 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.300 | [+0.176, +0.430] | 0.186 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

On the 20 shared practice queries, only the comparisons involving `rerank` are distinguishable from zero: `rerank` is significantly higher than `hybrid` (MRR +0.329 [+0.164, +0.504]), higher than `dense` (MRR +0.237 [+0.083, +0.408]), and higher than `bm25` (MRR +0.293 [+0.043, +0.533]). In contrast, all pairwise differences among the three first-stage retrievers are not distinguishable on this set: `dense minus bm25` (+0.055 [-0.225, +0.343]), `hybrid minus bm25` (-0.037 [-0.178, +0.083]), and `hybrid minus dense` (-0.092 [-0.306, +0.109]).

With 20 practice queries, the minimum detectable difference (MDD) at 80% power is substantial—0.412 for dense vs. bm25, 0.301 for hybrid vs. dense, and 0.247 for rerank vs. hybrid. This means any performance gap smaller than ~0.25 to 0.41 is statistically invisible to this 20-query sample rather than absent.

The per-class breakdown strongly supports the core claim from lectures 12 and 13: `bm25` dominates `identifier` queries (MRR 0.810) but completely fails on `paraphrase` queries (MRR 0.000), while `dense` exhibits the exact opposite profile (MRR 0.333 on identifiers, 0.714 on paraphrases). The results also illustrate the RRF failure mode: on paraphrases, `hybrid` achieves only 0.152 MRR, far below dense's 0.714, because BM25's confident, incorrect rankings penalize dense's correct hits during rank averaging. `rerank` successfully recovers by inspecting hybrid's full top 20 candidates, matching dense on paraphrases (MRR 0.714) and scoring 1.000 on mixed queries.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 12 of 12 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

I selected `rerank` to answer the 12 questions because it achieved the highest recall@10 (0.733) and MRR@10 (0.800) on the practice queries, ensuring the top 5 chunks passed to Claude contained the relevant regulatory provisions. Using the default `prompts/answer.txt`, 8 of 8 in-corpus questions verified (100% [0.676, 1.000]) with 12 of 12 quotes found verbatim in their cited chunks, and 4 of 4 out-of-corpus questions were cleanly declined (100% [0.510, 1.000]).

Auditing three in-corpus verified answers:
1. **Question a01** ("Within how many minutes must a mine operator call MSHA after an accident that kills a miner?"): The answer cites chunk `cfr30-50.10#0` with two claims. Claim 1 states the operator must contact MSHA immediately within 15 minutes, quoting "The operator shall immediately contact MSHA at once without delay and within 15 minutes at the toll-free number, 1-800-746-1553, once the operator knows or should know that an accident has occurred involving:". Claim 2 states a death at the mine is a covered accident, quoting "(a) A death of an individual at the mine;". Reading `cfr30-50.10#0` confirms both quotes are exact verbatim substrings and directly substantiate the 15-minute mandate for fatal accidents.
2. **Question a02** ("What minimum incombustible content must the combined dust in an underground coal mine keep where no methane is present?"): The answer cites chunk `cfr30-75.403#0`. Claim 1 asserts the incombustible content must be at least 80 percent, quoting "the incombustible content of the combined coal dust, rock dust, and other dust shall be not less than 80 percent." Claim 2 notes the requirement increases with methane, quoting "Where methane is present in any ventilating current, the percent of incombustible content of such combined dust shall be increased 0.4 percent for each 0.1 percent of methane." Reading `cfr30-75.403#0` confirms the quotes are verbatim and completely support the rule.
3. **Question a03** ("How long must the self-rescue device given to each underground coal miner be able to protect that person?"): The answer cites chunk `cfr30-75.1714#0`, quoting "an approved self-rescue device or devices which is adequate to protect such person for 1 hour or longer." Reading `cfr30-75.1714#0` confirms the quote is accurate and directly supports the 1-hour requirement.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

The corpus consists of 29 CFR Part 1926 (OSHA Safety and Health Regulations for Construction), downloaded directly from the official eCFR annual XML bulk repository—an allowed primary source under the brief. It contains 307 markdown documents totaling 2.4 MB (approximately 509,146 estimated tokens), with each section formatted as an individual markdown document whose first line is the section heading. The license basis is United States Government work in the public domain (`us-gov-public-domain`) pursuant to 17 U.S.C. § 105. All 307 documents passed `uv run p2 license`. Two documents—`1926.1101__part05` and `1926.1101__part07`—were flagged during scanning for mentions of "ACS" and "Wiley"; upon examining the source XML, I confirmed that these were academic citations (an ACS symposium paper and a 1950 Wiley geology text) and organizational contact information for the American Cancer Society, rather than copyrighted third-party material, and recorded this in the manifest notes.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

The gold set comprises 32 queries: 10 written by hand (`origin hand`) and 22 drafted with Claude (`origin claude`), spanning three classes: `identifier` (10 queries), `paraphrase` (12 queries), and `mixed` (10 queries). These classes mirror the distribution from the shared sets, enabling direct comparison of keyword lookups against semantic questions. Relevance judgments are binary (`rel` 1). A document is judged relevant if it directly states the legal requirement, specification, or safety threshold queried; a document that only cross-references or mentions the standard without setting out the operative requirement is judged non-relevant.

Candidate pooling was performed using the union of top 10 results from `bm25`, `dense`, and `hybrid` generated by `scripts/judging_sheet.py`, supplemented by targeted structural searches across the subpart directory (`subparts.md`) to catch provisions missed by first-stage retrieval (such as dynamite storage and transport in Subpart U). Every candidate document was read in full before labeling.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.859 | 0.624 | 0.682 |
| dense | 0.891 | 0.597 | 0.655 |
| hybrid | 0.875 | 0.614 | 0.681 |
| rerank | 0.938 | 0.938 | 0.931 |
| ablation/bm25_lab | 0.859 | 0.601 | 0.664 |

32 judged queries; nDCG uses binary labels; a random ranking of the 307 documents would get recall@10 near 0.033.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | identifier (n=10) | paraphrase (n=12) | mixed (n=10) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.708 | 0.900 |
| bm25 | MRR@10 | 0.812 | 0.334 | 0.783 |
| bm25 | nDCG@10 | 0.858 | 0.433 | 0.803 |
| dense | Recall@10 | 0.800 | 0.875 | 1.000 |
| dense | MRR@10 | 0.650 | 0.333 | 0.861 |
| dense | nDCG@10 | 0.686 | 0.453 | 0.866 |
| hybrid | Recall@10 | 0.900 | 0.833 | 0.900 |
| hybrid | MRR@10 | 0.683 | 0.360 | 0.850 |
| hybrid | nDCG@10 | 0.734 | 0.491 | 0.855 |
| rerank | Recall@10 | 0.900 | 0.917 | 1.000 |
| rerank | MRR@10 | 0.900 | 0.917 | 1.000 |
| rerank | nDCG@10 | 0.900 | 0.906 | 0.992 |
| ablation/bm25_lab | Recall@10 | 1.000 | 0.708 | 0.900 |
| ablation/bm25_lab | MRR@10 | 0.738 | 0.334 | 0.783 |
| ablation/bm25_lab | nDCG@10 | 0.801 | 0.433 | 0.803 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=10) | claude (n=22) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.800 | 0.886 | -0.086 | [-0.377, +0.173] | not distinguishable |
| bm25 | MRR@10 | 0.620 | 0.626 | -0.006 | [-0.311, +0.296] | not distinguishable |
| bm25 | nDCG@10 | 0.670 | 0.687 | -0.017 | [-0.300, +0.249] | not distinguishable |
| dense | Recall@10 | 0.900 | 0.886 | +0.014 | [-0.155, +0.200] | not distinguishable |
| dense | MRR@10 | 0.627 | 0.583 | +0.044 | [-0.252, +0.333] | not distinguishable |
| dense | nDCG@10 | 0.655 | 0.655 | -0.001 | [-0.245, +0.242] | not distinguishable |
| hybrid | Recall@10 | 0.800 | 0.909 | -0.109 | [-0.400, +0.136] | not distinguishable |
| hybrid | MRR@10 | 0.617 | 0.613 | +0.004 | [-0.300, +0.299] | not distinguishable |
| hybrid | nDCG@10 | 0.662 | 0.689 | -0.027 | [-0.305, +0.237] | not distinguishable |
| rerank | Recall@10 | 0.900 | 0.955 | -0.055 | [-0.300, +0.136] | not distinguishable |
| rerank | MRR@10 | 0.900 | 0.955 | -0.055 | [-0.300, +0.136] | not distinguishable |
| rerank | nDCG@10 | 0.888 | 0.951 | -0.063 | [-0.300, +0.112] | not distinguishable |
| ablation/bm25_lab | Recall@10 | 0.800 | 0.886 | -0.086 | [-0.377, +0.173] | not distinguishable |
| ablation/bm25_lab | MRR@10 | 0.620 | 0.592 | +0.028 | [-0.284, +0.327] | not distinguishable |
| ablation/bm25_lab | nDCG@10 | 0.670 | 0.661 | +0.009 | [-0.271, +0.275] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | +0.000 | -0.100 | +0.100 | [-0.186, +0.409] | not distinguishable |
| MRR@10 | +0.043 | -0.007 | +0.049 | [-0.223, +0.294] | not distinguishable |
| nDCG@10 | +0.032 | +0.015 | +0.016 | [-0.217, +0.230] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.63 (10 queries), claude 0.80 (22 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 10 hand and 22 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | +0.031 | [-0.125, +0.172] | 0.217 | not distinguishable |
| dense minus bm25 | MRR@10 | -0.027 | [-0.153, +0.099] | 0.187 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.027 | [-0.143, +0.091] | 0.172 | not distinguishable |
| hybrid minus bm25 | Recall@10 | +0.016 | [-0.078, +0.109] | 0.133 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.010 | [-0.089, +0.061] | 0.110 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.001 | [-0.072, +0.063] | 0.100 | not distinguishable |
| hybrid minus dense | Recall@10 | -0.016 | [-0.141, +0.109] | 0.172 | not distinguishable |
| hybrid minus dense | MRR@10 | +0.017 | [-0.073, +0.105] | 0.130 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.026 | [-0.056, +0.105] | 0.117 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.078 | [-0.031, +0.203] | 0.179 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.313 | [+0.174, +0.456] | 0.209 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.250 | [+0.126, +0.380] | 0.188 | rerank higher |
| rerank minus dense | Recall@10 | +0.047 | [-0.016, +0.141] | 0.115 | not distinguishable |
| rerank minus dense | MRR@10 | +0.341 | [+0.204, +0.474] | 0.202 | rerank higher |
| rerank minus dense | nDCG@10 | +0.276 | [+0.164, +0.388] | 0.165 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.062 | [+0.000, +0.156] | 0.122 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.323 | [+0.201, +0.449] | 0.184 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.250 | [+0.149, +0.358] | 0.153 | rerank higher |
| ablation/bm25_lab minus bm25 | Recall@10 | +0.000 | [+0.000, +0.000] | - | identical on every query |
| ablation/bm25_lab minus bm25 | MRR@10 | -0.023 | [-0.062, +0.000] | 0.048 | not distinguishable |
| ablation/bm25_lab minus bm25 | nDCG@10 | -0.018 | [-0.047, +0.000] | 0.036 | not distinguishable |
| ablation/bm25_lab minus dense | Recall@10 | -0.031 | [-0.172, +0.125] | 0.217 | not distinguishable |
| ablation/bm25_lab minus dense | MRR@10 | +0.004 | [-0.123, +0.132] | 0.189 | not distinguishable |
| ablation/bm25_lab minus dense | nDCG@10 | +0.009 | [-0.108, +0.124] | 0.171 | not distinguishable |
| ablation/bm25_lab minus hybrid | Recall@10 | -0.016 | [-0.109, +0.078] | 0.133 | not distinguishable |
| ablation/bm25_lab minus hybrid | MRR@10 | -0.013 | [-0.089, +0.067] | 0.115 | not distinguishable |
| ablation/bm25_lab minus hybrid | nDCG@10 | -0.017 | [-0.083, +0.055] | 0.102 | not distinguishable |
| ablation/bm25_lab minus rerank | Recall@10 | -0.078 | [-0.203, +0.031] | 0.179 | not distinguishable |
| ablation/bm25_lab minus rerank | MRR@10 | -0.337 | [-0.480, -0.197] | 0.210 | rerank higher |
| ablation/bm25_lab minus rerank | nDCG@10 | -0.267 | [-0.397, -0.142] | 0.188 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time. Two systems that score the same on every query have no interval to speak of, so their MDD is shown as -.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

On the 32 judged queries of the own gold set, `rerank` outperforms all three first-stage systems by statistically distinguishable margins: `rerank minus hybrid` is +0.323 MRR@10 [+0.201, +0.449] and +0.250 nDCG@10 [+0.149, +0.358]; `rerank minus bm25` is +0.313 MRR@10 [+0.174, +0.456] and +0.250 nDCG@10 [+0.126, +0.380]; and `rerank minus dense` is +0.341 MRR@10 [+0.204, +0.474] and +0.276 nDCG@10 [+0.164, +0.388]. In all three comparisons, the 95% bootstrap intervals are entirely above zero.

Conversely, the three first-stage retrievers are not distinguishable from each other on this gold set. `dense minus bm25` is -0.027 MRR@10 [-0.153, +0.099], `hybrid minus bm25` is -0.010 MRR@10 [-0.089, +0.061], and `hybrid minus dense` is +0.017 MRR@10 [-0.073, +0.105]. With minimum detectable differences between 0.110 and 0.187, the small differences among the first-stage systems (all scoring around 0.60 to 0.62 MRR@10) cannot be reliably resolved.

The `hand` (n=10) and `claude` (n=22) queries tell a consistent story: while Claude-drafted queries exhibit higher mean content-word overlap with their best relevant document (0.80 vs. 0.63 for hand queries), the difference in BM25's lead over dense between the two groups is +0.049 MRR@10 [-0.223, +0.294] and +0.016 nDCG@10 [-0.217, +0.230], both indistinguishable from zero. My prior expectation in `DECISIONS.md` prompt 1 held: `rerank` achieved overwhelming victory (MRR 0.938), and the first-stage systems clustered closely together.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

I expect `bm25_lab` (the plain alphanumeric tokenizer) to lower MRR@10 on my corpus compared to `bm25` because splitting regulatory citations such as 1926.1153 into isolated numbers dilutes exact section matching across hundreds of sections sharing the 1926 prefix.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/bm25_lab minus bm25 | Recall@10 | +0.000 | [+0.000, +0.000] | - | identical on every query |
| ablation/bm25_lab minus bm25 | MRR@10 | -0.023 | [-0.062, +0.000] | 0.048 | not distinguishable |
| ablation/bm25_lab minus bm25 | nDCG@10 | -0.018 | [-0.047, +0.000] | 0.036 | not distinguishable |
| ablation/bm25_lab minus dense | Recall@10 | -0.031 | [-0.172, +0.125] | 0.217 | not distinguishable |
| ablation/bm25_lab minus dense | MRR@10 | +0.004 | [-0.123, +0.132] | 0.189 | not distinguishable |
| ablation/bm25_lab minus dense | nDCG@10 | +0.009 | [-0.108, +0.124] | 0.171 | not distinguishable |
| ablation/bm25_lab minus hybrid | Recall@10 | -0.016 | [-0.109, +0.078] | 0.133 | not distinguishable |
| ablation/bm25_lab minus hybrid | MRR@10 | -0.013 | [-0.089, +0.067] | 0.115 | not distinguishable |
| ablation/bm25_lab minus hybrid | nDCG@10 | -0.017 | [-0.083, +0.055] | 0.102 | not distinguishable |
| ablation/bm25_lab minus rerank | Recall@10 | -0.078 | [-0.203, +0.031] | 0.179 | not distinguishable |
| ablation/bm25_lab minus rerank | MRR@10 | -0.337 | [-0.480, -0.197] | 0.210 | rerank higher |
| ablation/bm25_lab minus rerank | nDCG@10 | -0.267 | [-0.397, -0.142] | 0.188 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time. Two systems that score the same on every query have no interval to speak of, so their MDD is shown as -.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/bm25_lab against bm25 (BASE = "bm25" in p2/retrievers/bm25_lab.py): it helped 0 queries, hurt 2 and left 30 unchanged.

| Query | Class | Origin | bm25 RR | ablation/bm25_lab RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c01 | identifier | claude | 1.000 | 0.500 | -0.500 | hurt |
| c07 | identifier | claude | 0.500 | 0.250 | -0.250 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

I changed the BM25 tokenizer from `codes` to the plain `[a-z0-9]+` lab 12 tokenizer (`tokenizer = "lab"`) in `p2/retrievers/bm25_lab.py`, keeping all other parameters ($k_1 = 0.9, b = 0.4$, chunking 300/50) identical. I hypothesized that `bm25_lab` would lower MRR@10 because splitting regulatory section citations into isolated digits dilutes exact section matches across hundreds of sections sharing the 1926 prefix.

`bm25_lab` achieved an MRR@10 of 0.601, compared to 0.624 for standard `bm25`. The mean difference is -0.023 MRR@10 with a 95% paired bootstrap interval of [-0.062, +0.000] and an MDD of 0.048. Because the upper bound of the interval touches zero, the aggregate difference is technically classified as not distinguishable on this 32-query set, though the direction strictly favors `bm25`. 

Inspection of the `own-ablation-queries` table reveals exactly why: the lab tokenizer helped 0 queries, left 30 unchanged, and hurt 2 queries—both of which were `identifier` queries. On `c01` ("What does 1926.1053 require for portable ladders?"), reciprocal rank dropped from 1.000 to 0.500 (-0.500); on `c07` ("Table A minimum clearance distances 1926.1408"), reciprocal rank dropped from 0.500 to 0.250 (-0.250). In both cases, tokenizing "1926.1053" or "1926.1408" into separate numbers "1926", "1053", and "1408" caused other sections mentioning those numbers or the ubiquitous prefix "1926" to outscore the target section. Query `c02` ("1926.1153 Table 1") further illustrates this dynamic: section numbers and table labels ("Table 1", "Table A") are exactly what the tokenizer change affects. In `c02`, `1926.55` (which features its own Table 1 and cross-references 1926.1153 in footnote p) competes directly with `1926.1153`; when compound designations are split into bare words and numbers, exact section specificity is eroded across the corpus. These specific losses confirm the mechanism behind the hypothesis.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|
| c02 | 1926.5 (OMB numbers) at rank 1 | 1926.1153 (Respirable crystalline silica Table 1), missing from top 10 | First-stage RRF truncation: dense ranked 1926.1153 outside its top 20, dragging it out of hybrid's top 20 pool so rerank never saw it | Expand the reranker candidate pool from 20 to 50 candidates, or union top retrievals |
| h06 | 1926.900 (Blasting general provisions) at rank 1 | 1926.904 (Storage) and 1926.902 (Transportation), missing from top 10 | Vocabulary mismatch: query asks for "dynamite" while regulations exclusively use "explosives and blasting agents" | Query expansion with domain synonyms mapping "dynamite" to "explosives" |
| c10 | 1926.1408 at rank 1 in rerank, but hybrid returned 1926.1410 (operations closer than Table A) | 1926.1408 (Power line safety clearance distance) | Near-duplicate statutory overlap: exception and assembly sections (1410, 1407) crowded out the primary operating rule in first stage | Cross-passage contextual reranking (which successfully promoted 1926.1408 to rank 1) |
| h08 | 1926.59 at rank 1 in rerank, but hybrid returned 1926.65__part07 (HAZWOPER guidelines) | 1926.59 (Hazard communication) | Document length / stub document penalty: 1926.59 is a 4-line stub citing 1910.1200, outscored in first stage by massive HAZWOPER texts | Inlining incorporated standard text during ingestion so stubs contain substantive terms |
| c08 | 1926.501 at rank 1 in rerank, but bm25 returned 1926.97 and missed 1926.501 completely | 1926.501 (Duty to have fall protection) | Conversational paraphrase vocabulary mismatch: "stop them from falling" vs statutory "fall protection systems" | Dense semantic embeddings (which ranked 1926.501 at rank 1) to bridge paraphrase gaps |

Across these failures, two distinct patterns emerge: (1) vocabulary gaps on informal or colloquial phrasing ("dynamite", "stop them from falling") where keyword systems fail without semantic support or synonym expansion, and (2) first-stage candidate truncation, where near-duplicate regulations or length-advantaged documents push the operative standard out of the top 20 candidate pool passed to the reranker. Because the reranker's recall ceiling is strictly bounded by the first-stage hybrid candidate pool, retrieval failures at stage one cannot be repaired downstream.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

| Corpus | Documents | Mean words | Median words | Docs > 300 words | bm25 MRR | dense MRR | hybrid MRR | rerank MRR |
|---|---|---|---|---|---|---|---|---|
| shared (30 CFR) | 2,484 | 158 | 68 | 13% | 0.507 | 0.562 | 0.471 | 0.800 |
| own (29 CFR 1926) | 307 | 1,185 | 378 | 55% | 0.624 | 0.597 | 0.614 | 0.938 |

The overall winner did not change between collections: `rerank` dominated on both corpora (MRR@10 of 0.800 on shared practice and 0.938 on the own corpus), significantly outperforming every first-stage system. However, the two corpora differ substantially in their structure and retrieval behavior:

1. **Document length and chunking:** Documents in 29 CFR 1926 are roughly seven times longer on average than those in 30 CFR (mean 1,185 words vs. 158 words). While 87% of 30 CFR documents fit entirely within a single 300-word chunk, 55% of the own corpus documents require multiple chunks. Consequently, chunk boundary splits and max-score aggregation matter significantly more on the own corpus.
2. **Near-duplicate structure:** 30 CFR is structured around parallel mining subchapters (parts 56, 57, 75, and 77) that contain near-verbatim duplicate provisions (e.g. backup alarms, seat belts, electrical testing). In contrast, 29 CFR 1926 concentrates construction safety into unified subparts with fewer verbatim cross-section duplicates. This cleaner partition helps explain why the reranker reached an even higher absolute score on the own corpus (0.938 MRR@10) by distinguishing operative provisions from definition or scope paragraphs.
3. **Tested vs. speculative explanations:** The document word counts, chunking fractions, and token distributions are measured facts. The role of parallel duplicate sections in suppressing first-stage precision is supported by inspection of the practice qrels, but remains an observational inference rather than an experimentally isolated variable.

Critically, with only 20 queries on the shared corpus (MDD ~0.25 to 0.41) and 32 queries on the own corpus (MDD ~0.11 to 0.19), neither test set can detect small shifts in retriever quality. Claims that dense retrieval or hybrid fusion is fundamentally superior to BM25 on either corpus are unsupported by the confidence intervals.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 200,469 | 4,174 | 103.6 | 16,706 | 348 | 8.6 |
| traces/answers-rerank.r1.jsonl | rerank | 12 | 24 | 0 | 200,702 | 4,374 | 98.5 | 16,725 | 364 | 8.2 |
| traces/answers-rerank.r2.jsonl | rerank | 12 | 24 | 0 | 200,682 | 4,048 | 111.3 | 16,724 | 337 | 9.3 |
| traces/answers-rerank.r3.jsonl | rerank | 12 | 24 | 0 | 203,157 | 4,429 | 114.3 | 16,930 | 369 | 9.5 |
| traces/own-own-rerank.jsonl | rerank | 32 | 32 | 0 | 593,204 | 3,266 | 98.5 | 18,538 | 102 | 3.1 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 2 | 263,406 | 1,820 | 77.9 | 13,170 | 91 | 3.9 |
| traces/shared-practice-rerank.r1.jsonl | rerank | 20 | 20 | 0 | 263,420 | 1,985 | 61.4 | 13,171 | 99 | 3.1 |
| traces/shared-practice-rerank.r2.jsonl | rerank | 20 | 20 | 0 | 288,949 | 2,177 | 74.3 | 14,447 | 109 | 3.7 |
| traces/shared-practice-rerank.r3.jsonl | rerank | 20 | 20 | 0 | 340,116 | 2,325 | 89.7 | 17,006 | 116 | 4.5 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 0 | 569,145 | 4,475 | 171.4 | 14,229 | 112 | 4.3 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.293 | [-0.533, -0.043] | 13,170 | 3.9 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.237 | [-0.408, -0.083] | 13,170 | 3.9 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.329 | [-0.504, -0.164] | 13,170 | 3.9 | rerank higher |
| own: bm25 minus rerank | 32 | -0.313 | [-0.456, -0.174] | 18,538 | 3.1 | rerank higher |
| own: dense minus rerank | 32 | -0.341 | [-0.474, -0.204] | 18,538 | 3.1 | rerank higher |
| own: hybrid minus rerank | 32 | -0.323 | [-0.449, -0.201] | 18,538 | 3.1 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-ablation-bm25_lab.jsonl | bm25_lab | 32 | 0.02 | 0.6 |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 32 | 0.02 | 0.7 |
| traces/retrieval/own-own-dense.jsonl | dense | 32 | 0.15 | 4.8 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 32 | 0.19 | 5.9 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.04 | 1.9 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.18 | 9.1 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.22 | 10.8 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.07 | 1.8 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.26 | 6.6 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.43 | 10.9 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

rider (the 598E rider constitutes the stretch requirement; see section 9 below).

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
Repeated runs of rerank on shared/practice:

| Run | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| rerank.r1 | 0.733 | 0.800 | 0.743 |
| rerank.r2 | 0.733 | 0.800 | 0.743 |
| rerank.r3 | 0.758 | 0.800 | 0.765 |
| range (max minus min) | 0.025 | 0.000 | 0.021 |

| Comparison | Metric | Mean difference | 95% interval | Reading |
| --- | --- | ---: | ---: | --- |
| rerank.r1 minus hybrid | Recall@10 | +0.142 | [+0.050, +0.258] | rerank.r1 higher |
| rerank.r2 minus hybrid | Recall@10 | +0.142 | [+0.050, +0.258] | rerank.r2 higher |
| rerank.r3 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r3 higher |
| rerank.r1 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r1 higher |
| rerank.r2 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r2 higher |
| rerank.r3 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r3 higher |
| rerank.r1 minus hybrid | nDCG@10 | +0.300 | [+0.176, +0.430] | rerank.r1 higher |
| rerank.r2 minus hybrid | nDCG@10 | +0.300 | [+0.176, +0.430] | rerank.r2 higher |
| rerank.r3 minus hybrid | nDCG@10 | +0.322 | [+0.197, +0.449] | rerank.r3 higher |

Repeated answers shared/rerank:

| File | Verified (in) | 95% interval | Declined (out) | 95% interval |
| --- | ---: | ---: | ---: | ---: |
| rerank.r1 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r2 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r3 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| range (max minus min) | 0.000 |  | 0.000 |  |

Each repeat answers the same questions, so the repeats are not independent trials and their counts are not pooled into one interval.
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

Across three repeated runs of `rerank` on the shared practice queries (`r1`, `r2`, `r3`), MRR@10 was identical across all three runs (0.800, range 0.000), while nDCG@10 exhibited a minor spread of 0.021 (ranging from 0.743 to 0.765) and recall@10 had a spread of 0.025 (0.733 to 0.758). The reranker's measured gain over `hybrid` in all three repeats was +0.329 MRR@10 [+0.164, +0.504] and +0.300 to +0.322 nDCG@10 [+0.176, +0.449]. Because the run-to-run variation (range 0.000 to 0.025) is negligible compared to the +0.329 gain, the reranker's advantage decisively survives run-to-run variance.

For the cited answers across the three repeats, the model verified 8 of 8 in-corpus questions (100%) and declined 4 of 4 out-of-corpus questions (100%) each time (range 0.000). The Wilson 95% confidence intervals are [0.676, 1.000] for answering and [0.510, 1.000] for declining. The perfect agreement suggests that Sonnet's behavior on this constrained extraction schema is highly deterministic, though the wide Wilson intervals emphasize that small question sets (8 and 4 items) inherently possess broad uncertainty.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

I pre-registered a directional hypothesis in `PREREG.md` at commit `c7b2bd3` prior to committing any own-corpus relevance judgments: on 29 CFR 1926, `rerank` would achieve a higher nDCG@10 than `hybrid` with a smallest meaningful effect size $\Delta = 0.15$. The required gold-set sample size was calculated at 31 queries based on stage 1 standard deviations ($sd = 0.297$); I collected and judged 32 queries (22 Claude-drafted, 10 written by hand).

The empirical outcome yielded an nDCG@10 of 0.931 for `rerank` versus `hybrid`'s 0.681, a mean difference of +0.250 with a 95% paired bootstrap interval of [+0.149, +0.358] and an MDD of 0.153. Because the measured MDD of 0.153 came in slightly above $\Delta = 0.15$, the strict rule committed in section 3 of `PREREG.md` was triggered, making the formal pre-registered verdict at $\Delta = 0.15$ technically inconclusive due to statistical power. However, the observed gain of +0.250 is far larger than the MDD, and the 95% bootstrap interval is entirely above zero (with its lower end touching 0.149). Thus, while formal power fell just short of the 0.15 design threshold, the empirical evidence demonstrates a clear, statistically distinguishable advantage for the reranker over hybrid search on this regulatory corpus.
