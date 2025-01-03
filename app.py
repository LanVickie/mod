import streamlit as st
from openai import OpenAI
import json

# Function to serialize the output
def serialize(obj):
    """Recursively walk object's hierarchy."""
    if isinstance(obj, (bool, int, float, str)):
        return obj
    elif isinstance(obj, dict):
        obj = obj.copy()
        for key in obj:
            obj[key] = serialize(obj[key])
        return obj
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(serialize(item) for item in obj)
    elif hasattr(obj, '__dict__'):
        return serialize(obj.__dict__)
    else:
        return repr(obj)  # Don't know how to handle, convert to string

# Access the OpenAI API key from Streamlit secrets
api_key = st.secrets["openai_secret"]
api_url = st.secrets["openai_url"]
work_email = st.secrets["work_email"]
private_email = st.secrets["my_email"]

# Initialize the OpenAI client with the API key from secrets
client = OpenAI(base_url=api_url, api_key=api_key)

# Streamlit UI components
st.title("OpenAI Moderation API Demo")
# Show different content based on the user's email address.
if st.experimental_user.email == work_email:
    display_jane_content()
elif st.experimental_user.email == private_email:
    display_adam_content()
else:
    st.write("Please contact us to get access!")

# Get dictionaries of cookies and headers
st.context.cookies
st.context.headers

user_input = st.text_area("Enter text to moderate")

if st.button('Moderate'):
    response = client.moderations.create(input=user_input)
    output = response.results[0]
    serialized_output = serialize(output)
    json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)
    st.json(json_output)
