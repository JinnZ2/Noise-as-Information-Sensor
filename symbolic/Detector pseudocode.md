# PHANTOM DETECTOR - pseudocode

# Inputs:
#  - corpus: list of (doc_id, text, domain_tag)
#  - seed_signals: functions that score text for signals (silence, metaphor_overuse, translation_gap, jargon_mismatch)

# Outputs:
#  - candidates: dict term -> {score, signals, domains, examples}

from collections import defaultdict, Counter

def extract_candidates(corpus):
    # simple phrase extraction (n-grams + named entities)
    phrase_counter = Counter()
    phrase_examples = defaultdict(list)
    domain_map = defaultdict(set)
    for doc_id, text, domain in corpus:
        phrases = ngram_extract(text, n=(1,3))  # implement with tokenizer
        for p in phrases:
            phrase_counter[p] += 1
            if len(phrase_examples[p]) < 3:
                phrase_examples[p].append((doc_id, excerpt_around(text, p)))
            domain_map[p].add(domain)
    return phrase_counter, phrase_examples, domain_map

def score_signals(corpus, phrase):
    # signal scorers return normalized 0..1
    s_silence = silence_signal(phrase, corpus)           # e.g., frequently implied but rarely defined
    s_metaphor = metaphor_overuse(phrase, corpus)        # collocation with metaphors
    s_translation = translation_gap(phrase, corpus)     # different label in other domain for same concept
    s_jargon = jargon_mismatch(phrase, corpus)          # appears as technical vs folk term discrepancies
    # weights can be tuned
    score = 0.35*s_silence + 0.25*s_translation + 0.2*s_metaphor + 0.2*s_jargon
    return score, {"silence": s_silence, "translation": s_translation, "metaphor": s_metaphor, "jargon": s_jargon}

def detect_phantoms(corpus, min_score=0.4, min_domains=2):
    phrase_counter, examples, domain_map = extract_candidates(corpus)
    candidates = {}
    for phrase, cnt in phrase_counter.items():
        if cnt < 3: continue  # require minimal frequency
        score, signals = score_signals(corpus, phrase)
        if score >= min_score and len(domain_map[phrase]) >= min_domains:
            candidates[phrase] = {
                "score": round(score,3),
                "signals": signals,
                "domains": list(domain_map[phrase]),
                "examples": examples[phrase]
            }
    # sort candidates by score
    return dict(sorted(candidates.items(), key=lambda kv: kv[1]["score"], reverse=True))

# Helper scorers (ideas)
# - silence_signal: compute ratio of occurrences where phrase is used without adjacent definitional patterns ("is", "means", "defined as")
# - translation_gap: compute cross-domain mapping using bilingual embeddings or clustering; high gap when cluster distances show separate labels
# - metaphor_overuse: collocation with known metaphor markers ("like", "as", "felt", senses)
# - jargon_mismatch: compare phrase frequency to technical lexicons per domain


Notes:
	•	Start with lightweight heuristics; tune weights with your own corpora.
	•	Use embeddings (sentence-transformers) for cross-domain clustering to detect synonyms used in separate fields.
	•	Keep flagged candidates in a review queue: human-in-the-loop is central.
