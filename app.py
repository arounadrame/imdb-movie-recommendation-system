import streamlit as st
from recommender import MovieRecommender

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

col1, col2 = st.columns([1, 14])

with col1:
    st.image("imdb-logo.png", width=150)

with col2:
    st.markdown(
        "<h1 style='margin-bottom:0;'>Movie Recommendation System</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color:#b3b3b3;'>This app recommends movies, based on content similarity using TF-IDF and cosine similarity.</p>",
        unsafe_allow_html=True
    )
    st.markdown("🌟 Based on IMDB Top 1000 movies 🌟")

# --------------------------------------------------
# Load recommender (cached)
# --------------------------------------------------
@st.cache_resource
def load_recommender():
    return MovieRecommender("movies_cleaned.csv")

recommender = load_recommender()

# --------------------------------------------------
# Movie selection
# --------------------------------------------------
movie_list = recommender.df["Series_Title"].sort_values()
selected_movie = st.selectbox(
    "Select a movie you like:",
    movie_list
)

# --------------------------------------------------
# Recommendation button
# --------------------------------------------------
if st.button("Recommend movies 🎥"):
    recommendations = recommender.get_recommendations(
        selected_movie,
        top_n=10 # Number of movies displayed
    )

    st.subheader("Recommended movies for you")

        # Display recommendations in rows of 5
    for i in range(0, len(recommendations), 5):
        cols = st.columns(5)

        for col, (_, row) in zip(cols, recommendations.iloc[i:i+5].iterrows()):
            with col:
                st.image(row["Poster_Link"], width="content")
                st.markdown(f"**{row['Series_Title']}**")
                st.markdown(
                f"<span class='rating'>⭐ IMDb: {row['IMDB_Rating']}</span>",
                unsafe_allow_html=True
                )
                st.caption(row["Genre"])

                st.caption(f"🔍 Similarity: {row['Similarity']:.2f}")

                with st.expander("Overview"):
                    st.write(row["Overview"])


