import textwrap
import google.generativeai as genai
import streamlit as st
import toml
import pathlib

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("api_key")

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def try_generate_content(api_key, prompt, temperature, top_p, top_k, max_output_tokens):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
        },
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ],
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

st.title("State Changes Informer 🌟")
st.write("Enter a real-life example to learn about the state changes that occur.")

example_input = st.text_input("Real-life example:", "")

st.sidebar.title("Settings ⚙️")
st.sidebar.write("Adjust the parameters for content generation.")
temperature = st.sidebar.slider("Temperature", 0.1, 1.0, 0.7)
top_p = st.sidebar.slider("Top P", 0.1, 1.0, 1.0)
top_k = st.sidebar.slider("Top K", 1, 50, 1)
max_output_tokens = st.sidebar.slider("Max Output Tokens", 100, 2048, 2048)

if example_input:
    prompt = f"Explain the state changes that occur in the following real-life example: {example_input}"
    generated_content = try_generate_content(api_key, prompt, temperature, top_p, top_k, max_output_tokens)
    
    if generated_content:
        st.markdown(to_markdown(generated_content))
    else:
        st.error("Failed to generate content. Please check your API key and try again.")