PHANTOM WORD MAP — usage & purpose

PHANTOM_WORD_MAP.json catalogs sensed-but-unnamed concepts that repeatedly exert semantic pull across domains. Use it to:
	•	Record candidate phantom words (labels, detection signals, example contexts).
	•	Link detectors (silence, metaphor drift, cross-domain word mismatches) to items that show gravitational pull.
	•	Surface “dark matter” in conversation and corpora so humans can name and test the concepts.

Quick workflow:
	1.	Run the detector pipeline on a corpus → produces candidate phrases + signals.
	2.	Inspect candidates; if persistent, create a phantom_words entry (code, label, description, examples).
	3.	Track gravitational_pull strength over time (low/med/high) and add links to repo issues for prototype experiments.

Principles:
	•	Treat these entries as living hypotheses — update, split, or deprecate as more evidence arrives.
	•	Prioritize examples that show cross-domain resonance (same pattern appearing in at least two distinct fields/genres).
	•	Respect context: flagged items are prompts for human sense-making, not automated renaming.


detector.py

What it does
	•	Extracts candidate phrases (n-grams + named entities).
	•	Scores them by:
	•	Silence: how often they appear without a nearby definition.
	•	Jargon mismatch: how differently the phrase clusters across domains (via embeddings).
	•	Flags phantoms with a composite score ≥ 0.4.

Example output
anisotropy {'score': 0.62, 'silence': 0.5, 'jargon_mismatch': 0.74, 'domains': ['engineering','geology'], 'examples': [...]}
reciprocity {'score': 0.45, 'silence': 0.6, 'jargon_mismatch': 0.22, 'domains': ['policy','economics'], 'examples': [...]}


