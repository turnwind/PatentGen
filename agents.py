from abc import ABC, abstractmethod
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL

class BaseAgent(ABC):
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    
    @abstractmethod
    def process(self, content):
        pass

    def get_completion(self, prompt, temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in API call: {e}")
            return None

class AnalysisAgent(BaseAgent):
    """论文分析Agent，负责分析论文的核心创新点和技术特征"""
    
    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一个专业的专利分析专家，擅长分析论文中的创新点和技术特征。
请仔细分析论文内容，识别：
1. 核心技术创新点
2. 关键技术特征
3. 技术效果
4. 应用领域
5. 现有技术中存在的问题"""

    def process(self, content):
        prompt = f"""请分析以下论文内容，提供详细的技术分析报告：

{content}

请按照以下格式输出：
1. 技术领域：[详细说明]
2. 背景技术存在的问题：[列出具体问题]
3. 核心技术创新点：[详细说明]
4. 关键技术特征：[列出并解释]
5. 技术效果：[详细说明]
6. 潜在应用领域：[列出并说明]
"""
        return self.get_completion(prompt)

class AbstractAgent(BaseAgent):
    """摘要生成Agent，负责生成专业的专利摘要"""
    
    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一个专业的专利摘要撰写专家，精通中国专利申请的摘要撰写规范。
摘要撰写要求：
1. 字数控制在200-300字之间
2. 清晰说明技术领域
3. 突出技术问题和解决方案
4. 重点描述技术效果
5. 使用规范的专利用语"""

    def process(self, content):
        prompt = f"""请基于以下技术分析报告，撰写一份专业的专利摘要：

{content}

要求：
1. 第一句话说明技术领域
2. 描述现有技术存在的问题
3. 说明本发明的技术方案
4. 强调取得的技术效果
5. 使用"本发明"、"所述"等专利常用词"""
        return self.get_completion(prompt)

class ClaimsAgent(BaseAgent):
    """权利要求书生成Agent，负责生成专业的权利要求"""
    
    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一个专业的专利权利要求撰写专家，精通中国专利申请的权利要求撰写规范。
权利要求撰写要求：
1. 符合专利法的撰写规范
2. 包括独立权利要求和从属权利要求
3. 使用规范的连接词和引用方式
4. 每个技术特征的描述要准确完整"""

    def process(self, content):
        prompt = f"""请基于以下技术分析报告，撰写一份完整的专利权利要求书：

{content}

要求：
1. 独立权利要求应包括前序部分和特征部分
2. 从属权利要求应当引用在前的权利要求
3. 使用"其特征在于"、"所述"等规范用语
4. 按照技术方案的展开顺序编写多条从属权利要求
5. 确保权利要求之间的引用关系正确"""
        return self.get_completion(prompt)

class DescriptionAgent(BaseAgent):
    """说明书生成Agent，负责生成详细的专利说明书"""
    
    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一个专业的专利说明书撰写专家，精通中国专利申请的说明书撰写规范。
说明书撰写要求：
1. 结构完整，包括所有必要章节
2. 详细描述技术方案
3. 提供具体实施例
4. 说明技术效果
5. 使用规范的专利用语"""

    def process(self, content):
        prompt = f"""请基于以下技术分析报告，撰写一份详细的专利说明书：

{content}

要求：
1. 包括以下章节：
   - 技术领域
   - 背景技术
   - 发明内容（包括技术问题、技术方案和有益效果）
   - 附图说明（如有）
   - 具体实施方式
2. 每个章节的内容要详实
3. 至少提供两个具体实施例
4. 详细说明技术原理和实现方式
5. 使用规范的专利用语"""
        return self.get_completion(prompt)

class DrawingDescriptionAgent(BaseAgent):
    """附图说明生成Agent，负责生成附图说明部分"""
    
    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一个专业的专利附图说明撰写专家，精通中国专利申请的附图说明撰写规范。
附图说明撰写要求：
1. 清晰说明每个附图的内容
2. 使用规范的附图标记说明方式
3. 与说明书主体保持一致"""

    def process(self, content):
        prompt = f"""请基于以下技术分析报告，生成专利附图说明：

{content}

要求：
1. 列出所有需要的附图
2. 为每个技术特征编号
3. 说明附图中的标记含义
4. 确保与说明书中的描述一致"""
        return self.get_completion(prompt)
