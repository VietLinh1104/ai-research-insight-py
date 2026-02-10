import streamlit as st
import sys
import os

# Add parent directory to path to import app module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.research_service import ResearchService

st.set_page_config(page_title="AI Research Insight (NewsAPI)", layout="wide")

st.title("🚀 AI-Research Insight: Trợ lý Nghiên cứu Tin Tức (NewsAPI)")

with st.sidebar:
    st.header("Cấu hình")
    api_key = st.text_input("Gemini API Key (nếu chưa có trong .env)", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
    
    news_key = st.text_input("News API Key (nếu chưa có trong .env)", type="password", help="Đăng ký tại newsapi.org")
    if news_key:
        os.environ["NEWS_API_KEY"] = news_key

topic = st.text_input("Nhập chủ đề bạn muốn nghiên cứu:", placeholder="Ví dụ: Chiến tranh lạnh, Bitcoin Trend, Công nghệ AI...")

if st.button("🔍 Bắt đầu Nghiên cứu", type="primary"):
    if not topic:
        st.warning("Vui lòng nhập chủ đề!")
    else:
        with st.spinner('Đang phân tích ý định và tìm kiếm dữ liệu tin tức...'):
            try:
                service = ResearchService()
                result = service.run(topic)
                
                # Hiển thị kết quả phân tích Intent
                if "intent_analysis" in result:
                    intent = result["intent_analysis"]
                    st.success(f"Phân tích Ý định hoàn tất!")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Quốc gia ưu tiên", intent.get("location", "N/A"))
                    with col2:
                        st.metric("Ngôn ngữ", intent.get("hl", "N/A"))
                    with col3:
                        st.metric("Khung thời gian", intent.get("time_horizon", "N/A"))
                    
                    st.info(f"💡 Lý do: {intent.get('reasoning')}")

                # Hiển thị câu trả lời tổng quan
                st.subheader("📝 Tổng quan Nghiên cứu")
                st.write(result["answer"])
                
                # Hiển thị nguồn tài liệu
                st.subheader("📰 Nguồn tin tức liên quan (NewsAPI)")
                if "sources" in result and result["sources"]:
                    for idx, article in enumerate(result["sources"]):
                        with st.expander(f"{idx+1}. {article.get('title', 'Tiêu đề không có sẵn')}"):
                            st.caption(f"**Nguồn:** {article.get('source')} - **Ngày:** {article.get('published_at')}")
                            st.write(f"**Mô tả:** {article.get('snippet', 'Không có mô tả')}")
                            st.markdown(f"[Đọc chi tiết ->]({article.get('link')})")
                else:
                    st.warning("Không tìm thấy tin tức nào phù hợp.")
                    
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {str(e)}")
                st.error("Vui lòng kiểm tra lại API Key trong file .env hoặc nhập ở sidebar.")
