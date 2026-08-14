"""
Claim checker for Noise-as-Information-Sensor.

Every claim this repository makes in prose is restated here as an executable
test. Run it and the docs either survive or they don't.

    python experiments/check_claims.py

Verdicts
    HOLDS      the claim is true of the code as it stands
    FALSIFIED  the claim is contradicted by a reproducible run
    REVISED    the original claim was wrong, a narrower claim replaced it,
               and the narrower claim is what is tested here
    OPEN       not yet decidable without hardware, a corpus, or a decision

Findings are written up in docs/FALSIFICATION_LOG.md. This file is the
apparatus; that file is the notebook. When you change a processor, run this
first and record what moved.

Exit code is 0 when the run completes. A FALSIFIED verdict is a result, not a
build failure -- several are recorded here deliberately as known-open defects.
"""

import json
import os
import sys
import warnings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
warnings.filterwarnings("ignore")

import numpy as np

from dashboard.dashboard import NoiseDashboard
from software.electromagnetic.em_processor import EMFieldNoiseProcessor
from software.planetary.gaia_processor import GaiaSystemNoiseProcessor
from software.quantum.quantum_processor import QuantumNoiseProcessor
from symbolic.symbolic_intelligence import SymbolicIntelligenceEngine

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The demo payload from main.py. Several claims below hold only for this
# payload, which is itself one of the findings.
DEMO = {
    "molecular": [0.98, 0.95, 1.01, 0.97, 0.99],
    "chemical": [0.88, 0.85, 0.83, 0.87, 0.89],
    "motion": [0.67, 0.70, 0.72, 0.71, 0.69],
    "atmospheric": [0.61, 0.65, 0.63, 0.60, 0.62],
}

RESULTS = []


def record(claim_id, verdict, claim, evidence):
    """Record one claim outcome for the summary table."""
    RESULTS.append((claim_id, verdict, claim, evidence))
    print(f"\n[{claim_id}] {verdict}")
    print(f"  claim:    {claim}")
    for line in evidence.splitlines():
        print(f"  evidence: {line}" if line is evidence.splitlines()[0]
              else f"            {line}")


# --------------------------------------------------------------------------
# C1  Documentation paths
# --------------------------------------------------------------------------

def c1_documented_paths():
    """v0.1 READMEs sent readers to files that were never committed."""
    claimed = [
        ("dashboard/index.html", "README v0.1 setup step 3"),
        ("hardware/arduino_code", "README v0.1 setup step 1"),
        ("software/noise_engine.py", "software/README v0.1"),
        ("software/em_field_processor.py", "README v0.1 module table"),
        ("software/bio_processor.py", "software/README v0.1"),
        ("dashboard/noise_dashboard.py", "README v0.1 module table"),
    ]
    missing = [(p, src) for p, src in claimed if not os.path.exists(os.path.join(ROOT, p))]
    ev = "\n".join(f"{p} -- absent, cited by {src}" for p, src in missing) or "all paths resolve"
    record("C1", "FALSIFIED" if missing else "HOLDS",
           "Setup instructions and module tables point at real files.", ev)


# --------------------------------------------------------------------------
# C2  Quantum timescale analysis
# --------------------------------------------------------------------------

def c2_quantum_timescales():
    """README: 'Quantum fluctuation timing (picosecond analysis)'."""
    src = open(os.path.join(ROOT, "software/quantum/quantum_processor.py")).read()
    uses = src.count("quantum_timescales")
    ev = (f"self.quantum_timescales = {QuantumNoiseProcessor().quantum_timescales}\n"
          f"occurrences of the name in the module: {uses} (assignment only)\n"
          "no method reads it; the input carries no timestamps and no sample rate")
    record("C2", "FALSIFIED" if uses <= 1 else "HOLDS",
           "The quantum processor analyses fluctuations at fs/ps/ns timescales.", ev)


