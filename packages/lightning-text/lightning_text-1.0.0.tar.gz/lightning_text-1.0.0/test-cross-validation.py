import gzip
import json
from pathlib import Path

import numpy as np
import sklearn
import sklearn.metrics
import sklearn.model_selection

from lightning_text import FastTextClassifier, preprocess_text

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

X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=0,
)

ftc = FastTextClassifier()
cv = sklearn.model_selection.cross_validate(
    ftc,
    X,
    y,
    cv=5,
    scoring='f1',
    n_jobs=4,
)

print(cv)
