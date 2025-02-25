from dataclasses import dataclass
from dataclasses import field
from dataclasses import replace
from itertools import chain
from typing import Optional
from typing import Union
from decimal import Decimal
from enum import Flag
from enum import auto
from copy import deepcopy
from .filter_complex import FilterGraph
from .filter_complex import FilterChain
from .filter_complex import Filter

from functools import partial

"""
ffmpeg [global_options] {[input_file_options] -i input_url} ... {[output_file_options] output_url} ... 
https://www.youtube.com/watch?v=0To1aYglVHE
"""


ArgValueType = str | int | Decimal | float | Union[FilterGraph, FilterChain, Filter]


class ArgFlag(Flag):
    OUT = auto()
    IN = auto()
    GLOBAL = auto()


@dataclass(frozen=True)
class FFmpegArg:
    key: str
    flag: ArgFlag
    value: Optional[ArgValueType] = field(default=None)
    stream_selector: str = field(default=None)

    def __getitem__(self, stream_selector: str) -> "FFmpegArg":
        return replace(self, stream_selector=stream_selector)

    def __add__(self, other: Union["FFmpegArg", "FFmpegChunk"]) -> "FFmpegChunk":
        chunk_resolution = {
            (ArgFlag.OUT, ArgFlag.OUT): FFmpegOutput,
            (ArgFlag.OUT, ArgFlag.OUT | ArgFlag.IN): FFmpegOutput,
            (ArgFlag.OUT | ArgFlag.IN, ArgFlag.OUT): FFmpegOutput,
            (ArgFlag.IN, ArgFlag.IN): FFmpegInput,
            (ArgFlag.IN, ArgFlag.IN | ArgFlag.OUT): FFmpegInput,
            (ArgFlag.OUT | ArgFlag.IN, ArgFlag.IN): FFmpegInput,
            (ArgFlag.IN | ArgFlag.OUT, ArgFlag.IN | ArgFlag.OUT): FFmpegInputOutput,
            (ArgFlag.GLOBAL, ArgFlag.GLOBAL): FFmpegGlobal,
        }
        if type(other) == FFmpegArg:
            if chunk := chunk_resolution.get((self.flag, other.flag)):
                return chunk() + self + other

        if issubclass(other.__class__, FFmpegChunk):
            if other.arg_type in self.flag:
                return replace(other, group_option=[self] + other.group_option)

            raise Exception(f"{self} and {other} doesn't match argflag type ")

        raise Exception(f"Can't add {self} + {other} ")

    def __call__(self, value=None, *args, **kwds) -> "FFmpegArg":
        return replace(self, value=value)

    def render(self) -> list[str]:
        key = self.key
        if self.stream_selector:
            key = f"{key}:{self.stream_selector}"
        value = []
        if self.value:
            value = [f'{self.value}']
            if type(self.value) in [FilterGraph, FilterChain, Filter]:
                value = [self.value.render()]

        return [f"-{key}"] + value


@dataclass(frozen=True)
class FFmpegChunk:
    arg_type: ArgFlag
    group_option: list = field(default_factory=list)

    def render(self) -> list:
        return (
            list(chain.from_iterable(opt.render() for opt in self.group_option))
            if self.group_option
            else []
        )

    def __add__(self, other: Union["FFmpegArg", "FFmpegChunk"]) -> "FFmpegChunk":
        if type(other) == FFmpegArg:
            if self.arg_type == other.flag:
                return replace(self, group_option=self.group_option + [other])

            if (
                type(self) == FFmpegInputOutput
            ):  # InOut chunk are virtual temporary and should generate a FFmpegInput or FFmpegOutput when it can deduce
                if (
                    other.flag == ArgFlag.IN
                ):  # InOut changes to IN if arg is makred as IN only
                    return FFmpegInput(
                        group_option=[
                            replace(o, flag=ArgFlag.IN) for o in self.group_option
                        ]
                        + [other]
                    )
                if (
                    other.flag == ArgFlag.OUT
                ):  # InOut changes to IN if arg is makred as IN only
                    return FFmpegOutput(
                        group_option=[
                            replace(o, flag=ArgFlag.OUT) for o in self.group_option
                        ]
                        + [other]
                    )

            if type(self) in [
                FFmpegInput,
                FFmpegOutput,
            ]:  # It's either a In or Out chunk, and arg needs to be specified
                if other.flag == ArgFlag.IN | ArgFlag.OUT:  # Global won't work
                    return replace(
                        self,
                        group_option=self.group_option
                        + [replace(other, flag=self.arg_type)],
                    )

        if issubclass(other.__class__, FFmpegChunk):
            chunk_resolution = {
                (ArgFlag.OUT, ArgFlag.OUT): FFmpegOutput,
                (ArgFlag.OUT, ArgFlag.OUT | ArgFlag.IN): FFmpegOutput,
                (ArgFlag.OUT | ArgFlag.IN, ArgFlag.OUT): FFmpegOutput,
                (ArgFlag.IN, ArgFlag.IN): FFmpegInput,
                (ArgFlag.IN, ArgFlag.OUT | ArgFlag.IN): FFmpegInput,
                (ArgFlag.OUT | ArgFlag.IN, ArgFlag.IN): FFmpegInput,
                (ArgFlag.IN | ArgFlag.OUT, ArgFlag.OUT | ArgFlag.IN): FFmpegInputOutput,
                (ArgFlag.GLOBAL, ArgFlag.GLOBAL): FFmpegGlobal,
            }
            if chunk := chunk_resolution.get((self.arg_type, other.arg_type)):
                if (self.arg_type, other.arg_type) == (ArgFlag.GLOBAL, ArgFlag.GLOBAL):
                    return chunk(group_option=self.group_option + other.group_option)
                self_url = None
                other_url = None

                if self.arg_type != ArgFlag.IN | ArgFlag.OUT:
                    self_url = self.url
                if other.arg_type != ArgFlag.IN | ArgFlag.OUT:
                    other_url = other.url

                if self_url and other_url and other_url != self_url:
                    raise Exception(
                        "Url defined in both part should. One should be None"
                    )

                url = {}
                if chunk != FFmpegInputOutput:
                    url = {"url": self_url if self_url else other_url}
                return chunk(group_option=self.group_option + other.group_option, **url)

        raise Exception(f"Can't add {self} + {other} ")


