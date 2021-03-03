# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SideMenu(Component):
    """A SideMenu component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- items (list; required): An array of id, label
- className (string; optional): Navbar class name"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, items=Component.REQUIRED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'items', 'className']
        self._type = 'SideMenu'
        self._namespace = 'sm'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'items', 'className']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['items']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SideMenu, self).__init__(**args)
