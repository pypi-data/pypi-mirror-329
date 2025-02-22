# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Lottie(Component):
    """A Lottie component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- ariaLabel (string; optional)

- ariaRole (string; optional)

- className (string; optional):
    The class of the component.

- direction (number; optional)

- height (string; optional):
    Pixel value for containers height.

- isClickToPauseDisabled (boolean; optional)

- isPaused (boolean; optional)

- isStopped (boolean; optional)

- options (dict; optional):
    Options passed to the Lottie animation (see
    https://www.npmjs.com/package/react-lottie for details).

- segments (list of numbers; optional)

- speed (number; optional)

- style (string; optional)

- title (string; optional)

- url (string; optional):
    If set, data will be downloaded from this url.

- width (string; optional):
    Pixel value for containers width."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_extensions'
    _type = 'Lottie'

    @_explicitize_args
    def __init__(
        self,
        children: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        className: typing.Optional[str] = None,
        options: typing.Optional[dict] = None,
        url: typing.Optional[str] = None,
        width: typing.Optional[str] = None,
        height: typing.Optional[str] = None,
        isStopped: typing.Optional[bool] = None,
        isPaused: typing.Optional[bool] = None,
        speed: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        segments: typing.Optional[typing.Sequence[typing.Union[int, float, numbers.Number]]] = None,
        direction: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        ariaRole: typing.Optional[str] = None,
        ariaLabel: typing.Optional[str] = None,
        isClickToPauseDisabled: typing.Optional[bool] = None,
        title: typing.Optional[str] = None,
        style: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'ariaLabel', 'ariaRole', 'className', 'direction', 'height', 'isClickToPauseDisabled', 'isPaused', 'isStopped', 'options', 'segments', 'speed', 'style', 'title', 'url', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'ariaLabel', 'ariaRole', 'className', 'direction', 'height', 'isClickToPauseDisabled', 'isPaused', 'isStopped', 'options', 'segments', 'speed', 'style', 'title', 'url', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Lottie, self).__init__(children=children, **args)
