import dash
from dash import html, dcc, Input, Output, State, callback_context
import uuid  # For generating unique IDs
from global_classes import VariableOutput
import dash_bootstrap_components as dbc
from styling import Readability

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

readability_obj = Readability()

custom_variables = html.Div(children = 
    [
        html.Div(style = {'display': 'flex', 'align-items': 'center', 'padding': '20px'},
            children = [
                html.Span("I would like to create a custom variable called ", style = {'margin-right': '10px'}, className = "text-info"),
                dcc.Input(id = "custom-vars-var-name", style = {"margin-right": "10px", 'width': '200px'}),
                html.Span("by", className = "text-info")
            ]
        ),
        html.Div(id = "custom-vars-fill-area", style = {'display': 'flex', 'align-items': 'center', "margin-left": "100px"},
            children = [
                dcc.Dropdown(
                    id = "custom-vars-operation", 
                    options = [{"label": "Dividing", "value": "division"}, {"label": "Adding", "value": "addition"}],
                    placeholder = "Operation",
                    style = {"width": "200px", "margin-right": "10px"}
                ),
                html.Div(id = "custom-vars-output-dropdown-div",
                    children = [
                ])
            ]
        ),
        html.Div(style = {"padding": 20},
            children = [
                dbc.Button(id = "create-custom-variable-button", children = "Create", className = "btn btn-primary btn-lg"),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Success!"), close_button = True),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close",
                                id = "close-centered",
                                className = "ms-auto",
                                n_clicks = 0,
                            )
                        )
                    ],
                    id = "custom-variable-created-modal",
                    is_open = False,
                )
            ]
        )
    ]
)

# Layout with a button to add a new dropdown and a placeholder for dynamically added dropdowns
app.layout = html.Div([
    custom_variables
])

@app.callback(
    Output("custom-vars-output-dropdown-div", "children"),
    Input("custom-vars-operation", "value"),
    State("custom-vars-output-dropdown-div", "children"),
)
def add_dropdown(operation, children):
    if operation == "division":
            return (
                dcc.Dropdown(id = "custom-vars-output-1-dropdown-div", options = [{"label": k, "value": v} for k, v in readability_obj.naming_dict_display_names_first.items()],
                    placeholder = "Output 1", style = {"margin-right": "10px", "width": "500px"}),
                html.Span("by", style = {'margin-right': '10px'}),
                dcc.Dropdown(id = "custom-vars-output-2-dropdown-div", options = [{"label": k, "value": v} for k, v in readability_obj.naming_dict_display_names_first.items()],
                            placeholder = "Output 2",
                            style = {"width": "500px"})
                    )
    # if n_clicks > 0:
    #     new_dropdown_id = str(uuid.uuid4())
    #     new_dropdown = dcc.Dropdown(
    #         id={'type': 'dynamic-dropdown', 'index': new_dropdown_id},
    #         options=[{'label': 'Initial Option', 'value': 'initial'}],
    #         value='initial'
    #     )
    #     children.append(html.Div([new_dropdown]))
    # return children

# @app.callback(
#     Output({'type': 'dynamic-dropdown', 'index': dash.ALL}, 'options'),
#     Input("update-options", "n_clicks"),
#     prevent_initial_call=True
# )
# def update_dropdown_options(n_clicks):
#     new_options = [
#         {'label': 'Option 1', 'value': 'option1'},
#         {'label': 'Option 2', 'value': 'option2'}
#     ]
#     return [new_options] * n_clicks  # Return a list of new options for each dropdown

if __name__ == '__main__':
    app.run_server(debug=True)

  