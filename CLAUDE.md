# CLAUDE.md - AI Assistant Guide for Noise-as-Information-Sensor

## Project Overview

A multi-scale sensor framework that treats environmental **noise as a primary source of intelligence** rather than error. The system decodes patterns across quantum, biological, electromagnetic, and planetary domains using signal processing, symbolic AI, and cross-domain resonance detection.

**Status:** Early-stage research prototype
**Language:** Python 3 (+ Arduino C++ firmware)
**License:** MIT

> **Read `docs/FALSIFICATION_LOG.md` before making claims about this code.**
> Round 1 tested 12 documented claims; 1 survived. Several defects are known,
> recorded, and deliberately still live. Do not assume the prose is accurate —
> `experiments/check_claims.py` is the authority on what is currently true.

## Repository Structure

```
Noise-as-Information-Sensor/
├── main.py                              # Entry point - orchestrates all processors
├── software/                            # Core Python analysis modules
│   ├── quantum/quantum_processor.py     # Fluctuation stats over an unlabelled sequence
│   ├── biological/biological_processor.py # Bio signals & inter-species coordination
│   ├── electromagnetic/em_processor.py  # Solar, geomagnetic, cosmic ray effects
│   ├── planetary/gaia_processor.py      # Atmospheric chaos & planetary feedback
│   └── arduino/
│       ├── noise_capture.ino            # Arduino firmware for sensor streaming
│       └── notes.txt                    # Supported sensors documentation
├── dashboard/
│   └── dashboard.py                     # Aggregator; prints a text summary to stdout
├── symbolic/                            # Symbolic intelligence & phantom word detection
│   ├── symbolic_intelligence.py         # Cross-domain resonance & alignment scoring
│   ├── phantom_detector.py              # NLP-based unnamed concept detection
│   ├── PHANTOM_WORD_MAP.json            # Catalog of sensed-but-unnamed concepts
│   └── README.md                        # Phantom word usage guide + known defects
├── experiments/
│   ├── check_claims.py                  # Every documented claim, executable
│   └── README.md                        # How to add a claim check
├── hardware/
│   └── README.md                        # Hardware design & component specs
├── docs/
│   ├── Field_Manual.md                  # Philosophical & technical manual
│   └── FALSIFICATION_LOG.md             # Claimed / run / falsified / revised / unknown
├── legacy/                              # Superseded files, kept as record
│   └── README.md                        # What was retired and why
└── README.md                            # Project overview
```

## Architecture

### Data Flow

```
Raw sensor data (4 channels)
    ├── molecular   → QuantumNoiseProcessor     → quantum coherence/entanglement
    ├── chemical    → BiologicalNoiseProcessor   → ecosystem communication/coordination
    ├── motion      → EMFieldNoiseProcessor      → solar/geomagnetic/cosmic ray effects
    └── atmospheric → GaiaSystemNoiseProcessor   → planetary coordination/feedback
                           │
                    NoiseDashboard (aggregator)
                           │
                  SymbolicIntelligenceEngine
                           │
                    alignment_score + symbolic_consensus
```

### Key Patterns

- **Modular Processor Architecture**: Each domain has an isolated processor class with independent analysis pipeline and dict-based output
- **Aggregator/Facade**: `NoiseDashboard` provides single interface to all four processors
- **Symbolic Reasoning Layer**: `SymbolicIntelligenceEngine` performs cross-domain coherence detection with weighted alignment scoring
- **Non-filtering Philosophy**: All data is preserved; intelligence is extracted from chaos without discarding noise

### Cross-Domain Weights (SymbolicIntelligenceEngine)

```python
quantum: 0.3, biological: 0.3, electromagnetic: 0.2, planetary: 0.2
resonance_threshold: 0.75
```

## Running the Project

```bash
# Run the main analysis pipeline
python main.py
```

```bash
# Core dependencies (numpy only)
pip install -r requirements.txt

# Check every documented claim against the code
python experiments/check_claims.py
```

```bash
# Optional NLP stack — only phantom_detector.py needs it (pulls in torch)
pip install -r requirements-nlp.txt
python -m spacy download en_core_web_sm
```

Key dependencies:

| Package | Used In | Purpose |
|---------|---------|---------|
| `numpy` | All 4 processors | Signal processing, correlation, entropy |
| `spacy` | phantom_detector.py | NLP tokenization (`en_core_web_sm` model) |
| `sentence-transformers` | phantom_detector.py | Cross-domain embeddings (`all-MiniLM-L6-v2`) |

`sentence-transformers` downloads model weights from huggingface.co **at first
use**, not at install time — it fails at scoring time in restricted networks.

## Known Defects (measured, not suspected)

Each carries a claim id from `experiments/check_claims.py`. **Do not "fix" these
casually** — C3, C5, C6 and C7 change published numbers and need their own
round with a before/after recorded.

