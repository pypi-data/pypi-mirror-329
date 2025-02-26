import typing as t

QuerySpec = t.Union[
    t.Mapping[str, t.Any],
    t.Iterable[t.Tuple[str, t.Any]]
]
