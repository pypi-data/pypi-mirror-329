# RangeLinePlot

RangeLinePlot is a Dash component library.

RangeLinePlot integrates with Plotly.js to create interactive line plots with a draggable range selector. The component allows users to highlight a selected range on the x- or y-axis and dynamically adjust it through drag-and-drop functionality.

![Demonstration](assets/rangelineplot.gif)

---

## Features

- **Interactive Range Selection**: Highlight a range on the x- or y-axis and adjust it interactively.
- **Customizable Styles**: Modify line, boundary, and gray zone styles to match your design.
- **Dash Integration**: Fully compatible with Python Dash applications.

---

## Installation

Install the component from [PyPI](https://pypi.org/project/dash-rangelineplot/) using `pip`:

```bash
pip install dash-rangelineplot
```
   
---

## Usage

```python
from dash import Dash, html
from rangelineplot import Rangelineplot

app = Dash(__name__)

app.layout = html.Div([
    Rangelineplot(
        id="example-plot",
        data={
            "x": list(range(10)),
            "y": [x ** 2 for x in range(10)],
        },
        range=[2, 6],  # Initial range
        axisType="x",  # Range applies to x-axis
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

### Props

| Prop              | Type                   | Default Value                         | Description                                                                 |
|-------------------|------------------------|---------------------------------------|-----------------------------------------------------------------------------|
| `id`              | `string`              | `None`                                | Unique identifier for the component.                                       |
| `data`            | `dict`                | `{"x": [], "y": []}`                  | Input data as two arrays: `x` and `y`. Must have equal lengths.            |
| `range`           | `list[number]`        | `None`                                | Initial range `[start, end]` for the selected axis.                        |
| `axisType`        | `string`              | `'x'`                                 | Specifies the axis for the range (`'x'` or `'y'`).                         |
| `lineStyle`       | `dict`                | `{color: '#1f77b4', width: 2}`        | Plotly line style for the main data trace.                                 |
| `grayZoneStyle`   | `dict`                | `{fillcolor: 'rgba(200,200,200,0.5)'}`| Fill style for gray zones outside the selected range.                      |
| `boundaryStyle`   | `dict`                | `{color: 'transparent', width: 20}`   | Line style for the draggable boundary lines.                               |

---
## Development

### Install Dependencies

If you’re contributing to the development of this component, install the necessary dependencies:

```bash
npm install
pip install -r requirements.txt
```

### Build the Component

After making changes to the React component, rebuild the bundle:

```bash
npm run build
python usage.py
```

The resulting files will be placed in the rangelineplot/ directory for use in the Python wrapper.

## License

This project is licensed under the MIT License.
