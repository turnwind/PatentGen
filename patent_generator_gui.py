import os
import PyPDF2
import docx
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, INPUT_DIR, OUTPUT_DIR, PATENT_PROMPTS, OPENAI_BASE_URL
from agents import AnalysisAgent, AbstractAgent, ClaimsAgent, DescriptionAgent, DrawingDescriptionAgent

class PatentGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("专利生成器")
        self.root.geometry("800x600")
        
        # 设置OpenAI客户端和Agents
        self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        self.analysis_agent = AnalysisAgent()
        self.abstract_agent = AbstractAgent()
        self.claims_agent = ClaimsAgent()
        self.description_agent = DescriptionAgent()
        self.drawing_agent = DrawingDescriptionAgent()
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建文件选择部分
        self.create_file_selection()
        
        # 创建进度显示部分
        self.create_progress_section()
        
        # 创建日志显示部分
        self.create_log_section()
        
        # 确保目录存在
        for dir_path in [INPUT_DIR, OUTPUT_DIR]:
            os.makedirs(dir_path, exist_ok=True)

    def create_file_selection(self):
        # 文件选择框架
        file_frame = ttk.LabelFrame(self.main_frame, text="选择论文", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 文件路径显示
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=60)
        self.file_path_entry.grid(row=0, column=0, padx=5)
        
        # 浏览按钮
        browse_btn = ttk.Button(file_frame, text="浏览", command=self.browse_file)
        browse_btn.grid(row=0, column=1, padx=5)
        
        # 生成按钮
        generate_btn = ttk.Button(file_frame, text="生成专利", command=self.generate_patent)
        generate_btn.grid(row=0, column=2, padx=5)

    def create_progress_section(self):
        # 进度框架
        progress_frame = ttk.LabelFrame(self.main_frame, text="生成进度", padding="5")
        progress_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var,
            maximum=100,
            length=780
        )
        self.progress_bar.grid(row=0, column=0, padx=5, pady=5)

    def create_log_section(self):
        # 日志框架
        log_frame = ttk.LabelFrame(self.main_frame, text="处理日志", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(log_frame, width=90, height=20)
        self.log_text.grid(row=0, column=0, padx=5, pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="选择论文PDF文件",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.file_path_var.set(filename)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def extract_text_from_pdf(self, pdf_path):
        """从PDF文件中提取文本"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                total_pages = len(reader.pages)
                
                for i, page in enumerate(reader.pages):
                    text += page.extract_text()
                    progress = (i + 1) / total_pages * 25  # PDF提取占25%进度
                    self.progress_var.set(progress)
                    self.root.update()
                
                return text
        except Exception as e:
            self.log_message(f"Error extracting text from PDF: {e}")
            return None

    def generate_patent_content(self, text, prompt_key, progress_start):
        """使用OpenAI API生成专利内容"""
        try:
            # 首先进行技术分析
            self.log_message("正在进行技术分析...")
            analysis_report = self.analysis_agent.process(text)
            if not analysis_report:
                return None
            
            self.progress_var.set(progress_start - 10)
            
            # 根据不同部分选择不同的Agent
            if prompt_key == "abstract":
                self.log_message("正在生成专利摘要...")
                content = self.abstract_agent.process(analysis_report)
            elif prompt_key == "claims":
                self.log_message("正在生成权利要求...")
                content = self.claims_agent.process(analysis_report)
            elif prompt_key == "description":
                self.log_message("正在生成说明书...")
                description = self.description_agent.process(analysis_report)
                self.progress_var.set(progress_start - 5)
                
                self.log_message("正在生成附图说明...")
                drawing_description = self.drawing_agent.process(analysis_report)
                content = f"{description}\n\n{drawing_description}"
            
            self.progress_var.set(progress_start)
            return content
            
        except Exception as e:
            self.log_message(f"Error generating {prompt_key}: {e}")
            return None

    def create_patent_document(self, abstract, claims, description, output_path):
        """创建专利文档"""
        try:
            doc = docx.Document()
            
            # 添加标题
            doc.add_heading('发明专利申请', 0)
            
            # 添加摘要
            doc.add_heading('摘要', 1)
            doc.add_paragraph(abstract)
            self.progress_var.set(90)
            
            # 添加权利要求
            doc.add_heading('权利要求', 1)
            doc.add_paragraph(claims)
            self.progress_var.set(95)
            
            # 添加说明书
            doc.add_heading('说明书', 1)
            doc.add_paragraph(description)
            
            # 保存文档
            doc.save(output_path)
            self.progress_var.set(100)
            return True
        except Exception as e:
            self.log_message(f"Error creating patent document: {e}")
            return False

    def generate_patent(self):
        input_file = self.file_path_var.get()
        if not input_file:
            messagebox.showerror("错误", "请选择论文PDF文件")
            return
        
        self.progress_var.set(0)
        self.log_message(f"开始处理文件: {input_file}")
        
        # 提取文本
        paper_text = self.extract_text_from_pdf(input_file)
        if not paper_text:
            messagebox.showerror("错误", "无法从PDF中提取文本")
            return
        
        # 生成专利内容
        abstract = self.generate_patent_content(paper_text, "abstract", 40)
        claims = self.generate_patent_content(paper_text, "claims", 60)
        description = self.generate_patent_content(paper_text, "description", 80)
        
        if not all([abstract, claims, description]):
            messagebox.showerror("错误", "生成专利内容失败")
            return
        
        # 创建输出文件名
        output_file = os.path.join(
            OUTPUT_DIR,
            f"专利申请书_{os.path.splitext(os.path.basename(input_file))[0]}.docx"
        )
        
        # 创建专利文档
        if self.create_patent_document(abstract, claims, description, output_file):
            self.log_message(f"专利文档已生成: {output_file}")
            messagebox.showinfo("成功", f"专利文档已生成：\n{output_file}")
        else:
            messagebox.showerror("错误", "创建专利文档失败")

def main():
    root = tk.Tk()
    app = PatentGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
