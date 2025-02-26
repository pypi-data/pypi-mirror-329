import typing
import warnings
from importlib.metadata import EntryPoint, entry_points

from kisters.network_store.model_library.base import BaseElement


def _get_all_subclasses(cls: typing.Any) -> set[typing.Any]:
    return set(cls.__subclasses__()).union(
        s for c in cls.__subclasses__() for s in _get_all_subclasses(c)
    )


all_controls: list[BaseElement] = []
all_nodes: list[BaseElement] = []
all_links: list[BaseElement] = []
all_groups: list[BaseElement] = []
elements_mapping: dict[str, dict[str, dict[str, BaseElement]]] = {}

group = "kisters.network_store.model_library.util"
eps: list[EntryPoint]
try:
    eps = entry_points(group=group)  # type: ignore
except TypeError:
    # before python 3.10
    eps = entry_points().get(group, [])

for entry_point in eps:
    ep = entry_point.load()
    elements_mapping[entry_point.name] = {
        "controls": {
            elem.__name__: elem
            for elem in _get_all_subclasses(ep.controls._Control)
            if not elem.__name__.startswith("_")
        },
        "links": {
            elem.__name__: elem
            for elem in _get_all_subclasses(ep.links._Link)
            if not elem.__name__.startswith("_")
        },
        "nodes": {
            elem.__name__: elem
            for elem in _get_all_subclasses(ep.nodes._Node)
            if not elem.__name__.startswith("_")
        },
        "groups": {
            elem.__name__: elem
            for elem in _get_all_subclasses(ep.groups._Group)
            if not elem.__name__.startswith("_")
        },
    }
    all_controls.extend(elements_mapping[entry_point.name]["controls"].values())
    all_links.extend(elements_mapping[entry_point.name]["links"].values())
    all_nodes.extend(elements_mapping[entry_point.name]["nodes"].values())
    all_groups.extend(elements_mapping[entry_point.name]["groups"].values())


def element_from_dict(obj: dict[str, typing.Any], validate: bool = True) -> BaseElement:
    if validate:
        warnings.warn(
            "argument validate to element_from_dict() is deprecated",
            DeprecationWarning,
            stacklevel=2,
        )
    domain = obj.get("domain")
    if not domain:
        msg = f"Missing attribute 'domain': {obj}"
        raise ValueError(msg)
    if domain not in elements_mapping:
        msg = f"Domain '{domain}' is not recognized."
        raise ValueError(msg)

    collection = obj.get("collection")
    if not collection:
        msg = f"Missing attribute 'collection': {obj}"
        raise ValueError(msg)
    if collection not in ("controls", "groups", "nodes", "links"):
        msg = f"Collection '{collection}' is not recognized."
        raise ValueError(msg)

    element_class = obj.get("element_class")
    if not element_class:
        msg = "Cannot instantiate: missing attribute 'element_class'"
        raise ValueError(msg)
    if element_class not in elements_mapping[domain][collection]:
        msg = f"Element class {domain}.{collection}.{element_class} is not recognized."
        raise ValueError(msg)
    element_model = elements_mapping[domain][collection][element_class]
    return element_model.model_validate(obj)


def element_to_dict(elem: BaseElement) -> dict[str, typing.Any]:
    warnings.warn(
        "element_to_dict is deprecated, use 'element.model_dump()'",
        DeprecationWarning,
        stacklevel=2,
    )
    return elem.model_dump(mode="json", exclude_none=True)