@dataclass(frozen=True)
class FFmpegIOChunk:
    url: Optional[str] = field(default=None)

    def __call__(self, url, *args, **kwargs) -> "FFmpegIOChunk":
        return replace(self, url=url)

    def check(self) -> None:
        if not self.url:
            raise Exception(
                f"Can't render properly, {self.__class__} with Undefined 'url'"
            )


@dataclass(frozen=True)
class FFmpegInput(FFmpegChunk, FFmpegIOChunk):
    arg_type: ArgFlag = field(default=ArgFlag.IN)

    def render(self) -> list[str]:
        self.check()
        return super().render() + ["-i", self.url]


@dataclass(frozen=True)
class FFmpegOutput(FFmpegChunk, FFmpegIOChunk):
    arg_type: ArgFlag = field(default=ArgFlag.OUT)

    def render(self) -> list[str]:
        self.check()
        return super().render() + [self.url]


@dataclass(frozen=True)
class FFmpegGlobal(FFmpegChunk):
    arg_type: ArgFlag = field(default=ArgFlag.GLOBAL)
    pass


@dataclass(frozen=True)
class FFmpegInputOutput(FFmpegChunk):
    arg_type: ArgFlag = field(default=ArgFlag.IN | ArgFlag.OUT)
    pass


@dataclass(frozen=True)
class FFmpegCmd:
    cmd :str = field(default="ffmpeg")
    global_chunk: FFmpegGlobal = field(default_factory=FFmpegGlobal)
    input_chunks: list[FFmpegInput] = field(default_factory=list)
    output_chunks: list[FFmpegOutput] = field(default_factory=list)

    def __add__(
        self, other: Union[FFmpegArg | FFmpegInput | FFmpegOutput | FFmpegGlobal]
    ) -> "FFmpegCmd":
        if type(other) not in [FFmpegArg, FFmpegInput, FFmpegOutput, FFmpegGlobal]:
            raise Exception(f"Can't add {type(other)} to FFmpegCmd")

        if type(other) == FFmpegArg:
            if other.flag == ArgFlag.IN | ArgFlag.OUT:
                raise Exception(f"Can't add '{other.key}':{type(other)} to FFmpegCmd")

            if other.flag == ArgFlag.IN:
                if not self.input_chunks:
                    return self + FFmpegInput() + other
                return replace(
                    self,
                    input_chunks=self.input_chunks[:-1]
                    + [self.input_chunks[-1] + other],
                )
            if other.flag == ArgFlag.OUT:
                if not self.output_chunks:
                    return self + FFmpegOutput() + other
                return replace(
                    self,
                    output_chunks=self.output_chunks[:-1]
                    + [self.output_chunks[-1] + other],
                )
            if other.flag == ArgFlag.GLOBAL:
                return replace(self, global_chunk=self.global_chunk + other)

        if type(other) == FFmpegInput:
            return replace(self, input_chunks=self.input_chunks + [other])
        if type(other) == FFmpegOutput:
            return replace(self, output_chunks=self.output_chunks + [other])
        if type(other) == FFmpegGlobal:
            return replace(self, global_chunk=self.global_chunk + other)

    def render(self) -> list[str]:
        return (
            [self.cmd]
            + self.global_chunk.render()
            + list(chain.from_iterable([chunk.render() for chunk in self.input_chunks]))
            + list(
                chain.from_iterable([chunk.render() for chunk in self.output_chunks])
            )
        )


@dataclass(frozen=True)
class FFprobe(FFmpegCmd):
    cmd : str = field(default="ffprobe")


IArg = partial(FFmpegArg, flag=ArgFlag.IN)
OArg = partial(FFmpegArg, flag=ArgFlag.OUT)
IOArg = partial(FFmpegArg, flag=ArgFlag.IN | ArgFlag.OUT)
GArg = partial(FFmpegArg, flag=ArgFlag.GLOBAL)
