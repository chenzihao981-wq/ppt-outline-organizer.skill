# ppt-outline-organizer 工作流详解

## 完整流程

### 1. 解压提纲 docx

```bash
python <docx-skill>/scripts/office/unpack.py 提纲.docx unpacked/
```

产出 `unpacked/word/document.xml`，这是需要编辑的核心文件。

### 2. 提取题目

从 XML 中提取所有题目文本。题目格式为 `<w:t>N. 题目文字</w:t>`。

用 Python 提取：
```python
import re
with open('unpacked/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()
questions = re.findall(r'<w:t>(\d+\.\s*[^<]+)</w:t>', content)
```

### 3. 从 PDF 查找答案

使用 Read 工具读取 PDF（每次最多20页），为每个题目定位答案。

**提取要点**：
- 答案必须来自 PDF 内容，不要编造
- 精简为 2-5 个要点
- 全部使用中文
- 如果 PDF 中找不到，标注"课件中未找到"

**写入 answers.json**：
```json
{
  "1. 题目文字": "①要点一；②要点二；③要点三",
  "2. 题目文字": "①要点一；②要点二"
}
```

**注意**：JSON 的 key 必须与 XML 中的 `<w:t>` 文本完全一致，包括编号前缀。

### 4. 写入红色答案

```bash
cd unpacked/
python <skill>/scripts/add_answers.py
```

脚本会：
- 读取 answers.json
- 在 XML 中找到每个题目
- 在题目段落的 `</w:p>` 前插入红色 `<w:r>` 节点
- 自动转义 `<` `>` 字符

### 5. 清理英文

在 XML 中搜索英文内容，按类型处理：
- 名词注释 `（English term）` → 删除
- 人名 → 查中文名替换
- 缩写 DNA/ATP 等 → 保留

### 6. 分条格式化

```bash
cd unpacked/
python <skill>/scripts/split_answers.py
```

脚本会：
- 找到所有红色答案段落
- 按 `；` 分割为多条
- 每条前加 ①②③... 编号
- 每条生成独立段落实现换行

### 7. 打包输出

```bash
python <docx-skill>/scripts/office/pack.py unpacked/ 输出副本.docx --original 提纲.docx --validate false
```

## 故障排除

### 题目匹配失败
- 检查 answers.json 的 key 是否与 XML 中的 `<w:t>` 文本完全一致
- 注意编号前缀：第2、3章题目在 XML 中是 `1. 题目文字` 格式

### XML 解析错误
- 检查答案中是否有未转义的 `<` `>` 字符
- add_answers.py 已自动处理转义

### 打包失败
- 使用 `--validate false` 跳过严格验证
- paraId 警告可忽略，不影响文件使用

### 编码问题
- Windows 下运行 Python 脚本需设置 `PYTHONUTF8=1`
- 或在命令前加 `chcp 65001`
