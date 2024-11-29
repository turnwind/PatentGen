import PyPDF2
from io import BytesIO
from agents import PatentAgent
from events import event_emitter
import datetime
import os

class PatentGenerator:
    def __init__(self, pdf_path=None):
        self.agent = PatentAgent()
        self.content = None
        self.abstract = None
        self.claims = None
        self.description = None

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
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # 提取所有页面的文本
                text_content = []
                for page in pdf_reader.pages:
                    text_content.append(page.extract_text())
                
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
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # 提取所有页面的文本
            text_content = []
            for page in pdf_reader.pages:
                text_content.append(page.extract_text())
            
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

    def generate_patent_abstract(self):
        try:
            # 使用统一的代理生成所有部分
            self.abstract = self.agent.generate_abstract(self.content)
            return self.abstract
            
        except Exception as e:
            event_emitter.emit_step_update({
                'message': f'生成失败: {str(e)}',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return None


    def generate_patent_claims(self):
        try:
            # 使用统一的代理生成所有部分
            self.claims = self.agent.generate_claims(self.content, self.abstract)
            return self.claims
            
        except Exception as e:
            event_emitter.emit_step_update({
                'message': f'生成失败: {str(e)}',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return None
        
    def generate_patent_description(self):
        try:
            # 使用统一的代理生成所有部分
            self.description = self.agent.generate_description(self.content, self.abstract, self.claims)
            return self.description
            
        except Exception as e:
            event_emitter.emit_step_update({
                'message': f'生成失败: {str(e)}',
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return None