import pandas as pd

df = pd.read_pickle('pickle/data.pkl')

indices = pd.read_pickle('pickle/indices.pkl')

cosine_sim2 = pd.read_pickle('pickle/cosine_similarity_matrix.pkl')

data_dict = pd.read_pickle("pickle/new_dict.pkl")


# Function to get data from the data_dict based on an array of indices, returning a dictionary of dictionaries
def get_data(arr: list) -> list:
    return [{**data_dict[i], "id": i} for i in arr]


# Function to get recommendations based on a movie ID and cosine similarity matrix
def get_recommendations(movie_ids: list, cosine_sim=cosine_sim2, top_n=10) -> list:
    combined_recommendations = set()

    for movie_id in movie_ids:
        try:
            # Get the index of the movie that matches the ID
            idx = indices[movie_id]
        except KeyError:
            print(f"Movie ID {movie_id} not found in indices.")
            continue

        # Get the pairwise similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the top_n most similar movies
        sim_scores = sim_scores[1:top_n + 1]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Get the movie IDs for the recommended movies and add to the set
        recommended_ids = df['id'].iloc[movie_indices].tolist()
        
        combined_recommendations.update(recommended_ids)
    
    return list(combined_recommendations)
    # Return the data for the combined recommendations as a dictionary of dictionaries
   