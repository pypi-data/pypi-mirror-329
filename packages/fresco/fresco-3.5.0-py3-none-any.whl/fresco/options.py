# Copyright 2015 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
import contextlib
import inspect
import itertools
import json
import logging
import typing as t
import os
import re
from decimal import Decimal
from pathlib import Path
from socket import gethostname
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Sequence
from typing import Union

from fresco.exceptions import OptionsLoadedException

__all__ = ["Options"]

logger = logging.getLogger(__name__)


class Options(dict):
    """\
    Options dictionary. An instance of this is attached to each
    :class:`fresco.core.FrescoApp` instance, as a central store for
    configuration options.
    """

    _loaded_callbacks: List[Callable[["Options"], None]]
    _is_loaded = False

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.__dict__["_loaded_callbacks"] = []

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, key, value):
        self[key] = value

    def onload(self, fn: Callable) -> Callable:
        """
        Register a function to be called once ``load`` has finished populating
        the options object.
        """
        if self._is_loaded:
            fn(self)
        else:
            self._loaded_callbacks.append(fn)
        return fn

    def do_loaded_callbacks(self):
        for func in self._loaded_callbacks:
            func(self)

    def trigger_onload(self):
        """
        Mark the options object as having loaded and call any registered
        onload callbacks
        """
        if self._is_loaded:
            raise OptionsLoadedException("Options have already been loaded")
        self.do_loaded_callbacks()
        self.__dict__["_is_loaded"] = True

    def copy(self):
        return self.__class__(super().copy())

    def load(
        self,
        sources: t.Union[str, t.Iterable[t.Union[Path, str]]],
        tags: Sequence[str] = [],
        use_environ=False,
        strict=True,
        dir=None,
        trigger_onload=True,
    ):
        """
        Find all files matching glob pattern ``sources`` and populates the
        options object from those with matching filenames containing ``tags``.

        :param sources:
            one or more glob patterns separated by ";",
            or a list of glob patterns

        :param tags:
            a list of tags to look for in file names.

        :param use_environ: if true, environment variables matching previously
                            loaded keys will be loaded into the options object.
                            This happens after all files have been processed.
        :param strict: if true, the first file loaded is assumed to contain
                       all available option keys. Any new key found in a later
                       file will raise an error.

        Files may be in python (``.py``), json (``.json``), TOML (``.toml``)
        format. Any other files will be interpreted as simple lists of
        ```key=value`` pairs.

        Tags in filenames are delimited with periods,
        for example ".env.production.py".
        The filename ``setttings.dev.local.ini`` would be
        considered to have the tags ``('dev', 'local')``

        Where filename contain multiple tags, all tags must match for the file
        to be loaded.

        Files are processed in the order that tags are specified in the
        ``tags`` parameter, and then in lexicographical order.
        For example, calling ``options.load(..., tags=["dev", "local"])`` would
        cause a file named "settings.dev" to be loaded before one named
        "settings.local".

        Tag names may contain the names of environment variable surrounded by
        braces, for example ``{USER}``. These will be substituted for the
        environment variable's value, with any dots or path separators replaced
        by underscores.

        The special variable ``{hostname}`` will be substituted for the current
        host's name with dots replaced by underscores.

        Files with the suffix ".sample" are unconditionally excluded.

        Files are loaded in the order specified by ``tags``, then in filename
        order. Environment variables, if requested, are loaded last.

        Example::

            opts = Options()
            opts.load(".env*", ["dev", "host-{hostname}", "local"])

        Would load options from files named ``.env``, ``.env.json``, ``.env.dev.py``
        and ``.env.local.py.``

        """
        if self._is_loaded:
            raise OptionsLoadedException("Options have already been loaded")

        tag_substitutions = os.environ.copy()
        tag_substitutions["hostname"] = gethostname()
        tag_substitutions = {
            k: v.replace(".", "_").replace(os.pathsep, "_")
            for k, v in tag_substitutions.items()
        }

        candidates: List[Path] = []
        if dir is None:
            dir = Path(".")
        else:
            dir = Path(dir)

        if isinstance(sources, str):
            sources = [s.strip() for s in sources.split(";")]
        for source in sources:
            sourcepath = dir / Path(source)
            candidates.extend(
                p
                for p in sourcepath.parent.glob(sourcepath.name)
                if p.suffix.lower() != ".sample"
            )

        if tags:
            subbed_tags = []
            for tag in tags:
                try:
                    subbed_tags.append(tag.format(**tag_substitutions))
                except KeyError:
                    pass
            tags = subbed_tags
            tagged_sources = []
            for p in candidates:
                candidate_tags = [t for t in str(p.name).split(".") if t][1:]
                if len(candidate_tags) == 0:
                    tagged_sources.append((candidate_tags, p))
                else:
                    # Ignore the final tag if it matches a common config file
                    # extension
                    if candidate_tags[-1].lower() in {
                        "py",
                        "sh",
                        "rc",
                        "txt",
                        "cfg",
                        "ini",
                        "json",
                        "toml",
                        "conf",
                    }:
                        candidate_tags.pop()

                    if all(t in tags for t in candidate_tags):
                        tagged_sources.append((candidate_tags, p))
            matched = [
                ts[1]
                for ts in sorted(
                    tagged_sources,
                    key=(
                        lambda ts: (
                            ([], ts[1])
                            if len(ts[0]) == 0 else
                            (sorted(tags.index(t) for t in ts[0]), ts[1])
                        )
                    )
                )
            ]
        else:
            matched = candidates

        for path in matched:
            existing_keys = set(self.keys())
            logger.info(f"Loading config from {path}")
            if path.suffix == ".py":
                self.update_from_file(str(path))
            elif path.suffix == ".toml":
                import toml

                with path.open("r") as f:
                    self.update(toml.load(f))
            elif path.suffix == ".json":
                with path.open("r") as f:
                    self.update(json.load(f))
            else:
                fullpath = path.resolve()
                with path.open("r") as f:
                    interpolations = dict(os.environ)
                    interpolations.update(self)
                    interpolations["__FILE__"] = str(fullpath)
                    interpolations["__DIR__"] = str(fullpath.parent)
                    self.update(
                        parse_key_value_pairs(
                            interpolations,
                            f,
                        )
                    )

            if strict and existing_keys and set(self.keys()) != existing_keys:
                raise AssertionError(
                    f"settings file {path} created undefined options: "
                    f"{set(self.keys()) - existing_keys}"
                )

            if use_environ:
                for k in self:
                    if k in os.environ:
                        self[k] = parse_value(self, os.environ[k])

        if trigger_onload:
            self.do_loaded_callbacks()
            self.__dict__["_is_loaded"] = True
        return self

    def update_from_file(self, path, load_all=False):
        """
        Update the instance with any symbols found in the python source file at
        `path`.

        :param path: The path to a python source file
        :param load_all: If true private symbols will also be loaded into the
                         options object.
        """
        ns: Dict[str, Any] = {"__file__": path}
        with open(path) as f:
            exec(f.read(), ns)
        self.update_from_dict(ns, load_all)

    def update_from_dict(self, d, load_all=False):
        """
        Update from the given list of key-value pairs.

        If ``load_all`` is True, all key-value pairs will be loaded.

        Otherwise, if the special key '__all__' is present, only those keys
        listed in __all__ will be loaded (same semantics as `from … import *`)

        Otherwise only those NOT beginning with ``_`` will be loaded.
        """
        if load_all:
            self.update(d)
        elif "__all__" in d:
            self.update((k, d[k]) for k in d["__all__"])
        else:
            self.update(
                (k, v) for k, v in d.items() if isinstance(k, str) and k and k[0] != "_"
            )

    def update_from_object(self, ob, load_all=False):
        """
        Update the instance with any symbols found in object ``ob``.

        :param load_all:
            If true private symbols will also be loaded into the options
            object.
        """
        self.update_from_dict(dict(inspect.getmembers(ob)), load_all)


