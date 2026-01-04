#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler


# In[5]:


df_movies = pd.read_csv('titles.csv')
df_movies.head(2)


# In[6]:


df_movies = df_movies.drop_duplicates()


# In[8]:


df_movies['production_countries']


# In[9]:


df_movies['production_countries'] = df_movies['production_countries'].str.replace(r"\[", '', regex=True).str.replace(r"'", '', regex=True).str.replace(r"\]", '', regex=True)
df_movies['lead_prod_country'] = df_movies['production_countries'].str.split(',').str[0]
df_movies['prod_countries_cnt'] = df_movies['production_countries'].str.split(',').str.len()
df_movies['lead_prod_country'] = df_movies['lead_prod_country'].replace('', np.nan)


# In[10]:


df_movies['lead_prod_country']


# In[11]:


df_movies['genres'] = df_movies['genres'].str.replace(r"\[", '', regex=True).str.replace(r"'", '', regex=True).str.replace(r"\]", '', regex=True)
df_movies['main_genre'] = df_movies['genres'].str.split(',').str[0]
df_movies['main_genre'] = df_movies['main_genre'].replace('', np.nan)


# In[12]:


df_movies['main_genre']


# In[13]:


df_movies.drop(['genres', 'production_countries'], axis=1, inplace=True)


# In[14]:


df_movies.isnull().sum()


# In[15]:


df_movies['runtime'].fillna(df_movies['runtime'].mean(), inplace=True)
df_movies['imdb_score'].fillna(df_movies['imdb_score'].mean(), inplace=True)
df_movies['imdb_votes'].fillna(0, inplace=True)
df_movies['tmdb_popularity'].fillna(0, inplace=True)
df_movies['tmdb_score'].fillna(df_movies['tmdb_score'].median(), inplace=True)
df_movies['seasons'].fillna(0, inplace=True)
df_movies.dropna(subset=['title'],inplace=True)

df_movies['lead_prod_country'].fillna('Unknown', inplace=True)
df_movies['main_genre'].fillna('Unknown', inplace=True)

print(df_movies.isna().sum())


# In[16]:


from sklearn.preprocessing import MinMaxScaler
numerical_cols = ['release_year', 'runtime', 'seasons', 'imdb_score',
                  'imdb_votes', 'tmdb_popularity', 'tmdb_score', 'prod_countries_cnt']
scaler = MinMaxScaler()
df_movies[numerical_cols] = scaler.fit_transform(df_movies[numerical_cols])

df_movies_encoded = pd.get_dummies(df_movies, columns=['type', 'lead_prod_country', 'main_genre'], drop_first=True)

print(f"Processed dataset shape: {df_movies_encoded.shape}")


# In[ ]:


dummies = pd.get_dummies(df_movies[['type', 'lead_prod_country', 'main_genre']], drop_first=True)
df_movies_dum = pd.concat([df_movies, dummies], axis=1)
df_movies_dum.drop(['type', 'lead_prod_country', 'main_genre'], axis=1, inplace=True)

from sklearn.preprocessing import MinMaxScaler

cols_to_drop = ['title', 'id'] 
df_cleaned = df_movies_dum.drop(columns=cols_to_drop, errors='ignore')

categorical_cols = df_cleaned.select_dtypes(include='object').columns
df_cleaned = pd.get_dummies(df_cleaned, columns=categorical_cols, drop_first=True)

scaler = MinMaxScaler()
df_scaled_array = scaler.fit_transform(df_cleaned)
df_scaled = pd.DataFrame(df_scaled_array, columns=df_cleaned.columns)

df_scaled.head()


# In[19]:


from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

eps_array = [0.2, 0.5, 1]
min_samples_array = [5, 10, 30]

for eps in eps_array:
    for min_samples in min_samples_array:
        clusterer = DBSCAN(eps=eps, min_samples=min_samples).fit(df_scaled)
        cluster_labels = clusterer.labels_
        unique_labels = set(cluster_labels)

        if len(unique_labels) == 1:
            print(f"Skipped: eps={eps}, min_samples={min_samples}, labels={unique_labels}")
            continue

        silhouette_avg = silhouette_score(df_scaled, cluster_labels)
        print("For eps =", eps,
              "For min_samples =", min_samples,
              "Number of clusters =", len(unique_labels) - (1 if -1 in unique_labels else 0),
              "Average silhouette_score =", silhouette_avg)



# In[20]:


dbscan_model = DBSCAN(eps=1, min_samples=5).fit(df_scaled)
print("For eps =", 1,
      "For min_samples =", 5,
      "Count clusters =", len(set(dbscan_model.labels_)),
      "The average silhouette_score is :", silhouette_score(df_scaled, dbscan_model.labels_))


# In[21]:


df_movies['dbscan_clusters'] = dbscan_model.labels_
df_movies.head(10)


# In[23]:


df_movies[['title', 'dbscan_clusters']].to_csv("clustered_movies.csv", index=False)


# In[88]:


df_movies['dbscan_clusters'] = dbscan_model.labels_
df_movies['dbscan_clusters'].value_counts()

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN

df_movies['dbscan_clusters'] = dbscan_model.fit_predict(df_scaled)

pca = PCA(n_components=2)
df_pca = pca.fit_transform(df_scaled)
df_movies['pca1'] = df_pca[:, 0]
df_movies['pca2'] = df_pca[:, 1]

plt.figure(figsize=(10, 8))

sns.scatterplot(data=df_movies, x='pca1', y='pca2', hue='dbscan_clusters', palette='Set1', s=100, alpha=0.7, edgecolor='w', legend=None)

plt.title('DBSCAN Clusters Visualization', fontsize=16)
plt.xlabel('Principal Component 1', fontsize=12)
plt.ylabel('Principal Component 2', fontsize=12)
plt.show()


# In[96]:


import random

def recommend_movie(movie_name: str):
    movie_name = movie_name.lower()

    df_movies['title_lower'] = df_movies['title'].astype(str).str.lower()

    movie = df_movies[df_movies['title_lower'].str.contains(movie_name, na=False)]

    if not movie.empty:
        cluster = movie['dbscan_clusters'].values[0]

        cluster_movies = df_movies[df_movies['dbscan_clusters'] == cluster]

        if len(cluster_movies) >= 5:
            recommended_movies = random.sample(list(cluster_movies.index), 5)
        else:
            recommended_movies = list(cluster_movies.index)

        print('--- We can recommend you these movies ---')
        for m in recommended_movies:
            print(df_movies.loc[m, 'title'])
    else:
        print('Movie not found in the database.')


# In[97]:


s = input('Input movie name: ')
print("\n\n")
recommend_movie(s)


# In[25]:


import pandas as pd

df_clustered = pd.read_csv("clustered_movies.csv")
df_clustered.head(10)  

