# tools/

Four instruments, added as a set under DISPATCH NOISE-1. Standard library only,
no numpy, parses under Python 3.9, phone-buildable. CC0 as a dispatch
condition; the repository's own LICENSE is MIT and these files carry the more
permissive of the two, stated here rather than assumed.

They do not read, call, modify or endorse anything in `software/`,
`dashboard/`, `symbolic/` or `experiments/`. Claims about them live in
`tools/CLAIM_TABLE.md` under `NC_*` ids, kept apart from the repository's own
`C1..C12` in `docs/FALSIFICATION_LOG.md`.

```
python3 tools/test_tools.py          # every selftest, check total printed
python3 tools/channel_loss.py        # N1 on its fixtures
python3 tools/rerun_find_rate.py     # N2
python3 tools/residual_partition.py  # N3
python3 tools/two_body_source.py     # N4
python3 tools/typed.py               # the thresholds in force
```

---

## The shared rule

**"Noise" is never a return value.**

What is left after the declared sources are removed comes back as a typed
residual carrying its provenance, or as a typed absence carrying its reason:

```
UNPARTITIONED(sources_declared=[...])   a residual, and what it is a residual against
CHANNEL_LOSS(channel=...)               detection lost between the data and the reader
SINGLE_FIND(k_runs=...)                 one positive over k runs; bounds, not a rate
NOT_EVALUABLE(reason=...)               the input cannot answer the question asked
UNSEARCHED                              not looked for. NOT a measured zero.
ABSENT_MEASURED                         looked for, not there. NOT the same as UNSEARCHED.
```

The vocabulary is closed. `typed()` refuses a kind outside it, which is how the
three N4 verdicts came to be added deliberately and recorded rather than
appearing by drift.

Every threshold lives in `thresholds.txt` with a status (`PLACEHOLDER` or
`DECLARED`) and a basis, and every value ever in force has a row in the
append-only `threshold_provenance.txt`. Every tool prints the whole threshold
table on every run: a PLACEHOLDER that never appears in an output is a
stipulation nobody can see they are relying on.

---

## N1 `channel_loss.py` — what the reading channel removed

How much detection is lost to the channel between the data and the reader,
versus the reader itself. Per channel: attempts, detections, and the reader.
Returns an exact Clopper-Pearson interval per channel, the loss, whether the
intervals overlap, and `CHANNEL_LOSS` when the mediated interval sits wholly
below the direct one.

The reader is held fixed across the comparison or the tool refuses — a rate
difference across two readers is not a property of the channel.

**Fixture: SECONDARY, RECONSTRUCTED_FROM_PERCENT.** A press report of the
preprint *"Autonomous AI agents discover reverse transcriptases with tandem
repeat arrays"*: models given the DNA directly described the array in >= 90% of
attempts, and with files and tools as low as 32%, the stated cause being that
the model often did not read enough raw DNA to see a full repeat. The real
counts are UNREAD — the host is not reachable from this session — so the
counts are rebuilt against an assumed denominator, and the denominator sweep
is printed because **the verdict moves across it while the published numbers
do not** (`NC_002`), and at the small end the point estimate moves too
(`NC_003`).

## N2 `rerun_find_rate.py` — one find, many misses

A result appeared in 1 run and not in k reruns; what does that bound? Returns
the per-run find probability with an exact interval, `SINGLE_FIND` when there
is exactly one, and the side-path share of finds. Misses are kept as rows
carrying their run ids, because which runs missed is the quantity a later
reader needs and a bare k/n throws it away.

It does not judge whether the find is real. A rarely-reached real result and a
once-reached artifact produce the same 1/11.

**Fixture: SECONDARY.** The finding reached by a side path in the original
campaign, ten reruns of the same campaign all missing it. The headline is
1 of 11 at [0.0023, 0.4128]; the sharper number is that the **assigned** path
found nothing in eleven runs (`NC_006`).

## N3 `residual_partition.py` — the residual is not error

After the declared sources are removed, what is left, and what could it be?
Returns `UNPARTITIONED` carrying `sources_declared` — a residual of 0.3 against
four declared sources and one against none are different findings — plus, per
candidate undeclared source, `consistent` / `inconsistent` / `not_testable`.

