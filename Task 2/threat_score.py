import numpy as np
import unittest


def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), mean + variance + 1, num_samples)


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


def calculate_aggregated_threat_score(department_data):
    """
    Combines `calculate_department_threat_score` and `aggregate_company_threat_score`
    to calculate the aggregated threat score for the company.
    """
    department_scores = []
    total_importance = 0

    for _, threat_scores, importance in department_data:
        department_score = calculate_department_threat_score(threat_scores, importance)
        department_scores.append(department_score)
        total_importance += importance

    return aggregate_company_threat_score(department_scores, total_importance)


class TestAggregatedThreatScore(unittest.TestCase):

    def test_generate_random_data(self):
        mean = 50
        variance = 20
        num_samples = 100
        data = generate_random_data(mean, variance, num_samples)
        self.assertTrue(np.all(data >= 0) and np.all(data <= 90))

    def test_calculate_aggregated_threat_score(self):
        department_data = [
            (100, np.random.randint(0, 90, 100), 2),
            (150, np.random.randint(0, 90, 150), 3),
            (200, np.random.randint(0, 90, 200), 1),
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_calculate_aggregated_threat_score_empty(self):
        department_data = []
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertEqual(aggregated_score, 0)

    def test_calculate_aggregated_threat_score_single_department(self):
        department_data = [
            (100, np.random.randint(0, 90, 100), 3)
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_all_departments_same_scores(self):
        department_data = [
            (100, np.full(100, 50), 2),
            (150, np.full(150, 50), 3),
            (200, np.full(200, 50), 1),
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertEqual(aggregated_score, 50)

    def test_one_high_scoring_department(self):
        department_data = [
            (100, np.random.randint(10, 30, 100), 1),  # Low scores
            (150, np.random.randint(10, 30, 150), 2),  # Low scores
            (200, np.random.randint(80, 90, 200), 3),  # High scores
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertGreater(aggregated_score, 50)

    def test_one_department_with_high_variance(self):
        department_data = [
            (100, np.full(100, 50), 2),  # Average scores
            (150, np.random.randint(50, 51, 150), 3),  # Uniform average
            (200, np.concatenate([np.random.randint(10, 20, 150), np.random.randint(80, 90, 50)]), 1),  # Skewed scores
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_different_number_of_users(self):
        department_data = [
            (50, np.random.randint(30, 70, 50), 1),  # Small department
            (200, np.random.randint(20, 80, 200), 2),  # Large department
            (10, np.random.randint(10, 90, 10), 3),  # Very small department
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)


if __name__ == "__main__":
    unittest.main()
