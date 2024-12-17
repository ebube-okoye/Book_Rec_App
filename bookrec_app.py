import streamlit as st
from openai import OpenAI
import os

# Setting up OpenAI API key

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key= api_key)

st.title('Book Recommendation Assistant 📚')
st.write('Get book recommendations based on your favorite genres and books!')

# Sidebar for user input
genre = st.sidebar.selectbox(
    'Select a genre:', 
    ['Fantasy', 'Science Fiction', 'Romance', 'Mystery', 'Thriller', 'Horror', 
     'Non-fiction', 'Historical Fiction', 'Young Adult', 'Classics']
)

similar_book = st.sidebar.text_input('Enter a book you liked (optional):')

recommendations = st.empty()

# Generate recommendations when button is clicked
if st.sidebar.button('Get Recommendations'):
    with st.spinner('Fetching recommendations...'):
        try:
            # Determine the prompt based on user input
            if similar_book.strip():
                prompt = (
                    f"Recommend 5 books similar to '{similar_book}' in the {genre} genre. "
                    "Include the title and author of each book."
                )
            else:
                prompt = (
                    f"Recommend 5 must-read books in the {genre} genre. "
                    "Include the title and author of each book."
                )

            # Use OpenAI to get book recommendations
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in book recommendations."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Display the recommendations
            recommendations.write(completion.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")