@contextlib.contextmanager
def override_options(options, other=None, **kwargs):
    """
    Context manager that updates the given Options object with new values.
    On exit, the old values will be restored.

    This function is provided to assist with writing tests. It directly
    modifies the given options object and does not prevent other threads from
    accessing the modified values.
    """
    saved: list[tuple[str, t.Any]] = []
    items: t.Iterable[tuple[str, t.Any]] = []
    if other is not None:

        keys = getattr(other, "keys", None)
        if keys and callable(keys):
            items = ((k, other[k]) for k in keys())

    if kwargs:
        items = itertools.chain(items, kwargs.items())

    NOT_PRESENT = object()

    for k, v in items:
        if k in options:
            saved.append((k, options[k]))
        else:
            saved.append((k, NOT_PRESENT))

        options[k] = v

    yield options
    for k, v in saved:
        if v is NOT_PRESENT:
            del options[k]
        else:
            options[k] = v


def parse_value(
    options: Mapping,
    v: str,
    interpolation_sub=re.compile(r"\$\{([^}]*)\}|\$(\w[\w\d]*)").sub,
    int_match=re.compile(r"^[+-]?[1-9][0-9]*$").match,
    decimal_match=re.compile(r"^[+-]?[0-9]*\.[0-9]*$").match,
) -> Union[str, int, Decimal, bool]:
    def interpolate(m):
        s = m.group(1) or m.group(2)
        return str(options.get(s, m.group(0)))

    v = interpolation_sub(interpolate, v).strip()
    if int_match(v):
        return int(v)
    if decimal_match(v):
        return Decimal(v)
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    if v and v[0] in "'\"" and v[-1] == v[0]:
        return v[1:-1]
    return v


