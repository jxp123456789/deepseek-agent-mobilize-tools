import requests

# -------------------------- 历史上的今天 --------------------------
def history_today() -> str:
    try:
        url = "https://api.pearktrue.cn/api/lsjt/"
        res = requests.get(url, timeout=10)
        # 接口返回纯文本，直接返回即可
        return "历史上的今天：\n" + res.text.strip()
    except:
        return "历史上的今天：1945年4月12日 罗斯福总统去世"

# -------------------------- 随机超能力（原名 hot_60s，只改内容不改函数名） --------------------------
def cnl() -> str:
    try:
        url = "https://api.pearktrue.cn/api/superpower"
        res = requests.get(url, timeout=10)
        data = res.json()
        if data.get("code")==200:
            ability = data["data"]["superpower"]
            defect = data["data"]["disadvantage"]
            return f"随机超能力：{ability}\n副作用：{defect}"
        return "随机超能力：获取成功"
    except:
        return "随机超能力：接口异常"

# -------------------------- 答案之书 --------------------------
def answers_book(question="我现在对吗"):
    try:
        url = "https://api.pearktrue.cn/api/answersbook/"
        res = requests.get(url, params={"question":question}, timeout=8)
        data = res.json()
        if data.get("code")==200:
            return f"答案之书：{data['data']}"
        return "答案之书：请提出你的问题"
    except:
        return "答案之书：相信自己"