from flask import Flask, render_template, jsonify, request

import pandas as pd
import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/')
def method_name():
    return render_template('index.html')

@app.route('/searchTitle', methods=["POST"])
def searchTitle():
    title = request.form["title"]
    respTable = table(title)
    print(jsonify(respTable))
    return jsonify(respTable)

# ----------------------------------------------------------------------------------------------------
# Modelo IA
# Funciones para la IA
target = os.path.join(app.static_folder, 'movies.csv')
movies = pd.read_csv(target)

target2 = os.path.join(app.static_folder, 'ratings.csv')
ratings = pd.read_csv(target2)

def clean_title(title):
    return re.sub("[():]", "", title)

movies["clean_title"] = movies["title"].apply(clean_title)

vectorizer = TfidfVectorizer(ngram_range=(1,2))

tfidf = vectorizer.fit_transform(movies["clean_title"])

def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    print(results)
    return results

def table(titleMovie):
    resp = search(titleMovie)
    movie_id = resp.iloc[0]["movieId"]
    similars = find_similar_movies(movie_id)
    print(similars)
    df = pd.DataFrame(resp)
    similars_recs =  pd.DataFrame(similars)
    table = df.to_html(index=False)
    tableRecs = similars_recs.to_html(index=False)
    # print(tableRecs)
    return (table,tableRecs)

def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
        
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(7).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]
