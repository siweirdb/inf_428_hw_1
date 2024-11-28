import csv

# Data for the test case
data = [
    {"Department": "Engineering", "ThreatScores": "[10, 20, 30, 40, 50]", "Importance": 5},
    {"Department": "Marketing", "ThreatScores": "[15, 25, 35, 45, 55]", "Importance": 5},
    {"Department": "Finance", "ThreatScores": "[0, 5, 10, 15, 20]", "Importance": 5},
    {"Department": "HR", "ThreatScores": "[25, 35, 45, 55, 65]", "Importance": 5},
    {"Department": "Science", "ThreatScores": "[30, 40, 50, 60, 70]", "Importance": 5},
]

# File name
file_name = "csv_files/test_all_departments_high_importance.csv"

# Writing data to CSV
with open(file_name, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Department", "ThreatScores", "Importance"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"CSV file '{file_name}' created successfully!")
