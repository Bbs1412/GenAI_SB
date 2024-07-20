import streamlit as st
import google.generativeai as palm
from langdetect import detect
from googletrans import Translator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("api.env")
api_key = os.getenv("PALM_API_KEY")

# Configure the PALM API with the API key
palm.configure(api_key=api_key)
translator = Translator()

# Initialize the Palm Text-Bison-001 Model
class TextBisonModel:
    def __init__(self):
        # List available models and select one
        self.models = [model for model in palm.list_models()]
        if len(self.models) > 1:
            # Select the text-bison model
            self.model_name = self.models[1].name
        else:
            st.error("No models found. Please check your API configuration.")
            st.stop()

    def generate_question(self, text, language):
        return generate_questions(self.model_name, text)

# Initialize model and translator
model = TextBisonModel()

# Function to generate questions from text
def generate_questions(model_name, text):
    try:
        response = palm.generate_text(
            model=model_name,
            prompt=f"Generate questions from the following text:\n\n {text} \n\n Questions:",
            max_output_tokens=150
        )
        questions = response.result.strip() if response.result else "No questions generated."
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        questions = "Error generating questions."

    return questions


# Function to structure the Streamlit app
def main():
    st.title("Inquisitive: A Multilingual AI Question Generator")

    # Input text from the user
    user_text = st.text_area(
        "Enter the text you want questions generated from:")

    # Language detection
    detected_language = detect(user_text) if user_text else None

    # Translate to English if not already in English
    if detected_language and detected_language != 'en':
        translated_text = translator.translate(
            user_text,
            src=detected_language,
            dest="en"
        ).text
    else:
        translated_text = user_text

    # Generate questions button
    if st.button("Generate Questions"):
        if user_text:
            # Generate questions
            questions = model.generate_question(
                translated_text, detected_language)

            # Translate questions back to the original language if translated
            if detected_language and detected_language != 'en':
                questions = translator.translate(
                    questions, src="en", dest=detected_language).text

            # Display generated questions
            st.subheader("Generated Questions:")
            st.write(questions)
        else:
            st.warning("Please enter some text.")


# Entry point
if __name__ == "__main__":
    main()
