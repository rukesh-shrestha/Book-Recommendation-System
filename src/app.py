from flask import Flask,jsonify,request
import pandas as pd
import sqlite3 as sql
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import numpy as np
import json
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
from configuration import DATABASE_PATH

app = Flask(__name__)
connect = sql.connect(DATABASE_PATH)

database_table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'",connect)
data_rating = pd.read_sql_query("SELECT * from pages_myrating",connect)
books = pd.read_sql_query("SELECT * from pages_book",connect)

pivoted_data=data_rating.pivot_table(index='places_id',columns='user_id',values='rating').fillna(0)

features= csr_matrix(pivoted_data.values)

model = NearestNeighbors(metric='cosine',algorithm='brute')
model.fit(features)

@app.route('/recommend',methods=["POST","GET"])
def hello_world():
    users = request.form.get("user_id")
    user_id = int(users)
    distances,indices = model.kneighbors(pivoted_data.iloc[user_id,:].values.reshape(1,-1),n_neighbors=7)
    recommended_items = set()
    for i in range(0,len(distances.flatten())):
        if i == 0:
            print('Recommendations for {0}:\n'.format(pivoted_data.index[user_id]))
        else:
            print('{0}: {1}, with distance of {2}:'.format(i, pivoted_data.index[indices.flatten()[i]],distances.flatten()[i]))
            recommended_items.add(pivoted_data.index[indices.flatten()[i]])
    items = tuple(recommended_items)
    recommended = '{}'.format(items)
    return jsonify(recommended)


tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

# Filling NaNs with empty string
books['genre'] = books['genre'].fillna('')
tfv_matrix = tfv.fit_transform(books['genre'])
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
indices = pd.Series(books.index, index=books['name']).drop_duplicates()

@app.route('/recommending',methods=["POST","GET"])
def recommend(sig=sig):	
    content = request.form.get("query")

    # Get the index corresponding to original_title
    idx = indices[content]
    # Get the pairwsie similarity scores 
    sig_scores = list(enumerate(sig[idx]))
    # Sort the movies 
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    # Scores of the 7 most similar movies
    sig_scores = sig_scores[1:7]
    # Movie indices
    book_indices = [i[0] for i in sig_scores]
    
   
    value = books['name'].iloc[book_indices]
    items = dict(value)
    return jsonify(items)






if __name__=='__main__':
    app.run(debug=True)