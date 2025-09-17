import pandas as pd
import os
import statistics

# Get the current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Read the CSV file
file_path = os.path.join(current_dir, 'data_24hr_hourly.csv')
data_24hr_hourly = pd.read_csv(file_path)

# Get the data
baseline = data_24hr_hourly['baseline_power'].tolist()
flexible = data_24hr_hourly['flexible_power'].tolist()

# Calculate the variance
baseline_variance = statistics.variance(baseline)
flexible_variance = statistics.variance(flexible)

# Print the variances
print("Baseline Variance:", baseline_variance)
print("Flexible Variance:", flexible_variance)

DeviationDecreaseFromTheFlatDemandProfile = 1 - (flexible_variance/baseline_variance)**0.5

# Print the results
print(DeviationDecreaseFromTheFlatDemandProfile)

