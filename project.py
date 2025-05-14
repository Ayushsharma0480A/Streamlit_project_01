import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from pygments.lexers.sql import language_re


#loading dataset
def load_dataset():
    return pd.read_csv("data.csv")
df= load_dataset()
st.title("Indian Movies Analysis Dashboard")
#search movie -partal or full
st.subheader("Search for a movie")
search_query=st.text_input("Enter a movie name(partial or full, case-insensitive)")
if search_query:
    search_result=df[df["Movie Name"].str.contains(search_query,case=False,na=False)]
    #this is filter condition
    if not search_result.empty:
        st.write(f" Found {len(search_result)} movie(s)")
        st.dataframe(search_result[["Movie Name", "Year", "Rating(10)", "Votes", "Genre", "Language"]])
    else:
        st.write("No results found")

st.sidebar.header("Filters")
genre_filter=st.sidebar.multiselect("Select Genre",df["Genre"].unique(),default=[])
if genre_filter:
    df=df[df["Genre"].isin(genre_filter)]

language_filter=st.sidebar.multiselect("Select Language",df["Language"].unique(),default=[])
if language_filter:
    df=df[df["Language"].isin(language_filter)]
year_filter=st.sidebar.slider("select year range",int(df["Year"].min()),int(df["Year"].max()),(1950,2025))
df=df[(df["Year"].between(*year_filter))]
st.subheader("fitered data")
st.dataframe(df)
rating_filter=st.sidebar.slider("Select Rating Range ", float(df["Rating(10)"].min()),float(df["Rating(10)"].max()), (0.0,10.0))
df=df[df["Rating(10)"].between(*rating_filter)]
st.subheader("visualizations")
st.subheader("Visualizations")
visualization_option=st.selectbox("Select a visualization or analysis condition",
             [
                 "Top 10 Movies by Rating",
                 "Top 10 Movies by Votes",
             ])
if visualization_option=="Top 10 Movies by Rating":
    st.markdown("### Top 10 Movies by Rating")
    top_movies_by_rating=df.sort_values(by="Rating(10)",ascending=False).head(10)
    st.write("Table: Top 10 Movies by Rating")
    st.dataframe(top_movies_by_rating)
    st.write("Bar Chart: Top 10 Movies by Rating")
    fig=px.bar(top_movies_by_rating, x="Movie Name", y="Rating(10)", title="Top 10 Movies by Rating")
    st.plotly_chart(fig)

elif visualization_option=="Top 10 Movies by Votes":
    st.markdown("### Top 10 Movies by Votes")
    top_movies_by_votes=df.sort_values(by="Votes",ascending=False).head(10)
    st.write("Table: Top 10 Movies by Votes")
    st.dataframe(top_movies_by_votes)
    st.write("Pie Chart: Top 10 Movies by Votes")
    fig=px.pie(top_movies_by_votes, names="Movie Name", values="Votes", title="Top 10 Movies by Votes")
    st.plotly_chart(fig)
