# PageIndex 网络下载问题 - 解决方案

## 问题
由于网络不稳定，无法通过wget/curl/git clone下载PageIndex

## 解决方案

### 方案1: 手动下载（推荐）

1. 在浏览器中访问: https://github.com/VectifyAI/PageIndex/archive/refs/heads/main.zip
2. 下载完成后，将文件放到: `~/Documents/unreal_rag/pageindex/PageIndex.zip`
3. 运行解压脚本:
   ```bash
   cd ~/Documents/unreal_rag/pageindex
   unzip PageIndex.zip
   mv PageIndex-main PageIndex
   ```

### 方案2: 使用代理/镜像

如果你有代理或其他网络访问方式:
```bash
export https_proxy=your_proxy:port
cd ~/Documents/unreal_rag
./setup_pageindex.sh
```

### 方案3: 使用GitHub CLI（如果已安装）

```bash
cd ~/Documents/unreal_rag/pageindex
gh repo clone VectifyAI/PageIndex
```

### 方案4: 从其他源获取

- Gitee镜像（如果有）
- 从同事/朋友处复制
- 使用离线包

## 临时替代方案

如果暂时无法获取PageIndex，您可以：

1. **直接使用文档**: 已收集的221个Markdown文件可以直接阅读
2. **简单的全文搜索**: 使用grep/ripgrep搜索文档
3. **等待更好的网络条件**: 稍后重试

## 检查文件完整性

下载完成后，验证文件:
```bash
cd ~/Documents/unreal_rag/pageindex
unzip -t PageIndex.zip  # 测试zip完整性
```

## 完成后的步骤

PageIndex就位后:
```bash
cd ~/Documents/unreal_rag
pip3 install -r requirements.txt
cp .env.example .env
# 编辑.env添加CHATGPT_API_KEY
cd pageindex/scripts
python3 build_index.py
```

---

**需要帮助?** 检查DELIVERY.md和QUICKSTART.md获取更多信息
