from abc import ABC, abstractmethod
from openai import OpenAI
import time
from datetime import datetime
from collections import deque
import threading
import json
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL
from patent_gen.events import event_emitter

class StepLogger:
    def __init__(self, max_steps=100):
        self.steps = deque(maxlen=max_steps)
        self._lock = threading.Lock()
    
    def log_step(self, step_data):
        with self._lock:
            # 添加时间戳
            if isinstance(step_data, dict):
                if 'timestamp' not in step_data:
                    step_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                step_data = {
                    'message': str(step_data),
                    'status': 'processing',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # 保存步骤
            self.steps.append(step_data)
            
            # 发送步骤更新事件
            try:
                event_emitter.emit_step_update(step_data)
            except Exception as e:
                print(f"Error emitting step update: {str(e)}")
    
    def get_steps(self):
        with self._lock:
            return list(self.steps)

# 创建全局步骤记录器
step_logger = StepLogger()

class BaseAgent(ABC):
    def __init__(self, name):
        self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        self.name = name
        self.step_counter = 0
        
    def log_step(self, step_name, input_data=None, output_data=None, status="processing"):
        """记录处理步骤"""
        self.step_counter += 1
        
        step_data = {
            'id': self.step_counter,
            'message': step_name,
            'status': status,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'input': input_data if input_data else "",
            'output': output_data if output_data else ""
        }
        
        # 使用内存中的步骤记录器
        step_logger.log_step(step_data)
        return step_data

    def run_llm(self, prompt, temperature=0.7):
        try:
            self.log_step("正在发送请求到LLM", prompt)
            
            messages = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=temperature,
                stream=True  # 假设API支持流式传输
            )
            
            for chunk in response:
                result = chunk.choices[0].delta.content
                if result == None:
                    break

                #self.log_step("收到LLM响应", None, result, "completed")
                yield result  # 使用yield返回结果，使其成为流的一部分   
                
        except Exception as e:
            error_msg = f"API调用错误: {str(e)}"
            self.log_step("发生错误", None, error_msg, "error")
            raise e

    @abstractmethod
    def process(self, content):
        pass

class PatentAgent(BaseAgent):
    """专利生成代理"""
    
    def __init__(self):
        super().__init__("专利生成代理")
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )

    def generate_abstract(self, content, examples):
        """生成专利摘要"""
        try:
            self.log_step("生成摘要", "正在生成专利摘要...", "", "processing")
            abstract_prompt = """
            你是一个专业的专利代理人。请根据以下研究论文内容和参考例子，生成一个专利摘要。要求：
            1. 遵循中国专利申请的格式要求
            2. 包含发明所要解决的技术问题
            3. 描述技术方案的主要技术特征
            4. 突出发明的有益效果
            5. 语言简洁明了
            6. 不超过300字
            7. 参考提供的例子的写作风格和格式
            
            研究论文内容：
            {content}

            参考例子：
            {examples}
            """
        # 调用run_llm函数，它现在是一个生成器，返回流式响应
            for part in self.run_llm(abstract_prompt.format(content=content, examples=examples)):
                yield part  # 逐个返回摘要的每一部分
            self.log_step("生成摘要", "专利摘要生成完成", "", "completed")

        except Exception as e:
            self.log_step("生成摘要", f"生成摘要失败: {str(e)}", "", "error")
            raise e

    def generate_claims(self, content, abstract, examples):
        """生成专利权利要求"""
        try:
            self.log_step("生成权利要求", "正在生成专利权利要求...", "", "processing")
            claims_prompt = """
            基于以下研究论文内容和参考例子，生成专利权利要求书。要求：
            1. 符合中国专利法对权利要求书的规定
            2. 包含独立权利要求和从属权利要求
            3. 使用标准的权利要求书撰写格式
            4. 保护范围要适当，既要覆盖核心技术特征，又不能过于宽泛
            5. 技术特征完整、清楚
            6. 从属权利要求应进一步限定独立权利要求的技术特征
            7. 参考提供的例子的写作风格和格式
            
            研究论文内容：
            {content}
            
            已生成的摘要：
            {abstract}

            参考例子：
            {examples}
            """
            # 调用run_llm函数，它现在是一个生成器，返回流式响应
            for part in self.run_llm(claims_prompt.format(content=content, abstract=abstract, examples=examples)):
                yield part  # 逐个返回摘要的每一部分
            self.log_step("生成权利要求", "专利权利要求生成完成", "", "completed")

        except Exception as e:
            self.log_step("生成权利要求", f"生成权利要求失败: {str(e)}", "", "error")
            raise e

    def generate_description(self, content, abstract, claims, examples):
        """生成专利说明书"""
        try:
            self.log_step("生成说明书", "正在生成专利说明书...", "", "processing")
            description_prompt = """
            基于以下研究论文内容和参考例子，生成专利说明书。要求：
            1. 符合中国专利法对说明书的规定
            2. 包含标准的说明书结构：技术领域、背景技术、发明内容、附图说明（如有）、具体实施方式
            3. 充分公开发明的技术方案
            4. 详细描述至少一种优选实施例
            5. 语言规范，避免使用"本发明"等字样
            6. 与权利要求书和摘要保持一致
            7. 参考提供的例子的写作风格和格式
            
            研究论文内容：
            {content}
            
            已生成的摘要：
            {abstract}
            
            已生成的权利要求：
            {claims}

            参考例子：
            {examples}
            """

            # 调用run_llm函数，它现在是一个生成器，返回流式响应
            for part in self.run_llm(description_prompt.format(
                content=content,
                abstract=abstract,
                claims=claims,
                examples=examples
            )):
                yield part  # 逐个返回摘要的每一部分

                
            self.log_step("专利生成完成", "专利说明书生成完成", "", "completed")

        except Exception as e:
            self.log_step("生成说明书", f"生成说明书失败: {str(e)}", "", "error")
            raise e

    def update_step_msg(self, message, part, content ):
        event_emitter.emit_step_update({
            'message': message,
            'type': 'content',
            'part': part,
            'content': content,
            'status': 'completed',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })


    def process(self, content, examples):
        pass

def get_agent_steps():
    """获取所有代理的处理步骤"""
    return step_logger.get_steps()

# 创建PatentAgent实例
patent_agent = PatentAgent()