It never scales a candidate and never subtracts one. Candidates carry a sign or
a shape; a magnitude field is refused at the constructor. A consistent
candidate is therefore never an attribution, several can be consistent at once,
and the tool ranks none of them.

Fixtures F1 (matching sign), F2 (opposite sign), F3 (no candidate listed). The
worked example — a survey item whose "yes" mixes two meanings with opposite
risk signs, so the residual in a tenure curve is the candidate rather than the
error — is text only and marked NOT RUN.

## N4 `two_body_source.py` — which body the signal is on

Two coupled bodies, one sensor site. Is the signal a property of the body at
risk, or of the body the sensor sits on? Returns `SOURCE_A_MODE`, `SOURCE_B`,
`TRAILER_CHANNEL_ABSENT` or `NOT_EVALUABLE`, with the amplitude ratio, the
phase lead, and whether the two agree.

Two refusals, both found while building the fixtures rather than while writing
the spec:

- **A phase lead against a quiet channel is not a measurement** (`NC_012`). F1
  as specified asks for a lead against a body that does not move; the tool
  refuses the phase and decides on amplitude alone, saying so. `F1b` is the
  case F1 was reaching for and ships beside it.
- **A lead is determined only modulo the forcing period** (`NC_013`). A
  constructed lag of 4 samples in a 40-sample period came back from the raw
  search as a lead of 36. Leads are wrapped into the principal branch and the
  sign is withheld near half a period.

The worked instance — a tractor cab and its trailer on a serpentine descent,
sensor in the cab, body at risk the trailer — is text. Its cross-link, the
ESP-1 packet under `stability-trigger-envelope/`, is **NAMED_AND_ABSENT**: no
such folder is in this repository and none is reachable from here, and nothing
was reconstructed in its place.

---

## STEP 0 — the inventory this drop was built against

Read before anything was written. Modules present, and what each claims:

| path | what it is | claims it makes |
|---|---|---|
| `main.py` | entry point, runs the pipeline on a 5-sample simulated payload | none of its own |
| `software/quantum/quantum_processor.py` | fluctuation statistics over an unlabelled sequence | coherence, entanglement strength, non-local correlations |
| `software/biological/biological_processor.py` | bio signals, inter-species coordination | ecosystem communication, collective intelligence |
| `software/electromagnetic/em_processor.py` | motion anomalies against two baselines | solar, geomagnetic, cosmic-ray readings |
| `software/planetary/gaia_processor.py` | atmospheric chaos, feedback | planetary coordination, climate intelligence |
| `dashboard/dashboard.py` | aggregator over the four | none of its own |
| `symbolic/symbolic_intelligence.py` | averages a domain's scalars against 0.75; weights 0.3/0.3/0.2/0.2 | alignment score, symbolic consensus |
| `symbolic/phantom_detector.py` | NLP detector (needs spacy + sentence-transformers) | silence signal, jargon mismatch |
| `experiments/check_claims.py` | executable checks for `C1..C12` | the repository's own claim record |
| `docs/FALSIFICATION_LOG.md` | round 1: 12 claims tested, 1 survived | `C1..C12`, `U1..U6` |

**Overlaps found: none** (`NC_001`). No existing module computes an interval, a
channel comparison, a rerun rate, a residual partition or a two-body source
attribution. The nearest neighbour is `symbolic_intelligence.py`, whose
`_detect_resonance` averages whatever scalars a domain returns — the operation
`C6` records as unit-free. These four tools do not call it, extend it or take a
position on it.

**Not run here:** `main.py`, the four processors and `experiments/check_claims.py`
all import numpy, which is not installed in this environment, so they were read
and not executed (`NC_020`). Nothing in `tools/` imports numpy.

**Not built, with the reason:** no `NC_*` claim was added to
`experiments/check_claims.py`. The repository's contributing rule asks for
exactly that; the dispatch's STEP 0 forbids editing or extending the existing
claims. The dispatch governs, the claim table sits here instead, and the
conflict is recorded rather than resolved quietly (`NC_019`).
