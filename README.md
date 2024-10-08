# 书生带你看奥运 —基于InternLM2.5 大模型的体育大赛播报平台

## 简介
"书生带你看奥运"项目基于 InternLM2.5 大模型，采用RAG 技术、XTuner 微调技术、LMDeploy 部署工具，为用户提供及时、可靠、准确的奥运信息。

本项目尝试打造一个全方位的体育大赛信息平台，旨在为广大体育爱好者提供全新的体育赛事体验 ，不仅能追踪赛事动态，还能深入分析运动员表现。用AI大模型技术扮演一个虚拟的新闻发布官和赛事评论员。

## 架构图
![架构图](https://github.com/user-attachments/assets/ba33f7e1-3c87-4558-b603-ba774bbfa052)
## 应用场景图
![效果图](https://github.com/user-attachments/assets/6ee69e45-a774-4351-94d2-935c458b857b)

## 项目视频
项目视频：https://www.bilibili.com/video/BV1SGeteMEF2/

## 配置环境

### 安装python 依赖包

```shell
pip install einops
pip install protobuf
```
### 安装Streamlit

```shell
pip install streamlit==1.36.0
```

### 安装 XTuner

```shell
# 创建一个目录，用来存放源代码
mkdir -p /root/InternLM/code

cd /root/InternLM/code

git clone -b v0.1.21  https://github.com/InternLM/XTuner

cd /root/InternLM/code/XTuner
pip install -e '.[deepspeed]'
```

### 安装 Llamaindex

```shell
pip install llama-index==0.10.38 llama-index-llms-huggingface==0.2.0 "transformers[torch]==4.41.1" "huggingface_hub[inference]==0.23.1" huggingface_hub==0.23.1 sentence-transformers==2.7.0 sentencepiece==0.2.0
```

### 下载 Sentence Transformer 模型

```shell
python download_hf.py
```

### 下载 NLTK 相关资源

```shell
cd /root
git clone https://gitee.com/yzy0612/nltk_data.git  --branch gh-pages
cd nltk_data
mv packages/*  ./
cd tokenizers
unzip punkt.zip
cd ../taggers
unzip averaged_perceptron_tagger.zip

```

### 下载模型

下载模型，并建立软连接
```shell
cd ~/model
ln -s /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b/ ./
mkdir /root/models
ln -s /root/share/new_models//Shanghai_AI_Laboratory/internlm2_5-7b-chat /root/models
ln -s /root/share/new_models/OpenGVLab/InternVL2-26B /root/models

```

## 运行

```shell
streamlit run app.py

```
## 致谢
感谢 上海人工智能实验室书生大模型实战营的培训和指导

感谢 OpenXLab 对项目的算力支持


[书生实战营GitHub仓库](https://github.com/InternLM/Tutorial)
