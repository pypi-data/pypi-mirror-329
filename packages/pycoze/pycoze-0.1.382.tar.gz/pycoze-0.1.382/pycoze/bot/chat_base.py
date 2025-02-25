import json
import os
from .lib import get_formatted_filelist_str, read_local_file, resolve_relative_path
from .message import info
from pycoze.ai import chat_stream_async, extract
from .tools import ToolExecutor
from typing import List
import time

def guess_files_in_message(cwd: str, user_message: str) -> List[str]:

    value = extract(
        {"includedFiles": ["relative path format", "relative path format", "..."]},
        'Please find the files mentioned in the text. If none, return {"includedFiles": []}:\n'
        + user_message,
    )
    return [resolve_relative_path(cwd, p) for p in value["includedFiles"]]


def user_task_prompt(conversation_history, cwd, user_input: str, programmer_mode: bool):
    if programmer_mode:
        potential_paths = guess_files_in_message(cwd, user_input)

        exist_files = get_formatted_filelist_str(cwd, True, 200)
        content = []
        for file_path in potential_paths:
            file_path = resolve_relative_path(cwd, file_path)
            if os.path.isfile(file_path):
                file_marker = f"[[{file_path}]]'"
                file_content = read_local_file(file_path)
                if not any(
                    file_marker in msg["content"] for msg in conversation_history
                ):
                    content.append(f"{file_marker}\n{file_content}")
        content_str = (
            "Partial contents of files are as follows:" + "\n".join(content)
            if content
            else ""
        )
        return f"""<task>
{user_input}
</task>

<environment_details>
Current working directory: {cwd}

List of files under path:
{exist_files}

{content_str}

</environment_details>
    """

    else:
        return f"""<task>
{user_input}
</task>
<environment_details>
Current working directory: {cwd}
</environment_details>
"""


def dumps_markdown_json(data):
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    return f"\n```json\n{json_str}\n```\n"



async def stream_openai_response(conversation_history, start_new_stream):
    """
    异步流式传输 OpenAI 聊天完成响应并处理结构化输出
    """
    stream = None
    buffer = ""
    in_json_block = False
    json_block_content = ""
    text_content = ""

    while True:
        # 检查是否需要重新创建流
        if stream is None or start_new_stream["value"]:
            if stream is not None:
                await stream.aclose()  # 关闭之前的流
            stream = chat_stream_async(conversation_history)  # 获取新的异步生成器
            start_new_stream["value"] = False  # 重置标志
            buffer = ""
            in_json_block = False
            json_block_content = ""
            text_content = ""

        # 使用 async for 迭代异步生成器
        try:
            async for chunk in stream:
                info("assistant", chunk)
                buffer += chunk

                # 检查是否需要重新创建流
                if start_new_stream["value"]:
                    break  # 退出当前的 async for 循环，进入下一次 while 循环

                # 处理 buffer 中的每一行
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not in_json_block:
                        if line.strip().lower().startswith("```json"):
                            if text_content:
                                yield ("text", text_content.strip())
                                text_content = ""
                            in_json_block = True
                        else:
                            text_content += line + "\n"
                    else:
                        if line.strip().lower().startswith("```") and in_json_block:
                            yield ("json", json_block_content.strip())
                            json_block_content = ""
                            in_json_block = False
                        else:
                            json_block_content += line + "\n"

            # 如果流正常结束，退出 while 循环
            break

        except Exception as e:
            # 捕获其他异常（如网络错误）
            print(f"Error: {e}", style="bold red")
            break

    # 处理 buffer 中剩余的内容
    if buffer:
        if in_json_block:
            buffer = buffer.split("```")[0]
            json_block_content += buffer
            yield ("json", json_block_content.strip())
        else:
            text_content += buffer
            if text_content:
                yield ("text", text_content.strip())


async def handle_user_inputs(
    conversation_history, user_input, cwd, abilities, has_any_tool, bot_setting
):
    no_exit_if_incomplete = bot_setting["systemAbility"]["no_exit_if_incomplete"]
    programmer_mode = bot_setting["systemAbility"]["programmer_mode"]
    show_tool_results = bot_setting["showToolResults"]

    start_new_stream = {
        "value": False
    }  # 当遇到AI准备执行JSON，即需要新信息的时候，用于强制停止当前stream，减少后续无效的tokens

    print("Processing user command", user_input)
    if user_input.lower() in ["exit", "quit"]:
        exit(0)
    # 将用户消息添加到对话历史
    conversation_history.append(
        {
            "role": "user",
            "content": user_task_prompt(
                conversation_history, cwd, user_input, programmer_mode
            ),
        }
    )
    need_break = False

    if no_exit_if_incomplete:
        okay_str = 'Okay, please continue. If the tasks within <task>...task content...</task> have been completed, execute the tool "complete_all_tasks". If you have a question, use "ask_follow_up_question".'
    else:
        okay_str = "Okay"
    while True:
        async for response in stream_openai_response(
            conversation_history, start_new_stream
        ):
            if len(response) == 2:
                if (
                    response[0] == "text"
                    and response[1].strip() != ""
                    or (response[0] == "json" and not has_any_tool)
                ):
                    if response[0] == 'text':
                        conversation_history.append(
                            {"role": "assistant", "content": response[1]}
                        )
                    else:
                        conversation_history.append(
                            {"role": "assistant", "content": "\n```" + response[0] + "\n" + response[1] + "\n```\n"}
                        )

                    conversation_history.append(
                        {
                            "role": "user",
                            "content": okay_str,
                        }
                    )
                    continue
                elif response[0] == "json":
                    info("assistant", "\n")
                    cleaned_content = response[1]
                    try:
                        tool_request = json.loads(cleaned_content)
                        tool_name = list(tool_request.keys())[0]
                    except json.JSONDecodeError as e:
                        conversation_history.append(
                            {
                                "role": "assistant",
                                "content": f"\n```json\n{cleaned_content}\n```\n",
                            }
                        )
                        conversation_history.append(
                            {
                                "role": "user",
                                "content": "Invalid JSON content:" + str(e),
                            }
                        )
                        continue

                    ok, is_json_dumps, result = ToolExecutor.execute_tool(
                        cwd, tool_request, abilities
                    )
                    
                    assistant_content = (
                        "Executing tool: "
                        + dumps_markdown_json(tool_request)
                        + "\n\n[Tool Result Begin]\n"
                        + result
                        + "\n[Tool Result End]\n"
                    )
                    lang = "json" if is_json_dumps else "text"
                    status_str = "✅\n" if ok else "❌\n"
                    if show_tool_results:
                        info("assistant", status_str + f"\n```{lang}\n" + result + "\n```\n\n")
                    else:
                        info("assistant", status_str)
                    conversation_history.append(
                        {"role": "assistant", "content": assistant_content}
                    )
                    if tool_name in ["complete_all_tasks", "ask_follow_up_question"]:
                        need_break = True
                        break
                    else:
                        conversation_history.append(
                            {
                                "role": "user",
                                "content": okay_str,
                            }
                        )
                        start_new_stream["value"] = True

        if need_break:
            break
        if not no_exit_if_incomplete and not start_new_stream["value"]:
            break
    last_conversation = conversation_history[-1]
    if last_conversation["role"] == 'user' and last_conversation["content"] == okay_str:
        conversation_history.pop()

# 示例调用
# user_input_list = [
#     "访问https://api-docs.deepseek.com/zh-cn/guides/chat_prefix_completion，并结合它编写一段代码，并保存"
# ]

# asyncio.run(handle_user_inputs(user_input_list))
