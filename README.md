# 🎧 Spotify Dashboard

🌐 [Live Demo](https://spotify-2024-038.streamlit.app/) – Try the app on Streamlit Cloud!

An interactive web dashboard built with **Streamlit** and **Plotly**, designed to explore and visualize Spotify's most popular tracks and artists. This project scrapes and analyzes track metadata, genres, album covers, and popularity metrics from Spotify's API to provide dynamic visual insights.

---

## 🚀 Features

- 🔍 **Searchable Song Info**: Look up any track to view its album art, genre, popularity, and a custom "Track Score" gauge.
- 📊 **Top Charts**: Interactive bar charts for the most streamed songs and artists.
- 🧭 **Dashboard Metrics**: High-level stats on total streams, genres, playlists, and track count.
- 🎨 **Custom Styling**: The dashboard includes tailored visuals using a CSS stylesheet for a clean aesthetic.
- 🧠 **Data Enrichment**: Automated genre and album cover scraping using the Spotify API.

---
## Tracks Dashboard
![Dashboard](https://github.com/omar038/Spotify-2024/blob/main/Gif/Tracks.gif)

## Artists Dashboard
![Dashboard](https://github.com/omar038/Spotify-2024/blob/main/Gif/Artists.gif)


## 🛠 Tech Stack

- Python
- Streamlit
- Plotly
- Pandas
- Spotify Web API

---

## 📂 File Overview

| File                          | Description                                           |
|------------------------------|-------------------------------------------------------|
| `Tracks.py`                  | Main dashboard script                                 |
| `style.css`                  | Custom styling for Streamlit app                     |
| `GenreAndCover scraping.py`  | Script to enrich the dataset using Spotify API        |
| `Spotify2024_with_genres_and_covers.csv` | Final processed dataset                    |

---

## 📦 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/spotify-dashboard.git
   cd spotify-dashboard

## Check it out & Try it Yourself https://spotify-2024-038.streamlit.app/
