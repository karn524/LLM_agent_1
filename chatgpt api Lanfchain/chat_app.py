# LangChainを用いたチャットアプリケーション
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage

#1 ChatModelの定義
llm = ChatOpenAI(model="gpt-4o-mini")

history = []
n = 10
for i in range(10):
    user_input = input("ユーザ入力:")
    if user_input == "exit":
        break

    #2 HumanMessageの作成と表示
    human_message = HumanMessage(user_input)
    human_message.pretty_print()

    #3　会話履歴の追加
    history.append(HumanMessage(user_input))

    #4 応答の作成と表示
    ai_message = llm.invoke(history)
    ai_message.pretty_print()

    #5会話履歴の追加
    history.append(ai_message)