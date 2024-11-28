import numpy as np
import unittest


def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)


def calculate_aggregated_threat_score(department_data):
    total_weighted_score = 0
    total_users = 0

    for users_count, threat_scores in department_data:
        avg_score = np.mean(threat_scores)

        weighted_score = avg_score * users_count
        total_weighted_score += weighted_score
        total_users += users_count

    if total_users == 0:
        return 0
    aggregated_score = total_weighted_score / total_users

    return np.clip(aggregated_score, 0, 90)



def generate_department_data():
    department_data = []

    for i in range(5):
        num_users = np.random.randint(10, 201)
        threat_scores = generate_random_data(mean=50, variance=20, num_samples=num_users)
        importance = np.random.randint(1, 6)
        department_data.append((num_users, threat_scores, importance))

    return department_data


if __name__ == "__main__":
    department_data = generate_department_data()

    aggregated_score = calculate_aggregated_threat_score(department_data)

    print(f"Aggregated Cybersecurity Threat Score: {aggregated_score}")


class TestAggregatedThreatScore(unittest.TestCase):
    def test_calculate_aggregated_threat_score(self):
        """General case with random data."""
        department_data = [
            (np.random.randint(50, 150), np.random.randint(0, 90, np.random.randint(50, 150)))
            for _ in range(5)  # Generate 5 random departments
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_calculate_aggregated_threat_score_empty(self):
        """No departments present."""
        department_data = []
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertEqual(aggregated_score, 0)

    def test_calculate_aggregated_threat_score_single_department(self):
        """Single department with random threat scores."""
        num_users = np.random.randint(50, 200)
        department_data = [(num_users, np.random.randint(0, 90, num_users))]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_all_departments_same_threat_scores(self):
        threat_score = np.random.randint(30, 60)
        department_data = [
            (np.random.randint(50, 150), [threat_score] * np.random.randint(50, 150))
            for _ in range(3)
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertEqual(aggregated_score, threat_score)

    def test_one_department_high_score_others_low(self):
        department_data = [
            (50, [20] * 50),
            (60, [90] * 60),
            (70, [10] * 70),
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)

        total_users = sum(users for users, _ in department_data)
        total_weighted_score = sum(users * np.mean(scores) for users, scores in department_data)
        expected_score = total_weighted_score / total_users

        self.assertAlmostEqual(aggregated_score, expected_score, places=2)

    def test_different_user_counts(self):
        department_data = [
            (np.random.randint(20, 50), np.random.randint(0, 90, np.random.randint(20, 50))),
            (np.random.randint(100, 200), np.random.randint(0, 90, np.random.randint(100, 200))),
            (np.random.randint(200, 300), np.random.randint(0, 90, np.random.randint(200, 300))),
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)



if __name__ == "__main__":
    unittest.main()