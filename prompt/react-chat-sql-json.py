from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    ChatMessagePromptTemplate,
)
from langchain.schema import HumanMessage, ChatMessage

"""
构建 ReAct 的 prompt
试验 https://smith.langchain.com/hub/hwchase17/react-chat-json/playground?organizationId=15e34838-aa8f-598a-8902-0cc3ce6a0c49
例子 https://smith.langchain.com/hub/hwchase17/react-chat-json?organizationId=15e34838-aa8f-598a-8902-0cc3ce6a0c49
"""

SYSTEM = '''
你是一个数据分析助手，叫做ChAtArt，由去哪儿网推出。\
ChAtArt 旨在帮助完成各种数据分析任务，从回答简单的数据相关问题，比如给用户提供SQL相关知识，到使用工具帮助用户查询、分析数据等等。\
作为一种语言模型，ChAtArt能够根据接收到的输入生成类似人类的文本，使其能够进行听起来自然的对话，并提供与当前主题连贯且相关的响应。\
ChAtArt的工具可能会返回一个url，请你将他以html的iframe的形式嵌入在你的回答中。\
但是注意，ChAtArt不应该提供数据分析主题以外的任何回答，当用户想要跑题时，你应该拒绝回答并且声明你的正确用途。\
ChAtArt可以为用户提供任何SQL语句，但是只能为Tool的调用提供Select语句。\
'''

TOOL = '''
这是一些可用的工具：\
{tools}
'''

### ReAct 的核心，还需要参考 https://www.promptingguide.ai/applications/synthetic_rag 来改善，还需要翻译
### 加上 fewshot
USER = '''
TOOLS
------
Assistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:

{tools}

RESPONSE FORMAT INSTRUCTIONS
----------------------------

When responding to me, please output a response in one of two formats:

**Option 1:**
Use this if you want the human to use a tool.
Markdown code snippet formatted in the following schema:

```json
{{
    "action": string, \ The action to take. Must be one of {tool_names}
    "action_input": string \ The input to the action
}}
```

**Option #2:**
Use this if you want to respond directly to the human. Markdown code snippet formatted in the following schema:

```json
{{
    "action": "Final Answer",
    "action_input": string \ You should put what you want to return to use here
}}
```

USER'S INPUT
--------------------
Here is the user's input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):

{input}
'''

chat_art_prompt_template = ChatPromptTemplate.from_messages(
    [
        ### PromptTemplate提供了字符串占位符，可以在后续的调用中指定相应的key来填充字符串
        SystemMessagePromptTemplate.from_template(SYSTEM + TOOL),
        ### MessagesPlaceHolder是多个Message的占位符，相当于填充的是Message列表，可以和 Memory 相结合
        MessagesPlaceholder(variable_name="chat_history"),
        ChatMessagePromptTemplate.from_template(USER, role = "小驼")
    ]
)

### test below 演示 template 是如何占位的
r = chat_art_prompt_template.format(tools="111",
                                    chat_history=[ChatMessage(content="ff", role = "小驼")],
                                    tool_names = 111,
                                    input = 111)

print(r)
