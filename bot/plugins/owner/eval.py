from neonize.aioze.client import NewAClient 
from bot.lib.serialize import Mess 
from bot.lib.msg_store import store 
import sys
import io
import traceback
import os
from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import Message
from typing import Any

async def aexec(code: str, client: NewAClient, m: Mess,store:store) -> Any:
    local_namespace = {}
    func_code = f"""
async def __eval_exec(client, m, store):
{chr(10).join(f'    {line}' for line in code.splitlines())}
"""

    try:
        exec(func_code, globals(), local_namespace)
    except SyntaxError as se:
        raise RuntimeError(
            f"Syntax Error in code:\n{se.text}\n{' ' * (se.offset - 1)}^\n{type(se).__name__}: {se.msg}"
        )

    eval_func = local_namespace.get("__eval_exec")
    if not eval_func:
        raise RuntimeError("Failed to compile code into a function.")

    return await eval_func(client, m,store)


async def eval_message(m: Mess, cmd: str, client: NewAClient,store:store):
    status_msg_info = None
    temp_file_name = "neonize_eval_output.txt"

    try:
        status_msg_info = await client.send_message(
            m.chat, "🔄 Processing eval command..."
        )
        status_msg_id = status_msg_info.ID

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = io.StringIO()
        redirected_error = io.StringIO()
        sys.stdout = redirected_output
        sys.stderr = redirected_error

        stdout_data = ""
        stderr_data = ""
        exception_data = ""
        execution_result = None

        try:
            execution_result = await aexec(cmd, client, m,store)
        except Exception as e:
            exception_data = traceback.format_exc()

        stdout_data = redirected_output.getvalue()
        stderr_data = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        final_output_parts = [f"```python\n{cmd}\n```"]

        if exception_data:
            final_output_parts.append(f"```python\nException:\n{exception_data}\n```")
        elif stderr_data:
            final_output_parts.append(f"```stderr\n{stderr_data}\n```")
        elif stdout_data:
            final_output_parts.append(f"```stdout\n{stdout_data}\n```")
        else:
            if execution_result is not None:
                try:
                    result_str = str(execution_result)
                except Exception:
                    result_str = f"<{type(execution_result).__name__} object>"
                final_output_parts.append(f"```Result:\n{result_str}\n```")
            else:
                final_output_parts.append(
                    "```Result:\n✅ Code executed successfully (no output).\n```"
                )

        final_output = "\n".join(final_output_parts)

        max_message_length = 4000
        if len(final_output) > max_message_length:
            try:
                with open(temp_file_name, "w", encoding="utf-8") as f:
                    f.write(final_output)

                await client.send_document(
                    m.chat,
                    temp_file_name,
                    filename="eval_output.txt",
                    caption=f"📝 Eval output (too long):\n```python\n{cmd[:50]}{'...' if len(cmd) > 50 else ''}\n```",
                    quoted=m.message,
                )
                await client.edit_message(
                    m.chat,
                    status_msg_id,
                    Message(conversation="✅ Eval done. Output sent as file."),
                )
            finally:
                if os.path.exists(temp_file_name):
                    try:
                        os.remove(temp_file_name)
                    except Exception as remove_err:
                        print(
                            f"Warning: Could not delete temp file {temp_file_name}: {remove_err}"
                        )
        else:
            await client.edit_message(
                m.chat, status_msg_id, Message(conversation=final_output)
            )

    except Exception as outer_error:
        error_trace = traceback.format_exc()
        print(f"[Eval Error - Outer] {outer_error}\n{error_trace}")
        if sys.stdout != old_stdout:
            sys.stdout = old_stdout
        if sys.stderr != old_stderr:
            sys.stderr = old_stderr
        if os.path.exists(temp_file_name):
            try:
                os.remove(temp_file_name)
            except:
                pass
        error_msg = f"💥 *Eval Error (Outer):*\n```python\n{str(outer_error)}\n```\n```traceback\n{error_trace[-1000:]}\n```"
        try:
            if status_msg_info:
                await client.edit_message(
                    m.chat, status_msg_info.ID, Message(conversation=error_msg)
                )
            else:
                await client.send_message(m.chat, error_msg)
        except:
            pass
          
async def execute(client,m,is_owner,text,body,store,**kwargs):
    if body.startswith("×>"):
        if not is_owner:
            await client.send_message(m.chat, "❌ Only owner can use eval!")
            return
        cmd = body[2:].strip()
        if not cmd:
            await client.send_message(m.chat, "❌ Please provide code to evaluate. Usage: `=> print('Hello')`")
            return
        try:
            await eval_message(m, cmd, client,store)
        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"[Eval Handler Error] {e}\n{error_trace}")
            await client.send_message(
                m.chat,
                f"💥 *Error in eval handler setup:*\n```python\n{str(e)}\n```\n```traceback\n{error_trace[-500:]}\n```",
            )

plugin = {
    "exec":execute
}