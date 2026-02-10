import os
from .gemini_service import GeminiService
from dotenv import load_dotenv

# Load key from .env
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class ResearchService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.valid_countries = [
            'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr', 'gb', 'gr', 
            'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 
            'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'
        ]
        # 'vn' is NOT supported by NewsAPI top-headlines currently, despite being ISO standard.
        
        self.valid_languages = [
            'ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'sv', 'ud', 'zh'
        ]
        # 'vi' (Vietnamese) is NOT supported by NewsAPI everything endpoint currently.

    def run(self, topic: str):
        # 1. Phân tích ý định tìm kiếm
        print(f"--- Đang phân tích ý định cho từ khóa: '{topic}' ---")
        intent = self.gemini_service.analyze_query_intent(topic)
        print(f"Kết quả phân tích: {intent}")
        
        # 2. Thực hiện tìm kiếm với NewsAPI
        search_results = []
        if NEWS_API_KEY:
            try:
                from newsapi import NewsApiClient
                newsapi = NewsApiClient(api_key=NEWS_API_KEY)
                
                # Parameters based on intent
                q = topic
                language = intent.get("hl", "en")
                country = intent.get("gl", "us")
                time_horizon = intent.get("time_horizon", "general")
                
                # Validate parameters against NewsAPI constraints
                if country not in self.valid_countries:
                    print(f"Warning: Country '{country}' not supported by NewsAPI. Falling back to None.")
                    country = None # Set to None to search all countries or rely on 'everything' endpoint
                
                if language not in self.valid_languages:
                     print(f"Warning: Language '{language}' not supported by NewsAPI. Falling back to 'en'.")
                     # If language is not supported, we might get better results by searching without language filter 
                     # but query matches usually imply language. However, API requires valid lang code if provided.
                     # Let's fallback to english for international coverage or None if allowed (API defaults to all).
                     # Actually, if query is in Vietnamese but lang=en, we might get nothing.
                     # Better strategy: If unsupported language, don't pass language param to Everything endpoint, let query language decide.
                     language = 'en' # Safe fallback

                print(f"Đang tìm kiếm với Country={country}, Language={language}")
                
                articles = []
                # Thử tìm kiếm theo quốc gia (Top Headlines) trước
                if country:
                    try:
                        response = newsapi.get_top_headlines(q=q, country=country, page_size=5)
                        articles = response.get("articles", [])
                    except Exception as e:
                        print(f"Không tìm thấy Top Headlines cho country={country}: {e}")
                        articles = []
                    
                # Nếu ít kết quả, chuyển sang tìm kiếm Everything (rộng hơn)
                if not articles or len(articles) < 3:
                     print("Chuyển sang chế độ tìm kiếm mở rộng (Everything)...")
                     sort_by = "relevancy" if time_horizon == "history" else "publishedAt"
                     
                     # Check if language is valid for everything endpoint. 
                     # If original intent language (e.g. 'vi') was invalid, we previously set it to 'en'.
                     # But searching Vietnamese query with lang='en' yields 0 results.
                     # So if intent['hl'] was not in valid_languages, we should NOT pass language param at all to get_everything.
                     
                     search_params = {
                         'q': q,
                         'sort_by': sort_by,
                         'page_size': 10
                     }
                     if intent.get("hl") in self.valid_languages:
                         search_params['language'] = intent.get("hl")
                     else:
                        print(f"Skipping language param because '{intent.get('hl')}' is not supported.")

                     try:
                        response = newsapi.get_everything(**search_params)
                        articles = response.get("articles", [])
                     except Exception as e:
                         print(f"Lỗi tìm kiếm Everything: {e}")

                # Format kết quả
                for art in articles:
                    search_results.append({
                        "title": art.get("title"),
                        "link": art.get("url"),
                        "snippet": art.get("description") or "Không có mô tả",
                        "source": art.get("source", {}).get("name"),
                        "published_at": art.get("publishedAt")
                    })
                
            except ImportError:
                 print("Lỗi: Chưa cài đặt thư viện 'newsapi-python'. Vui lòng chạy pip install newsapi-python")
                 search_results = [{"title": "Error: Library missing", "link": "#", "snippet": "Chưa cài đặt newsapi-python."}]
            except Exception as e:
                print(f"Lỗi khi gọi News API: {e}")
                search_results = [{"title": "Error: API failed", "link": "#", "snippet": str(e)}]
        else:
             print("Lưu ý: Không tìm thấy NEWS_API_KEY trong .env. Kết quả giả định được sử dụng.")
             # Mock data based on intent
             mock_snippet = f"Kết quả giả lập (NewsAPI Mode) cho chủ đề {topic} từ khu vực {intent.get('location')}."
             search_results = [
                {"title": f"Tin tức mới nhất về {topic}", "link": "http://newsapi.org/example/1", "snippet": mock_snippet, "source": "BBC News"},
                {"title": f"Phân tích chuyên sâu: {topic}", "link": "http://newsapi.org/example/2", "snippet": f"Bài viết bằng ngôn ngữ {intent.get('hl')}.", "source": "Local Daily"}
            ]

        # 3. Trả về kết quả
        return {
            "answer": f"Đã thực hiện nghiên cứu về '{topic}' sử dụng NewsAPI.\nPhân tích ngữ cảnh: {intent.get('reasoning')}. \nKhu vực ưu tiên: {intent.get('location')} ({intent.get('gl')}).",
            "intent_analysis": intent,
            "sources": search_results
        }
