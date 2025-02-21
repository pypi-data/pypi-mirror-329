from typing import Dict, Any, Optional, TypedDict
from dataclasses import dataclass, field

try:
    from funcnodes_react_flow import ReactPlugin
except (ModuleNotFoundError, ImportError):
    ReactPlugin = dict


class RenderOptions(TypedDict, total=False):
    """
    A typed dictionary for render options.

    Attributes:
      typemap (dict[str, str]): A dictionary mapping types to strings.
      inputconverter (dict[str, str]): A dictionary mapping input types to strings.
    """

    typemap: dict[str, str]
    inputconverter: dict[str, str]


@dataclass
class InstalledModule:
    """
    TypedDict for an installed module.

    Attributes:
        description (str): The description of the module.
        entry_points (Dict[str, LoadedModule]): Dictionary of entry points for the module.
    """

    name: str
    module: Any
    description: Optional[str] = None
    entry_points: Dict[str, Any] = field(default_factory=dict)
    react_plugin: Optional[ReactPlugin] = None
    render_options: Optional[RenderOptions] = None
    version: Optional[str] = None

    @property
    def rep_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "entry_points": list(self.entry_points.keys()),
            "version": self.version,
            "react_plugin": self.react_plugin is not None,
            "render_options": self.render_options is not None,
        }

    def __repr__(self) -> str:
        return f"InstalledModule({', '.join(f'{k}={v}' for k, v in self.rep_dict.items())})"

    def __str__(self) -> str:
        return self.__repr__()
