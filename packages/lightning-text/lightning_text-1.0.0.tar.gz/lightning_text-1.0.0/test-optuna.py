import gzip
import json
from pathlib import Path
from typing import Any, cast

import numpy as np
import optuna
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.model_selection import BaseCrossValidator, RepeatedStratifiedKFold

from lightning_text import FastTextClassifier, preprocess_text
from lightning_text.optuna import (
    OptunaSearchCV,
    Range,
    SupervisedTrainingHyperparametersSpace,
)

param_distributions: SupervisedTrainingHyperparametersSpace = {
    'epoch': Range(1, 100),
}
tries = 1


DATASET_DIR = Path('../dangerous-behavior-detection/dataset/base-dataset')
dataset_entries = []
with gzip.open(DATASET_DIR / 'violence.jsonl.gz', 'r') as file:
    for line in file:
        dataset_entries.append(json.loads(line))

X = np.array([
    [preprocess_text(entry['text'])]
    for entry in dataset_entries
])
y = np.array([
    1 if entry['label'] == 'violence' else 0 for entry in dataset_entries
])

estimator = FastTextClassifier(
    verbose=0,
)
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=0)


def metrics_to_optuna_goals(metrics: dict[str, Any]) -> float:
    last_mean_fbeta = metrics['mean_test_score'][-1]
    return last_mean_fbeta


study = optuna.create_study(direction='maximize')
search = OptunaSearchCV(
    estimator=estimator,
    study=study,
    hyperparameters_space=param_distributions,
    n_iter=tries,
    scoring=make_scorer(fbeta_score, pos_label=1, beta=1),
    optuna_metrics_exporter=metrics_to_optuna_goals,
    n_jobs=4,
    refit='fbeta',
    cv=cast(BaseCrossValidator, cv),
    show_progress_bar=True,
)

search.fit(X, y)

print(search.cv_results_)
print(search.best_index_)
print(search.best_params_)
print(search.best_score_)
print(search.best_estimator_)
