import streamlit as st
import google.generativeai as genai

st.title(":jp: Mochi-chan おはよう！:jp: ")
st.subheader("Your Japanese tour guide intern")

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")
prompt = "You are JanJan; a tourist guide-intern in Japan, being able to suggest points of interest across the country to tourists."

# Initialize the Gemini Model
model = None  # Initialize model variable
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Capture user input and generate bot response
if user_input := st.chat_input("Type your message here..."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # Use Gemini AI to generate a bot response only if the model is initialized
    if model:
        try:
            if not st.session_state.chat_history:  # Check if chat history is empty
                introduction = "Hello! I'm JanJan, your friendly tour guide-intern in Japan! I'm here to help you discover amazing places and experiences across the country."
                bot_response = introduction
            else:
                # Generate a response based on user input
                response = model.generate_content(f"{prompt} User said: {user_input}")
                bot_response = response.text.strip()  # Remove any extra whitespace

            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
    else:
        st.error("The model is not initialized. Please check your API key.")
