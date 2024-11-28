import numpy as np
import unittest


def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), mean + variance + 1, num_samples)


def calculate_department_threat_score(threat_scores):
    if len(threat_scores) == 0:
        return 0
    avg_threat_score = sum(threat_scores) / len(threat_scores)
    return avg_threat_score


def aggregate_company_threat_score(department_scores):
    if len(department_scores) == 0:
        return 0
    avg_score = sum(department_scores) / len(department_scores)
    return min(avg_score, 90)


def calculate_aggregated_threat_score(department_data):
    department_scores = []

    for _, threat_scores in department_data:
        department_score = calculate_department_threat_score(threat_scores)
        department_scores.append(department_score)

    return aggregate_company_threat_score(department_scores)


class TestAggregatedThreatScore(unittest.TestCase):

    def test_generate_random_data(self):
        mean = 50
        variance = 20
        num_samples = 100
        data = generate_random_data(mean, variance, num_samples)
        self.assertTrue(np.all(data >= 0) and np.all(data <= 90))

    def test_calculate_aggregated_threat_score(self):
        department_data = [
            (100, np.random.randint(0, 90, 100)),
            (150, np.random.randint(0, 90, 150)),
            (200, np.random.randint(0, 90, 200)),
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_calculate_aggregated_threat_score_empty(self):
        department_data = []
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertEqual(aggregated_score, 0)

    def test_calculate_aggregated_threat_score_single_department(self):
        department_data = [
            (100, np.random.randint(0, 90, 100))
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_all_departments_same_scores(self):
        department_data = [
            (100, np.full(100, 50)),
            (150, np.full(150, 50)),
            (200, np.full(200, 50)),
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertEqual(aggregated_score, 50)



    def test_one_department_with_high_variance(self):
        department_data = [
            (100, np.full(100, 50)),
            (150, np.random.randint(50, 51, 150)),
            (200, np.concatenate([np.random.randint(10, 20, 150), np.random.randint(80, 90, 50)])),
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_different_number_of_users(self):
        department_data = [
            (50, np.random.randint(30, 70, 50)),
            (200, np.random.randint(20, 80, 200)),
            (10, np.random.randint(10, 90, 10)),
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)


if __name__ == "__main__":
    unittest.main()
