# InsCodeAI 使用指南

## 简介
InsCodeAI 提供了多种功能，包括文本生成、图像生成与编辑、语音合成与识别以及 OCR 识别等。本文档将指导您如何安装和使用这些功能。

## 安装
要使用 InsCodeAI，请确保您的环境中已安装 Python 3.7 或更高版本。然后按照以下步骤进行安装：

1. **安装依赖**：
   ```bash
   pip install InsCode
   ```

2. **配置 API 密钥**：
   在代码中或环境变量中设置 `api_key` 和 `base_url`。例如：
   ```python
   client = InsCode(api_key="test_key")
   ```

## 功能使用案例

### 文本生成
#### 单次对话完成
```python
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "写一个冒泡排序"}
        ]}]
    )
    print(completion.model_dump_json())
```

#### 图像辅助对话完成
```python
    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "这是什么"},
            {"type": "image_url",
             "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}}
        ]}]
    )
    print(completion.model_dump_json())
```

#### 流式对话完成
```python
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "写一个冒泡排序"}
        ]}],
        stream=True,
        stream_options={"include_usage": True}
    )
    for chunk in completion:
        print(chunk.model_dump_json())
```

#### 图像辅助流式对话完成
```python
    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "这是什么"},
            {"type": "image_url",
             "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}}
        ]}],
        stream=True,
        stream_options={"include_usage": True}
    )
    for chunk in completion:
        print(chunk.model_dump_json())
```

### 图像生成与编辑
#### 图像生成
```python
    completion = client.images.generate(
        model="wanx-v1",
        prompt="a cat",
        n=1,
        size="1024*1024",
        response_format="url"
    )
    print(completion)
```

#### 图像编辑
```python
    image = open("/Users/wanghan/Documents/111_small.jpeg", "rb")
    completion = client.images.edit(
        model="wanx-style-repaint-v1",
        prompt="a girl",
        image=image,
        response_format="b64_json",
        extra_body={
            "params": json.dumps({
                "input": {
                    "style_index": 3
                },
                "parameters": {
                    "test": 1234
                }
            }, ensure_ascii=False)
        }
    )
    print(completion)
```

### 语音合成与识别
#### 语音合成 (TTS)
```python
    with client.audio.speech.with_streaming_response.create(
        model="cosyvoice-v1",
        voice="longxiaochun",
        input="SiliconCloud 上提供的fish audio模型是基于 70 万小时多语言音频数据训练的领先文本到语音（TTS）模型，支持中文、英语、日语、德语、法语、西班牙语、韩语、阿拉伯语等多种语言，并能够音色克隆，具有非常好的实时性。",
        response_format="mp3",
    ) as response:
        response.stream_to_file("test.mp3")
```

#### 语音识别
```python
    audio_file = open("/Users/wanghan/Downloads/hello_world_female2.wav", "rb")
    transcription = client.audio.transcriptions.create(model="paraformer-v2",
                                                       file=audio_file)
    print(transcription.text)
```

### OCR 识别
```python
    image_file = "/Users/wanghan/Documents/123.png"
    result = client.ocr.recognize(image=image_file)
    print(result)
```
