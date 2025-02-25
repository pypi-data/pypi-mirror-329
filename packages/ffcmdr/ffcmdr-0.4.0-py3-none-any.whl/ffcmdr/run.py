from subprocess import Popen
from subprocess import PIPE
from typing import Optional
from ffcmdr.cmd import FFmpegCmd

# From https://github.com/kkroening/ffmpeg-python/blob/master/ffmpeg/_run.py


# TODO : https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.create_subprocess_exec


def run_async(
    cmd: FFmpegCmd,
    *,
    stdin: Optional[int] = None,
    stdout: Optional[int] = None,
    stderr: Optional[int] = None,
    **kwargs,
) -> Popen:
    pipe_input = [i for i in cmd.input_chunks if i.url and i.url.startswith("pipe:")]
    pipe_output = [i for i in cmd.output_chunks if i.url and i.url.startswith("pipe:")]
    # TODO: Manage multiple pipe with mkfifo or mknod
    if not stdin and pipe_input:
        stdin = PIPE
    if not stdout and pipe_output:
        stdout = PIPE

    return Popen(cmd.render(), stdin=stdin, stdout=stdout, stderr=stderr, **kwargs)


def run(
    cmd: FFmpegCmd,
    *,
    stdin: Optional[int] = None,
    stdout: Optional[int] = None,
    stderr: Optional[int] = None,
    input_stream=None,
    **kwargs,
) -> tuple:

    process = run_async(cmd, stdin=stdin, stdout=stdout, stderr=stderr, **kwargs)
    out, err = process.communicate(input_stream)
    retcode = process.poll()
    if retcode:
        raise Exception(cmd, out, err)
    return out, err
