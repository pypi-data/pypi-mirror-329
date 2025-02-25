# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Rangelineplot(Component):
    """A Rangelineplot component.


Keyword arguments:

- id (string; optional):
    The component's id.

- axisType (a value equal to: 'x', 'y'; default 'x'):
    Which axis this range is for: 'x' or 'y'.

- boundaryStyle (dict; default {color: 'transparent', width: 20}):
    Plotly line style for the draggable boundaries.

- className (string; default ''):
    Additional CSS classes for the container <div>.

- data (dict; required):
    Data object containing parallel arrays `x` and `y`.

    `data` is a dict with keys:

    - x (list of numbers; required)

    - y (list of numbers; required)

- grayZoneStyle (dict; default {fillcolor: 'rgba(200,200,200,0.5)'}):
    Plotly fill style for gray zones outside the selected range.

- lineStyle (dict; default {color: '#1f77b4', width: 2}):
    Plotly line style for the main data trace.

- range (list of numbers; optional):
    The selected range, [start, end], for whichever axisType is
    chosen. If axisType='x', it refers to x-values. If 'y', it refers
    to y-values.

- style (dict; optional):
    CSS style to apply to the container <div>."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_rangelineplot'
    _type = 'Rangelineplot'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.REQUIRED, range=Component.UNDEFINED, axisType=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, lineStyle=Component.UNDEFINED, grayZoneStyle=Component.UNDEFINED, boundaryStyle=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'axisType', 'boundaryStyle', 'className', 'data', 'grayZoneStyle', 'lineStyle', 'range', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'axisType', 'boundaryStyle', 'className', 'data', 'grayZoneStyle', 'lineStyle', 'range', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Rangelineplot, self).__init__(**args)
