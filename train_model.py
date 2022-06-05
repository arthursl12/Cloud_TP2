import pandas as pd
import pickle

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline

# Reading dataset
dataset_folder = '/home/cunha/covid19-sample'
train = pd.read_csv(dataset_folder + '/training.csv', sep=';')
test = pd.read_csv(dataset_folder + '/test.csv', sep=';')

# Selecting only 'text' and 'country_code' columns
train_df = train[['text','country_code']].copy()
test_df = test[['text','country_code']].copy()

# Tranforming the country_code into American (1) or not (0)
train_df['country_code'] = (train_df['country_code'] == 'US').astype(int)
test_df['country_code'] = (test_df['country_code'] == 'US').astype(int)

# Separating the text from the country for the training
X_train, y_train = train_df['text'], train_df['country_code']
X_test, y_test = test_df['text'], test_df['country_code']

# Building a model, following the tutorial at:
# scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
text_clf = Pipeline([
    ('vect', CountVectorizer(stop_words='english')),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])

# Training
text_clf.fit(X_train,y_train)
print(f"Training score: {text_clf.score(X_train, y_train):.3f}")

# Accuracy in the test set
print(f"Test score: {text_clf.score(X_test, y_test):.3f}")

# Saving the model
filename = 'trained_model.sk'
pickle.dump(text_clf, open(filename, 'wb'))

# Note: to read it again just do
# loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.score(X_test, Y_test)