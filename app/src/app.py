import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from navbar import create_navbar
from flask import request

NAVBAR = create_navbar()
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
APP_TITLE = "Air crashes"

dash_app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.LUX,
        FA621,
    ],
    title=APP_TITLE,
    use_pages=True,
)

dash_app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{APP_TITLE}</title>
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>

    </body>
</html>
'''

dash_app.layout = dcc.Loading(
    id='loading_page_content',
    children=[
        html.Div([
            NAVBAR,
            dash.page_container
        ])
    ],
    color='primary',
    fullscreen=True
)

server = dash_app.server


@server.route('/_shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


if __name__ == '__main__':
    dash_app.run_server(debug=True)
