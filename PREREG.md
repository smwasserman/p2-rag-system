# Pre-registration (598E)

This file is for 598E students; it is the second half of the 598E rider, and 498E students can ignore it or delete it.

A pre-registration is a claim you write down, with the test that will judge it, before you can see the answer.
Its value is that the claim can be wrong in a way anyone can check, and that you cannot adjust it afterwards to fit the numbers.
A well-powered result that says "no effect as large as the one I cared about" scores as well as a confirmation, so you have no reason to bend the claim.

**Git history is how I will know the order.**
Commit this file, filled in through section 4, before the first commit that puts a judgment line into `eval/own/qrels.txt` (or any other file under `eval/own/`).
`uv run p2 check` reads `git log` to find the first commit in which sections 1 to 4 have no TODO marker left and some words of yours in each, and confirms that it comes before your first judgment; a copy that was filled in afterwards fails.
Right after that commit, `p2 check` names it and waits for your first judgment; it asks for section 5 separately, once you have scored your own corpus.
You may ingest your corpus and write queries first, but not the relevance judgments.
After that first commit, do not edit sections 1 to 4, because `p2 check` compares them with the commit where you filled them in.
If something must change, add a dated entry in section 6 and leave the original as it was.

You need your stage 1 scores for section 3, so score the shared corpus first.

---

## 1. Hypothesis

One sentence, about your own corpus, naming two of your systems and a direction.
For example: "On my corpus of Kubernetes documentation, `rerank` has a higher MRR@10 than `hybrid`, because the queries are paraphrases that a first-stage fusion ranks too low."
It should be something you could be wrong about.

On my corpus of OSHA construction regulations (29 CFR 1926), rerank has a higher nDCG@10 than hybrid, because the regulations are highly repetitive and structurally similar, so first stage retrievers surface many near duplicate or definitional passages that share the query's vocabulary, while an LLM reranker reads the query and all 20 candidates together in one prompt, so it can compare look alikes against each other and pick the one operative provision.

---

## 2. The smallest effect that matters

Name one metric, MRR@10 or nDCG@10, and choose it now so you cannot pick the better one afterwards.
Then say how large a difference between the two systems would matter to a person using the search, and why that size.
A difference of 0.02 is usually not worth a reranker's cost in time and tokens.
In this course, choose a Δ of at least 0.15 unless you argue for a larger one, because a smaller gap takes more queries than one project can judge.
Call your number Δ (delta).

Metric: nDCG@10. I chose it over MRR@10 because some queries have several relevant sections, and nDCG counts all of them, not just the first.
Δ = 0.15. A gap of this size matters to a user because the operative rule moves from somewhere in the top ten up to the first few results. Someone looking up a scaffold fall protection threshold usually acts on the first plausible section, and in 29 CFR 1926 that can be a definitions or scope paragraph. When a question has several relevant sections, such as the requirement and its training provision, 0.15 also means more of them show up without a second search. A wrong rule on a job site can mean an injury or a citation, so ~4 seconds and ~14,000 tokens per query is a fair price. A gain of 0.02 would reorder only a few queries.

---

## 3. How many queries you need

The size of the gold set follows from three numbers: how large a difference you want to detect (Δ), how variable the per-query differences are (sd), and the usual choices of a 5% false-alarm rate and 80% power.

```
n = ((1.96 + 0.84) * sd / Δ)^2
```

Here sd is the standard deviation of the per-query differences between your two systems, which `results/results.json` holds for the shared practice queries.
Compute it from your stage 1 runs for the same two systems, or the nearest pair you have, and say which pair you used.
With only 20 practice queries the sd is itself noisy, so be generous and round up.