| # | Defect |
|---|--------|
| C3 | `extract_fluctuations` adds `rng.normal(0, 0.001)` to real data, reseeded to 42 per call. Quantum outputs are not measurements. |
| C4 | EM layer is inert at demo scale; `0.0` conflates "no correlation" with "not enough data". |
| C5 | Quantum resonance verdict saturates with sample count — the entropy term is extensive. The demo payload hides this. |
| C6 | `alignment_score` averages booleans, Pearson *r*, and unbounded entropy against a fixed 0.75 threshold. No unit. |
| C7 | Minimum 4 samples per channel; fewer raises `ValueError` from inside numpy. Negative input → silent `nan`. |
| C8 | Output is not JSON-serialisable; numpy scalars leak through processor boundaries. |
| C10/C11/C12 | Phantom detector cannot reproduce its own documented example output. |

## Code Conventions

- **Class-based OOP** for all processors
- **snake_case** for methods and variables
- **Underscore prefix** for private methods (e.g., `_detect_resonance()`)
- **Dict-based data flow** between components (all processors return dictionaries)
- **Docstrings** on all public methods
- Each processor follows the pattern: `extract → correlate/analyze → detect → main pipeline method`
- Main pipeline method is always named `analyze_*_noise()` (e.g., `analyze_quantum_noise()`)

## Key Entry Points

| Entry Point | Purpose |
|-------------|---------|
| `main.py` | Full pipeline: dashboard + symbolic engine |
| `software/*/` processor modules | Can be imported and used individually |
| `symbolic/phantom_detector.py` | Standalone NLP tool (requires corpus input) |
| `software/arduino/noise_capture.ino` | Arduino firmware (upload via Arduino IDE) |

## Development Notes

### What exists

- Four core processor modules (quantum, biological, EM, planetary)
- Dashboard aggregator and symbolic intelligence engine
- Phantom word detection NLP tool with knowledge base
- Hardware specifications and Arduino starter code
- Claim-check harness (`experiments/check_claims.py`) and falsification log
- Documentation (Field Manual, READMEs) — now corrected against round 1

### What does NOT exist yet

- No unit test suite (pytest/unittest). `experiments/check_claims.py` checks
  documented claims, not units, and is not a substitute
- No CI/CD pipeline or GitHub Actions
- No pyproject.toml or package distribution setup
- No linting/formatting configuration
- No containerization (Docker)
- **No hardware validation whatsoever** — every result in this repo comes from
  simulated input. The Arduino sketch has never been run against a physical
  sensor in any record here

### When contributing code

1. Follow the existing class-based processor pattern
2. Return dictionaries from analysis methods for pipeline compatibility
3. Preserve the non-filtering philosophy - do not discard data as "noise"
4. Keep processors domain-isolated; cross-domain logic belongs in `symbolic/`
5. Use numpy for numerical operations (project standard)
6. Add docstrings to all public methods
7. Simulated/example data is acceptable for prototyping (see `main.py`) — but
   the `main.py` payload is *not* representative. C5 showed it sits in the one
   narrow regime that hides a saturated detector. Never validate a change
   against the demo payload alone
8. Add your claim to `experiments/check_claims.py` and run it. A claim that has
   not been run is not a finding
9. When you falsify something, record it in `docs/FALSIFICATION_LOG.md` and move
   the superseded file to `legacy/`. Do not delete it — precedent carries

### Scientific method loop

This repo runs on `hypothesise → run → result → falsified? → edit the claim →
search for unknowns → rerun`. Practically, for an AI assistant working here:

- Run `experiments/check_claims.py` before and after any change; earlier claims
  can die from later edits
- Record wrong guesses. C5's first hypothesis was backwards and the correction
  is more informative than the revised claim alone would have been
- Distinguish *repairing* from *changing the record*. Fixing unparseable JSON
  (C9) destroys nothing. Removing the synthetic noise injection (C3) invalidates
  every quantum number ever printed and belongs in its own round
- Open questions live in the log's U-table, not in code comments

### Arduino/Hardware

- Arduino sketch streams raw CSV data at 9600 baud: `timestamp,rawValue`
- Default sampling: 100 Hz on analog pin A0
- Supported sensors: electret mic, MQ gas sensors, piezo film, photodiode, magnetometer
- Hardware specs cover quantum, biological, EM, and planetary sensor layers

## Multi-Scale Reference

| Scale | Timescale | Processor | Sensor Examples |
|-------|-----------|-----------|-----------------|
| Quantum | fs - ns | `quantum_processor.py` | High-speed clock, entropy RNG |
| Biological | ms - min | `biological_processor.py` | VOC, CO2/CH4, soil sensors |
| Electromagnetic | ms - hr | `em_processor.py` | Magnetometer, Geiger counter |
| Planetary | hr - years | `gaia_processor.py` | Barometric, GPS, seismic |
