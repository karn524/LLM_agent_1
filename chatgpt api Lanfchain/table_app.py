from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_openai.chat_models import ChatOpenAI
import csv

#1 入力形式の定義
class CSVSaveToolInput(BaseModel):
    filename: str = Field(description="ファイル名")
    csv_text: str = Field(description="CSVのテキスト")
@tool("csv-save-tool", args_schema=CSVSaveToolInput)
def csv_save(filename: str, csv_text: str):
    """CSVテキストをファイルに保存する"""
    ## parse CSV text
    try:
        rows = list(csv.reader(csv_text.splitlines()))
    except Exception as e:
        return False
    
    # save to file
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return True

#3 ツールをLLMに紐付ける
llm = ChatOpenAI(model="gpt-4o-mini")
tools = [csv_save]
llm_with_tool = llm.bind_tools(tools=tools, tool_choice="csv-save-tool")

TABLE_PROMPT = """{user_input}結果はCSVファイルに保存してください。ただし、ファイル名は上記の内容から適切に決定してください。"""
prompt = PromptTemplate.from_template(TABLE_PROMPT)

#4 Runnableの作成
def get_tool_args(x):
    return x.tool_calls[0] # AIMessageからToolCallオブジェクトを取り出す。

runnable = prompt | llm_with_tool | get_tool_args | csv_save

user_input = "フィボナッチ数列の番号と値を10番目まで表にまとめて、CSVファイルに保存してください。"

#5 Runnableの実行と結果の確認
response = runnable.invoke(dict(user_input=user_input))
print(response)