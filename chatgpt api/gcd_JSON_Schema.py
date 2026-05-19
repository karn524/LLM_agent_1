from openai import OpenAI
import json
import math
from pydantic import BaseModel, Field

client = OpenAI()
print("準備OK")

#1 関数の情報を作成
gcd_function = {
    "name": "gcd",
    "description": "最大公約数を求める",
    "parameters": {
        "type": "object",
        "properties": {
            "num1": {"type": "number", "description": "整数1"},
            "num2": {"type": "number", "description": "整数2"},
        },
        "required": ["num1","num2"],
    },
}
tools = [{"type": "function", "function": gcd_function}]

messages = [
    {
        "role": "user",
        "content": "50141と53599の最大公約数を求めてください。",
    }
]

#2 ツールを渡して応答を生成
response = client.chat.completions.create(
    model="gpt-4o-mini", messages=messages, tools=tools
)
print(response.choices[0].message.content) #None
print(response.choices[0].finish_reason) #tool_calls
print(
    response.choices[0].message.tool_calls
) # [ChatCompletionMessageToolCall(...)]

#　関数情報の抽出
function_info = response.choices[0].message.tool_calls[0].function
name = function_info.name
args = json.loads(function_info.arguments)

# 最大公約数の計算
print(math.gcd(args["num1"], args["num2"])) # 1729

#1 Pydanticによる関数情報の作成
class GCD(BaseModel):
    num1: int = Field(description="整数１")
    num2: int = Field(description="整数２")

#2　関数情報をJSON Schemaに変換
gcd_function = {
    "name": "gcd",
    "description": "最大公約数を求める",
    "parameters": GCD.model_json_schema(),
}

# Pydanticを用いた因数の取得
parsed_result = GCD.model_validate_json(
    response.choices[0].message.tool_calls[0].function.arguments
)
print(parsed_result)

#　ツール利用全体の流れ
class LCM(BaseModel):
    num1: int = Field(description="整数１")
    num2: int = Field(description="整数２")

lcm_function = {
    "name": "lcm",
    "description": "最小公倍数を求める",
    "parameters": LCM.model_json_schema(),
}

tools = [
    {"type": "function", "function": gcd_function},
    {"type": "function", "function": lcm_function},
]

messages = [
    {
        "role": "user",
        "content": "50141と53599の最大公約数と最小公倍数を求めてください。",
    }
]

response = client.chat.completions.create(
    model="gpt-4o", messages=messages, tools=tools    
)
choice = response.choices[0]
if choice.finish_reason == "tool_calls":
    for tool in choice.message.tool_calls:
        if tool.function.name == "gcd":
            gcd_args = GCD.model_validate_json(tool.function.arguments)
            print(f"最大公約数: {math.gcd(gcd_args.num1, gcd_args.num2)}")
        elif tool.function.name == "lcm":
            lcm_args = LCM.model_validate_json(tool.function.arguments)
            print(f"最小公倍数: {math.lcm(lcm_args.num1,lcm_args.num2)}")
elif choice.finish_reason == "stop":
    print("AI: ", choice.message.content)


# response_foematの利用例
class Translations(BaseModel):
    english: str = Field(description="英語の文章")
    french: str = Field(description="フランス語の文章")
    chinese: str = Field(description="中国語の文章")

prompt = f"""\
以下に示す文章を英語・フランス語・中国語に翻訳してください。
ただし、アウトプットは後述するフォーマットのJSON形式で出力してください。
# 文章
吾輩は猫である。名前はまだない。

#出力フォーマット
いかにJSON Schema形式のフォーマットを示します。このフォーマットに従うオブジェクトの形で出力してください。
{Translations.model_json_schema()}"""

response = client.chat.completions.create(
    temperature=0.0,
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"},
)

translations = Translations.model_validate_json(response.choices[0].message.content)
print("英語:", translations.english)
print("フランス語:", translations.french)
print("中国語:", translations.chinese)


# JSON Schemaを利用する別の方法
prompt = f"""\
以下に示す文章を英語・フランス語・中国語に翻訳してください。
ただし、アウトプットは後述するフォーマットのJSON形式で出力してください。
# 文章
吾輩は猫である。名前はまだない。

#出力フォーマット
JSON Schemaに従う形式で出力してください。"""

response = client.beta.chat.completions.parse(
    temperature=0.0,
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    response_format=Translations,
)

translations = response.choices[0].message.parsed
print("英語:", translations.english)
print("フランス語:", translations.french)
print("中国語:", translations.chinese)