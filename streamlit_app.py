import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config as the first Streamlit command
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
    plt.plot(data['First published'], data['Approximate sales in millions'], color='darkorange', linewidth=2)
    plt.title('Best Selling Books: First Published vs Sales', fontsize=16)
    plt.xlabel('Years')
    plt.ylabel('Sales in Millions')
    plt.grid()
    return plt

# Function to display top selling books
def display_top_selling_books(data):
    data_sales = data.sort_values(by='Approximate sales in millions', ascending=False).head(10)
    return data_sales.set_index('Book')['Approximate sales in millions']

# Function to display top authors
def display_top_authors(data):
    top_authors = data.groupby('Author(s)')['Approximate sales in millions'].sum().sort_values(ascending=False).head(10)
    return top_authors

# Function to display genre distribution
def display_genre_distribution(data):
    genre_counts = data['Genre'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette=["darkorange"])
    plt.title('Top 10 Genres in Best-Selling Books', fontsize=16)
    plt.xlabel('Count')
    plt.ylabel('Genre')
    return plt

# Function to plot sales trend by publication year
def plot_sales_by_decade(data):
    data['Decade'] = (data['First published'].dt.year // 10) * 10
    decade_sales = data.groupby('Decade')['Approximate sales in millions'].sum()
    
    plt.figure(figsize=(10, 6))
    decade_sales.plot(kind='bar', color='darkorange')
    plt.title('Total Sales per Decade', fontsize=16)
    plt.xlabel('Decade')
    plt.ylabel('Total Sales (Millions)')
    return plt

# Main Streamlit app
def main():
    st.title("Best Selling Books Dashboard")
    st.sidebar.header("Data Selection")
    
    # Load data
    data = load_data()

    # Create columns for layout
    col1, col2 = st.columns(2)

    # Display plots in the columns
    with col1:
        st.subheader("Sales Trend")
        st.pyplot(plot_sales_trend(data))

        st.subheader("Top Selling Books")
        st.bar_chart(display_top_selling_books(data))

    with col2:
        st.subheader("Top Authors")
        st.bar_chart(display_top_authors(data))

        st.subheader("Genre Distribution")
        st.pyplot(display_genre_distribution(data))

        st.subheader("Sales by Decade")
        st.pyplot(plot_sales_by_decade(data))

if __name__ == "__main__":
    main()
