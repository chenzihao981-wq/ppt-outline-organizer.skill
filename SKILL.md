---
name: ppt-outline-organizer-skill
description: >-
  从PDF课件中提取答案，填充到docx复习提纲中，生成分条格式的复习副本。
  适用于韩国大学课件（PPT转PDF）和docx提纲文件。
  关键词：考试复习、提纲填充、课件答案、PDF提取、红色答案、分条列点。
  触发词：考试复习、提纲、课件、答案填充、review、exam、outline、fill answers。
license: MIT
metadata:
  author: mao
  version: 1.0.0
  created: 2026-06-23
  last_reviewed: 2026-06-23
  review_interval_days: 90
  dependencies:
    - url: https://github.com/nickvdyck/docx
      name: docx (npm)
      type: npm
---

# /ppt-outline-organizer

从PDF课件中查找答案，填充到docx复习提纲，生成分条格式的复习副本。

## Trigger

用户输入包含以下关键词时激活：
- 考试复习、提纲填充、课件答案
- review, exam, outline, fill answers
- PDF + docx + 答案

示例调用：
```
/ppt-outline-organizer 根据这三个PDF课件，找到提纲里的题目答案，用红色写进去
/ppt-outline-organizer 把课件答案填到复习提纲里，分条列点
/ppt-outline-organizer 用这三个PPT的答案补全提纲.docx
```

## 工作流程

### 输入
- **docx 提纲**：包含题目的 Word 文档，题目格式为 `1. 题目文字`，每个题目一个段落
- **PDF 课件**：一个或多个 PDF 文件（PPT转PDF、电子版教材等，需可提取文字）

### 输出
- **副本 docx**：在原始提纲基础上，每个题目后面添加红色答案，按 ①②③... 分条列点，每条换行
- 原始提纲文件保持不动

### 步骤

#### 1. 读取提纲
使用 docx skill 的 unpack 工具解压 docx，读取 `word/document.xml`：
```bash
python <docx-skill-path>/scripts/office/unpack.py 提纲.docx unpacked/
```
从 XML 中提取所有题目文本（在 `<w:t>` 标签中，格式为 `数字. 题目文字`）。

#### 2. 从 PDF 中查找答案
使用 Read 工具读取每个 PDF（每次最多20页）。
为每个题目在 PDF 内容中定位相关答案，整理为中文要点。

**注意事项**：
- 韩国课件通常为韩中双语或韩英双语，重点提取中文或可翻译的内容
- 答案需精简为 2-5 个要点
- 如果 PDF 中找不到某题答案，标注"课件中未找到相关内容"

#### 3. 写入答案（红色字体）
将答案写入解压后的 XML。每个答案作为新的 `<w:r>` 节点插入到题目段落的 `</w:p>` 之前：
```xml
<w:r>
  <w:rPr>
    <w:rFonts w:hint="eastAsia"/>
    <w:color w:val="FF0000"/>
  </w:rPr>
  <w:t xml:space="preserve">答案内容</w:t>
</w:r>
```

使用 `scripts/add_answers.py` 自动完成：
```bash
cd unpacked/
python <skill-path>/scripts/add_answers.py
```
答案数据需预先写入 `answers.json`，格式为 `{"题目文字": "答案内容"}`。

**注意**：题目 key 必须与 XML 中的 `<w:t>` 文本完全匹配（包括编号前缀如 `1. `）。

#### 4. 清理英文
在 XML 中检查英文内容：
- **名词注释**（如 `（Bacteria，原核）`）→ 删除括号及内容
- **人名** → 查中文名替换
- **标准缩写**（DNA、ATP 等）→ 保留

#### 5. 生成分条副本
使用 `scripts/split_answers.py` 将每个答案按 `；` 分割为 ①②③... 格式：
```bash
cd unpacked/
python <skill-path>/scripts/split_answers.py
```

#### 6. 打包输出
```bash
python <docx-skill-path>/scripts/office/pack.py unpacked/ 输出副本.docx --original 提纲.docx --validate false
```

## XML 编辑注意事项

- `<` 必须转义为 `&lt;`，`>` 转义为 `&gt;`
- `xml:space="preserve"` 用于保留前导空格
- 打包时使用 `--validate false` 跳过严格的 XML 验证（paraId 等警告可忽略）
- 编码问题：Python 脚本需设置 `PYTHONUTF8=1`

## 参考文档

详细工作流和故障排除见 `references/workflow.md`。
