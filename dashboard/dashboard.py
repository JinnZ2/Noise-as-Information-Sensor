# dashboard/dashboard.py

from software.quantum.quantum_processor import QuantumNoiseProcessor
from software.biological.biological_processor import BiologicalNoiseProcessor
from software.em_field.em_processor import EMFieldNoiseProcessor
from software.planetary.gaia_processor import GaiaSystemNoiseProcessor

class NoiseDashboard:
    def __init__(self):
        self.quantum = QuantumNoiseProcessor()
        self.biological = BiologicalNoiseProcessor()
        self.electromagnetic = EMFieldNoiseProcessor()
        self.gaia = GaiaSystemNoiseProcessor()

    def analyze_all(self, raw_sensor_data):
        q_result = self.quantum.analyze_quantum_noise(raw_sensor_data['molecular'])
        b_result = self.biological.analyze_biological_noise(raw_sensor_data['chemical'])
        e_result = self.electromagnetic.analyze_em_field_noise(raw_sensor_data['motion'])
        g_result = self.gaia.analyze_gaia_noise(raw_sensor_data['atmospheric'])

        return {
            '🌌 QUANTUM NOISE ANALYSIS': q_result,
            '🌱 BIOLOGICAL NETWORK CHATTER': b_result,
            '⚡ ELECTROMAGNETIC FIELD EFFECTS': e_result,
            '🌍 GAIA SYSTEM INTELLIGENCE': g_result
        }

    def display_summary(self, analysis_result):
        for category, results in analysis_result.items():
            print(f"\n{category}")
            for key, value in results.items():
                print(f"  {key.replace('_', ' ').capitalize()}: {value}")
