import sys
import os
import streamlit as st
import time


app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_dir)
from app.Backend.main import Sdlc_Pipeline


st.title("💬 AI Agent ")
st.caption("🚀 An AI Agent powered by Crew.ai")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


input_data = st.chat_input("Please Enter Your Requirements Here ...........")

if input_data:
    with st.chat_message("user"):
        st.markdown(input_data)

    with st.spinner("Processing ⚙️"):
        try:
            sdlc_pipeline = Sdlc_Pipeline()
            sdlc_pipeline.create_agents()
            sdlc_pipeline.create_tasks()
            sdlc_pipeline.assemble_crew()
            result = sdlc_pipeline.kickoff(input_data)
           
            with st.chat_message("assistant"):
                st.markdown(result)
                

        except Exception as e:
            error_msg = "❌ Your Gemini Quote Exceeded! Please buy a subscription plan.\n\n" + str(e)
            


with st.sidebar:
    st.image( "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5Yp2IJuTmpSPijmE0ID-puoaFJNCEvaqmyw&s",width=600,)
    st.title("Automate SDLC Process 🚀")
    choice = st.radio(
        "Navigation",
        [
            "Data Collection",
            "ReqAnalyzer",
            "DesignCraft",
            "CodeMate",
            "TestGenie",
            "DeployWizard",
            "MaintainerAI",
        ],
    )
    st.info(
        "Create smart AI agents 🤖 to automate tasks in software development 💻 and make the process faster & better ⚡. And it's damn right magic! 🎩✨"
    )
