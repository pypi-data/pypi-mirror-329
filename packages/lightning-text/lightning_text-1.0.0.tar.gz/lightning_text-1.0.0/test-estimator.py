import numpy as np
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils.multiclass import is_multilabel
from sklearn.utils.validation import check_is_fitted, validate_data

from lightning_text import FastTextClassifier


class CheckWrapper(FastTextClassifier):
    # sometimes I miss Java
    def fit(self, X, y, label_encoder=None):
        self.feature_names_in_ = None
        X, y = validate_data(
            self,
            X,
            y,
            dtype=X.dtype if hasattr(X, 'dtype') else np.str_,
            multi_output=is_multilabel(y),
            ensure_2d=hasattr(X, 'shape') and len(X.shape) == 2,
        )
        X = np.array([
            [str(row).replace('\n', ' ')]
            for row in X
        ])

        feature_names_in = self.feature_names_in_
        n_features_in = self.n_features_in_

        result = super().fit(X, y, label_encoder=label_encoder)

        self.feature_names_in_ = feature_names_in
        self.n_features_in_ = n_features_in

        return result

    def predict_proba(self, X):
        check_is_fitted(self)

        X = validate_data(
            self,
            X,
            reset=False,
            dtype=X.dtype if hasattr(X, 'dtype') else np.str_,
            ensure_2d=hasattr(X, 'shape') and len(X.shape) == 2,
        )

        X = np.array([
            [str(row).replace('\n', ' ')]
            for row in X
        ])

        feature_names_in = self.feature_names_in_
        n_features_in = self.n_features_in_
        self.feature_names_in_ = None
        self.n_features_in_ = 1

        result = super().predict_proba(X)

        self.feature_names_in_ = feature_names_in
        self.n_features_in_ = n_features_in

        return result


check_estimator(CheckWrapper())
