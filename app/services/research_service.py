class ResearchService:
    def run(self, topic: str):
        return {
            "answer": f"Đây là kết quả nghiên cứu cho chủ đề: {topic}",
            "sources": []
        }
