import pandas as pd
import numpy as np
try:
    df = pd.read_csv("clustered_movies.csv")
    df['title_lower'] = df['title'].str.lower()
except Exception as e:
    print("Error loading dataset:", e)
    df = pd.DataFrame(columns=['title', 'dbscan_clusters', 'title_lower'])

def recommend_similar(title):
    title = title.strip().lower()
    
    # Use lowercase for comparison
    df['title_lower'] = df['title'].str.lower()

    if title not in df['title_lower'].values:
        return [" Movie not found in dataset"]

    cluster_id = df[df['title_lower'] == title]['dbscan_clusters'].values[0]

    if cluster_id == -1:
        return ["No similar movies found (noise cluster)"]

    similar = df[(df['dbscan_clusters'] == cluster_id) & (df['title_lower'] != title)]

    return similar['title'].head(5).tolist()



