# DS4200-Project
# DS4200 – Spotify Listening History Visualization

A data visualization project for DS4200 (Information Presentation & Visualization) at Northeastern University, exploring personal Spotify streaming history through interactive charts.

## Overview

This project analyzes Spotify listening data across multiple accounts/time periods to uncover patterns in music consumption — by month, year, and genre.

## Visualizations

- **Heatmap** (`heatmap.html`) — listening activity broken down by month and year, built with Altair
- **Sankey Diagram** (`sankey.html`) — flow from months to top music genres, built with Plotly

## Data

- Multiple Spotify streaming history CSV files (`streaming_history.csv`, `spotify_history 2.csv`, etc.)
- `track_data_final.csv` — enriched track data including artist genres
- `Platform_usage.csv` — platform-level usage data

## Tech Stack

- **Python** — data processing (`pandas`, `altair`, `plotly`)
- **HTML/CSS/JS** — front-end presentation pages

## How to Run

```bash
pip install pandas altair plotly
python visualizations.py
```

This generates `heatmap.html` and `sankey.html`, which can be opened directly in a browser.

## Project Structure

```
├── data.py                  # Data loading & cleaning utilities
├── visualizations.py        # Main visualization scripts
├── visualization_1/2.py     # Additional charts
├── index.html               # Portfolio landing page
├── heatmap.html             # Generated heatmap
├── sankey.html              # Generated Sankey diagram
└── *.csv                    # Spotify & track data
```
