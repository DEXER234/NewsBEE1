import streamlit as st
import requests
import json
import hashlib
import datetime  # Add this import at the top of your file

# Global variables for categories
categories = ['General', 'Business', 'Health', 'Sports', 'Technology']
API_KEY = "08c6016dd4c84ab29d292a2efab337cc"  # Replace with your NewsAPI key
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


# Hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Load existing users from the JSON file
def load_users():
    try:
        with open("users.json", "r") as file:
            data = json.load(file)
        return data.get("users", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        st.error("Error loading users. Please check the users.json file.")
        return []  # Return an empty list if there's an error


# Save new users to the JSON file
def save_users(users):
    try:
        with open("users.json", "w") as file:
            json.dump({"users": users}, file)
    except IOError:
        st.error("Error saving users. Please check your file permissions.")


# User signup
def signup():
    st.subheader("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up", key="signup_button"):
        if username and password:
            users = load_users()
            if any(user['username'] == username for user in users):
                st.error("Username already exists!")
            else:
                users.append({
                    "username": username,
                    "password": hash_password(password)
                })
                save_users(users)
                st.success("Signup successful! Please log in.")
        else:
            st.warning("Please fill in all fields.")


# User login
def login():
    st.subheader("Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log In", key="login_button"):
        users = load_users()
        hashed_pw = hash_password(password)
        if any(user['username'] == username and user['password'] == hashed_pw for user in users):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password!")


# Fetch news articles using NewsAPI
def fetch_news(category="general"):
    params = {
        'category': category.lower(),
        'country': 'us',
        'apiKey': API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return articles
    else:
        st.error(f"Failed to fetch news. Status code: {response.status_code}. Please check your API key.")
        return []


# Display news articles
def display_articles(articles):
    if not articles:
        st.warning("No articles found.")
        return
    for index, article in enumerate(articles):
        st.subheader(article['title'])
        if article.get('urlToImage'):
            st.image(article['urlToImage'], use_container_width=True)
        st.write(article.get('description', "No description available."))
        st.write("---")
        
        # Updated to use a button for "Read more"
        if st.button("Read more", key=f"read_more_button_{index}"):
            st.write(f"[Link to article]({article['url']})")  # Optionally, you can keep the link for reference
        
        # Share button functionality
        if st.button("Share", key=f"share_button_{index}"):
            st.write("Share this article:")
            st.markdown("""
                <a href="https://www.facebook.com/sharer/sharer.php?u={}" target="_blank">
                    <i class='bx bxl-facebook-circle' style='font-size: 24px;'></i>
                </a>
                <a href="https://twitter.com/intent/tweet?url={}" target="_blank">
                    <i class='bx bxl-twitter' style='font-size: 24px;'></i>
                </a>
                <a href="https://www.linkedin.com/shareArticle?mini=true&url={}" target="_blank">
                    <i class='bx bxl-linkedin' style='font-size: 24px;'></i>
                </a>
                <a href="mailto:?subject=Check this article&body={}" target="_blank">
                    <i class='bx bxl-email' style='font-size: 24px;'></i>
                </a>
                <a href="https://api.whatsapp.com/send?text={}" target="_blank">
                    <i class='bx bxl-whatsapp' style='font-size: 24px;'></i>
                </a>
            """.format(article['url'], article['url'], article['url'], article['url'], article['url']), unsafe_allow_html=True)


def main():
    st.title("NewsBee-In")
    
    # Add company logo
    st.image("C:\ONP\logo-transparent-png.png", use_container_width=True)  # Updated to use use_container_width

    # Include Boxicons CSS for icons
    st.markdown("""
        <link href='https://unpkg.com/boxicons@2.1.1/css/boxicons.min.css' rel='stylesheet'>
    """, unsafe_allow_html=True)

    # User Authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Add company icon to the sidebar
    st.sidebar.image("C:\ONP\logo-transparent-png.png", use_container_width=True)  # Updated to use use_container_width

    # Display today's date and time in the sidebar
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
    st.sidebar.write(f"**Current Date and Time:** {current_time}")  # Display date and time

    if not st.session_state.logged_in:
        # Updated to use radio buttons for Login/Signup
        option = st.sidebar.radio("Login/Signup", ["Login", "Sign Up"])
        if option == "Login":
            login()
        else:
            signup()
    else:
        st.sidebar.success(f"Welcome, {st.session_state.username}!")
        if st.sidebar.button("Log Out"):
            st.session_state.logged_in = False
        
        # News Portal Interface
        st.header("Latest News")
        
        # Category Selection
        category = st.sidebar.radio("Select Category", categories)
        articles = fetch_news(category)
        display_articles(articles)


if __name__ == "__main__":
    main()
