import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenAI配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = "https://api.chatanywhere.tech" 
OPENAI_MODEL = "gpt-4-1106-preview"  # 使用最新的GPT-4模型
OPENAI_MODEL = "claude-3-5-sonnet-20241022"
OPENAI_MODEL = "gpt-4o-mini"