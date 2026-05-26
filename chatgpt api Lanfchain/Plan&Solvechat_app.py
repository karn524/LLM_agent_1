from pydantic import BaseModel, Field
from langchain_core.runnables.base import Runnable

# Plam-and-Solveに利用するモデル
class ActionItem(BaseModel):
    action_name: str = Field(description="アクション名")
    action_description: str = Field(description="アクションの詳細")

class Plan(BaseModel):
    """アクションプランを格納する"""
    problem: str = Field(description="問題の説明")
    actions: list[ActionItem] = Field(description="実行すべきアクションリスト")

class ActionResult(BaseModel):
    """実行時の考えと結果を格納する"""

    thoughs: str = Field(description="検討内容")
    result: str = Field(description="結果")


# 個別タスクの実行Runnableを作成
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai.output_parsers.tools import PydanticToolsParser

ACTION_PROMPT = """問題をアクションに分解して解いています。
これまでのアクションの結果と、次に行うべきアクションを示すので、実際にアクションを実行してその結果を報告してください。
# 問題
{problem}
# アクションプラン
{action_items}
# これまでのアクションの結果
{action_results}
# 次のアクション
{next_action}"""

llm = ChatOpenAI(model="gpt-4o-mini")
llm_action = llm.bind_tools([ActionResult], tool_choice="AtionResult")
action_parser = PydanticToolsParser(tools=[ActionItem], first_tool_only=True)

action_prompt = PromptTemplate.from_template(ACTION_PROMPT)
action_runnable = action_prompt | llm_action | action_parser

# action_loop関数
from langchain_core.messages import AIMessage

def action_loop(action_plan: Plan) -> AIMessage:
    problem = action_plan.problem
    actions = action_plan.actions

    #1 計画の全体像を箇条書きにする
    action_items = "\n".join(["* " + action.action_name for action in actions])
    action_results_str = ""

    #2 ActionItemを取り出すループ
    for i, action in enumerate(actions):
        print("="*20)
        print(f"[{i+1}/{len(actions)}]以下のアクションを実行します。")
        print(action.action_name)

        #3 次のアクションの説明を作成
        next_action = f"*{action.action_name} \n{action.action_description}"
        response = action_runnable.invoke(dict(problem=problem, action_items=action_items, action_results=action_results_str, next_action=next_action))

        #4 実行結果を追記する
        action_results_str += f"*{action.action_name} \n{response.result}\n"

        print("-" *10 + "検討内容" + "-" *10)
        print(response.thoughts)
        print("-" *10 + "結果" + "-" *10)
        print(response.result)

        #5 実行結果の全体をAIMessageとして返す
        return AIMessage(action_results_str)


# タスクの複雑さによる分岐
plan_parser= PydanticToolsParser(tools=[Plan], first_tool_only=True)

def route(ai_message: AIMessage) -> Runnable | AIMessage:
    if ai_message.response_metadata["finish_reason"] == "tool_calls":
        return plan_parser | action_loop
    else:
        return ai_message
    

#　Plan-and-Solve Runnableの作成
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

PLAN_AND_SOLVE_PROMPT = """\
ユーザーの質問がすく雑な場合は、アクションプランを作成し、そのあとに1つずつ実行するPlan-and-Solve形式をとります。
これが必要とした判断した場合は、Planツールによってアクションプランを保存してください。"""
system_prompt = SystemMessage(PLAN_AND_SOLVE_PROMPT)
chat_prompt = ChatPromptTemplate.from_messages([system_prompt,MessagesPlaceholder(variable_name="history")])

llm_plan = llm.bind_tools(tools=[Plan])
planning_runnable = chat_prompt | llm_plan | route


# Plan-and-Solveを利用したチャットボット
# チャット部分の作成
from langchain_core.messages import HumanMessage

history = []
n = 10
for i in range(10):
    user_input = input("ユーザ入力 : ")
    if user_input == "exit":
        break
    #1 HumanMessageの作成と表示
    human_message = HumanMessage(user_input)
    human_message.pretty_print()
    #2 会話履歴の追加
    history.append(HumanMessage(user_input))
    #3 応答の作成と表示
    ai_message = planning_runnable.invoke(dict(history=history))
    ai_message.pretty_print()
    #4 会話履歴の追加
    history.append(ai_message)
