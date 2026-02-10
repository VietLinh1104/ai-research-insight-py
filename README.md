🚀 AI-Research Insight: Trợ lý Nghiên cứu & Phân tích Tri thức Đa chiều
AI-Research Insight là một hệ thống hỗ trợ nghiên cứu thông minh, ứng dụng các mô hình ngôn ngữ lớn (LLM) và cơ sở dữ liệu vector để giúp người dùng khám phá, tóm tắt và phân tích các chủ đề phức tạp một cách hệ thống.

📌 Tổng quan dự án
Thay vì chỉ cung cấp các đường link bài báo rời rạc, hệ thống này tự động thu thập, phân tích và kết nối các nguồn thông tin để tạo ra một "bản đồ tri thức" toàn diện cho người dùng.

Lĩnh vực: Artificial Intelligence, Natural Language Processing (NLP).

Công nghệ lõi: RAG (Retrieval-Augmented Generation), Vector Database, LLMs.

✨ Tính năng nổi bật
1. Tìm kiếm & Gợi ý thông minh (Smart Discovery)
Sử dụng Semantic Search để hiểu ý định người dùng thay vì chỉ so khớp từ khóa.

Tự động crawl dữ liệu thời gian thực từ các nguồn uy tín.

2. Phân tích tri thức nâng cao (Advanced Analytics)
Topic Modeling (LDA): Tự động phân loại bài báo vào các nhóm chủ đề (Ví dụ: Lịch sử, Xu hướng, Tranh luận).

Sentiment Analysis: Phân tích thái độ của bài viết để cung cấp cái nhìn đa chiều (Tích cực/Tiêu cực).

Knowledge Graph: Trực quan hóa mối quan hệ giữa các thực thể (Người, Địa danh, Sự kiện).

3. Trợ lý hỏi đáp (Chat-with-Research)
Áp dụng quy trình RAG để trả lời câu hỏi dựa trên dữ liệu tìm được.

Trích dẫn nguồn (Citations) chính xác cho từng câu trả lời, hạn chế tình trạng AI "ảo giác".

🏗 Kiến trúc hệ thống
Dự án được xây dựng dựa trên sự phối hợp của 4 khối thuật toán chính:

Embedding & Vector Search: Sử dụng Sentence-BERT và ChromaDB để số hóa văn bản và tìm kiếm theo khoảng cách Cosine.

RAG Workflow: Kết nối dữ liệu từ Vector DB với Gemini API thông qua LangChain.

NER (Named Entity Recognition): Sử dụng spaCy để trích xuất thực thể cho đồ thị tri thức.

Topic & Sentiment: Sử dụng LDA và Transformer-based models để phân loại dữ liệu.

🛠 Công nghệ sử dụng (Tech Stack)
Ngôn ngữ: Python 3.10+

AI Frameworks: LangChain, HuggingFace Transformers.

LLM: Google Gemini Pro API.

Vector Database: ChromaDB / Pinecone.

NLP Tools: spaCy, NLTK, Gensim.

Dashboard: Streamlit.

📋 Lộ trình thực hiện (Roadmap)
[x] Giai đoạn 1: Thiết kế kiến trúc và chọn nguồn dữ liệu.

[ ] Giai đoạn 2: Xây dựng module Crawl và tiền xử lý dữ liệu.

[ ] Giai đoạn 3: Triển khai Vector DB và luồng RAG cơ bản.

[ ] Giai đoạn 4: Tích hợp NER, LDA và vẽ Knowledge Graph.

[ ] Giai đoạn 5: Hoàn thiện UI/UX với Streamlit và đóng gói sản phẩm.

🚀 Hướng dẫn cài đặt (Quick Start)
Bash
# Clone dự án
git clone https://github.com/username/ai-research-insight.git

# Cài đặt thư viện
pip install -r requirements.txt

# Thiết lập API Key trong file .env
GEMINI_API_KEY=your_key_here
SERP_API_KEY=your_key_here

# Chạy ứng dụng
streamlit run app.py