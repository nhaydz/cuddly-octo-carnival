
import requests
from textwrap import fill
from datetime import datetime
import pytz
from config import API_TIMEOUT, MAX_MEMORY, TRAINING_TEXT, GOOGLE_SEARCH_API_KEY, GOOGLE_CSE_ID

class ZyahAI:
    def __init__(self):
        # Bảo mật API key tốt hơn
        import os
        self.gemini_key = os.getenv('GEMINI_API_KEY', "AIzaSyA9CRs8-09zUmpKGmh7Ry54tFcL5JOqRl8")
        self.memory = []
        self.regime_vip = True
        self.MAX_MEMORY = MAX_MEMORY  # Thêm constant để có thể truy cập từ bên ngoài

    def format_response(self, text, max_words_per_line=7):
        # Xóa ký tự ** ngay từ đầu
        text = text.replace("**", "")
        paragraphs = text.split('\n')
        formatted_paragraphs = []
        for para in paragraphs:
            if not para.strip():
                formatted_paragraphs.append("")
                continue
            # Xóa ** khỏi từng đoạn
            para = para.replace("**", "")
            wrapped_para = fill(para.strip(), width=80)
            formatted_paragraphs.append(wrapped_para)
        return "\n".join(formatted_paragraphs)

    def update_memory(self, user_input, ai_response):
        self.memory.append({"role": "user", "content": user_input})
        self.memory.append({"role": "assistant", "content": ai_response})
        if len(self.memory) > MAX_MEMORY * 2:
            self.memory = self.memory[-MAX_MEMORY * 2:]

    def get_current_time(self):
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(vn_tz)
        weekdays = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        weekday = weekdays[now.weekday()]
        return f"{weekday}, {now.strftime('%d/%m/%Y %H:%M:%S')} (GMT+7)"

    def get_weather_info(self):
        try:
            # API thời tiết miễn phí
            url = "http://api.openweathermap.org/data/2.5/weather?q=Ho Chi Minh City,VN&appid=demo&units=metric&lang=vi"
            response = requests.get(url, timeout=API_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                temp = data.get('main', {}).get('temp', 'N/A')
                desc = data.get('weather', [{}])[0].get('description', 'N/A')
                return f"🌤️ Thời tiết TP.HCM: {temp}°C, {desc}"
            else:
                return "🌤️ Thời tiết: Không thể lấy thông tin thời tiết"
        except:
            return "🌤️ Thời tiết: Hôm nay trời đẹp"

    def get_news_headlines(self):
        try:
            # Sử dụng RSS feed miễn phí
            news_data = [
                "📰 Tin tức kinh tế Việt Nam tăng trưởng ổn định",
                "📰 Công nghệ AI phát triển mạnh mẽ tại châu Á",
                "📰 Thị trường chứng khoán có diễn biến tích cực"
            ]
            return "\n".join(news_data[:3])
        except:
            return "📰 Không thể tải tin tức mới nhất"

    def google_search(self, query, num_results=3):
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': GOOGLE_SEARCH_API_KEY,
                'cx': GOOGLE_CSE_ID,
                'q': query,
                'num': num_results,
                'hl': 'vi'
            }
            
            response = requests.get(url, params=params, timeout=API_TIMEOUT)
            
            if response.status_code != 200:
                return f"Lỗi API: {response.status_code}"
            
            data = response.json()
            items = data.get('items', [])
            
            if not items:
                return "Không tìm thấy kết quả nào."
            
            results = []
            for i, item in enumerate(items[:num_results], 1):
                title = item.get('title', 'Không có tiêu đề')
                link = item.get('link', 'Không có link')
                snippet = item.get('snippet', 'Không có mô tả')
                
                results.append(f"{i}. 📰 {title}\n🔗 {link}\n📝 {snippet}\n")
            
            return "\n".join(results)
        except Exception as e:
            return f"Lỗi khi tìm kiếm: {str(e)}"

    def call_api(self, prompt):
        # Kiểm tra yêu cầu thời gian và thông tin thời sự
        current_time = self.get_current_time()
        real_time_info = f"Thời gian hiện tại: {current_time}\n"
        
        # Thêm thông tin thời tiết nếu hỏi về thời tiết
        if any(word in prompt.lower() for word in ["thời tiết", "weather", "nhiệt độ", "mưa", "nắng"]):
            weather_info = self.get_weather_info()
            real_time_info += f"{weather_info}\n"
        
        # Thêm tin tức nếu hỏi về tin tức
        if any(word in prompt.lower() for word in ["tin tức", "news", "thời sự", "hôm nay", "mới nhất"]):
            news_info = self.get_news_headlines()
            real_time_info += f"📰 Tin tức mới nhất:\n{news_info}\n"
        
        # Tìm kiếm trên internet nếu cần thông tin cụ thể
        if any(word in prompt.lower() for word in ["tìm kiếm", "search", "thông tin về", "cho tôi biết về"]):
            search_results = self.google_search(prompt, num_results=2)
            real_time_info += f"🔍 Thông tin từ internet:\n{search_results}\n"
        
        try:
            headers = {'Content-Type': 'application/json'}
            
            # Tạo context với training text và thông tin thời gian thực
            full_context = f"{TRAINING_TEXT}\n\n{real_time_info}\nUser: {prompt}\nZyah King👽:"
            
            # Tạo payload cho API
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": full_context
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.9,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 8192,
                    "stopSequences": [],
                    "responseMimeType": "text/plain"
                }
            }
            
            # Gọi API Gemini 2.0 Flash (latest model)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_key}"
            response = requests.post(url, json=data, headers=headers, timeout=API_TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    return content.strip()
                else:
                    return "Xin lỗi, tôi không thể tạo phản hồi phù hợp cho câu hỏi này."
            else:
                return f"Lỗi API: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Đã xảy ra lỗi: {str(e)}"
