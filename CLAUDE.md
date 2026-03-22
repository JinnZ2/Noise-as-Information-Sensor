# CLAUDE.md - AI Assistant Guide for Noise-as-Information-Sensor

## Project Overview

A multi-scale sensor framework that treats environmental **noise as a primary source of intelligence** rather than error. The system decodes patterns across quantum, biological, electromagnetic, and planetary domains using signal processing, symbolic AI, and cross-domain resonance detection.

**Status:** Early-stage research prototype
**Language:** Python 3 (+ Arduino C++ firmware)
**License:** MIT

## Repository Structure

```
Noise-as-Information-Sensor/
├── main.py                              # Entry point - orchestrates all processors
├── software/                            # Core Python analysis modules
│   ├── quantum/quantum_processor.py     # Quantum noise (femto/nanosecond scale)
│   ├── biological/biological_processor.py # Bio signals & inter-species coordination
│   ├── electromagnetic/em_processor.py  # Solar, geomagnetic, cosmic ray effects
│   ├── planetary/gaia_processor.py      # Atmospheric chaos & planetary feedback
│   └── arduino/
│       ├── noise_capture.ino            # Arduino firmware for sensor streaming
│       └── notes.txt                    # Supported sensors documentation
├── dashboard/
│   └── dashboard.py                     # Multi-layer noise intelligence aggregator
├── symbolic/                            # Symbolic intelligence & phantom word detection
│   ├── symbolic_intelligence.py         # Cross-domain resonance & alignment scoring
│   ├── phantom_detector.py              # NLP-based unnamed concept detection
│   ├── PHANTOM_WORD_MAP.json            # Catalog of sensed-but-unnamed concepts
│   ├── Detector pseudocode.md           # Algorithm design doc
│   └── README.md                        # Phantom word usage guide
├── hardware/
│   └── README.md                        # Hardware design & component specs
├── docs/
│   └── Field_Manual.md                  # Philosophical & technical manual
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
# Install dependencies
pip install -r requirements.txt

# For phantom_detector.py, also install the spaCy model:
python -m spacy download en_core_web_sm
```

Key dependencies:

| Package | Used In | Purpose |
|---------|---------|---------|
| `numpy` | All 4 processors | Signal processing, correlation, entropy |
| `spacy` | phantom_detector.py | NLP tokenization (`en_core_web_sm` model) |
| `sentence-transformers` | phantom_detector.py | Cross-domain embeddings (`all-MiniLM-L6-v2`) |

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
- Comprehensive documentation (Field Manual, READMEs)

### What does NOT exist yet

- No test suite (no pytest, unittest, or test files)
- No CI/CD pipeline or GitHub Actions
- No pyproject.toml or package distribution setup
- No linting/formatting configuration
- No build system or package distribution setup
- No containerization (Docker)

### When contributing code

1. Follow the existing class-based processor pattern
2. Return dictionaries from analysis methods for pipeline compatibility
3. Preserve the non-filtering philosophy - do not discard data as "noise"
4. Keep processors domain-isolated; cross-domain logic belongs in `symbolic/`
5. Use numpy for numerical operations (project standard)
6. Add docstrings to all public methods
7. Simulated/example data is acceptable for prototyping (see `main.py`)

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
