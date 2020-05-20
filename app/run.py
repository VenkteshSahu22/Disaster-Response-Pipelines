import json
import plotly
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from collections import Counter
from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
from sklearn.externals import joblib
from sqlalchemy import create_engine
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np


app = Flask(__name__)

class StartingVerbExtractor(BaseEstimator, TransformerMixin):

    def starting_verb(self, text):
        sentence_list = sent_tokenize(text)
        for sentence in sentence_list:
            pos_tags = nltk.pos_tag(tokenize(sentence))
            first_word, first_tag = pos_tags[0]
            if first_tag in ['VB', 'VBP'] or first_word == 'RT':
                return True
        return False

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_tagged = pd.Series(X).apply(self.starting_verb)
        return pd.DataFrame(X_tagged)


def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens
def compute_word_counts(messages, load=True, filepath='../data/counts.npz'):
    '''
    input: (
        messages: list or numpy array
        load: Boolean value if load or run model
        filepath: filepath to save or load data
            )
    Function computes the top 20 words in the dataset with counts of each term
    output: (
        top_words: list
        top_counts: list
            )
    '''
    if load:
        # load arrays
        data = np.load(filepath)
        return list(data['top_words']), list(data['top_counts'])
    else:
        # get top words
        counter = Counter()
        for message in messages:
            tokens = tokenize(message)
            for token in tokens:
                counter[token] += 1
        # top 20 words
        top = counter.most_common(20)
        top_words = [word[0] for word in top]
        top_counts = [count[1] for count in top]
        # save arrays
        np.savez(filepath, top_words=top_words, top_counts=top_counts)
        return list(top_words), list(top_counts)


# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('DisasterResponse', engine)

# load model
model = joblib.load("../models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    category_requests_total = df.iloc[:, 4:].sum()
    category_names = list(category_requests_total.index)
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
     # Top 20 word counts
    word_counts_path = "../data/counts.npz"
    word_counts = compute_word_counts(df['message'].tolist(), False, word_counts_path)
    top_20_words = word_counts[0]
    top_20_counts = word_counts[1]    
    
    
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        }
        ,{
            'data': [
                Bar(
                    x=category_names,
                    y=category_requests_total,
                )
            ],

            'layout': {
                'title': 'Distribution of categories',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {

                },
            }
        }
        ,
        {
            'data': [
                Bar(
                    x=top_20_words,
                    y=top_20_counts
                )
            ],

            'layout': {
                'title': 'Top 20 Word Counts',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Words"
                }
            }
        }
        
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()