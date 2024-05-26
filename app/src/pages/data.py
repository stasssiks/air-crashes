import os
import pandas as pd
from reportlab.pdfgen import canvas
from dash import html, dcc, register_page, callback, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import dash
from flask import send_file, Flask
from .helpers import load_data

app = Flask(__name__)
app = dash.Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP])

register_page(
    __name__,
    name='Data',
    top_nav=True,
    path='/data'
)

raw_data = pd.read_csv(load_data('crashes-raw.csv'))
processed_data = pd.read_csv(load_data('crashes-processed.csv'))


def layout():
    return html.Div([
        dbc.ButtonGroup(
            [
                dbc.Button("Raw Data", id="raw-button", n_clicks=0),
                dbc.Button("Processed Data", id="processed-button", n_clicks=0)
            ],
            style={'margin': '20px'}
        ),
        html.Div(id='data-table-container'),
        html.Div([
            dbc.Button("Export to CSV", id="export-csv-button", className="mr-2"),
            dcc.Download(id="download-csv"),
            dbc.Button("Export to PDF", id="export-pdf-button"),
            dcc.Download(id="download-pdf")
        ], style={'margin': '20px'})
    ])


@callback(
    Output('data-table-container', 'children'),
    Output('raw-button', 'style'),
    Output('processed-button', 'style'),
    Input('raw-button', 'n_clicks'),
    Input('processed-button', 'n_clicks'),
    State('raw-button', 'n_clicks_timestamp'),
    State('processed-button', 'n_clicks_timestamp')
)
def update_table_and_buttons(raw_clicks, processed_clicks, raw_timestamp, processed_timestamp):
    if processed_timestamp is None or (raw_timestamp is not None and raw_timestamp > processed_timestamp):
        data = raw_data
        raw_style = {'background-color': 'lightblue'}
        processed_style = {'background-color': 'darkgrey'}
    else:
        data = processed_data
        raw_style = {'background-color': 'darkgrey'}
        processed_style = {'background-color': 'lightblue'}

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        page_size=20,
        style_table={'height': '700px', 'overflowY': 'auto'},
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        page_action='native',
        style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '150px', 'maxWidth': '200px'},
        style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
    ), raw_style, processed_style


@callback(
    Output('download-csv', 'data'),
    Input('export-csv-button', 'n_clicks'),
    State('raw-button', 'n_clicks_timestamp'),
    State('processed-button', 'n_clicks_timestamp'),
    prevent_initial_call=True
)
def export_csv(n_clicks, raw_timestamp, processed_timestamp):
    if processed_timestamp is None or (raw_timestamp is not None and raw_timestamp > processed_timestamp):
        data = raw_data
    else:
        data = processed_data
    csv_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'exported_data.csv')
    data.to_csv(csv_path, index=False)
    return dcc.send_file(csv_path)


@callback(
    Output('download-pdf', 'data'),
    Input('export-pdf-button', 'n_clicks'),
    State('raw-button', 'n_clicks_timestamp'),
    State('processed-button', 'n_clicks_timestamp'),
    prevent_initial_call=True
)
def export_pdf(n_clicks, raw_timestamp, processed_timestamp):
    if processed_timestamp is None or (raw_timestamp is not None and raw_timestamp > processed_timestamp):
        data = raw_data
    else:
        data = processed_data
    pdf_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'exported_data.pdf')
    generate_pdf(data, pdf_path)
    return dcc.send_file(pdf_path)


def truncate_string(s, max_length):
    if len(s) > max_length:
        return s[:max_length] + '...'
    return s


def generate_pdf(data, pdf_path):
    custom_page_width = 1800
    custom_page_height = 600
    c = canvas.Canvas(pdf_path, pagesize=(custom_page_width, custom_page_height))
    width, height = custom_page_width, custom_page_height
    font_size = 8
    c.setFont("Helvetica", font_size)

    x_offset = 40
    y_offset = height - 40
    row_height = 12

    columns = data.columns.tolist()
    col_widths = {col: (width - 2 * x_offset) / len(columns) for col in columns}
    x_positions = [x_offset + sum(col_widths[columns[i]] for i in range(j)) for j in range(len(columns))]

    for i, column in enumerate(columns):
        c.drawString(x_positions[i], y_offset, truncate_string(column, 14))
    y_offset -= row_height

    for i, row in enumerate(data.itertuples(index=False, name=None)):
        if y_offset < row_height:
            c.showPage()
            c.setFont("Helvetica", font_size)
            y_offset = height - 40
            for i, column in enumerate(columns):
                c.drawString(x_positions[i], y_offset, truncate_string(column, 14))
            y_offset -= row_height

        for j, cell in enumerate(row):
            c.drawString(x_positions[j], y_offset, truncate_string(str(cell), 14))
        y_offset -= row_height

    c.save()
