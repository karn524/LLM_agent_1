from openai import OpenAI

client = OpenAI()
print("準備OK")

response = client.chat.completions.create(
    temperature = 0.0,
    model = "gpt-4o-mini",
    messages=[{"role": "user", "content": "こんにちは"}],
)

history = []
n = 10 #会話の上限
model = "gpt-4o-mini"
for _ in range(n):
    user_input = input("ユーザ入力: ")
    if user_input == "exit":
        break
    print(f"ユーザ: {user_input}")
    history.append({"role": "user", "content": user_input})

    #1 stream=Tureでストリーミングを有効化
    stream = client.chat.completions.create(
        model=model, messages=history, stream=True
    )
    print("AI: ", end="")

    #2 応答を集める文字列
    ai_content = ""

    #3　ストリーミングの各チャンクを処理
    for chunk in stream:
        #4 messageではなくdelta
        content = chunk.choices[0].delta.content

        #5 ChoiceDeltaのfinish_reasonがstopなら生成完了
        if chunk.choices[0].finish_reason == "stop":
            break
        print(content, end="")
        ai_content += content
    print()
    history.append({"role": "assistant", \
    "content": ai_content})
