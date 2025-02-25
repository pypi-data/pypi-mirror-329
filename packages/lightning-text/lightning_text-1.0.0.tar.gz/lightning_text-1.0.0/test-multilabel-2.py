import gzip
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import classification_report, hamming_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer

from lightning_text import FastTextClassifier, preprocess_text

SAMPLES_LIMIT = 1_000
DATASET_DIR = Path('../article-topic-classification/dataset/preprocessed')
DATASET_NAME = 'post_topics.filtered.vectorized_target'
LOSS = 'ova'

dataset_entries = []
with gzip.open(DATASET_DIR / f'{DATASET_NAME}.jsonl.gz', 'r') as file:
    for line in file:
        dataset_entries.append(json.loads(line))
        if len(dataset_entries) >= SAMPLES_LIMIT:
            break

target_vectorizer = MultiLabelBinarizer()
target_vectorizer.fit([
    [
        topic.replace(' ', '_')
        for topic in entry['topic']
    ]
    for entry in train_test_split(
        dataset_entries,
        test_size=0.2,
        random_state=0,
    )[0]
])

X = np.array([
    [preprocess_text(entry['title'] + ' ' + entry['perex'])]
    for entry in dataset_entries
])
Y = target_vectorizer.transform([
    [
        topic.replace(' ', '_')
        for topic in entry['topic']
    ]
    for entry in dataset_entries
])

X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=0,
)
# Train the classifier

classifier = FastTextClassifier(
    loss=LOSS,
)
classifier.fit(X_train, Y_train)

# Evaluate the classifier

Y_pred = classifier.predict(X_test)

print(f'Hamming loss: {hamming_loss(Y_test, Y_pred)}')
print(classification_report(Y_test, Y_pred))

# Retry with label encoder

classifier = FastTextClassifier(
    loss=LOSS,
)
classifier.fit(X_train, Y_train, label_encoder=target_vectorizer)

Y_pred = classifier.predict(X_test)

print(f'Hamming loss: {hamming_loss(Y_test, Y_pred)}')
print(classification_report(Y_test, Y_pred))
