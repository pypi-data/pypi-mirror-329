import json
from .chat_base import handle_user_inputs
from .lib import get_abilities, get_system_prompt
from .message import INPUT_MESSAGE, output, CHAT_DATA, clear_chat_data
import os
import asyncio
from pycoze import utils
import tempfile
import re
import datetime
from pathlib import Path


def eclipse_tool_result(text, threshold=100):
    pattern = r'\[Tool Result Begin\](.*?)\[Tool Result End\]'
    
    def replace_match(match):
        content = match.group(1)
        if len(content) < threshold:
            return match.group(0)  # 返回原始匹配内容，不替换
        else:
            return '[Tool Result Begin]...[Tool Result End]'
    
    replaced_text = re.sub(pattern, replace_match, text, flags=re.DOTALL)
    return replaced_text

def output_chat_history(file_path, chat_history):
    with open(file_path, 'w', encoding='utf-8') as f:
        for chat in chat_history:
            f.write(chat["role"] + ":\n" + chat["content"] + "\n\n")
        

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
    current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_history_folder = os.path.join(os.path.dirname(bot_setting_file), "chatHistory")
    os.makedirs(chat_history_folder, exist_ok=True)
    chat_history_file = os.path.join(chat_history_folder, current_time_str + "_no_subject.txt")

    with open(bot_setting_file, encoding="utf-8") as f:
        bot_setting = json.load(f)
    abilities = get_abilities(bot_setting)

    continuouslyRememberToolResults = bot_setting["continuouslyRememberToolResults"]
    programmer_mode = bot_setting["programmerMode"]
    if programmer_mode:
        cwd = bot_setting["specifiedWorkingDirectory"]
    else:
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
        is_save_fail = False
        try:
            output_chat_history(chat_history_file, conversation_history)
        except Exception as e:
            print(f"Error writing chat history to file: {e}")
            is_save_fail = True
        eclipse_conversation_history = [{"role": msg["role"], "content": eclipse_tool_result(msg["content"])} for msg in conversation_history]
        if not continuouslyRememberToolResults:
            conversation_history = eclipse_conversation_history
        if is_save_fail:
            # 去除工具结果后，重新保存
            try:
                output_chat_history(chat_history_file, eclipse_conversation_history)
            except Exception as e:
                print(f"Error writing chat history to file: {e}")
            


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
