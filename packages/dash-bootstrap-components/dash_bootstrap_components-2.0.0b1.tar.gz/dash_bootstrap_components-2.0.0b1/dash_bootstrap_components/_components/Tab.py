# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class Tab(Component):
    """A Tab component.
Create a single tab. Should be used as a component of Tabs.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this Tab.

- id (string; optional):
    The ID of the Tab.

- activeLabelClassName (string; optional):
    **DEPRECATED** Use `active_label_class_name` instead  Additional
    CSS classes to apply to the Tabs. The classes specified with this
    prop will be applied to the NavLink in the tab when it is active.

- activeTabClassName (string; optional):
    **DEPRECATED** Use `active_tab_class_name` instead  Additional CSS
    classes to apply to the Tabs. The classes specified with this prop
    will be applied to the NavItem in the tab when it is active.

- active_label_class_name (string; optional):
    Additional CSS classes to apply to the Tabs. The classes specified
    with this prop will be applied to the NavLink in the tab when it
    is active.

- active_label_style (dict; optional):
    Defines CSS styles which will override styles previously set. The
    styles set here apply to the NavLink in the tab when it is active.

- active_tab_class_name (string; optional):
    Additional CSS classes to apply to the Tabs. The classes specified
    with this prop will be applied to the NavItem in the tab when it
    is active.

- active_tab_style (dict; optional):
    Defines CSS styles which will override styles previously set. The
    styles set here apply to the NavItem in the tab when it is active.

- className (string; optional):
    **DEPRECATED** Use `class_name` instead.  Additional CSS classes
    to apply to the Tabs.

- class_name (string; optional):
    Additional CSS classes to apply to the Tabs.

- disabled (boolean; optional):
    Determines if Tab is disabled or not - defaults to False.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components  See
    https://react.dev/learn/rendering-lists#why-does-react-need-keys
    for more info.

- label (string; optional):
    The tab's label, displayed in the tab itself.

- labelClassName (string; optional):
    **DEPRECATED** Use `label_class_name` instead  Additional CSS
    classes to apply to the Tabs. The classes specified with this prop
    will be applied to the NavLink in the tab.

- label_class_name (string; optional):
    Additional CSS classes to apply to the Tabs. The classes specified
    with this prop will be applied to the NavLink in the tab.

- label_style (dict; optional):
    Defines CSS styles which will override styles previously set. The
    styles set here apply to the NavLink in the tab.

- style (dict; optional):
    Defines CSS styles which will override styles previously set. The
    styles set here apply to the content of the Tab.

- tabClassName (string; optional):
    **DEPRECATED** Use `tab_class_name` instead  Additional CSS
    classes to apply to the Tabs. The classes specified with this prop
    will be applied to the NavItem in the tab.

- tab_class_name (string; optional):
    Additional CSS classes to apply to the Tabs. The classes specified
    with this prop will be applied to the NavItem in the tab.

- tab_id (string; optional):
    Optional identifier for tab used for determining which tab is
    visible if not specified, and Tab is being used inside Tabs
    component, the tabId will be set to \"tab-i\" where i is (zero
    indexed) position of tab in list tabs pased to Tabs component.

- tab_style (dict; optional):
    Defines CSS styles which will override styles previously set. The
    styles set here apply to the NavItem in the tab."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_bootstrap_components'
    _type = 'Tab'

    @_explicitize_args
    def __init__(
        self,
        children: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        *,
        label: typing.Optional[str] = None,
        tab_id: typing.Optional[str] = None,
        disabled: typing.Optional[bool] = None,
        style: typing.Optional[dict] = None,
        tab_style: typing.Optional[dict] = None,
        active_tab_style: typing.Optional[dict] = None,
        label_style: typing.Optional[dict] = None,
        active_label_style: typing.Optional[dict] = None,
        class_name: typing.Optional[str] = None,
        tab_class_name: typing.Optional[str] = None,
        active_tab_class_name: typing.Optional[str] = None,
        label_class_name: typing.Optional[str] = None,
        active_label_class_name: typing.Optional[str] = None,
        key: typing.Optional[str] = None,
        className: typing.Optional[str] = None,
        tabClassName: typing.Optional[str] = None,
        activeTabClassName: typing.Optional[str] = None,
        labelClassName: typing.Optional[str] = None,
        activeLabelClassName: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['children', 'id', 'activeLabelClassName', 'activeTabClassName', 'active_label_class_name', 'active_label_style', 'active_tab_class_name', 'active_tab_style', 'className', 'class_name', 'disabled', 'key', 'label', 'labelClassName', 'label_class_name', 'label_style', 'style', 'tabClassName', 'tab_class_name', 'tab_id', 'tab_style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'activeLabelClassName', 'activeTabClassName', 'active_label_class_name', 'active_label_style', 'active_tab_class_name', 'active_tab_style', 'className', 'class_name', 'disabled', 'key', 'label', 'labelClassName', 'label_class_name', 'label_style', 'style', 'tabClassName', 'tab_class_name', 'tab_id', 'tab_style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Tab, self).__init__(children=children, **args)
