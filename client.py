"""
Client script to post a JSON with some test 
samples to the Flask API

Usage:
python client.py      (post a single random sample)
python client.py N    (post N random samples)
"""

import pandas as pd
import requests
import sys

def get_test_dataset_samples(n=1):
    # Reading test dataset
    dataset_folder = '/home/cunha/covid19-sample'
    test = pd.read_csv(dataset_folder + '/test.csv', sep=';')

    # Selecting only 'text' and 'country_code' columns
    test_df = test[['text','country_code']].copy()

    # Tranforming the country_code into American (1) or not (0)
    test_df['country_code'] = (test_df['country_code'] == 'US').astype(int)

    # Separating the text from the country for sending
    X_test, y_test = test_df['text'], test_df['country_code']
    
    # Select n random samples
    X_samples = X_test.sample(n)
    y_true = y_test[X_samples.index]
    return X_samples, y_true

def call_api(X_samples, y_true, url='http://localhost:5002/api/american'):
    # POST a JSON to the flask application for each sample
    # and print the results
    
    for index, tweet_text in X_samples.items():
        r = requests.post(url, json={"text": tweet_text})
        result = r.json()['is_american']
        date = r.json()['model_date']
        version = r.json()['version']

        print(f"ID\t{index}\t: " + 
              f"true={y_true[index]}, " + 
              f"pred={result}, " + \
              f"version={version}, " + \
              f"last_updated={date}")

def main ():
    if (len(sys.argv) == 1):
        # No argument, use default=1 sample
        X_samples, y_true = get_test_dataset_samples()
    else:
        n=int(sys.argv[1])
        X_samples, y_true = get_test_dataset_samples(n)
    call_api(X_samples, y_true)
    
if __name__ == "__main__":
    main()