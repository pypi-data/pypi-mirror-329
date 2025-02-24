import json
from .chat_base import handle_user_inputs
from .lib import get_abilities, get_system_prompt
from .message import INPUT_MESSAGE, output, CHAT_DATA, clear_chat_data
import os
import asyncio
from pycoze import utils
import tempfile
import re

def eclipse_tool_result(text):
    # 使用正则表达式匹配 [Tool Result Begin] 和 [Tool Result End] 之间的内容
    pattern = r'\[Tool Result Begin\].*?\[Tool Result End\]'
    # 将匹配到的内容替换为 [Tool Result Begin]...[Tool Result End]
    replaced_text = re.sub(pattern, '[Tool Result Begin]...[Tool Result End]', text, flags=re.DOTALL)
    return replaced_text


async def check_interrupt_file(interval, interrupt_file, chat_task):
    while True:
        await asyncio.sleep(interval)
        if os.path.exists(interrupt_file):
            os.remove(interrupt_file)
            chat_task.cancel()
            break


async def run_with_interrupt_check(
    conversation_history,
    user_input,
    cwd: str,
    abilities,
    has_any_tool,
    bot_setting,
    interrupt_file,
):
    clear_chat_data()
    try:
        chat_task = asyncio.create_task(
            handle_user_inputs(
                conversation_history,
                user_input,
                cwd,
                abilities,
                has_any_tool,
                bot_setting,
            )
        )
        check_task = asyncio.create_task(
            check_interrupt_file(0.5, interrupt_file, chat_task)
        )
        result = await chat_task
        return result
    except asyncio.CancelledError:
        return CHAT_DATA["info"]
    except Exception as e:
        import traceback

        print(traceback.format_exc())
        return None  # 返回 None 或者处理异常后的结果
    finally:
        if not chat_task.done():
            chat_task.cancel()
        # 确保即使发生异常也会取消检查任务
        if not check_task.done():
            check_task.cancel()
            try:
                await check_task
            except asyncio.CancelledError:
                pass  # 忽略取消错误


def chat(bot_setting_file: str):
    with open(bot_setting_file, encoding="utf-8") as f:
        bot_setting = json.load(f)
    abilities = get_abilities(bot_setting)
    remember_tool_results = bot_setting["remember_tool_results"]

    cwd = tempfile.mkdtemp()
    system_prompt, has_any_tool = get_system_prompt(abilities, bot_setting)
    conversation_history = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]
    while True:
        clear_chat_data()
        input_text = input()
        if not input_text.startswith(INPUT_MESSAGE):
            raise ValueError("Invalid message")
        message = json.loads(input_text[len(INPUT_MESSAGE) :])
        user_input = message["content"]
        params = utils.params
        if "interruptFile" in params:
            asyncio.run(
                run_with_interrupt_check(
                    conversation_history,
                    user_input,
                    cwd,
                    abilities,
                    has_any_tool,
                    bot_setting,
                    params["interruptFile"],
                )
            )
        else:
            asyncio.run(
                handle_user_inputs(
                    conversation_history,
                    user_input,
                    cwd,
                    abilities,
                    has_any_tool,
                    bot_setting,
                )
            )
        output("assistant", CHAT_DATA["info"])
        if not remember_tool_results:
            conversation_history = [{"role": msg["role"], "content": eclipse_tool_result(msg["content"])} for msg in conversation_history]


def get_chat_response(bot_setting_file: str, user_input: str):
    with open(bot_setting_file, encoding="utf-8") as f:
        bot_setting = json.load(f)
    abilities = get_abilities(bot_setting)
    cwd = tempfile.mkdtemp()
    system_prompt, has_any_tool = get_system_prompt(abilities, bot_setting)
    conversation_history = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]
    asyncio.run(
        handle_user_inputs(
            conversation_history, user_input, cwd, abilities, has_any_tool, bot_setting
        )
    )

    return CHAT_DATA["info"]
