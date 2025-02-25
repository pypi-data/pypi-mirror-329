# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Modal(Component):
    """A Modal component.
Create a toggleable dialog using the Modal component. Toggle the visibility with the
`is_open` prop.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of the Modal.

- id (string; optional):
    The ID of the Modal.

- autoFocus (boolean; optional):
    **DEPRECATED** Use `autofocus` instead          Puts the focus on
    the modal when initialized.

- autofocus (boolean; optional):
    Puts the focus on the modal when initialized.

- backdrop (boolean | a value equal to: 'static'; optional):
    Includes a modal-backdrop element. Alternatively, specify 'static'
    for a backdrop which doesn't close the modal on click.

- backdropClassName (string; optional):
    **DEPRECATED** Use `backdrop_class_name` instead  Additional CSS
    classes to apply to the modal-backdrop.

- backdropStyle (dict; optional):
    **DEPRECATED** Use `content_style` instead.  Inline CSS styles to
    apply to the backdrop.

- backdrop_class_name (string; optional):
    Additional CSS classes to apply to the modal-backdrop.

- backdrop_style (dict; optional):
    Inline CSS styles to apply to the backdrop.

- centered (boolean; optional):
    If True, vertically center modal on page.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  Additional CSS classes
    to apply to the Modal.

- class_name (string; optional):
    Additional CSS classes to apply to the Modal.

- contentClassName (string; optional):
    **DEPRECATED** Use `content_class_name` instead  Additional CSS
    classes to apply to the modal-content.

- contentStyle (dict; optional):
    **DEPRECATED** Use `content_style` instead.  Inline CSS styles to
    apply to the content.

- content_class_name (string; optional):
    Additional CSS classes to apply to the modal content.

- content_style (dict; optional):
    Inline CSS styles to apply to the content.

- dialogClassName (string; optional):
    **DEPRECATED** Use `dialog_class_name` instead  Additional CSS
    classes to apply to the modal-dialog.

- dialogStyle (dict; optional):
    **DEPRECATED** Use `dialog_style` instead.  Inline CSS styles to
    apply to the dialog.

- dialog_class_name (string; optional):
    Additional CSS classes to apply to the modal.

- dialog_style (dict; optional):
    Inline CSS styles to apply to the dialog.

- enforceFocus (boolean; optional):
    When True The modal will prevent focus from leaving the Modal
    while open.

- fade (boolean; optional):
    Set to False for a modal that simply appears rather than fades
    into view.

- fullscreen (boolean | a value equal to: 'sm-down', 'md-down', 'lg-down', 'xl-down', 'xxl-down'; optional):
    Renders a fullscreen modal. Specifying a breakpoint will render
    the modal as fullscreen below the breakpoint size.

- is_open (boolean; optional):
    Whether modal is currently open.

- keyboard (boolean; optional):
    Close the modal when escape key is pressed.

- labelledBy (string; optional):
    **DEPRECATED** Use `labelledby` instead  The ARIA labelledby
    attribute.

- labelledby (string; optional):
    The ARIA labelledby attribute.

- role (string; optional):
    The ARIA role attribute.

- scrollable (boolean; optional):
    It True, scroll the modal body rather than the entire modal when
    it is too long to all fit on the screen.

- size (string; optional):
    Set the size of the modal. Options sm, lg, xl for small, large or
    extra large sized modals, or leave undefined for default size.

- style (dict; optional):
    Additional inline CSS styles to apply to the Modal.

- tag (string; optional):
    HTML tag to use for the Modal, default: div.

- zIndex (number | string; optional):
    **DEPRECATED** Use `zindex` instead  Set the z-index of the modal.
    Default 1050.

- zindex (number | string; optional):
    Set the z-index of the modal. Default 1050."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_bootstrap_components'
    _type = 'Modal'

    @_explicitize_args
    def __init__(
        self,
        children: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        *,
        is_open: typing.Optional[bool] = None,
        centered: typing.Optional[bool] = None,
        scrollable: typing.Optional[bool] = None,
        size: typing.Optional[str] = None,
        backdrop: typing.Optional[typing.Union[bool, Literal["static"]]] = None,
        fullscreen: typing.Optional[typing.Union[bool, Literal["sm-down", "md-down", "lg-down", "xl-down", "xxl-down"]]] = None,
        keyboard: typing.Optional[bool] = None,
        fade: typing.Optional[bool] = None,
        style: typing.Optional[dict] = None,
        dialog_style: typing.Optional[dict] = None,
        content_style: typing.Optional[dict] = None,
        backdrop_style: typing.Optional[dict] = None,
        class_name: typing.Optional[str] = None,
        dialog_class_name: typing.Optional[str] = None,
        backdrop_class_name: typing.Optional[str] = None,
        content_class_name: typing.Optional[str] = None,
        tag: typing.Optional[str] = None,
        autofocus: typing.Optional[bool] = None,
        enforceFocus: typing.Optional[bool] = None,
        role: typing.Optional[str] = None,
        labelledby: typing.Optional[str] = None,
        zindex: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number], str]] = None,
        dialogStyle: typing.Optional[dict] = None,
        contentStyle: typing.Optional[dict] = None,
        backdropStyle: typing.Optional[dict] = None,
        className: typing.Optional[str] = None,
        backdropClassName: typing.Optional[str] = None,
        contentClassName: typing.Optional[str] = None,
        dialogClassName: typing.Optional[str] = None,
        autoFocus: typing.Optional[bool] = None,
        labelledBy: typing.Optional[str] = None,
        zIndex: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number], str]] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'autoFocus', 'autofocus', 'backdrop', 'backdropClassName', 'backdropStyle', 'backdrop_class_name', 'backdrop_style', 'centered', 'className', 'class_name', 'contentClassName', 'contentStyle', 'content_class_name', 'content_style', 'dialogClassName', 'dialogStyle', 'dialog_class_name', 'dialog_style', 'enforceFocus', 'fade', 'fullscreen', 'is_open', 'keyboard', 'labelledBy', 'labelledby', 'role', 'scrollable', 'size', 'style', 'tag', 'zIndex', 'zindex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'autoFocus', 'autofocus', 'backdrop', 'backdropClassName', 'backdropStyle', 'backdrop_class_name', 'backdrop_style', 'centered', 'className', 'class_name', 'contentClassName', 'contentStyle', 'content_class_name', 'content_style', 'dialogClassName', 'dialogStyle', 'dialog_class_name', 'dialog_style', 'enforceFocus', 'fade', 'fullscreen', 'is_open', 'keyboard', 'labelledBy', 'labelledby', 'role', 'scrollable', 'size', 'style', 'tag', 'zIndex', 'zindex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Modal, self).__init__(children=children, **args)
