import pdfplumber
import os
from patent_gen.agents import PatentAgent
from patent_gen.events import event_emitter
import datetime

class PatentGenerator:
    def __init__(self, pdf_path=None):
        self.agent = PatentAgent()
        self.content = ""
        self.abstract = ""
        self.claims = ""
        self.description = ""

        if pdf_path:
            self.process_pdf_file(pdf_path)
        
    def process_pdf_file(self, pdf_path):
        """处理PDF文件路径"""
        try:
            event_emitter.emit_step_update({
                'message': '正在处理PDF文件...',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            # 从文件读取PDF
            with pdfplumber.open(pdf_path) as pdf:
                # 提取所有页面的文本
                text_content = []
                for page in pdf.pages:
                    # 提取页面文本，并保留基本格式
                    page_text = page.extract_text(x_tolerance=3, y_tolerance=3)
                    if page_text:
                        text_content.append(page_text)
                
                self.content = "\n".join(text_content)
            
            event_emitter.emit_step_update({
                'message': 'PDF文件处理完成',
                'status': 'completed',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            return True
            
        except Exception as e:
            event_emitter.emit_step_update({
                'message': f'PDF处理失败: {str(e)}',
                'status': 'error',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return False
    
    def process_pdf(self, pdf_file):
        """处理PDF文件对象"""
        try:
            event_emitter.emit_step_update({
                'message': '正在处理PDF文件...',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            # 从BytesIO读取PDF
            with pdfplumber.open(pdf_file) as pdf:
                # 提取所有页面的文本
                text_content = []
                for page in pdf.pages:
                    # 提取页面文本，并保留基本格式
                    page_text = page.extract_text(x_tolerance=3, y_tolerance=3)
                    if page_text:
                        text_content.append(page_text)
            
                self.content = "\n".join(text_content)
            
            event_emitter.emit_step_update({
                'message': 'PDF文件处理完成',
                'status': 'completed',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            return True
            
        except Exception as e:
            event_emitter.emit_step_update({
                'message': f'PDF处理失败: {str(e)}',
                'status': 'error',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return False
    
    def read_pdf_examples(self, examples_dir):
        """
        Read all PDF files from the examples directory and return their text content
        
        Args:
            examples_dir (str): Path to the directory containing example PDF files
            
        Returns:
            str: Concatenated text content from all PDF files
        """ 
        
        if not os.path.exists(examples_dir):
            return ""
        example_texts = []
    
        # 遍历examples目录下的所有PDF文件
        for filename in os.listdir(examples_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(examples_dir, filename)
                try:
                    # 使用pdfplumber读取PDF文件
                    with pdfplumber.open(file_path) as pdf:
                        # 提取文本内容
                        text = ""
                        for page in pdf.pages:
                            # 提取页面文本，并保留基本格式
                            page_text = page.extract_text(x_tolerance=3, y_tolerance=3)
                            print(page_text)
                            if page_text:
                                text += page_text + "\n"
                    
                    if text.strip():  # 只有当提取到文本时才添加到示例中
                        example_texts.append(f"示例 {filename}:\n{text}\n")
                    
                except Exception as e:
                    print(f"Error reading PDF file {filename}: {str(e)}")
                    continue
        
        # 合并所有示例文本
        return "\n".join(example_texts) if example_texts else ""

    def generate_patent_header(self):
        """生成专利文档"""
        if not self.content:
            raise ValueError("请先上传PDF文件")
            
        try:
            # 使用统一的代理生成所有部分
            result = self.agent.process(self.content)
            return result
            
        except Exception as e:
            event_emitter.emit_step_update({
                'message': f'生成失败: {str(e)}',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return None

    def generate_patent_abstract(self, examples=""):
        """生成专利摘要（流式响应）"""
        if not self.content:
            raise ValueError("请先上传PDF文件")
        try:
            # 使用统一的代理生成所有部分
            for abstract_part in self.agent.generate_abstract(self.content, examples):
                self.abstract += abstract_part
                yield abstract_part  # 逐个返回摘要的每一部分
                
            # 所有部分生成完毕后，可以在这里执行一些收尾工作
            event_emitter.emit_step_update({
                'message': '摘要生成完成',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            event_emitter.emit_step_update({
                'message': f'生成摘要失败: {str(e)}',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            raise e


    def generate_patent_claims(self, examples=""):
        """生成专利权利要求"""
        if not self.content:
            raise ValueError("请先上传PDF文件")
            
        try:
            # 使用统一的代理生成所有部分
            for claims_part in self.agent.generate_claims(self.content, self.abstract, examples):
                self.claims += claims_part
                yield claims_part
            # 所有部分生成完毕后，可以在这里执行一些收尾工作
            event_emitter.emit_step_update({
                'message': '权利要求部分生成完成',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            event_emitter.emit_step_update({
                'message': f'生成权利要求失败: {str(e)}',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            raise e
        
    def generate_patent_description(self, examples = ""):
        try:
            # 使用统一的代理生成所有部分
            for description_part in self.agent.generate_description(self.content, self.abstract, self.claims, examples):
                self.description += description_part
                yield description_part

            # 所有部分生成完毕后，可以在这里执行一些收尾工作
            event_emitter.emit_step_update({
                'message': '说明书部分生成完成',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            event_emitter.emit_step_update({
                'message': f'生成说明书失败: {str(e)}',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return e