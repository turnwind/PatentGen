import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenAI配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#OPENAI_API_KEY = "sk-svcacct-sNAGGSl47dHE0QS6ZBwF2Gu4W9ogMY_F57LLVU4elVSZrM-rWSUTilQhexhxb1oeHT3BlbkFJNPVWVHgD1TB3qE8OdhVTqgir5ZA9_d_va9mcntpwzaa-0HH9wi8w15s8fXUAHvu2wA"
OPENAI_BASE_URL = "https://api.chatanywhere.tech" 
OPENAI_MODEL = "gpt-4-1106-preview"  # 使用最新的GPT-4模型
OPENAI_MODEL = "claude-3-5-sonnet-20241022"
OPENAI_MODEL = "gpt-4o-mini"

# 文件路径配置
INPUT_DIR = "input"
OUTPUT_DIR = "output"
TEMPLATE_DIR = "templates"

# 确保必要的目录存在
for dir_path in [INPUT_DIR, OUTPUT_DIR, TEMPLATE_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# 专利生成提示词
PATENT_PROMPTS = {
    "abstract": """请将以下论文转换为中国发明专利的摘要格式。
要求：
1. 字数在200-300字之间
2. 应当写明发明专利申请所公开的内容属于什么技术领域
3. 描述所要解决的技术问题、解决问题的技术方案和主要用途  
4. 语言简要，不得使用商业性宣传用语


论文摘要： 
{text}
""",
    
    "claims": """请基于以下论文内容生成符合中国发明专利要求的权利要求书。
要求：
1. 包括独立权利要求和从属权利要求
2. 每条权利要求应当用一个自然段描述
3. 独立权利要求应当包括前序部分和特征部分
4. 从属权利要求应当包括引用部分和限定部分
5. 使用规范的专利用语

论文内容：
{text}
""",

    "description": """请基于以下论文内容生成符合中国发明专利要求的说明书。
要求：
1. 包括技术领域、背景技术、发明内容、附图说明和具体实施方式等部分
2. 说明书应当清楚、完整地公开发明
3. 用词规范，符合专利文献习惯用语
4. 避免使用商业性宣传用语

论文内容：
{text}
"""
}
