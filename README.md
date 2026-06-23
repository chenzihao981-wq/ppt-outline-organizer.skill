# PPT Outline Organizer

从PDF课件中提取答案，填充到docx复习提纲中，生成分条格式的复习副本。

## 功能

- 自动从PDF课件（PPT转PDF）中查找题目答案
- 以红色字体填充到docx提纲的每道题目后
- 支持分条列点格式（①②③...），每条换行
- 适用于韩国大学课件，也适用于其他语言的PDF+docx组合

## 安装

### Claude Code

```bash
git clone https://github.com/chenzihao981-wq/ppt-outline-organizer.skill.git ~/.claude/skills/ppt-outline-organizer
```

### Cursor

```bash
git clone https://github.com/chenzihao981-wq/ppt-outline-organizer.skill.git .cursor/rules/ppt-outline-organizer
```

### 通用路径（Gemini CLI、Kiro 等）

```bash
git clone https://github.com/chenzihao981-wq/ppt-outline-organizer.skill.git ~/.agents/skills/ppt-outline-organizer
```

### 使用安装脚本

```bash
cd ppt-outline-organizer.skill
chmod +x install.sh
./install.sh
```

## 使用方法

打开新会话，输入：

```
/ppt-outline-organizer 根据PDF课件填充复习提纲
```

### 输入

- **docx 提纲**：包含题目的Word文档，题目格式为 `1. 题目文字`
- **PDF 课件**：一个或多个PDF文件（PPT转PDF、电子版教材等）

### 输出

- **副本 docx**：每个题目后添加红色答案，按 ①②③... 分条列点

## 工作流程

1. 解压 docx 提纲，读取 XML 中的题目
2. 从 PDF 课件中查找每道题的答案
3. 将答案以红色字体写入 XML
4. 清理英文注释
5. 按分号分割答案为多条，加圆圈编号
6. 打包输出副本 docx

## 依赖

- Python 3
- docx skill（用于解压/打包 docx）

## 许可证

MIT
