# AUTO GENERATED FILE - DO NOT EDIT

export sidemenu

"""
    sidemenu(;kwargs...)

A SideMenu component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `items` (Array; required): An array of id, label
- `className` (String; optional): Navbar class name
"""
function sidemenu(; kwargs...)
        available_props = Symbol[:id, :items, :className]
        wild_props = Symbol[]
        return Component("sidemenu", "SideMenu", "sm", available_props, wild_props; kwargs...)
end

