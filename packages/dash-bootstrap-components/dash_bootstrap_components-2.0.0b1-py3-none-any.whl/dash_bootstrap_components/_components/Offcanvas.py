# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Offcanvas(Component):
    """An Offcanvas component.
Create a toggleable hidden sidebar using the Offcanvas component.
Toggle the visibility with the `is_open` prop.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of the Offcanvas.

- id (string; optional):
    The ID of the Offcanvas.

- autoFocus (boolean; optional):
    **DEPRECATED** Use `autofocus` instead          Puts the focus on
    the modal when initialized.

- autofocus (boolean; optional):
    Puts the focus on the offcanvas when initialized.

- backdrop (boolean | a value equal to: 'static'; default True):
    Includes an offcanvas-backdrop element. Alternatively, specify
    'static' for a backdrop which doesn't close the modal on click.

- backdropClassName (string; optional):
    **DEPRECATED** - Use backdrop_class_name instead.  CSS class to
    apply to the backdrop.

- backdrop_class_name (string; optional):
    CSS class to apply to the backdrop.

- className (string; optional):
    **DEPRECATED** - Use class_name instead.  Additional CSS classes
    to apply to the Offcanvas.

- class_name (string; optional):
    Additional CSS classes to apply to the Offcanvas.

- close_button (boolean; default True):
    Specify whether the Offcanvas should contain a close button in the
    header.

- is_open (boolean; default False):
    Whether offcanvas is currently open.

- keyboard (boolean; optional):
    If True, the offcanvas will close when the escape key is pressed.

- labelledBy (string; optional):
    **DEPRECATED** Use `labelledby` instead  The ARIA labelledby
    attribute.

- labelledby (string; optional):
    The ARIA labelledby attribute.

- placement (a value equal to: 'start', 'end', 'top', 'bottom'; optional):
    Which side of the viewport the offcanvas will appear from.

- scrollable (boolean; optional):
    Allow body scrolling while offcanvas is open.

- style (dict; optional):
    Additional inline CSS styles to apply to the Offcanvas.

- title (a list of or a singular dash component, string or number; optional):
    The header title."""
    _children_props = ['title']
    _base_nodes = ['title', 'children']
    _namespace = 'dash_bootstrap_components'
    _type = 'Offcanvas'

    @_explicitize_args
    def __init__(
        self,
        children: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        *,
        is_open: typing.Optional[bool] = None,
        title: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        placement: typing.Optional[Literal["start", "end", "top", "bottom"]] = None,
        backdrop: typing.Optional[typing.Union[bool, Literal["static"]]] = None,
        close_button: typing.Optional[bool] = None,
        keyboard: typing.Optional[bool] = None,
        scrollable: typing.Optional[bool] = None,
        style: typing.Optional[dict] = None,
        class_name: typing.Optional[str] = None,
        backdrop_class_name: typing.Optional[str] = None,
        autofocus: typing.Optional[bool] = None,
        labelledby: typing.Optional[str] = None,
        className: typing.Optional[str] = None,
        backdropClassName: typing.Optional[str] = None,
        autoFocus: typing.Optional[bool] = None,
        labelledBy: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'autoFocus', 'autofocus', 'backdrop', 'backdropClassName', 'backdrop_class_name', 'className', 'class_name', 'close_button', 'is_open', 'keyboard', 'labelledBy', 'labelledby', 'placement', 'scrollable', 'style', 'title']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'autoFocus', 'autofocus', 'backdrop', 'backdropClassName', 'backdrop_class_name', 'className', 'class_name', 'close_button', 'is_open', 'keyboard', 'labelledBy', 'labelledby', 'placement', 'scrollable', 'style', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Offcanvas, self).__init__(children=children, **args)
