from typing import Callable, List

import dash
import dash_bootstrap_components as dbc
import imaging_server_kit as serverkit
import numpy as np
import plotly.graph_objects as go
import skimage.measure
from dash import ctx, dcc, html
from dash.dependencies import Input, Output, State


class Viewer:
    def __init__(self) -> None:
        self.fig = go.Figure()
        self.fig.update_xaxes(
            autorange=True,
            constrain="domain",
            showgrid=False,
            showticklabels=False,
            showline=False,
            zeroline=False,
        )
        self.fig.update_yaxes(
            autorange="reversed",
            constrain="domain",
            scaleanchor="x",
            showgrid=False,
            showticklabels=False,
            showline=False,
            zeroline=False,
        )
        self.fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            dragmode=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )

        self.layer_stack = []  # LayerDataTuple convention

    def get_layer_data_by_name(self, layer_name: str):
        for data, data_params, data_type in self.layer_stack:
            if data_params.get("name") == layer_name:
                return data

    @property
    def layer_idx_image(self):
        return len(self.image_layer_names)

    @property
    def layer_idx_labels(self):
        return len(self.labels_layer_names)

    @property
    def layer_names(self):
        return [
            data_params["name"] for (data, data_params, data_type) in self.layer_stack
        ]

    @property
    def image_layer_names(self):
        return [
            data_params["name"]
            for (data, data_params, data_type) in self.layer_stack
            if data_type == "image"
        ]

    @property
    def labels_layer_names(self):
        return [
            data_params["name"]
            for (data, data_params, data_type) in self.layer_stack
            if data_type == "labels"
        ]

    def add_image(self, image: np.ndarray):
        """Add an image to the figure."""
        layer_name = f"Image-{self.layer_idx_image}"
        if image.ndim == 2:
            self.fig.add_heatmap(
                z=image,
                zmax=np.max(image),
                zmin=np.min(image),
                colorscale="gray",
                opacity=1.0,
                showscale=False,
                name=layer_name,
            )
        elif image.ndim == 3:
            self.fig.add_trace(
                go.Image(z=image, opacity=1.0, name=layer_name),
            )
        self.layer_stack.append((image, {"name": layer_name}, "image"))

    def add_labels(self, labels: np.ndarray):
        """Add a segmentation map (labels) to the figure."""
        layer_name = f"Labels-{self.layer_idx_image}"
        contour = skimage.measure.find_contours(labels)
        for ctr in contour:
            y, x = ctr.T - 1
            self.fig.add_scatter(
                x=x,
                y=y,
                mode="lines",
                showlegend=False,
                line=dict(color="#3D9970", width=2),
                hoverinfo="skip",
                opacity=1.0,
                fill="toself",
                name=layer_name,
            )

        self.layer_stack.append((labels, {"name": layer_name}, "labels"))

    def remove_layer_by_name(self, layer_name):
        indeces_to_remove = []
        for idx, trace in enumerate(self.fig.data):
            if trace.name == layer_name:
                indeces_to_remove.append(idx)

        fig_data = list(self.fig.data)
        new_list = []
        for index in range(len(fig_data)):
            if index not in indeces_to_remove:
                new_list.append(fig_data[index])
        self.fig.data = tuple(new_list)

        for idx, (data, props, type) in enumerate(self.layer_stack):
            if props.get("name") == layer_name:
                self.layer_stack.pop(idx)
                break

    def display_data_tuple(self, data_tuple):
        for layer_data, layer_params, layer_type in data_tuple:
            if layer_type == "image":
                self.add_image(layer_data)  # Use layer_data for the image
            elif layer_type == "labels":
                self.add_labels(layer_data)  # Use layer_data for the labels
            else:
                print("Unknown layer type: ", layer_type)


def generate_dash_app(
    algo_name, algo_params, run_fnct: Callable, sample_image_fnct: Callable, prefix: str = "/demo/"
) -> dash.Dash:
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
        requests_pathname_prefix=prefix,
    )

    viewer = Viewer()

    parameters_ui = _parameters_ui(viewer, algo_params)

    app.layout = _app_layout(viewer, algo_name, parameters_ui)

    algo_inputs = _parameters_inputs(algo_params)

    app = _add_callbacks(app, viewer, algo_params, run_fnct, sample_image_fnct, algo_inputs)

    return app


def _parameters_ui(viewer, algo_params) -> List:
    algo_param_names = list(algo_params.keys())
    algo_param_values = list(algo_params.values())

    parameters_ui = []
    for param_value, param_name in zip(algo_param_values, algo_param_names):
        parameters_ui.append(dbc.Label(param_value.get("title")))

        param_widget_type = param_value.get("widget_type")
        if param_widget_type == "image":
            component = dcc.Dropdown(
                id=param_name,
                options=viewer.image_layer_names,
            )
        elif param_widget_type == "labels":
            component = dcc.Dropdown(
                id=param_name,
                options=viewer.labels_layer_names,
            )
        elif param_widget_type == "dropdown":
            component = dcc.Dropdown(id=param_name, options=param_value.get("enum"))
        elif param_widget_type == "int":
            component = dcc.Input(
                id=param_name,
                type="number",
                min=param_value.get("minimum"),
                max=param_value.get("maximum"),
                value=param_value.get("default"),
                step=1,  # temporary - to distinguish it from float
            )
        elif param_widget_type == "float":
            component = dcc.Input(
                id=param_name,
                type="number",
                min=param_value.get("minimum"),
                max=param_value.get("maximum"),
                value=param_value.get("default"),
                step=0.1,  # temporary - to distinguish it from int
            )
        elif param_widget_type == "bool":
            default = param_value.get("default")
            component = dcc.Checklist(
                id=param_name,
                options=[{"label": "", "value": str(default)}],  # simplifyable?
            )
        elif param_widget_type == "str":
            component = dcc.Input(
                id=param_name, type="text", value=param_value.get("default")
            )
        else:
            continue

        parameters_ui.append(component)

    run_btn = dbc.Button("Run", id="run-algorithm", class_name="btn-primary")
    parameters_ui.append(run_btn)

    sample_image_btn = dbc.Button(
        "Sample image", id="sample-image-btn", class_name="btn-secondary"
    )
    parameters_ui.append(sample_image_btn)

    return parameters_ui


