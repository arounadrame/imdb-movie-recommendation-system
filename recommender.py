import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    """
    Content-based movie recommendation system using TF-IDF and cosine similarity.
    """

    def __init__(self, data_path: str):
        """
        Initialize the recommender system.

        Parameters
        ----------
        data_path : str
            Path to the cleaned movie dataset.
        """
        self.df = pd.read_csv(data_path)
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self._build_model()

    def _build_model(self):
        """
        Build the TF-IDF matrix and compute cosine similarity.
        """
        tfidf = TfidfVectorizer(
            stop_words="english",
            max_features=5000
        )

        # Vectorize combined text features
        self.tfidf_matrix = tfidf.fit_transform(
            self.df["combined_features"]
        )

        # Compute cosine similarity between all movies
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)

    def get_recommendations(self, movie_title: str, top_n: int):
        """
        Get top-N movie recommendations similar to the given movie.

        Parameters
        ----------
        movie_title : str
            Title of the reference movie.
        top_n : int, optional
            Number of recommendations to return (default=5).

        Returns
        -------
        pd.DataFrame
            DataFrame containing recommended movies.
        """
        if movie_title not in self.df["Series_Title"].values:
            raise ValueError("Movie title not found in dataset.")

        # Get index of the selected movie
        movie_idx = self.df[
            self.df["Series_Title"] == movie_title
        ].index[0]

        # Get similarity scores for this movie
        similarity_scores = list(
            enumerate(self.similarity_matrix[movie_idx])
        )

        # Sort movies by similarity score
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        # Exclude the movie itself
        similarity_scores = similarity_scores[1: top_n + 1]

        # Get movie indices
        movie_indices = [i[0] for i in similarity_scores]
        similarity_values = [s[1] for s in similarity_scores]

        # Return recommendations
        
        results = self.df.loc[
            movie_indices,
            ["Series_Title", "Genre", "IMDB_Rating", "Poster_Link", "Overview"]
            ].copy()
        
        results["Similarity"] = similarity_values 
        
        return results.reset_index(drop=True)
