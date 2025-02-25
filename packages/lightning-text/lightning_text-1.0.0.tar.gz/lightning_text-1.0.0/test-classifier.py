import gzip
import json
import pickle
from pathlib import Path

import numpy as np
import sklearn
import sklearn.metrics
import sklearn.model_selection
from sklearn.preprocessing import LabelEncoder

from lightning_text import FastTextClassifier, preprocess_text

DATASET_DIR = Path('../dangerous-behavior-detection/dataset/base-dataset')
dataset_entries = []
with gzip.open(DATASET_DIR / 'violence.jsonl.gz', 'r') as file:
    for line in file:
        dataset_entries.append(json.loads(line))

X = np.array([[preprocess_text(entry['text'])] for entry in dataset_entries])
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
ftc.fit(X_train, y_train)

y_pred = ftc.predict(X_test)

print(sklearn.metrics.classification_report(y_test, y_pred))

print('=' * 80)

# test de/serialization
print(ftc.predict_proba(X_test[:2]))
pickled = pickle.dumps(ftc)
ftc2 = pickle.loads(pickled)
print(ftc2.predict_proba(X_test[:2]))

print(y_pred[:2])

# Test label encoding

label_encoder = LabelEncoder()
label_encoder.fit(["other", "violence"])
ftc = FastTextClassifier()
ftc.fit(X_train, y_train, label_encoder=label_encoder)
y_pred = ftc.predict(X_test)
print(sklearn.metrics.classification_report(y_test, y_pred))
print(ftc.predict_proba(X_test[:2]))
print(y_pred[:2])

print('=' * 80)

# Test non-contiguous labels

y = np.array([
    2 if entry['label'] == 'violence' else -1 for entry in dataset_entries
])
y_train, y_test = sklearn.model_selection.train_test_split(
    y,
    test_size=0.2,
    random_state=0,
)
ftc = FastTextClassifier()
ftc.fit(X_train, y_train)

y_pred = ftc.predict(X_test)
print(sklearn.metrics.classification_report(y_test, y_pred))

# Test 1D input

X = np.array([preprocess_text(entry['text']) for entry in dataset_entries])
X_train, X_test = sklearn.model_selection.train_test_split(
    X,
    test_size=0.2,
    random_state=0,
)
ftc = FastTextClassifier()
ftc.fit(X_train, y_train)

y_pred = ftc.predict(X_test)
print(sklearn.metrics.classification_report(y_test, y_pred))
