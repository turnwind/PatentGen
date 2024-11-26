# 专利生成器 (Patent Generator)

这是一个基于OpenAI API的专利生成工具，可以将学术论文转换为符合中国专利申请格式的文档。

## 功能特点

- 支持PDF格式论文输入
- 自动提取论文关键内容
- 使用OpenAI API生成专利相关内容
- 生成符合中国专利申请格式的Word文档

## 安装说明

1. 克隆项目到本地
2. 安装依赖：
```bash
pip install -r requirements.txt
```
3. 创建.env文件并添加OpenAI API密钥：
```
OPENAI_API_KEY=your_api_key_here
```

## 使用方法

1. 将论文PDF文件放在input目录下
2. 运行程序：
```bash
python patent_generator.py
```
3. 生成的专利文档将保存在output目录下

## 注意事项

- 请确保您有足够的OpenAI API额度
- 生成的专利文档可能需要进一步人工审核和修改
- 建议在使用前仔细阅读中国专利申请相关规定
