from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")

#1 テンプレートの作成
TRANSLATION_PROMPT = """以下の文章を{language}に翻訳し、翻訳結果のみを返してください。{source_text}"""
prompt = PromptTemplate.from_template(TRANSLATION_PROMPT)

#2 Runnableの作成
runnable = prompt | llm

language = "日本語"
source_text = """cogito, ergo sum"""

#3 Runnableの実行と結果の表示
response = runnable.invoke(dict(language=language, source_text=source_text))
response.pretty_print()