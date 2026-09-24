# tools/ — claim table

Claims about the four instruments in this directory. Ids are `NC_*` and are
**distinct from the dispatch's tool names N1–N4** and from the repository's own
`C1..C12` in `docs/FALSIFICATION_LOG.md`. Nothing here restates, endorses or
extends an older claim.

Four of these ids -- NC_002, NC_006, NC_009, NC_013 -- are also rows in
`experiments/check_claims.py`, so one claim carries one id in both files. The
rest are not executable there and the table says which and why.

Every claim below is a property of code in this directory, recomputable by
anyone with the clone:

```
python3 tools/test_tools.py          # the instruments' own selftests
python3 experiments/check_claims.py  # the repository harness, NC rows included
```

The check total is printed by that command and is deliberately not written
here. A count stored in a document is a second place for it to drift.

---

## What was found by building, not by reading

| id | claim | status |
|----|-------|--------|
| NC_002 | **N1: with the counts unread, the verdict is a property of the assumed denominator.** The two published percentages are fixed. Read at n=10 the intervals overlap and the tool returns VALUE; at n=25 and above they are disjoint and it returns CHANNEL_LOSS. Nothing about the report changed. | SUPPORTED |
| NC_003 | **N1: at a small assumed denominator the POINT moves too, not only the interval.** An integer count over a small denominator cannot represent an arbitrary percentage: at n=5 the reconstructed loss is 0.60 against a published 0.58. A second reconstruction artifact sits inside the first — the tie rule. Python's built-in `round()` is half-to-even and sends a published 90% at n=5 to 4/5; the declared rule here is half-up and sends it to 5/5. A tie rule that alternates direction with the parity of the denominator is invisible unless it is named. | SUPPORTED |
| NC_004 | **N1: both published figures are BOUNDS, and in opposite directions.** ">= 90%" and "as low as 32%". Read as points they overstate the direct channel and overstate the gap. The fixture reads them as points because a point estimate needs one, and states that doing so is the most favourable reading of the loss available from the report. | SUPPORTED |
| NC_006 | **N2: the sharper number is not the one the headline carries.** The single find came off a SIDE path, so the ASSIGNED path found nothing in eleven runs: 0/11, interval [0.0000, 0.2849], against the headline 1/11 at [0.0023, 0.4128]. The tighter bound is on the route the campaign was designed around. | SUPPORTED |
| NC_012 | **N4: a phase lead against a quiet channel is not a measurement, so fixture F1 as specified cannot be read.** F1 asks for a lead against a body that does not move; with body B flat, any lag the correlation returns is a property of B's residual variation rather than of the coupling. The tool returns the phase NOT_EVALUABLE and decides on amplitude alone, saying so. `F1b` is the case F1 was reaching for and is shipped beside it. | SUPPORTED |
| NC_013 | **N4: the lead is determined only modulo the forcing period, and the branch was being chosen by accident.** A constructed LAG of 4 samples in a 40-sample period came back from the raw search as a LEAD of 36 — the same peak read on the other branch. The sign of the lead is what the agreement check reads, so the branch choice was deciding a verdict. Leads are now wrapped into the principal branch (−P/2, +P/2], and near half a period the sign is withheld rather than reported. | SUPPORTED, repaired |
| NC_016 | **The closed `KINDS` vocabulary refused N4's verdicts on first build.** That is the tuple doing its job rather than a defect. It was widened deliberately, the three new members are commented at the site, and the widening is recorded in `threshold_provenance.txt` — a widening that leaves no trace is the guard being stepped around rather than used. | SUPPORTED |

## Refusals built in, each demonstrated in both directions

| id | claim | status |
|----|-------|--------|
| NC_005 | **N1 refuses to compare two channels read by different readers.** A rate difference across two readers is not a property of the channel. NOT_EVALUABLE with the two readers named. | SUPPORTED |
| NC_008 | **N2's side-path share is `None` with no finds, never 0.0.** An empty numerator over an empty denominator is not a zero, and a 0.0 there would read as "no find came off a side path" on a campaign that found nothing. | SUPPORTED |
| NC_009 | **N3 never scales and never subtracts a candidate.** Candidates carry a SIGN or a SHAPE and nothing else; `candidate()` refuses a magnitude, scale, amplitude, coefficient, weight, size or gain field outright. Asserted behaviourally: the residual series is identical with and without any candidate list. A fitted magnitude makes every candidate consistent, which is how an unexplained remainder becomes a confirmed mechanism with no measurement taken. | SUPPORTED |
| NC_010 | **N3 keeps `not_testable` apart from `inconsistent`.** A candidate whose prediction requires a variable the data does not carry has not failed; it was not asked. The two call for different next actions. | SUPPORTED |
| NC_011 | **N3's empty declaration is the loudest form of UNPARTITIONED, not the quietest.** With nothing declared the residual is the whole observation, and `sources_declared: []` says so rather than reading as a small remainder. | SUPPORTED |
| NC_014 | **N4 treats amplitude and phase pointing opposite ways as NOT_EVALUABLE, not as a verdict with a caveat.** Two readings disagreeing is not a finding. | SUPPORTED |
| NC_015 | **N4's TRAILER_CHANNEL_ABSENT and an instrumented-but-flat body do not collapse.** A body that was not instrumented has not been shown to be quiet. The two return different kinds and the constructor keeps them apart at intake. | SUPPORTED |
| NC_007 | **N2's SINGLE_FIND bounds the process, not the result.** A rarely-reached real result and a once-reached artifact produce the same 1/11. The typed return exists so the interval is not read as a confidence in the finding. Misses are kept as rows carrying their run ids rather than collapsed into a denominator. | SUPPORTED |

