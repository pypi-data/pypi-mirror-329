import gzip
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import classification_report, hamming_loss
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer

from lightning_text import FastTextClassifier, preprocess_text

SAMPLES_LIMIT = 1_000
DATASET_DIR = Path('../article-topic-classification/dataset/preprocessed')
DATASET_NAME = 'post_topics.filtered.vectorized_target'

dataset_entries = []
with gzip.open(DATASET_DIR / f'{DATASET_NAME}.jsonl.gz', 'r') as file:
    for line in file:
        dataset_entries.append(json.loads(line))
        if len(dataset_entries) >= SAMPLES_LIMIT:
            break

target_vectorizer = MultiLabelBinarizer()
target_vectorizer.fit([entry['topic'] for entry in dataset_entries])


X = np.array([
    [preprocess_text(entry['title'] + ' ' + entry['perex'])]
    for entry in dataset_entries
])
Y = target_vectorizer.transform([entry['topic'] for entry in dataset_entries])

print(X.shape, Y.shape)


X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=0,
)

classifier = MultiOutputClassifier(
    FastTextClassifier(
        verbose=0,
    ),
    n_jobs=4,
)

classifier.fit(X_train, Y_train)
Y_pred = classifier.predict(X_test)

print(f'Hamming loss: {hamming_loss(Y_test, Y_pred)}')
print(classification_report(Y_test, Y_pred))
