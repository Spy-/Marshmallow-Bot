import subprocess


async def sysexec(cmd, message, args):
    if args:
        try:
            process = subprocess.Popen(args, stdout=subprocess.PIPE)
            output, error = process.communicate()
            response = f"```\n{output.decode('utf-8')}\n```"
            if error:
                cmd.log.info(f'Error in SysExec: {error}')
        except Exception:
            response = 'An error occurred.'
    else:
        response = 'No input.'
    await message.channel.send(response)