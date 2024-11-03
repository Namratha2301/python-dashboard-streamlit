import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown(f'<style>{open("styles.css").read()}</style>', unsafe_allow_html=True)
# Set page config
st.set_page_config(page_title="Best Selling Books Dashboard", layout="wide")

# Function to load data
@st.cache_data
def load_data():
    data = pd.read_csv("best-selling-books.csv")
    data['Genre'].fillna('Unknown', inplace=True)
    data['First published'] = pd.to_datetime(data['First published'], errors='coerce', format='%Y')
    data.dropna(subset=['First published'], inplace=True)
    return data

# Function to plot sales trend
def plot_sales_trend(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['First published'], data['Approximate sales in millions'], color='saddlebrown', linewidth=2)
    plt.title('Best Selling Books: First Published vs Sales', fontsize=16)
    plt.xlabel('Years')
    plt.ylabel('Sales in Millions')
    plt.grid()
    st.pyplot(plt)

# Function to display top selling books
def display_top_selling_books(data):
    data_sales = data.sort_values(by='Approximate sales in millions', ascending=False).head(10)
    st.bar_chart(data_sales.set_index('Book')['Approximate sales in millions'])

# Function to display top authors
def display_top_authors(data):
    top_authors = data.groupby('Author(s)')['Approximate sales in millions'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_authors)

# Function to display genre distribution
def display_genre_distribution(data):
    genre_counts = data['Genre'].value_counts().head(10)
    plt.figure(figsize=(10, 8))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="YlOrBr")
    plt.title('Top 10 Genres in Best-Selling Books', fontsize=16)
    plt.xlabel('Count')
    plt.ylabel('Genre')
    st.pyplot(plt)

# Function to plot sales trend by publication year
def plot_sales_by_decade(data):
    data['Decade'] = (data['First published'].dt.year // 10) * 10
    decade_sales = data.groupby('Decade')['Approximate sales in millions'].sum()
    
    plt.figure(figsize=(12, 6))
    decade_sales.plot(kind='bar', color='#D2691E')
    plt.title('Total Sales per Decade')
    plt.xlabel('Decade')
    plt.ylabel('Total Sales (Millions)')
    st.pyplot(plt)

# Main Streamlit app
def main():
    st.title("Best Selling Books Dashboard")
    st.sidebar.header("Data Selection")
    
    # Load data
    data = load_data()

    st.subheader("Sales Trend")
    plot_sales_trend(data)

    st.subheader("Top Selling Books")
    display_top_selling_books(data)

    st.subheader("Top Authors")
    display_top_authors(data)

    st.subheader("Genre Distribution")
    display_genre_distribution(data)

    st.subheader("Sales by Decade")
    plot_sales_by_decade(data)

if __name__ == "__main__":
    main()
