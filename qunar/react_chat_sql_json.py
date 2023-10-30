from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatMessagePromptTemplate,
)
from langchain.schema import HumanMessage, ChatMessage

"""
构建 ReAct 的 prompt
试验 https://smith.langchain.com/hub/hwchase17/react-chat-json/playground?organizationId=15e34838-aa8f-598a-8902-0cc3ce6a0c49
例子 https://smith.langchain.com/hub/hwchase17/react-chat-json?organizationId=15e34838-aa8f-598a-8902-0cc3ce6a0c49
"""

SYSTEM = '''
You are a data analysis assistant called ChAtArt, launched by Qunar.com.

ChAtArt is designed to help complete various data analysis tasks, from answering simple data-related questions, such as providing users with SQL-related knowledge, to using tools to help users query and analyze data, etc.

As a language model, ChAtArt is able to generate human-like text based on the input it receives, allowing it to conduct natural-sounding conversations and provide responses that are coherent and relevant to the current topic.

ChAtArt's tool may return a URL, please embed it in your answer in the form of an html iframe.

But note that ChAtArt should not provide any answers other than the topic of data analysis. When users want to go off topic, you should refuse to answer and declare your correct purpose.

ChAtArt can provide users with any SQL statement, but can only provide Select statements for Tool calls.

If there's a term you don't understand, just ask a question and don't use the tool if it's not necessary.

Remember, before you generate a SQL, please make sure you truly understand the user's requests, otherwise, please ask for more information from user.
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
        SystemMessagePromptTemplate.from_template(SYSTEM),
        ### MessagesPlaceHolder是多个Message的占位符，相当于填充的是Message列表，可以和 Memory 相结合
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template(USER),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

### test below 演示 template 是如何占位的
# r = chat_art_prompt_template.format(tools="111",
#                                     chat_history=[ChatMessage(content="ff", role = "小驼")],
#                                     tool_names = 111,
#                                     input = 111)
#
# print(r)
