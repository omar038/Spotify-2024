import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Artists",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg"
)



with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", width=120)
st.sidebar.title("Spotify Analysis")
st.sidebar.markdown("""
Dive into the world of Spotify's artists, and genres.

*Search your favorite artist to find where they shine.*
*Discover the most popular genres and artists.*

Enjoy an interactive and insightful look into music analytics!🎶
""")
st.title("Spotify Tracks Analysis")

df = pd.read_csv("Spotify2024_with_genres_and_covers.csv")

df['Release Date'] = pd.to_datetime(df['Release Date'])

col1 , col2 =st.columns(2)
with col1:
    # Count top 20 genres
    genre_count = df['Genre'].value_counts().head(20).reset_index()
    genre_count.columns = ['Genre', 'Count']
    # Create pie chart
    fig = px.pie(
        genre_count,
        names='Genre',
        values='Count',
        title='Top 20 Genres by Number of Tracks',
        color_discrete_sequence=px.colors.sequential.Greens  # Optional: green gradient
    )
    # Remove background and grid
    fig.update_layout(

        plot_bgcolor='rgba(0,0,0,0)',  # transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # transparent around the chart
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    # Show chart
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Count top 10 artists
    artist_count = df['Artist'].value_counts().reset_index().head(10)
    artist_count.columns = ['Artist', 'Count']  # Rename columns
    fig = px.bar(
        artist_count,
        x='Artist',
        y='Count',
        title='Top 10 Artists with Most Tracks',
        color_discrete_sequence=['#1DB954']  # Optional: Spotify green
    )
    fig.update_layout(
        width=500,
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',  # remove chart background
        paper_bgcolor='rgba(0,0,0,0)',  # remove around chart
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)


# Artist search input
artist_name = st.text_input("Search by Artist Name")

# Filter the DataFrame by artist name (case-insensitive, partial match)
if artist_name:
    filtered_df = df[df['Artist'].str.contains(artist_name, case=False, na=False)]

    if not filtered_df.empty:
        st.markdown(f"### Results for '{artist_name}'")
        st.dataframe(filtered_df)
    else:
        st.warning("No tracks found for that artist.")
