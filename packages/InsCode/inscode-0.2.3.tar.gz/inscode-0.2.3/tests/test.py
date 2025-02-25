import json
from InsCode import InsCode

client = InsCode(api_key="a843561eed3d4d748593254e95716886")


def test_chat_completion():
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "写一个冒泡排序"}
        ]}]
    )

    print(completion.model_dump_json())


def test_image_chat_completion():
    # completion = client.chat.completions.create(
    #     model="qwen-vl-plus",
    #     messages=[{"role": "user", "content": [
    #         {"type": "text", "text": "这是什么"},
    #         {"type": "image_url",
    #          "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"}}
    #     ]}]
    # )
    image = open("/Users/wanghan/Documents/111_small.jpeg", "rb")
    import base64
    image_base64 = base64.b64encode(image.read()).decode('utf-8')
    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        stream=False,
        # messages=[{"role": "user", "content": [
        #     {"type": "text", "text": "这是什么"},
        #     {"type": "image_url",
        #      "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        # ]}]
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "写一个冒泡排序"},
        ]}]
    )

    print(completion.model_dump_json())

def test_chat_stream():
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "写一个冒泡排序"}
        ]}],
        stream=False,
        stream_options={"include_usage": True}
    )
    for chunk in completion:
        print(chunk.model_dump_json())


def test_image_chat_stream():
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


def test_image_generation():
    completion = client.images.generate(
        model="wanx-v1",
        prompt="a cat",
        n=1,
        size="1024*1024",
        response_format="url"
    )
    print(completion)


def test_image_edit():
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


def test_audio_tts():
    with client.audio.speech.with_streaming_response.create(
        model="cosyvoice-v1",
        voice="longxiaochun",  # 此处传入空值，表示使用动态音色
        # 用户输入信息
        input="SiliconCloud 上提供的fish audio模型是基于 70 万小时多语言音频数据训练的领先文本到语音（TTS）模型，支持中文、英语、日语、德语、法语、西班牙语、韩语、阿拉伯语等多种语言，并能够音色克隆，具有非常好的实时性。",
        response_format="mp3",
    ) as response:
        response.stream_to_file("test.mp3")


def test_audio_recognition():
    audio_file = open("/Users/wanghan/Downloads/hello_world_female2.wav", "rb")
    transcription = client.audio.transcriptions.create(model="paraformer-v2",
                                                       file=audio_file)
    print(transcription.text)


def test_ocr():
    image_file = "/Users/wanghan/Documents/123.png"
    result = client.ocr.recognize(image=image_file)
    print(result)


test_chat_completion()
