# software/electromagnetic/em_processor.py

import numpy as np

class EMFieldNoiseProcessor:
    def __init__(self):
        self.solar_baseline = [0.45, 0.50, 0.55]
        self.geomagnetic_baseline = [0.65, 0.70, 0.68]

    def detect_motion_anomalies(self, molecular_motion_data):
        """Detect unexpected molecular speed variations"""
        expected = np.mean(molecular_motion_data)
        return [x for x in molecular_motion_data if abs(x - expected) > 0.1]

    def correlate_solar_activity(self, anomalies):
        """Compare anomalies to solar data trends"""
        solar_sim = np.corrcoef(anomalies[:3], self.solar_baseline)[0, 1]
        return round(solar_sim, 3)

    def correlate_geomagnetic_activity(self, anomalies):
        """Compare anomalies to geomagnetic data trends"""
        geo_sim = np.corrcoef(anomalies[:3], self.geomagnetic_baseline)[0, 1]
        return round(geo_sim, 3)

    def detect_cosmic_ray_signatures(self, anomalies):
        """Detect high-energy impact spikes"""
        return len([a for a in anomalies if a > 1.2])

    def analyze_em_field_noise(self, molecular_motion_data):
        anomalies = self.detect_motion_anomalies(molecular_motion_data)
        solar_effects = self.correlate_solar_activity(anomalies)
        geomagnetic_effects = self.correlate_geomagnetic_activity(anomalies)
        cosmic_rays = self.detect_cosmic_ray_signatures(anomalies)

        return {
            'solar_field_effects': solar_effects,
            'geomagnetic_influences': geomagnetic_effects,
            'cosmic_ray_impacts': cosmic_rays
        }
