import os

api_key = os.environ.get("OPENAI_API_KEY")

if api_key:
    print("OpenAI APIキーが設定されています。")
else:
    print("OpenAI APIキーが見つかりません。")

from openai import OpenAI

client = OpenAI()

print("準備OK")

#1　クライアントの作成
client = OpenAI()


#2　応答の生成
response = client.chat.completions.create(
    temperature = 0.0,
    model = "gpt-4o-mini",
    messages=[{"role": "user", "content": "こんにちは"}],
)


#3　応答の表示
print(response.choices[0].message.content)

history = []
n = 10 #会話回数の上限
model = "gpt-4o-mini"
for _ in range(n):
    #1 ユーザーからの入力を受け取る
    user_input = input("ユーザー: ")
    if user_input == "exit": # exitと入力されたら終了
        break
    print(f"ユーザー: {user_input}")

    #2 会話履歴に新たな入力をユーザー入力として追加する
    history.append({"role": "user", "content": user_input})

    #3ChatGPTに会話履歴を入力して新たな応答を取得する
    response = client.chat.completions.create(\
        model=model, messages=history)
    content = response.choices[0].message.content

    #4 新たな応答を表示する
    print(f"AI: {content}")

    #5 会話履歴に新たな応答をAIの出力として追加する
    history.append({"role": "assistant", "content": content})



