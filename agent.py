from openai import OpenAI
from tools.weather import xinzhi_weather
from tools.pearapi import history_today,  answers_book, cnl

# 配置大模型
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key="sk-f5653c6fef5542eebcf4b789ab9bad29",
)

# 定义所有工具
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "xinzhi_weather",
            "description": "查询城市实时天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "history_today",
            "description": "查询历史上的今天",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cnl",
            "description": "获取随机超能力",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "answers_book",
            "description": "答案之书",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "用户的问题"}
                },
                "required": ["question"]
            }
        }
    }
]

# 工具映射
TOOL_MAP = {
    "xinzhi_weather": xinzhi_weather,
    "history_today": history_today,
    "cnl":cnl,
    "answers_book": answers_book
}


def run_agent(query: str):
    messages = [{"role": "user", "content": query}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    response_msg = response.choices[0].message
    tool_calls = response_msg.tool_calls

    if not tool_calls:
        print("🤖 模型回答：", response_msg.content)
        return

    # 只执行工具，只输出结果 → 彻底删掉崩溃的二次对话！
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        func_args = eval(tool_call.function.arguments)
        result = TOOL_MAP[func_name](**func_args)
        print(f"✅ 调用工具：{func_name}")
        print(f"📊 工具结果：{result}")


if __name__ == "__main__":
    while True:
        user_input = input("请输入问题（退出：q）：")
        if user_input == "q":
            break
        run_agent(user_input)