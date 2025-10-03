import asyncio

async def execute(client, m, body, is_owner, **kwargs):
    if body.startswith("&"):
        if not is_owner:
            return await m.reply("Only owner!")
        command = body[1:].strip()
        process = await asyncio.create_subprocess_shell(
            f"zsh -c {repr(command)}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if stdout:
            await m.reply(stdout.decode())
        if stderr:
            await m.reply(stderr.decode()) 
    
plugin = {
    "exec": execute
}