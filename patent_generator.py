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
    
    def generate_patent(self):
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

def main():
    # 检查必要的目录是否存在
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 检查API密钥
    if not OPENAI_API_KEY:
        print("请在.env文件中设置OPENAI_API_KEY")
        return

    generator = PatentGenerator()

    # 处理input目录中的所有PDF文件
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"在{INPUT_DIR}目录中没有找到PDF文件")
        return

    for pdf_file in pdf_files:
        input_path = os.path.join(INPUT_DIR, pdf_file)
        print(f"\n处理文件: {pdf_file}")
        generator = PatentGenerator(input_path)
        patent = generator.generate_patent()
        if patent:
            output_file = os.path.join(
                OUTPUT_DIR,
                f"专利申请书_{os.path.splitext(os.path.basename(input_path))[0]}.docx"
            )
            with open(output_file, 'w') as f:
                f.write(patent)
            print(f"专利文档已生成: {output_file}")

if __name__ == "__main__":
    main()
