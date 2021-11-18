"""ProbabilityThresholdEarlyClassifier test code."""
import numpy as np
from numpy import testing
from sklearn.ensemble import RandomForestClassifier

from sktime.classification.early_classification import \
    ProbabilityThresholdEarlyClassifier
from sktime.datasets import load_unit_test
from sktime.datatypes._panel._convert import from_nested_to_3d_numpy


def test_prob_threshold_on_unit_test_data():
    """Test of ProbabilityThresholdEarlyClassifier on unit test data."""
    # load unit test data
    X_train, y_train = load_unit_test(split="train", return_X_y=True)
    X_test, y_test = load_unit_test(split="test", return_X_y=True)
    indices = np.random.RandomState(0).choice(len(y_train), 10, replace=False)

    # train probability threshold
    pt = ProbabilityThresholdEarlyClassifier(
        random_state=0, classification_points=[6, 12, 18, 24], probability_threshold=0.8, estimator=Catch22Classifier(n_estimators=10)
    )
    pt.fit(X_train, y_train)

    X_test = from_nested_to_3d_numpy(X_test)
    states = None
    for i in pt.classification_points:
        probas = pt.predict_proba(X_test[indices, :, :i])
        decisions, states = pt.decide_prediction_safety(X_test, probas, states)
        print(decisions)

    # # assert probabilities are the same
    # testing.assert_array_almost_equal(
    #     probas, prob_threshold_unit_test_probas, decimal=2
    # )