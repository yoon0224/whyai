import textwrap
import google.generativeai as genai
import streamlit as st
import pathlib
import toml

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

def try_generate_content(api_key, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config={
                                      "temperature": 0.9,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 2048,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

def main():
    st.title("🌤️ Layered Structure of the Air")
    
    st.write("Enter the name of the atmospheric layer to learn about its characteristics and temperature changes.")
    
    layer = st.selectbox(
        "Select an atmospheric layer:",
        ["Troposphere", "Stratosphere", "Mesosphere", "Thermosphere", "Exosphere"]
    )
    
    st.write("You selected:", layer)
    
    prompt = f"Describe the characteristics and temperature changes of the {layer}."
    if st.button("Generate Explanation"):
        with st.spinner('Generating...'):
            content = try_generate_content(api_key, prompt)
            if content:
                st.markdown(to_markdown(content))
            else:
                st.error("Failed to generate content. Please try again.")

if __name__ == "__main__":
    main()