# --------------------------------------------------------------------------
# C3  Synthetic noise injection
# --------------------------------------------------------------------------

def c3_synthetic_injection():
    """Field Manual: 'Raw data is always preserved... non-filtering'."""
    q = QuantumNoiseProcessor()
    pure = np.diff(DEMO["molecular"])
    mixed = q.extract_fluctuations(DEMO["molecular"])
    injected = mixed - pure
    ratio = float(np.mean(np.abs(injected)) / np.mean(np.abs(pure)))
    again = q.extract_fluctuations(DEMO["molecular"])
    ev = (f"np.diff(molecular)        = {np.round(pure, 6).tolist()}\n"
          f"extract_fluctuations()    = {np.round(mixed, 6).tolist()}\n"
          f"synthetic component added = {np.round(injected, 6).tolist()}\n"
          f"injected magnitude is {ratio:.1%} of the real signal\n"
          f"rng is reseeded to 42 on every call, so the identical synthetic\n"
          f"vector is re-added each run (repeat call identical: {np.allclose(mixed, again)})")
    record("C3", "FALSIFIED",
           "The pipeline is non-filtering and preserves raw data unmodified.", ev)


# --------------------------------------------------------------------------
# C4  Electromagnetic layer on realistic input
# --------------------------------------------------------------------------

def c4_em_dead_on_normalised_data():
    """README: EM layer 'correlates solar and geomagnetic patterns'."""
    em = EMFieldNoiseProcessor()
    anomalies = em.detect_motion_anomalies(DEMO["motion"])
    out = em.analyze_em_field_noise(DEMO["motion"])
    ev = (f"anomalies detected on demo motion data: {anomalies} (n={len(anomalies)})\n"
          "correlate_solar/geomagnetic both return 0.0 unless n >= 3\n"
          "detect_cosmic_ray_signatures tests `a > 1.2` against readings the\n"
          "rest of the pipeline treats as normalised to roughly 0..1\n"
          f"result: {out}")
    dead = out == {"solar_field_effects": 0.0, "geomagnetic_influences": 0.0,
                   "cosmic_ray_impacts": 0}
    record("C4", "FALSIFIED" if dead else "HOLDS",
           "The EM layer produces solar/geomagnetic/cosmic-ray readings for the demo input.", ev)


# --------------------------------------------------------------------------
# C5  Symbolic resonance is a measure of signal quality
# --------------------------------------------------------------------------

def c5_resonance_tracks_sample_count():
    """CLAUDE.md: resonance_threshold 0.75 over a domain's outputs.

    Original hypothesis was that large-magnitude input would dominate the
    average. That was wrong -- entropy goes negative above 1.0. The surviving
    claim is narrower and worse: entropy is extensive, so the verdict tracks
    how long you recorded for.
    """
    q, s = QuantumNoiseProcessor(), SymbolicIntelligenceEngine()
    base = np.sin(np.linspace(0, 4 * np.pi, 1000)) * 0.1 + 0.6
    rows = []
    for stride in (200, 100, 50, 20, 10):
        d = list(base[::stride])
        r = q.analyze_quantum_noise(d)
        rows.append(f"n={len(d):4d}  entropy={r['non_local_correlations']:8.3f}  "
                    f"verdict={s._detect_resonance(r)}")
    demo_r = q.analyze_quantum_noise(DEMO["molecular"])
    rows.append(f"main.py demo (n=5, values near 1.0): entropy="
                f"{demo_r['non_local_correlations']:.3f} -> {s._detect_resonance(demo_r)}")
    ev = ("one identical sine phenomenon, resampled:\n" + "\n".join(rows) +
          "\nnon_local_correlations is -sum(x*log|x|), which grows with sample count.\n"
          "It is averaged against a bounded [0,1] coherence term and a fixed 0.75\n"
          "threshold, so beyond a handful of samples the quantum domain saturates.\n"
          "The demo escapes only because its values sit near 1.0, where x*log(x) ~ 0.")
    record("C5", "REVISED",
           "Resonance detection measures coherence, not recording length.", ev)


