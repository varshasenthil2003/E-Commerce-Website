import streamlit as st

def home():
    pass

def about():
    pass
def contact():
    pass

# Create a dictionary of page names and their corresponding functions
pages = {
    "Home": home(),
    "About": about(),
    "Contact": contact()
}
st.markdown("""
<div style="background-color: #f2f2f2; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
    <p>This is some text inside the div box.</p>
</div>""",unsafe_allow_html=True)


