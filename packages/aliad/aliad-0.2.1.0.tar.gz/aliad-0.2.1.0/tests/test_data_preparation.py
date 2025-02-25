import numpy as np
import unittest

class TestSplitDataset(unittest.TestCase):

    def setUp(self):
        self.X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
        self.y = np.array([0, 1, 0, 1, 0, 1])
        self.X_dict = {'feature1': np.array([[1], [3], [5], [7], [9], [11]]), 'feature2': np.array([[2], [4], [6], [8], [10], [12]])}

    def test_basic_train_test_split(self):
        data_splits = split_dataset(self.X, self.y, test_size=0.33, random_state=42)
        self.assertEqual(len(data_splits['X_train']), 4)
        self.assertEqual(len(data_splits['X_test']), 2)

    def test_train_val_test_split_with_fractions(self):
        data_splits = split_dataset(self.X, self.y, test_size=0.2, val_size=0.2, random_state=42)
        self.assertEqual(len(data_splits['X_train']), 3)
        self.assertEqual(len(data_splits['X_val']), 1)
        self.assertEqual(len(data_splits['X_test']), 2)

    def test_specifying_number_of_samples(self):
        data_splits = split_dataset(self.X, self.y, test_size=2, val_size=2, random_state=42)
        self.assertEqual(len(data_splits['X_train']), 2)
        self.assertEqual(len(data_splits['X_val']), 2)
        self.assertEqual(len(data_splits['X_test']), 2)

    def test_train_test_split_no_shuffling(self):
        data_splits = split_dataset(self.X, self.y, test_size=0.5, shuffle=False)
        self.assertTrue((data_splits['X_train'] == self.X[:3]).all())
        self.assertTrue((data_splits['X_test'] == self.X[3:]).all())

    def test_handling_dict_of_arrays(self):
        data_splits = split_dataset(self.X_dict, self.y, test_size=2, val_size=2, random_state=42)
        self.assertEqual(len(data_splits['X_train']['feature1']), 2)
        self.assertEqual(len(data_splits['X_val']['feature1']), 2)
        self.assertEqual(len(data_splits['X_test']['feature1']), 2)

    def test_only_specifying_train_size(self):
        data_splits = split_dataset(self.X, self.y, train_size=0.7, random_state=42)
        self.assertEqual(len(data_splits['X_train']), 4)
        self.assertEqual(len(data_splits['X_test']), 2)

    def test_edge_case_with_one_sample(self):
        X_single = np.array([[1, 2]])
        y_single = np.array([0])
        data_splits = split_dataset(X_single, y_single, test_size=0.5, random_state=42)
        self.assertEqual(len(data_splits['X_train']), 1)
        self.assertEqual(len(data_splits['X_test']), 0)

if __name__ == '__main__':
    unittest.main()