def _parameters_inputs(algo_params):
    algo_param_names = list(algo_params.keys())
    algo_inputs = [Input("run-algorithm", "n_clicks")] + [
        State(algo_param_name, "value") for algo_param_name in algo_param_names
    ]
    return algo_inputs


def _app_layout(viewer, algo_name, parameters_ui) -> dbc.Container:
    return dbc.Container(
        fluid=True,
        className="main-container",
        children=[
            html.Header([html.H1(f"Algorithm: {algo_name}")]),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                dbc.Label("Layer list", className="font-weight-bold"),
                                dcc.Dropdown(id="layer-list"),
                                dbc.Button(
                                    "Remove",
                                    id=f"layer-remove-btn",
                                    class_name="btn-secondary",
                                ),
                            ],
                            id="layers",
                            className="layer-column",
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                dcc.Upload(
                                    ["Upload data"],
                                    className="upload-data",
                                    id="upload-data",
                                    multiple=False,
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="graph",
                                            figure=viewer.fig,
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                    className="graph-container",
                                ),
                            ],
                            className="graph-column",
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(
                                    parameters_ui,
                                    id="parameters-layout",
                                    className="algorithm-parameters",
                                ),
                            ],
                            className="parameters-column",
                        ),
                    ),
                ],
                className="main-row",
            ),
            html.Footer(["EPFL - 2024"]),
        ],
    )


def _runnable_params(viewer, algo_params, algo_inputs):
    algo_parameter_types = [
        param_value.get("widget_type") for param_value in list(algo_params.values())
    ]

    algo_runnable_params = {}
    for algo_param_name, algo_param_type, value in zip(
        list(algo_params.keys()), algo_parameter_types, algo_inputs
    ):
        if algo_param_type in ["image", "labels"]:
            parsed_value = viewer.get_layer_data_by_name(value)
        else:
            parsed_value = value

        algo_runnable_params[algo_param_name] = parsed_value

    return algo_runnable_params


def _add_callbacks(
    dash_app: dash.Dash, viewer, algo_params, run_fnct, sample_image_fnct, algo_inputs
) -> dash.Dash:
    @dash_app.callback(
        Output("graph", "figure", allow_duplicate=True),
        Input("layer-remove-btn", "n_clicks"),
        State("layer-list", "value"),
        prevent_initial_call=True,
    )
    def remove_layer_by_name(nclicks, layer_name) -> go.Figure:
        if nclicks is not None:
            viewer.remove_layer_by_name(layer_name)
            return viewer.fig
        
    @dash_app.callback(
        Output("graph", "figure", allow_duplicate=True),
        Input("sample-image-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def sample_image_callback(nclicks) -> go.Figure:
        print("Button clicked !!!")
        if (nclicks is not None):
            sample_images = sample_image_fnct()
            for sample_image in sample_images:
                viewer.add_image(sample_image)
            return viewer.fig
        else:
            return viewer.fig

    @dash_app.callback(Output("layer-list", "options"), Input("graph", "figure"))
    def update_layer_list(figure_contents) -> List:
        return viewer.layer_names

    @dash_app.callback(
        Output("graph", "figure", allow_duplicate=True),
        Input("upload-data", "contents"),
        prevent_initial_call=True,
    )
    def upload_image(contents) -> go.Figure:
        if contents is not None:
            _, content_string = contents.split(",")
            image = serverkit.decode_contents(content_string)
            viewer.add_image(image)
            return viewer.fig

    @dash_app.callback(
        Output("parameters-layout", "children", allow_duplicate=True),
        Output("layer-list", "options", allow_duplicate=True),
        Input("graph", "figure"),
        prevent_initial_call=True,
    )
    def update_parameters_layout(figure_contents):
        return _parameters_ui(viewer, algo_params), viewer.layer_names

    @dash_app.callback(
        Output("graph", "figure", allow_duplicate=True),
        *algo_inputs,
        prevent_initial_call=True,
    )
    def output_callback(nclicks, *algo_inputs) -> go.Figure:
        if (ctx.triggered_id == "run-algorithm") & (nclicks is not None):
            algo_runnable_params = _runnable_params(viewer, algo_params, algo_inputs)
            data_tuple = run_fnct(**algo_runnable_params)
            viewer.display_data_tuple(data_tuple)
            return viewer.fig
        else:
            return viewer.fig

    return dash_app
