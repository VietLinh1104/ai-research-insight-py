import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            try:
                # Based on environment check, 'models/gemini-2.5-flash' is available and working.
                # Using this as the primary model.
                self.model = genai.GenerativeModel(
                    model_name='models/gemini-2.5-flash',
                    generation_config={"response_mime_type": "application/json"}
                )
            except Exception as e:
                print(f"Error initializing model: {e}")

    def analyze_query_intent(self, query: str) -> dict:
        """
        Analyzes the user query to determine the best search parameters.
        Returns a dictionary with location, language, and potential time horizon.
        """
        # Re-check key/model if not initialized
        if not self.model:
             apikey = os.getenv("GEMINI_API_KEY")
             if apikey:
                 genai.configure(api_key=apikey)
                 try:
                    self.model = genai.GenerativeModel(
                        model_name='models/gemini-2.5-flash',
                        generation_config={"response_mime_type": "application/json"}
                    )
                 except Exception:
                     pass
        
        if not self.model:
            return {
                "gl": "us", "hl": "en", "location": "United States",
                "time_horizon": "general", "reasoning": "Model not initialized (Missing API Key?)"
            }

        prompt = f"""
        Bạn là một chuyên gia phân tích ý định tìm kiếm (Search Intent Analyst).
        Thực hiện phân tích từ khóa sau: '{query}'.

        Nhiệm vụ:
        1. Xác định quốc gia/khu vực nguồn gốc hoặc uy tín nhất cho chủ đề này (gl).
        2. Xác định ngôn ngữ chính phù hợp nhất để tìm kiếm (hl).
        3. Xác định khung thời gian (time_horizon): 'history' (lịch sử/nguồn gốc), 'trend' (xu hướng mới), hoặc 'general' (chung).

        Trả về kết quả dưới dạng JSON với các trường:
        {{
            "gl": "mã_quốc_gia_iso_3166-1_alpha-2 (ví dụ: us, vn, jp)",
            "hl": "mã_ngôn_ngữ_iso_639-1 (ví dụ: en, vi, ja)",
            "location": "Tên quốc gia đầy đủ (ví dụ: United States, Vietnam)",
            "time_horizon": "history" | "trend" | "general",
            "reasoning": "Giải thích ngắn gọn tại sao chọn khu vực này"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            # With response_mime_type="application/json", response.text should be valid JSON
            return json.loads(response.text)
        except Exception as e:
            print(f"Error analyzing query intent: {e}")
            # Default fallback
            return {
                "gl": "us",
                "hl": "en",
                "location": "United States",
                "time_horizon": "general",
                "reasoning": "Default backup due to error."
            }
