import streamlit as st


# Define a function to check login credentials
def authenticate(username, password):
    if username == "admin" and password == "password":
        return True
    else:
        return False


# Create a Streamlit app
def main():
    st.title("Login Page")
    st.write("Please enter your credentials to log in.")

    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Create a login button to submit the credentials
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Logged in as {}".format(username))
            # Redirect to home page or another app
        else:
            st.error("Incorrect username or password")


if __name__ == "__main__":
    main()