def parse_key_value_pairs(options, lines: Iterable[str]):
    lines = (line.split("#", 1)[0] for line in lines)
    pairs = (line.split("=", 1) for line in lines if "=" in line)

    options = dict(options)
    values = {}
    for k, v in pairs:
        k = k.strip()
        values[k] = options[k] = parse_value(options, v)
    return values


def list_from_str(s, separator=","):
    """
    Return the value of ``s`` split into a list of times by ``separator``.
    Spaces around items will be stripped.
    """
    if isinstance(s, str):
        if not s.strip():
            return []
        return [item.strip() for item in s.split(",")]
    raise TypeError(f"Expected string, got {s!r}")


def dict_from_options(
    prefix: str, options: t.Mapping[str, Any], recursive: bool = False
) -> t.Dict[str, Any]:
    """
    Create a dictionary containing all items in ``options`` whose keys start
    with ``prefix``, with that prefix stripped.

    Example:

        >>> from fresco.options import Options, dict_from_options
        >>> options = Options(
        ...      {"DATABASE_HOST": "127.0.0.1", "DATABASE_USER": "scott"}
        ... )
        >>> dict_from_options("DATABASE_", options)
        {'HOST': '127.0.0.1', 'USER': 'scott'}

    If ``recursive`` is True, a recursive splitting will be
    applied. The last character of ``prefix`` will be used as the separator,
    for example::

        >>> from fresco.options import dict_from_options
        >>> options = Options(
        ...      {
        ...          "DATABASE_DEV_HOST": "127.0.0.1",
        ...          "DATABASE_DEV_USER": "scott",
        ...          "DATABASE_PROD_HOST": "192.168.0.78",
        ...          "DATABASE_PROD_HOST": "tiger",
        ...      }
        ... )
        >>> dict_from_options("DATABASE_", options, recursive=True)
        {'DEV': {'HOST': '127.0.0.1', ...}, 'PROD': {'HOST', ...}}

    """

    prefixlen = len(prefix)
    d = {k[prefixlen:]: v for k, v in options.items() if k.startswith(prefix)}

    def recursive_split(d: t.Mapping[str, Any], sep: str) -> t.Dict[str, Any]:
        d_: t.Dict[str, Any] = {}
        for k in d:
            if sep in k:
                ks = k.split(sep)
                subdict = d_
                for subkey in ks[:-1]:
                    subdict = subdict.setdefault(subkey, {})
                subdict[ks[-1]] = d[k]
            else:
                d_[k] = d[k]
        return d_

    if recursive:
        return recursive_split(d, prefix[-1])
    return d
