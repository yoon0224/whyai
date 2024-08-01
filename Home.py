import textwrap
import google.generativeai as genai
import streamlit as st
import toml
import pathlib



st.title("조사활동 도우미")
st.write("왼쪽 메뉴에서 조사하려는 주제를 선택하세요.")