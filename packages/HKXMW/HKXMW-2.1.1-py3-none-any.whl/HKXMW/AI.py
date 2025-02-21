import re
import requests


def story(role, content):
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    data = {
            "max_tokens": 60,     # 回复长度限制
            "top_k": 5,             # 灵活度
            "temperature": 0.6,     # 随机性
            "messages": [
        {
            # 设置对话背景或赋予模型角色，该设定会贯穿整轮对话，对全局的模型生成结果产生影响。对应作为'role'为'system'时，'content'的值
            "role": "system",
            "content": "你是一位非常优秀的" + role + "，请根据我的提问，非常科学、有趣和严谨的回答我。"
        },
        {
            # 对大模型发出的具体指令，用于描述需要大模型完成的目标任务和需求说明。会与角色设定中的内容拼接，共同作为'role'为'system'时，'content'的值
            "role": "user",
            "content": content + "(一定要80个字左右，语句必须完整，语句必须完整，不准出现断句。)"
        }
    ],
    "model": "4.0Ultra"
    }
    data["stream"] = True
    header = {
            "Authorization": "Bearer paNyLCaJQOpyOBmflKZp:yhBhAlSFMwaqlVKAtDbv"
    }
    response = requests.post(url, headers=header, json=data, stream=True)

    # 流式响应解析示例
    response.encoding = "utf-8"
    contents = ""
    result = response.iter_lines(decode_unicode="utf-8")
    result = str(list(result))
     
    # 正则表达式模式
    pattern = r'"content":"(.*?)"'

    # 使用re.findall查找所有匹配的内容
    contents = re.findall(pattern, result, re.DOTALL)
    s = "   "
    for i in contents:
        s += i
    if '\\' in s:
        s = s.replace('\\', "")
    if '*' in s:
        s = s.replace('*', "")
    sum_ = """"""
    for i in range(0,len(s),17):
        sum_ = sum_ + s[i:i+17] + "\n"
    return sum_