## Scope, absences and what was not built

| id | claim | status |
|----|-------|--------|
| NC_001 | **Nothing in `tools/` duplicates an existing module.** The repository before this drop held four domain processors, an aggregator, a symbolic engine, an NLP detector and a claim harness. None computes an interval, a channel comparison, a rerun rate, a residual partition or a two-body source attribution. The nearest neighbour is `symbolic_intelligence.py`, which averages whatever scalars a domain returns — the operation `C6` in the falsification log records as unit-free — and these four tools do not touch it, call it or endorse it. | SUPPORTED |
| NC_017 | **The N4 cross-link is a cross-repo pointer, PENDING.** `JinnZ2/Simulators, stability-trigger-envelope/ (ESP-1) -- PENDING, not yet landed`. Checked 2026-09-24 against that repository as available to this session: 213 folders, no `stability-trigger-envelope` among them; the nearest by name are `trigger-geometry/` and `envelope-asymmetry/`, neither of which is it. The pointer names where the packet is expected and reconstructs nothing. | SUPPORTED, target checked |
| NC_018 | **Every published-value fixture is SECONDARY and its primary is UNREAD.** Probed 2026-09-24T11:25Z: `www.biorxiv.org`, `arxiv.org` and `www.nature.com` return no response through this environment's egress policy, with `github.com` answering as the control. No count in any fixture was transcribed from a paper. | UNVERIFIED |
| NC_019 | **The dispatch/contributing conflict was a misreading on my part, and is now closed.** First filing withheld the `NC_*` rows from `experiments/check_claims.py`, reading STEP 0's "do NOT edit, endorse or extend older claims" as covering the file rather than the claims in it. The operator clarified on 2026-09-24 that adding new rows is neither editing nor endorsing an older claim, and that the dispatch wording was **overbroad**. Four rows were then added under the repository's own contributing rule. The insertion is provably pure: `git diff` reports **162 insertions and 0 deletions**, and every `C1..C12` verdict is byte-identical before and after (`FALSIFIED=9 HOLDS=1 OPEN=1 REVISED=1` on the C rows both runs). The `NC_*` checks import from `tools/` only and touch no processor, so an NC row cannot move because a C row moved. | CLOSED by clarification |
| NC_020 | **CORRECTED. The harness runs.** First filing recorded that `experiments/check_claims.py` could not be run because numpy was absent from this environment, and that the processors were read and not executed. That was true of the environment as first found and false of the environment available: `pip install numpy` succeeded (2.4.6) when the clarification made running the harness necessary. The correction is recorded here rather than replacing the original line, because a first filing that reported an absence it had not tried to remove is the more useful half. **Baseline captured before any NC row was added**, so the no-movement result rests on a measurement and not on an assumption. What survives unchanged: nothing in `tools/` imports numpy, and the four instruments still run where numpy is absent. | CORRECTED |
| NC_021 | **Nothing here is a measurement of anything physical.** No sensor, no vehicle, no campaign, no survey. Three of the four tools run on CONSTRUCTED fixtures whose expected values are known in advance because they were authored; the fourth runs on percentages from a press report. Whether any of the four separates what it claims to separate on real data is untouched in both directions. | UNVERIFIED |

---

## What would refute these

- **NC_002 / NC_003** die if the preprint's real per-channel counts are read and
  the verdict is stable across them. They are claims about what an unread
  denominator costs, not about the biology.
- **NC_012 / NC_013** die if a cross-correlation is shown to recover a lead
  against a channel at or below its own variance floor, or to determine a sign
  at half a period. Both are properties of the operation and neither depends on
  the fixtures.
- **NC_009** dies the moment any function in `residual_partition.py` returns a
  quantity fitted to the residual. The behavioural check is in the selftest.
- **NC_001** dies if a reader finds an existing module computing any of the four
  quantities. The overlap scan behind it is a read of every `.py` in the
  repository, listed in `tools/README.md`.
- **NC_017** closes the moment the ESP-1 packet lands in `JinnZ2/Simulators`.
  It is a statement about where a pointer points and what is currently at the
  other end, not about the packet's content, which is unread in both states.