Some numbers to calibrate against.
At sd 0.3 and Δ 0.10 the formula gives about 71 queries, and with the t distribution's small-sample correction it is a few more, about 73.
At sd 0.3, a gold set of 30 queries can only detect a difference of about 0.15, which is why 30 queries cannot support a claim about a gap of 0.10.
The spreads you will measure on the shared practice queries are mostly larger than 0.3: from about 0.31 for `hybrid` against `bm25` to about 0.66 for `dense` against `bm25`.
For `rerank` against `hybrid` the sd is about 0.39, so a Δ of 0.10 needs about 120 queries, 0.15 about 55, and 0.20 about 31.
So the course's Δ of 0.15 means about 55 queries for that pair; at an sd of 0.66 it would mean about 150, so compare a pair whose spread you can afford.
Choose Δ and the size of your gold set together: the smallest effect that matters to a user, and a number of queries you can write and judge in the time you have.
If the two do not meet, say which one you gave ground on and why.

After you score the own corpus, the minimum detectable difference that `uv run p2 score` prints for your two systems is this same calculation run the other way.
It should come out at or below your Δ.
If it does not, your queries varied more than your stage 1 sd suggested, and you will say so in the outcome.

sd = 0.297: the standard deviation of per-query nDCG@10 differences between rerank and hybrid on the 20 shared practice queries (results/results.json).
n = ((1.96 + 0.84) × 0.297 / 0.15)² ≈ 30.7, so 31 queries.
I will write 32 queries: 22 drafted by Claude and 10 written by hand.
The sd comes from only 20 queries on a different corpus, so it is noisy. The 0.39 the course gives for this pair, and my own measured 0.394, are MRR@10 spreads, and at that spread Δ 0.15 would need about 55 queries. My nDCG@10 spread was 0.297. If `uv run p2 score` prints a minimum detectable difference above 0.15, I will report the result as inconclusive at that Δ.

---

## 4. The test, and what each result will mean

The test is the paired 95% interval of the mean difference between your two systems on your own gold set, from the `own-pairs` table that `uv run p2 score` writes in `EVAL.md`.
Write the rule now.
This is the default rule, and you can tighten it, but do not loosen it after you see your numbers.

| The interval is | I will say |
|---|---|
| entirely above zero in the direction I predicted | supported: the difference is distinguishable from zero |
| entirely on the other side of zero | contradicted: the opposite of my hypothesis holds on this gold set |
| around zero, with both ends inside plus or minus Δ | well-powered null: a difference as large as Δ is ruled out |
| around zero, with an end beyond plus or minus Δ | inconclusive: the gold set could not settle it, and I say so |

I keep the default rule as written, and I compute the interval once on the full gold set. I will not add or drop queries after seeing it.
The systems are rerank (prediction: higher) and hybrid, the metric is nDCG@10, Δ is 0.15, and the interval is the paired 95% bootstrap interval in the own-pairs table.

---

## 5. Outcome (write this after the fact)

What was the interval?
Which row of the table in section 4 is it?
Did your gold set reach the size section 3 asked for, and what was the minimum detectable difference that `uv run p2 score` printed?
What would you do next, and what would you want a reader to take from this?

The paired 95% bootstrap interval for rerank minus hybrid on nDCG@10 is [+0.149, +0.358] with a mean difference of +0.250. This falls in the first row of the table in section 4: entirely above zero in the direction predicted, so the hypothesis is supported and the difference is distinguishable from zero. The gold set reached 32 judged queries (22 drafted by Claude, 10 written by hand), meeting and exceeding the target size of 31 queries from section 3. The minimum detectable difference printed by `uv run p2 score` was 0.153, practically matching the pre-registered Δ of 0.15. Next, I would investigate the interaction between chunk size and first-stage recall, as 55% of the own corpus documents exceed one 300-word chunk. A reader should take away that an LLM reranker providing full-context cross-passage comparison delivers a substantial and statistically robust gain (+0.250 nDCG@10) over rank-fusion hybrid search on structurally dense, repetitive regulatory codes.

---

## 6. Amendments

Dated entries only, one per change, each saying what changed and why.
Leave this section as it is if nothing changed.
