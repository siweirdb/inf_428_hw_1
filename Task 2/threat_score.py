import numpy as np
import unittest

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(mean - variance, mean + variance + 1, num_samples)

def calculate_department_threat_score(threat_scores, importance):
    if len(threat_scores) == 0:
        return 0
    avg_threat_score = sum(threat_scores) / len(threat_scores)
    weighted_score = avg_threat_score * importance
    return weighted_score


def aggregate_company_threat_score(department_scores, total_importance):
    total_score = sum(department_scores)
    normalized_score = total_score / total_importance if total_importance > 0 else 0
    return min(normalized_score, 90)

class TestCompanyThreatScore(unittest.TestCase):
    def setUp(self):
        self.departments = [
            {"name": "Engineering", "mean": 30, "variance": 10, "num_samples": 100, "importance": 3},
            {"name": "Marketing", "mean": 25, "variance": 5, "num_samples": 90, "importance": 2},
            {"name": "Finance", "mean": 40, "variance": 15, "num_samples": 80, "importance": 4},
            {"name": "HR", "mean": 20, "variance": 10, "num_samples": 50, "importance": 1},
            {"name": "Science", "mean": 35, "variance": 12, "num_samples": 110, "importance": 5},
        ]

    def test_calculate_department_threat_score(self):
        scores = generate_random_data(30, 10, 100)
        score = calculate_department_threat_score(scores, 3)
        self.assertTrue(0 <= score <= 270, "Threat score should be between 0 and 270")

    def test_aggregate_company_threat_score(self):
        scores = [100, 150, 200]
        total_importance = 10
        agg_score = aggregate_company_threat_score(scores, total_importance)
        self.assertTrue(0 <= agg_score <= 90, "Aggregated score should be between 0 and 90")

    def test_case_1_equal_importance_similar_means(self):
        scores = []
        total_importance = sum(dept['importance'] for dept in self.departments)
        for dept in self.departments:
            threat_scores = generate_random_data(dept["mean"], dept["variance"], dept["num_samples"])
            scores.append(calculate_department_threat_score(threat_scores, dept["importance"]))
        agg_score = aggregate_company_threat_score(scores, total_importance)
        self.assertTrue(0 <= agg_score <= 90, "Aggregated score should stay within 0 - 90 range")

    def test_case_2_high_importance_outlier_department(self):
        self.departments[0] = {"name": "Engineering", "mean": 80, "variance": 5, "num_samples": 150, "importance": 5}
        scores = []
        total_importance = sum(dept['importance'] for dept in self.departments)
        for dept in self.departments:
            threat_scores = generate_random_data(dept["mean"], dept["variance"], dept["num_samples"])
            scores.append(calculate_department_threat_score(threat_scores, dept["importance"]))
        agg_score = aggregate_company_threat_score(scores, total_importance)
        self.assertTrue(0 <= agg_score <= 90, "Aggregated score should stay within 0 - 90 range")

    def test_case_3_no_users_in_department(self):
        self.departments[4]["num_samples"] = 0
        scores = []
        total_importance = sum(dept['importance'] for dept in self.departments)
        for dept in self.departments:
            threat_scores = generate_random_data(dept["mean"], dept["variance"], dept["num_samples"])
            scores.append(calculate_department_threat_score(threat_scores, dept["importance"]))
        agg_score = aggregate_company_threat_score(scores, total_importance)
        self.assertTrue(0 <= agg_score <= 90, "Aggregated score should stay within 0 - 90 range")

    def test_case_4_large_user_disparity(self):
        self.departments[2]["num_samples"] = 1000
        scores = []
        total_importance = sum(dept['importance'] for dept in self.departments)
        for dept in self.departments:
            threat_scores = generate_random_data(dept["mean"], dept["variance"], dept["num_samples"])
            scores.append(calculate_department_threat_score(threat_scores, dept["importance"]))
        agg_score = aggregate_company_threat_score(scores, total_importance)
        self.assertTrue(0 <= agg_score <= 90, "Aggregated score should stay within 0 - 90 range")

if __name__ == "__main__":
    unittest.main()
