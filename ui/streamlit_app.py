import streamlit as st
from app.services.research_service import ResearchService

st.title("AI Research Assistant")

topic = st.text_input("Nhập chủ đề nghiên cứu")

if st.button("Nghiên cứu"):
    service = ResearchService()
    result = service.run(topic)
    st.write(result["answer"])
