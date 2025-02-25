from typing import Union
from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field
from dataclasses import replace

"""
NAME             ::= sequence of alphanumeric characters and '_'
FILTER_NAME      ::= NAME["@"NAME]
LINKLABEL        ::= "[" NAME "]"
LINKLABELS       ::= LINKLABEL [LINKLABELS]
FILTER_ARGUMENTS ::= sequence of chars (possibly quoted)
FILTER           ::= [LINKLABELS] FILTER_NAME ["=" FILTER_ARGUMENTS] [LINKLABELS]
FILTERCHAIN      ::= FILTER [,FILTERCHAIN]
FILTERGRAPH      ::= [sws_flags=flags;] FILTERCHAIN [;FILTERGRAPH]
"""

Chainable = Union["FilterChain", "Filter", "FilterGraph"]

"""
    TODO: Do same as for cmd with pre generated filter component
"""


class Filter:

    def __init__(self, name: str, *args, **kwargs):
        self._name = name
        self._args = args
        self._kwargs = kwargs

        self._in_labels = []
        self._out_labels = []

    def __call__(self, *args, **kwargs):
        return Filter(self._name, *args, **kwargs)

    def __getitem__(self, val: range) -> "Filter":
        new = deepcopy(self)
        new._in_labels = val.start or []
        new._out_labels = val.stop or []

        return new

    def __rshift__(self, other: Chainable):

        if type(other) == Filter:
            fg = FilterChain() >> self
            return fg >> other
        if type(other) == FilterChain:
            return replace(other, filters=[self] + other.filters)
        if type(other) == FilterGraph:
            fg = FilterChain() >> self

            return replace(
                other,
                chains=[self >> other.chains[0] if other.chains else self]
                + other.chains[1:],
            )

    def __add__(self, other: Chainable):

        if type(other) == Filter:
            return (FilterChain() >> self) + (FilterChain() >> other)
        if type(other) == FilterChain:
            return (FilterChain() >> self) + other
        if type(other) == FilterGraph:
            return (FilterGraph() >> self) + other

    def render(self):
        filter_render = f"{self._name}"

        all_args = []
        if self._args:
            args_render = ":".join([str(arg) for arg in self._args])
            all_args.append(args_render)

        if self._kwargs:
            kwargs_render = ":".join(
                [f"{key}={value}" for key, value in self._kwargs.items()]
            )
            all_args.append(kwargs_render)

        if all_args:
            all_args_render = ":".join(all_args)
            filter_render = "=".join([filter_render, all_args_render])

        labels_render = []
        if self._in_labels:
            in_labels = "".join([f"[{label}]" for label in self._in_labels])
            labels_render.append(in_labels)
        labels_render.append(filter_render)
        if self._out_labels:
            out_labels = "".join([f"[{label}]" for label in self._out_labels])
            labels_render.append(out_labels)
        return "".join(labels_render)


@dataclass
class FilterChain:
    filters: list[Filter] = field(default_factory=list)

    def __rshift__(self, other: Chainable):

        if type(other) == FilterChain:
            return replace(self, filters=self.filters + other.filters)

        if type(other) == Filter:
            return replace(self, filters=self.filters + [other])

        if type(other) == FilterGraph:
            fg = FilterGraph()
            fg = fg >> self
            return fg >> other

    def __add__(self, other: Chainable) -> "FilterGraph":

        if type(other) == Filter:
            return FilterGraph(
                chains=([replace(self)] if self.filters else []) + [deepcopy(other)]
            )
        if type(other) == FilterChain:
            return FilterGraph(
                chains=([replace(self)] if self.filters else [])
                + ([deepcopy(other)] if other.filters else [])
            )
        if type(other) == FilterGraph:
            if len(other.chains) > 0:
                return FilterGraph(chains=[replace(self)]) + FilterGraph(
                    chains=other.chains[:]
                )
            return FilterGraph(chains=[replace(self)]) + other

    def render(self):
        return ",".join([filter.render() for filter in self.filters])


@dataclass
class FilterGraph:
    chains: list[FilterChain] = field(default_factory=list)

    def __rshift__(self, other: Chainable):
        if type(other) == FilterGraph:
            return replace(self, chains=self.chains + other.chains)
        if type(other) == FilterChain:
            return replace(self, chains=self.chains + [other])
        if type(other) == Filter:
            fg = FilterChain()
            if len(self.chains) > 0:
                fg = self.chains[-1]
            fg = fg >> other
            return replace(self, chains=self.chains[:-1] + [fg])

    def __add__(self, other: Chainable) -> "FilterGraph":

        if type(other) == Filter:
            return replace(self, chains=self.chains + [FilterChain() >> other])
        if type(other) == FilterChain:
            return replace(self, chains=self.chains + [other] if other.filters else [])
        if type(other) == FilterGraph:
            return replace(self, chains=self.chains + other.chains)

    def render(self):
        return ";".join([chain.render() for chain in self.chains])
