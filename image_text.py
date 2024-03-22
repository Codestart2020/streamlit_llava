import json
import re
import requests
import streamlit as st
import base64

# API URL and headers
URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}


# Function to send request to the API
def send_request(prompt_text, images=None):
    data = {
        "model": "llava",
        "stream": False,
        "prompt": prompt_text,
        "images": [images] if images else None,
        "temperature": 0.2,
    }

    try:
        response = requests.post(URL, headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return f"HTTP error occurred: {err}"
    except Exception as err:
        return f"An error occurred: {err}"

    response_text = response.text
    data = json.loads(response_text)
    actual_response = data.get('response', '')
    actual_response = re.sub(r'\d', '', actual_response)
    return actual_response


# Streamlit app class
class App:
    def __init__(self):
        self.set_config()
        self.setup_ui()


    # Function to set up Streamlit UI
    def setup_ui(self):
        st.title("Botbox")
        st.write("llava is a language model that generates text based on the input prompt."
                 " It can also generate text based on images.")

        with st.form(key='user_input_form'):
            unloaded_images = st.file_uploader("Upload your images here", type=["png", "jpg", "jpeg"])
            prompt = st.text_input("Enter your prompt here:")
            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                if unloaded_images:
                    images = base64.b64encode(unloaded_images.read()).decode("utf-8")
                    st.image(unloaded_images, caption="Uploaded Image", use_column_width=True)

                    if prompt:
                        with st.spinner('Generating response...'):
                            response = send_request(prompt, images)
                            if response:
                                st.markdown(response)

                if prompt and not unloaded_images:
                    with st.chat_message("User"):
                        st.markdown(prompt)

                    with st.spinner('Generating response...'):
                        response = send_request(prompt, None)
                        with st.chat_message("ai"):
                            if response:
                                st.markdown(response)

    def set_config(self):
        st.set_page_config(
            page_title="Botbox",
            page_icon=":robot:",
            layout="wide",
            initial_sidebar_state="auto",
        )


# Run the Streamlit app
if __name__ == "__main__":

    app = App()
