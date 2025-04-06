import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go



st.set_page_config(
    layout="wide",
    page_title="Spotify Analysis",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg"
)


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load dataset
file_path = "Spotify2024_with_genres_and_covers.csv"
df = pd.read_csv(file_path)

df['Genre'] = df['Genre'].fillna('POP')
# Convert necessary columns to appropriate types
df["Release Date"] = pd.to_datetime(df["Release Date"], errors='coerce')
df["Spotify Streams"] = pd.to_numeric(df["Spotify Streams"].str.replace(',', ''), errors='coerce')
df["Track Score"] = pd.to_numeric(df["Track Score"], errors='coerce')
df['Spotify Playlist Count'] = pd.to_numeric(df['Spotify Playlist Count'], errors='coerce').fillna(0)

# Sidebar Navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", width=120)
st.sidebar.title("Spotify Analysis")
st.sidebar.markdown("""
Welcome to the **Spotify Dashboard** 🎧  
Explore the most streamed songs and artists, track scores, and genres.

Use the navigation below to switch.
""")

st.write("# Songs Dashboard")
# Overview Section
c1 , c2 ,c3 , c4 =st.columns(4)

with c1:
    st.metric('Number of streams', f"{df['Spotify Streams'].sum() / 1_000_000_000:.0f}B")
with c2:
    st.metric('Number Of Tracks',f"{df['Track'].nunique() / 1_000:}K")
with c3:
    st.metric('Number of Genres',f"{df['Genre'].nunique():,}")
with c4:
    st.metric('Number of Playlists',f"{df['Spotify Playlist Count'].sum() / 1_000_00:.2f}M")

top_tracks = (
    df.groupby("Track", as_index=False)["Spotify Streams"].sum()  # Sum streams for duplicate tracks
    .sort_values(by="Spotify Streams", ascending=False)  # Sort by streams
    .head(10)  # Get the top 10 tracks
)

st.subheader("Top 10 Most Streamed Tracks")

# Define your custom light and dark green color palette
custom_colors = ["#A8E6A3", "#5C9E5C"]  # Light green and dark green

# Create the bar chart with the grouped data
fig = px.bar(
    top_tracks,
    x="Track",
    y="Spotify Streams",
    title=" ",
    color_discrete_sequence=custom_colors  # Apply the custom color palette
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Removes the inner plot background
    paper_bgcolor='rgba(0,0,0,0)'  # Removes the outer chart background
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

#search bar
search_query = st.text_input("Search for a song", "")
search_results = df[df["Track"].str.contains(search_query, case=False, na=False)] if search_query else df
if not search_results.empty:
        song = search_results.iloc[0]
        st.subheader(f"{song['Track']} - {song['Artist']}")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if pd.notna(song["Album Cover URL"]):
                st.image(song["Album Cover URL"], width=200)
        
        with col2:
            st.write(f"**Release Date:** {song['Release Date'].date()}")
            st.write(f"**Streams:** {song['Spotify Streams']:,}")
            st.write(f"**Genre:** {song['Genre'] if pd.notna(song['Genre']) else 'Unknown'}")
            st.write(f"**Popularity:** {song['Spotify Popularity']}")
        with col3:
         
            track_score = song["Track Score"] if pd.notna(song["Track Score"]) else 0
            gauge_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=track_score,
                title={"text": "Track Score", "font": {"color": "#3B6207"}},
                gauge={
                    "axis": {"range": [0, 1000]},
                    "bar": {"color": "#8FBC30"},


                }
                ,
                number={"font": {"color": "#72AB78"}}
                
            ))
            gauge_fig.update_layout(
            width=300,  # Set the width of the chart
            height=250,  # Set the height of the chart
            plot_bgcolor='rgba(0,0,0,0)',  # Removes the inner plot background
            paper_bgcolor='rgba(0,0,0,0)'  # Removes the outer chart background
    )
            # Display the gauge chart in Streamlit
            st.plotly_chart(gauge_fig , use_container_width=True)