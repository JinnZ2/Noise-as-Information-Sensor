# main.py

from dashboard.dashboard import NoiseDashboard

# Simulated raw input data for testing
raw_sensor_data = {
    'molecular': [0.98, 0.95, 1.01, 0.97, 0.99],
    'chemical': [0.88, 0.85, 0.83, 0.87, 0.89],
    'motion': [0.67, 0.7, 0.72, 0.71, 0.69],
    'atmospheric': [0.61, 0.65, 0.63, 0.6, 0.62]
}

if __name__ == "__main__":
    dashboard = NoiseDashboard()
    results = dashboard.analyze_all(raw_sensor_data)
    dashboard.display_summary(results)