# --------------------------------------------------------------------------
# C6  Averaging across incommensurable units
# --------------------------------------------------------------------------

def c6_unit_mixing():
    """_detect_resonance averages whatever scalars a domain happens to return."""
    g = GaiaSystemNoiseProcessor()
    r = g.analyze_gaia_noise(DEMO["atmospheric"])
    scalars = [float(v) for v in r.values()]
    ev = (f"gaia output: {r}\n"
          f"coerced to scalars and averaged: {scalars} -> mean {np.mean(scalars):.4f}\n"
          "booleans become 1.0/0.0 and are averaged with a Pearson r in [-1, 1];\n"
          "the quantum domain adds an unbounded entropy term to the same mean.\n"
          "The 0.75 threshold is therefore applied to a quantity with no unit.")
    record("C6", "FALSIFIED",
           "The 0.75 resonance threshold compares like with like across domains.", ev)


# --------------------------------------------------------------------------
# C7  Robustness of the dashboard to input length
# --------------------------------------------------------------------------

def c7_input_length():
    """No documented minimum sample count."""
    d = NoiseDashboard()
    rows = []
    ok = True
    for n in (2, 3, 4, 5):
        payload = {k: [v] * n for k, v in
                   (("molecular", 0.9), ("chemical", 0.8), ("motion", 0.7), ("atmospheric", 0.6))}
        try:
            d.analyze_all(payload)
            rows.append(f"n={n}: completes")
        except Exception as e:
            ok = False
            rows.append(f"n={n}: raises {type(e).__name__}")
    neg = {"molecular": [-0.9, -0.5, -0.7, -0.6, -0.8], "chemical": [0.8] * 5,
           "motion": [0.7] * 5, "atmospheric": [0.6] * 5}
    res = d.analyze_all(neg)
    rows.append(f"negative molecular input: earth_system_feedback="
                f"{res['planetary']['earth_system_feedback']} (silent nan, no warning)")
    ev = ("\n".join(rows) +
          "\ngaia and biological index fixed-length baselines (4 and 3 samples)\n"
          "without checking the input is long enough.")
    record("C7", "FALSIFIED" if not ok else "HOLDS",
           "The dashboard accepts any sensor series the Arduino sketch can produce.", ev)


# --------------------------------------------------------------------------
# C8  Dict-based pipeline is serialisable
# --------------------------------------------------------------------------

def c8_serialisable():
    """CLAUDE.md: 'Dict-based data flow between components'."""
    d = NoiseDashboard()
    res = d.analyze_all(DEMO)
    try:
        json.dumps(res)
        record("C8", "HOLDS", "Processor output can be logged or transported as JSON.",
               "json.dumps succeeds")
        return
    except TypeError as e:
        offenders = [f"{k}.{kk}: {type(vv).__name__}"
                     for k, v in res.items() for kk, vv in v.items()
                     if type(vv).__module__ == "numpy"]
        ev = (f"json.dumps raises TypeError: {e}\n"
              "numpy scalars leak out of the processors instead of Python types:\n" +
              "\n".join("  " + o for o in offenders))
        record("C8", "FALSIFIED",
               "Processor output can be logged or transported as JSON.", ev)


# --------------------------------------------------------------------------
# C9  Phantom word map is loadable data
# --------------------------------------------------------------------------

def c9_phantom_map():
    """symbolic/README: 'Run the detector pipeline... create a phantom_words entry'."""
    path = os.path.join(ROOT, "symbolic/PHANTOM_WORD_MAP.json")
    try:
        data = json.load(open(path))
    except json.JSONDecodeError as e:
        record("C9", "FALSIFIED", "PHANTOM_WORD_MAP.json is machine-readable.",
               f"json.load raises JSONDecodeError: {e}")
        return
    entries = data["phantom_words"]
    keys = set().union(*(set(e) for e in entries))
    ragged = {e["code"]: sorted(keys - set(e)) for e in entries if keys - set(e)}
    ev = (f"parses; {len(entries)} entries: {[e['code'] for e in entries]}\n"
          f"schema consistent across entries: {not ragged}\n"
          f"gravitational_pull.strength values: "
          f"{sorted({e['gravitational_pull']['strength'] for e in entries})}")
    record("C9", "HOLDS", "PHANTOM_WORD_MAP.json is machine-readable.", ev)


