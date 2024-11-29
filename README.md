# PatentGen - 智能专利文档生成器

PatentGen 是一个基于人工智能的专利文档生成工具，能够自动将研究论文转换为标准的专利申请文档。它使用先进的自然语言处理技术，帮助研究人员和专利代理人快速生成高质量的专利申请文档。

## 功能特点

- 🚀 自动提取PDF论文中的核心技术内容
- 📝 智能生成符合标准的专利摘要、权利要求和说明书
- 💡 实时显示生成进度和处理状态
- 📊 支持Web界面和桌面GUI两种使用方式
- 📄 自动导出标准格式的Word文档
- 🔄 支持实时预览和编辑生成的内容

## 系统要求

- Python 3.8+
- Windows/Linux/MacOS
- 2GB+ 可用内存
- 网络连接（用于API调用）

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/PatentGen.git
cd PatentGen
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置API密钥：
   - 复制 `config.py.example` 为 `config.py`
   - 在 `config.py` 中设置你的 OpenAI API 密钥和基础URL

## 使用方法

### Web界面

1. 启动Web服务器：
```bash
python app.py
```

2. 打开浏览器访问：`http://localhost:5000`

3. 使用步骤：
   - 点击"选择文件"上传PDF论文
   - 点击"生成专利"开始处理
   - 实时查看生成进度和内容
   - 下载生成的Word文档

### 桌面GUI

1. 启动桌面应用：
```bash
python patent_generator_gui.py
```

2. 使用步骤：
   - 点击"浏览"选择PDF文件
   - 点击"生成专利"开始处理
   - 查看处理日志和进度
   - 生成完成后自动保存Word文档

## 目录结构

```
PatentGen/
├── app.py              # Web应用主程序
├── patent_generator_gui.py  # 桌面GUI程序
├── patent_generator.py # 专利生成核心逻辑
├── agents.py          # AI代理实现
├── events.py          # 事件处理系统
├── config.py          # 配置文件
├── templates/         # Web界面模板
├── static/           # Web静态资源
├── input/            # 输入文件目录
├── output/           # 输出文件目录
└── uploads/          # 上传文件临时目录
```

## 配置说明

在 `config.py` 中可以配置以下参数：

- `OPENAI_API_KEY`: OpenAI API密钥
- `OPENAI_BASE_URL`: API基础URL
- `OPENAI_MODEL`: 使用的语言模型（默认：gpt-4-1106-preview）
- `INPUT_DIR`: 输入文件目录
- `OUTPUT_DIR`: 输出文件目录

## 注意事项

1. 确保PDF文件内容清晰可提取
2. 建议使用A4大小的PDF文件
3. 生成过程可能需要几分钟，请耐心等待
4. 生成的内容可能需要进一步人工审核和修改

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。在提交代码前，请确保：

1. 代码符合 PEP 8 规范
2. 添加了必要的注释和文档
3. 通过了所有测试

## 更新日志

### v1.0.0 (2024-03-xx)
- 初始版本发布
- 支持Web界面和桌面GUI
- 实现基本的专利文档生成功能
- 添加实时进度显示
- 支持Word文档导出
