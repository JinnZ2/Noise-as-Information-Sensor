# legacy/

Superseded files, kept deliberately.

Nothing here is maintained and nothing here should be followed as instructions.
It is kept because **precedent carries**: a claim that was made and later
falsified is part of the record, and deleting it would make the project look
like it always knew what it knows now. It didn't. The point of this folder is
that a future reader can see what was believed, and `docs/FALSIFICATION_LOG.md`
tells them what happened to it.

If you are looking for current documentation, go to the root `README.md`.

## Contents

| File | Superseded by | Why it was retired |
|------|---------------|--------------------|
| `README.v0.1.md` | root `README.md` | Setup steps pointed at `dashboard/index.html` and `hardware/arduino_code/`, neither of which was ever committed. Its module table listed `em_field_processor.py` and `noise_dashboard.py`; the files are named `em_processor.py` and `dashboard.py`. See claim C1. |
| `software-README.v0.1.md` | root `README.md` | Documented `bio_processor.py` and a central fusion engine `noise_engine.py`. `noise_engine.py` does not exist and never did — its described role is filled by `dashboard.py` plus `symbolic_intelligence.py`. Also claimed `dashboard.py` provides "real-time visualizations"; it prints a text summary. See claim C1. |
| `detector-pseudocode.v0.1.md` | `symbolic/phantom_detector.py` | Design sketch for the phantom detector, written before implementation. Retained because it specifies **four** signals — silence, translation gap, metaphor overuse, jargon mismatch — with weights 0.35/0.25/0.2/0.2, while the implementation shipped only two, reweighted 0.6/0.4. The two dropped signals were never refuted, only unimplemented. See open question U2. |
| `PHANTOM_WORD_MAP.v0.1.broken.json` | `symbolic/PHANTOM_WORD_MAP.json` | Byte-for-byte snapshot of the map while it had a JSON syntax error (a trailing comma plus a stray `}` at the end of the array) that made it unparseable for its whole committed life. Kept as evidence for claim C9 — the file was cited by `symbolic/README.md` as a working pipeline output, and no code had ever successfully loaded it. |

## Rules for this folder

1. Files arrive here **verbatim**. Do not clean up a file on its way in — the
   defects are the evidence.
2. Every arrival gets a row in the table above and an entry in
   `docs/FALSIFICATION_LOG.md`.
3. Nothing here is imported by running code. If something in `legacy/` is still
   needed, it isn't legacy — move it back.
4. Retirement is not deletion. If a claim here turns out to be right after all,
   say so in the log and move the claim forward; leave the file.