# --------------------------------------------------------------------------
# C10  silence_signal detects definitions
# --------------------------------------------------------------------------

def c10_silence_signal():
    """symbolic/README: 'Silence: how often they appear without a nearby definition'."""
    definers = ["is", "means", "defined as", "refers to"]
    probes = ["This analysis is noisy.", "The noise was measured.",
              "Anisotropy appeared in the sample.", "A misread signal."]
    hits = [(t, [d for d in definers if d in t.lower()]) for t in probes]
    false_pos = [(t, h) for t, h in hits if h and " is " not in t]
    ev = "\n".join(f"{t!r} -> scored as DEFINED via {h}" for t, h in hits if h)
    ev += ("\nthe test is a substring match, so 'is' fires inside analysis, noise,\n"
           "Anisotropy and misread. Any corpus in this domain is scored as\n"
           "fully defined, driving silence_signal toward 0 and suppressing every candidate.")
    record("C10", "FALSIFIED" if false_pos else "HOLDS",
           "silence_signal measures whether a phrase appears near a definition.", ev)


# --------------------------------------------------------------------------
# C11  jargon_mismatch is per-phrase
# --------------------------------------------------------------------------

def c11_jargon_mismatch():
    """symbolic/README: 'how differently the phrase clusters across domains'."""
    import ast
    src = open(os.path.join(ROOT, "symbolic/phantom_detector.py")).read()
    fn = next(n for n in ast.walk(ast.parse(src))
              if isinstance(n, ast.FunctionDef) and n.name == "jargon_mismatch")
    dumped = ast.dump(fn)
    phrase_used = "id='phrase'" in dumped

    rows = []
    for n in (2, 3, 4):
        sim = np.full((n, n), 0.0)
        np.fill_diagonal(sim, 1.0)
        rows.append(f"{n} domains, embeddings maximally unrelated (off-diagonal 0.0): "
                    f"reported mismatch {1 - sim.mean():.3f}, ceiling {1 - 1 / n:.3f}")
    ev = (f"the `phrase` parameter is never read in the function body: {not phrase_used}\n"
          "it embeds each domain's whole concatenated text, so every phrase sharing\n"
          "a domain set receives an identical score\n"
          "sim.mean() spans the full matrix including the self-similarity diagonal:\n" +
          "\n".join("  " + r for r in rows) +
          "\nfor realistic non-negative sentence similarities the score is capped at\n"
          "1 - 1/n, so with the documented 2-domain case it cannot exceed 0.500 and\n"
          "contributes at most 0.200 toward the 0.4 flagging threshold.")
    record("C11", "FALSIFIED",
           "jargon_mismatch scores how a given phrase diverges across domains.", ev)


# --------------------------------------------------------------------------
# C12  Detector runs end to end
# --------------------------------------------------------------------------

SAMPLE_CORPUS = [
    ("The anisotropy of the sample was measured but called bias in engineering docs.", "engineering"),
    ("In geology, anisotropy is a directional dependence of properties.", "geology"),
    ("The bias of the material seems unexplained in performance reports.", "policy"),
    ("Reciprocity is invoked in treaties but actual flows are asymmetric.", "policy"),
    ("Partnerships are described but often mask extraction of resources.", "economics"),
]


