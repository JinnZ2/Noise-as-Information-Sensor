# symbolic/symbolic_intelligence.py

import numpy as np

class SymbolicIntelligenceEngine:
    def __init__(self):
        self.resonance_threshold = 0.75
        self.cross_domain_weights = {
            'quantum': 0.3,
            'biological': 0.3,
            'electromagnetic': 0.2,
            'planetary': 0.2
        }

    def extract_resonant_patterns(self, fused_data):
        symbolic_signals = {}
        for domain, data in fused_data.items():
            symbolic_signals[domain] = self._detect_resonance(data)
        return symbolic_signals

    def _detect_resonance(self, data):
        """Detects strong coherent signals within a noisy dataset"""
        if isinstance(data, dict):
            signal_strengths = list(data.values())
        elif isinstance(data, list):
            signal_strengths = data
        else:
            signal_strengths = [float(data)]

        avg_strength = np.mean(signal_strengths)
        if avg_strength >= self.resonance_threshold:
            return "Resonance Detected"
        else:
            return "Subthreshold"

    def calculate_cross_layer_alignment(self, symbolic_signals):
        alignment_score = 0
        contributing = []

        for domain, verdict in symbolic_signals.items():
            weight = self.cross_domain_weights.get(domain, 0.1)
            if verdict == "Resonance Detected":
                alignment_score += weight
                contributing.append(domain)

        return {
            "alignment_score": round(alignment_score, 3),
            "contributing_domains": contributing,
            "symbolic_consensus": "Coherent" if alignment_score > 0.7 else "Incoherent"
        }
