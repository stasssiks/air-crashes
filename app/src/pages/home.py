from dash import html, register_page

register_page(
    __name__,
    name='Home',
    top_nav=True,
    path='/'
)

text_style = {
    'font-size': '24px',
    'padding': '10px 20px'
}

header_style = {
    'font-size': '28px',
    'padding': '10px 0'
}

list_item_style = {
    'font-size': '24px',
    'padding': '5px 20px'
}


def layout():
    page_layout = html.Div([
        html.P(
            "Welcome to the Crash Prediction Dashboard! This application provides insights and forecasts "
            "related to vehicular crashes. Our goal is to help you understand the trends and factors affecting "
            "crash occurrences and provide you with tools to predict future crashes.",
            style=text_style
        ),
        html.P(
            "This project focuses on creating an interactive web application for analyzing and providing "
            "statistics on airplane crashes using a dataset downloaded from Kaggle. The application allows data "
            "visualization and provides various statistics and analyses related to airplane crashes.",
            style=text_style
        ),
        html.Ul([
            html.Li([
                html.H4("Application Functionality", style=header_style),
                html.P(
                    "The application offers the following features:",
                    style=text_style
                ),
                html.Ul([
                    html.Li(
                        "Analysis of crashes by year, location, causes, operator, and aircraft type: Users can browse "
                        "and filter data based on various criteria.",
                        style=list_item_style),
                    html.Li(
                        "Visualization of survival rates and predictions based on historical data: The application "
                        "includes various charts and visualizations that show survival rates and allow predictions of "
                        "future trends.",
                        style=list_item_style),
                    html.Li(
                        "Viewing raw and processed data: Users can view both the original and processed data and "
                        "export them in CSV and PDF formats.",
                        style=list_item_style)
                ])
            ]),
            html.Li([
                html.H4("Installation and Running the Application", style=header_style),
                html.P(
                    "To run the application, follow these steps:",
                    style=text_style
                ),
                html.Ol([
                    html.Li([
                        html.P("Clone the repository", style=list_item_style),
                        html.Pre(
                            "git clone https://github.com/your-repository/airplane-crashes.git\ncd airplane-crashes",
                            style=list_item_style)
                    ]),
                    html.Li([
                        html.P("Install required packages", style=list_item_style),
                        html.P("Ensure you have Python installed. Then, install the required packages using:",
                               style=list_item_style),
                        html.Pre("pip install -r requirements.txt", style=list_item_style)
                    ]),
                    html.Li([
                        html.P("Run the application", style=list_item_style),
                        html.P("Start the application with the command:",
                               style=list_item_style),
                        html.Pre("python app.py", style=list_item_style)
                    ]),
                    html.Li([
                        html.P("Access the application", style=list_item_style),
                        html.P("Open a web browser and go to:", style=list_item_style),
                        html.Pre("http://127.0.0.1:8050", style=list_item_style)
                    ])
                ])
            ]),
            html.Li([
                html.H4("Tools and Libraries Used", style=header_style),
                html.P(
                    "The application is built using the following tools and libraries:",
                    style=text_style
                ),
                html.Ul([
                    html.Li("Dash: A framework for building web applications in Python.",
                            style=list_item_style),
                    html.Li("Plotly: A library for creating interactive charts and visualizations.",
                            style=list_item_style),
                    html.Li("Pandas: A library for data manipulation and analysis.",
                            style=list_item_style),
                    html.Li("NumPy: A library for numerical computations.",
                            style=list_item_style),
                    html.Li("Scipy: A library for scientific and technical computing.",
                            style=list_item_style),
                    html.Li("Statsmodels: A library for statistical modeling and time series analysis.",
                            style=list_item_style),
                    html.Li("Matplotlib: A library for creating static, animated, and interactive visualizations.",
                            style=list_item_style),
                    html.Li("Joblib: A library for efficient saving and loading of Python objects.",
                            style=list_item_style)
                ])
            ])
        ])
    ], style={'padding': '20px'})
    return page_layout