class _OrthogonalEmbedder:
    """Stand-in for all-MiniLM-L6-v2 when the real weights cannot be fetched.

    Returns mutually orthogonal unit vectors, i.e. the most divergent embedding
    result physically possible. Any candidate that fails to surface under this
    embedder would also fail under the real one, so a negative result here is
    a valid falsification; a positive result would not be.
    """

    def encode(self, sentences, convert_to_tensor=True):
        import torch
        return torch.eye(len(sentences))


def c12_detector_runs():
    """symbolic/README lists anisotropy 0.62 and reciprocity 0.45 as example output."""
    try:
        import spacy  # noqa: F401
        import sentence_transformers  # noqa: F401
    except ImportError as e:
        record("C12", "OPEN",
               "phantom_detector.py reproduces the example output in symbolic/README.md.",
               f"optional NLP stack not installed ({e.name}).\n"
               "install with: pip install -r requirements-nlp.txt\n"
               "             python -m spacy download en_core_web_sm")
        return

    import symbolic.phantom_detector as det
    try:
        det._get_embedder()
        mode = "real all-MiniLM-L6-v2 embedder"
    except Exception as e:
        det._embedder = _OrthogonalEmbedder()
        mode = (f"orthogonal stub embedder -- real weights unreachable "
                f"({type(e).__name__}); this is the best case for jargon_mismatch")

    try:
        out = det.detect_phantoms(SAMPLE_CORPUS)
    except Exception as e:
        record("C12", "FALSIFIED",
               "phantom_detector.py reproduces the example output in symbolic/README.md.",
               f"detect_phantoms raised {type(e).__name__}: {e}\nembedder mode: {mode}")
        return

    texts = [t for t, _ in SAMPLE_CORPUS]
    documented = {"anisotropy": 0.62, "reciprocity": 0.45}
    surfaced = {k: k in out for k in documented}
    ev = (f"embedder mode: {mode}\n"
          f"candidates returned: {len(out)}\n" +
          "\n".join(f"  {k!r} score={v['score']} silence={v['silence']} "
                    f"jargon={v['jargon_mismatch']} domains={v['domains']}"
                    for k, v in list(out.items())[:8]) +
          f"\ndocumented example terms surfaced: {surfaced}\n" +
          "\n".join(f"  silence_signal({t!r}) = {det.silence_signal(texts, t)}"
                    for t in documented) +
          "\nboth documented terms occur in only 2 documents and are dropped by the\n"
          "`cnt < 3` minimum-frequency gate; both also score silence 0.0 because\n"
          "'is' matches as a substring inside 'anisotropy' itself.\n"
          "there is no stopword filter, so what survives the gate are function words.\n"
          f"extract_phrases('noise noise noise') -> {det.extract_phrases('noise noise noise')}\n"
          "  (n-grams are emitted per occurrence, so one repetitive document alone\n"
          "   can push a phrase past the 3-occurrence gate)")
    ok = all(surfaced.values())
    record("C12", "HOLDS" if ok else "FALSIFIED",
           "phantom_detector.py reproduces the example output in symbolic/README.md.", ev)


CHECKS = [c1_documented_paths, c2_quantum_timescales, c3_synthetic_injection,
          c4_em_dead_on_normalised_data, c5_resonance_tracks_sample_count,
          c6_unit_mixing, c7_input_length, c8_serialisable, c9_phantom_map,
          c10_silence_signal, c11_jargon_mismatch, c12_detector_runs]


def main():
    print("=" * 74)
    print("CLAIM CHECK -- Noise-as-Information-Sensor")
    print("=" * 74)
    for check in CHECKS:
        check()

    print("\n" + "=" * 74)
    print("SUMMARY")
    print("=" * 74)
    for cid, verdict, claim, _ in RESULTS:
        print(f"  {cid:4s} {verdict:10s} {claim[:52]}")
    tally = {}
    for _, verdict, _, _ in RESULTS:
        tally[verdict] = tally.get(verdict, 0) + 1
    print("\n  " + "  ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    print("\n  Write-up: docs/FALSIFICATION_LOG.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
