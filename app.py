# Import libraries
import streamlit as st
import pandas as pd
import re

def convert_google_sheet_url(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)

    return new_url

# Replace with your modified URL
url = 'https://docs.google.com/spreadsheets/d/1OEF7hqNWgpVEy9xYT-S9F_MPeh9h8l_IhjNhph23u0Q/edit?usp=sharing'

new_url = convert_google_sheet_url(url)

print(new_url)
# https://docs.google.com/spreadsheets/d/1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg/export?gid=1606352415&format=csv

df = pd.read_csv(new_url, dtype=str)

# Page setup
st.set_page_config(page_title="Search for Homebrew Recipes", page_icon=":beers:", layout="wide")
st.title("Search for Homebrew Recipes.")
st.markdown(":beers::beers::beers: Stockpiles of brewing knowledge is locked in days and weeks of masterly crafted BrewTube videos. Find a good recipe and brew it. :beers::beers::beers:")

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("", value="Search videos by title or beer style. Start here.")

VIDEO_PATH = "./pour.mp4"
st.video(VIDEO_PATH, format="video/mp4", start_time=0)

# Filter the dataframe using masks
m1 = df["Title"].str.contains(text_search)
m2 = df["Description"].str.contains(text_search)
df_search = df[m1 | m2]

# Show the results, if you have a text_search
if text_search:
    for idx, row in df_search.iterrows():
        col1, col2 = st.columns([2, 3])  # Adjust the column widths as needed
        with col1:
            youtube_url = f"https://www.youtube.com/watch?v={row['Video ID']}"
            st.markdown(f'<a href="{youtube_url}" target="_blank"><img src="{row["Thumbnails"]}" width="500"></a>', unsafe_allow_html=True)
            st.markdown(f'**Click the thumbnail to watch video.**')
        with col2:
            st.markdown(f"**Title:** {row['Title']}")
            if row['Recipe']:
                st.markdown(f"**Recipe:**")
                st.code(row['Recipe'])
                #st.markdown(f"**Recipe:**\n<pre>{row['Recipe']}</pre>", unsafe_allow_html=True)
        st.markdown("---")

# Show the dataframe (we'll delete this later)
st.write(df)

