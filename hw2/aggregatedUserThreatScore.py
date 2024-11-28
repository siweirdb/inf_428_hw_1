import numpy as np
import unittest
from fetch_data import fetch_data_from_elasticsearch


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
    department_scores = []
    total_importance = 0

    for _, threat_scores, importance in department_data:
        department_score = calculate_department_threat_score(threat_scores, importance)
        department_scores.append(department_score)
        total_importance += importance

    return aggregate_company_threat_score(department_scores, total_importance)


class TestAggregatedThreatScore(unittest.TestCase):

    def test_calculate_aggregated_threat_score(self):
        department_data = fetch_data_from_elasticsearch("test_calculate_aggregated_threat_score")
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_all_departments_same_scores(self):
        department_data = fetch_data_from_elasticsearch("test_all_departments_same_scores")
        department_data = [(dep_id, [50] * len(scores), imp) for dep_id, scores, imp in department_data]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertEqual(aggregated_score, 50)

    def test_one_high_scoring_department(self):
        department_data = fetch_data_from_elasticsearch("test_one_high_scoring_department")
        if department_data:
            department_data[0] = (department_data[0][0], [80] * len(department_data[0][1]), department_data[0][2])
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertGreater(aggregated_score, 50)

    def test_one_department_with_high_variance(self):
        department_data = fetch_data_from_elasticsearch("test_one_department_with_high_variance")
        if department_data:
            skewed_scores = np.concatenate([np.random.randint(10, 20, 150), np.random.randint(80, 90, 50)]).tolist()
            department_data[0] = (department_data[0][0], skewed_scores, department_data[0][2])
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_no_users_in_department(self):
        department_data = fetch_data_from_elasticsearch("test_no_users_in_department")
        department_data.append(("empty_dept", [], 3))  # Adding a department with no users
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_all_departments_high_importance(self):
        department_data = fetch_data_from_elasticsearch("test_all_departments_high_importance")
        department_data = [(dep_id, scores, 5) for dep_id, scores, imp in department_data]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)


if __name__ == "__main__":
    unittest.main()
