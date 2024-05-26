import dash
import joblib
from dash import html, dcc, register_page, callback, Output, Input
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
from scipy.stats import linregress
import numpy as np
import plotly.express as px
import plotly.colors
from .helpers import load_data

register_page(__name__, name='Analysis', top_nav=True, path='/analysis')


def layout():
    """Defines the layout of the Analysis page."""
    button_group = html.Div([
        html.Button("Time", id='btn-time', n_clicks=0),
        html.Button("Location", id='btn-location', n_clicks=0),
        html.Button("Causes", id='btn-causes', n_clicks=0),
        html.Button("Operator", id='btn-operator', n_clicks=0),
        html.Button("Survival", id='btn-survival', n_clicks=0),
        html.Button("Forecast", id='btn-correlation-studies', n_clicks=0)
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'})

    graph_container = html.Div(id='graph-container')

    return html.Div([
        button_group,
        graph_container
    ])


@callback(
    Output('graph-container', 'children'),
    Output('btn-time', 'style'),
    Output('btn-location', 'style'),
    Output('btn-causes', 'style'),
    Output('btn-operator', 'style'),
    Output('btn-survival', 'style'),
    Output('btn-correlation-studies', 'style'),
    [Input('btn-time', 'n_clicks'),
     Input('btn-location', 'n_clicks'),
     Input('btn-causes', 'n_clicks'),
     Input('btn-operator', 'n_clicks'),
     Input('btn-survival', 'n_clicks'),
     Input('btn-correlation-studies', 'n_clicks')]
)
def display_graph(btn_time, btn_location, btn_causes, btn_operator, btn_survival, btn_correlation):
    """
    Displays the appropriate graph based on which button is clicked.
    Also changes the style of the active button.
    """
    triggered = [t['prop_id'] for t in dash.callback_context.triggered]
    base_style = {'font-size': '20px', 'border': 'none', 'padding': '10px 20px', 'color': 'white'}
    styles = {
        'btn-time': {**base_style, 'background-color': 'darkgrey'},
        'btn-location': {**base_style, 'background-color': 'darkgrey'},
        'btn-causes': {**base_style, 'background-color': 'darkgrey'},
        'btn-operator': {**base_style, 'background-color': 'darkgrey'},
        'btn-survival': {**base_style, 'background-color': 'darkgrey'},
        'btn-correlation-studies': {**base_style, 'background-color': 'darkgrey'}
    }

    active_style = {'font-size': '20px', 'border': 'none', 'padding': '10px 20px', 'color': 'white',
                    'background-color': 'lightblue'}

    if 'btn-time.n_clicks' in triggered:
        styles['btn-time'] = active_style
    elif 'btn-location.n_clicks' in triggered:
        styles['btn-location'] = active_style
    elif 'btn-causes.n_clicks' in triggered:
        styles['btn-causes'] = active_style
    elif 'btn-operator.n_clicks' in triggered:
        styles['btn-operator'] = active_style
    elif 'btn-survival.n_clicks' in triggered:
        styles['btn-survival'] = active_style
    elif 'btn-correlation-studies.n_clicks' in triggered:
        styles['btn-correlation-studies'] = active_style
    else:
        styles['btn-time'] = active_style

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    processed_data = pd.read_csv(load_data('crashes-processed.csv'))

    if button_id == 'btn-time':
        fig1 = create_yearly_incidents_figure(processed_data)
        fig2 = create_seasonal_distribution_figure(processed_data)
        graph_layout = html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)
        ])
    elif button_id == 'btn-location':
        fig1 = create_location_graph(processed_data)
        fig2 = create_top_locations_figure(processed_data)
        fig3 = create_most_crashes_by_destination_figure(processed_data)
        graph_layout = html.Div([
            html.Div([
                dcc.Graph(figure=fig1, style={'width': '70%'}),
                dcc.Graph(figure=fig2, style={'width': '30%'})
            ], style={'display': 'flex'}),
            html.Div([
                dcc.Graph(figure=fig3)
            ])
        ])
    elif button_id == 'btn-causes':
        fig1 = create_top_causes_figure(processed_data)
        fig2 = create_casualties_by_cause_figure(processed_data)
        graph_layout = html.Div([
            dcc.Graph(figure=fig1, style={'width': '50%'}),
            dcc.Graph(figure=fig2, style={'width': '50%'})
        ], style={'display': 'flex', 'flex-direction': 'row'})
    elif button_id == 'btn-operator':
        fig1 = create_operator_figure(processed_data)
        fig2 = create_aircraft_figure(processed_data)
        graph_layout = html.Div([
            dcc.Graph(figure=fig1, style={'width': '50%'}),
            dcc.Graph(figure=fig2, style={'width': '50%'})
        ], style={'display': 'flex', 'flex-direction': 'row'})
    elif button_id == 'btn-survival':
        fig1 = create_survival_figure(processed_data)
        fig2 = create_casualty_season_plots(processed_data)
        graph_layout = html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)
        ])
    elif button_id == 'btn-correlation-studies':
        fig1 = create_forecast_chart()
        graph_layout = html.Div([
            dcc.Graph(figure=fig1)
        ])
    else:
        fig1 = create_yearly_incidents_figure(processed_data)
        fig2 = create_seasonal_distribution_figure(processed_data)
        graph_layout = html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)
        ])

    return graph_layout, styles['btn-time'], styles['btn-location'], styles['btn-causes'], styles['btn-operator'], \
           styles['btn-survival'], styles['btn-correlation-studies']


def standardized_plot_layout(fig, min_val=None, max_val=None):
    """
    Standardizes the layout of the plot with consistent formatting and color scale.

    Args:
        fig (go.Figure): The plotly figure to update.
        min_val (int/float, optional): Minimum value for the color scale. Defaults to None.
        max_val (int/float, optional): Maximum value for the color scale. Defaults to None.
    """
    if min_val is None or max_val is None:
        min_val, max_val = 0, 1

    tickvals = np.linspace(min_val, max_val, num=5)
    ticktext = [f'{int(val)}' for val in tickvals]

    fig.update_layout(
        font=dict(color='grey'),
        title=dict(font=dict(size=20)),
        xaxis=dict(
            title=dict(font=dict(size=15)),
            tickfont=dict(color='grey', size=12),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(font=dict(size=15)),
            tickfont=dict(color='grey', size=12),
            showgrid=False
        ),
        legend=dict(
            font=dict(color='grey', size=12)
        ),
        coloraxis=dict(
            colorbar=dict(
                title='Count',
                tickvals=tickvals,
                ticktext=ticktext,
                lenmode='fraction',
                len=0.8,
                outlinewidth=0,
                tickcolor='grey',
                tickfont=dict(color='grey')
            ),
            colorscale='Sunsetdark',
            cmin=min_val,
            cmax=max_val
        )
    )
    return fig


def create_yearly_incidents_figure(processed_data):
    """
    Creates a bar chart of incidents per year with a trend line.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    processed_data['Date'] = pd.to_datetime(processed_data['Date'])
    data_by_year = processed_data['Date'].dt.year.value_counts().sort_index()
    slope, intercept, r_value, p_value, std_err = linregress(data_by_year.index, data_by_year.values)
    line = slope * np.array(data_by_year.index) + intercept

    min_val = data_by_year.values.min()
    max_val = data_by_year.values.max()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_by_year.index,
        y=data_by_year.values,
        marker=dict(
            color=data_by_year.values,
            coloraxis="coloraxis"
        ),
        text=[f'{val / sum(data_by_year.values) * 100:.2f}%' for val in data_by_year.values],
        textposition='auto',
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=data_by_year.index,
        y=line,
        mode='lines',
        name='Trend Line',
        line=dict(color='red', width=3),
        showlegend=False
    ))

    fig.update_layout(
        title='Incidents Per Year',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Number of Incidents')
    )

    standardized_plot_layout(fig, min_val, max_val)
    return fig


def create_seasonal_distribution_figure(processed_data):
    """
    Creates a pie chart showing the seasonal distribution of crashes.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    data_by_season = processed_data['Season'].value_counts()

    fig = go.Figure(data=[
        go.Pie(
            labels=data_by_season.index,
            values=data_by_season.values,
            name='Seasonal Distribution',
            textinfo='percent+label',
            textfont=dict(size=15),
            marker=dict(colors=['#821E70', '#DB3878', '#EE6D6E', '#FCCF92'])
        )
    ])

    fig.update_layout(
        title='Seasonal Distribution of Crashes',
        showlegend=True
    )
    standardized_plot_layout(fig)
    return fig


def create_location_graph(processed_data):
    """
    Creates a choropleth map showing the global distribution of crashes.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    country_counts = processed_data['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']

    min_val = country_counts['Count'].min()
    max_val = country_counts['Count'].max()

    fig = px.choropleth(country_counts,
                        locations="Country",
                        locationmode='country names',
                        color="Count",
                        range_color=(min_val, max_val),
                        labels={'Count': 'Number of Crashes'},
                        title='Global Distribution of Crashes')
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        height=700
    )
    standardized_plot_layout(fig, min_val, max_val)
    return fig


def create_top_locations_figure(processed_data):
    """
    Creates a horizontal bar chart showing the top 10 crash locations.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    location_counts = processed_data['Country'].value_counts().sort_values(ascending=True).tail(10)
    total_counts = location_counts.sum()

    sunsetdark = plotly.colors.sequential.Sunsetdark

    def get_color(value, max_value):
        norm_value = value / max_value
        color_index = int(norm_value * (len(sunsetdark) - 1))
        return sunsetdark[color_index]

    max_count = location_counts.max()
    colors = [get_color(val, max_count) for val in location_counts.values]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=location_counts.values,
        y=location_counts.index,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{v} ({v / total_counts:.2%})' for v in location_counts.values],
        textposition='auto'
    ))

    fig.update_layout(
        title="Top 10 Crash Locations",
        xaxis=dict(title='Count'),
        yaxis=dict(type='category'),
    )

    standardized_plot_layout(fig)
    return fig


def create_most_crashes_by_destination_figure(processed_data):
    """
    Creates a horizontal bar chart showing the top 10 destinations with the most crashes.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    destination_counts = processed_data['Schedule'].value_counts().sort_values(ascending=True).tail(10)
    total_counts = destination_counts.sum()

    sunsetdark = plotly.colors.sequential.Sunsetdark

    def get_color(value, max_value):
        norm_value = value / max_value
        color_index = int(norm_value * (len(sunsetdark) - 1))
        return sunsetdark[color_index]

    colors = [get_color(val, destination_counts.max()) for val in destination_counts.values]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=destination_counts.values,
        y=destination_counts.index,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{v} ({v / total_counts:.2%})' for v in destination_counts.values],
        textposition='auto'
    ))

    fig.update_layout(
        title="Top 10 Destinations with Most Crashes",
        xaxis=dict(title='Number of Crashes'),
        yaxis=dict(type='category'),
        height=700
    )
    standardized_plot_layout(fig)
    return fig


def create_top_causes_figure(processed_data):
    """
    Creates a horizontal bar chart showing the top 5 crash causes.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    cause_counts = processed_data['Crash cause'].value_counts().sort_values(ascending=True).tail(5)
    total_causes = cause_counts.sum()

    sunsetdark = plotly.colors.sequential.Sunsetdark

    def get_color(value, max_value):
        norm_value = value / max_value
        color_index = int(norm_value * (len(sunsetdark) - 1))
        return sunsetdark[color_index]

    max_count = cause_counts.max()
    colors = [get_color(val, max_count) for val in cause_counts.values]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cause_counts.values,
        y=cause_counts.index,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{v} ({v / total_causes:.2%})' for v in cause_counts.values],
        textposition='auto'
    ))

    fig.update_layout(
        title="Top 5 Crash Causes",
        xaxis=dict(title='Count'),
        yaxis=dict(type='category')
    )
    standardized_plot_layout(fig)
    return fig


def create_casualties_by_cause_figure(processed_data):
    """
    Creates a horizontal bar chart showing the total casualties by crash cause.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    casualty_data = processed_data.groupby('Crash cause')['Total fatalities'].sum().sort_values(ascending=True).tail(5)
    total_fatalities = casualty_data.sum()

    sunsetdark = plotly.colors.sequential.Sunsetdark

    def get_color(value, max_value):
        norm_value = value / max_value
        color_index = int(norm_value * (len(sunsetdark) - 1))
        return sunsetdark[color_index]

    max_count = casualty_data.max()
    colors = [get_color(val, max_count) for val in casualty_data.values]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=casualty_data.values,
        y=casualty_data.index,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{v} ({v / total_fatalities:.2%})' for v in casualty_data.values],
        textposition='auto'
    ))

    fig.update_layout(
        title="Total Casualties by Crash Cause",
        xaxis=dict(title='Total Casualties'),
        yaxis=dict(type='category')
    )
    standardized_plot_layout(fig)
    return fig


def create_operator_figure(processed_data):
    """
    Creates a horizontal bar chart showing the top 10 incidents by operator.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    data_by_operator = processed_data['Operator'].value_counts().sort_values(ascending=True).tail(10)
    total_operator = data_by_operator.sum()

    sunsetdark = plotly.colors.sequential.Sunsetdark

    def get_color(value, max_value):
        norm_value = value / max_value
        color_index = int(norm_value * (len(sunsetdark) - 1))
        return sunsetdark[color_index]

    max_count = data_by_operator.max()
    colors = [get_color(val, max_count) for val in data_by_operator.values]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_by_operator.values,
        y=data_by_operator.index,
        orientation='h',
        text=[f'{v} ({v / total_operator:.2%})' for v in data_by_operator.values],
        textposition='auto',
        marker=dict(color=colors)
    ))

    fig.update_layout(
        title='Top 10 Incidents by Operator',
        xaxis=dict(title='Count'),
        yaxis=dict(title='Operator'),
        height=700
    )
    standardized_plot_layout(fig)
    return fig


def create_aircraft_figure(processed_data):
    """
    Creates a horizontal bar chart showing the top 10 incidents by aircraft type.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    data_by_aircraft = processed_data['Aircraft'].value_counts().sort_values(ascending=True).tail(10)
    total_aircraft = data_by_aircraft.sum()

    sunsetdark = plotly.colors.sequential.Sunsetdark

    def get_color(value, max_value):
        norm_value = value / max_value
        color_index = int(norm_value * (len(sunsetdark) - 1))
        return sunsetdark[color_index]

    max_count = data_by_aircraft.max()
    colors = [get_color(val, max_count) for val in data_by_aircraft.values]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_by_aircraft.values,
        y=data_by_aircraft.index,
        orientation='h',
        text=[f'{v} ({v / total_aircraft:.2%})' for v in data_by_aircraft.values],
        textposition='auto',
        marker=dict(color=colors)
    ))

    fig.update_layout(
        title='Top 10 Incidents by Aircraft',
        xaxis=dict(title='Count'),
        yaxis=dict(title='Aircraft'),
        height=700  # Increase height
    )
    standardized_plot_layout(fig)
    return fig


def create_survival_figure(processed_data):
    """
    Creates a stacked bar chart showing annual fatalities and total on board.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    processed_data['Date'] = pd.to_datetime(processed_data['Date'], errors='coerce')
    processed_data['Year'] = processed_data['Date'].dt.year
    yearly_data = processed_data.groupby('Year').agg({
        'Total fatalities': 'sum',
        'Total on board': 'sum'
    }).reset_index()

    sunsetdark = plotly.colors.sequential.Sunsetdark
    color1 = sunsetdark[2]
    color2 = sunsetdark[5]

    fig = go.Figure(data=[
        go.Bar(name='Total fatalities', x=yearly_data['Year'], y=yearly_data['Total fatalities'], marker_color=color1),
        go.Bar(name='Total on board', x=yearly_data['Year'], y=yearly_data['Total on board'], marker_color=color2)
    ])
    fig.update_layout(
        barmode='stack',
        title='Annual Fatalities',
        xaxis_title='Year',
        yaxis_title='Number of People',
        legend_title='Type',
        height=700
    )
    standardized_plot_layout(fig)
    return fig


def create_casualty_season_plots(processed_data):
    """
    Creates subplots showing casualties by top causes across seasons.

    Args:
        processed_data (pd.DataFrame): The processed data containing incidents information.

    Returns:
        go.Figure: The plotly figure object.
    """
    top_causes = processed_data['Crash cause'].value_counts().head(5).index.tolist()
    data_filtered = processed_data[processed_data['Crash cause'].isin(top_causes)]
    casualties_by_cause_season = data_filtered.groupby(['Crash cause', 'Season'])['Total fatalities'].sum().unstack(
        fill_value=0)
    data = casualties_by_cause_season
    max_casualties = data.max().max()

    fig = make_subplots(rows=1, cols=5, subplot_titles=data.index.tolist(), shared_yaxes=True)
    viridis = plotly.colors.sequential.Sunsetdark

    def get_color(value, max_value):
        norm_value = value / max_value
        color_index = int(norm_value * (len(viridis) - 1))
        return viridis[color_index]

    for i, cause in enumerate(data.index, 1):
        colors = [get_color(val, max_casualties) for val in data.loc[cause]]
        fig.add_trace(
            go.Bar(x=data.columns, y=data.loc[cause], name=cause, marker=dict(color=colors)),
            row=1, col=i
        )

    fig.update_layout(
        title_text="Casualties by Top Causes Across Seasons",
        showlegend=False,
        yaxis=dict(range=[0, max_casualties]),
        height=400
    )
    standardized_plot_layout(fig)
    return fig


def load_and_forecast():
    """
    Loads the ARIMA model and generates a forecast for the next 10 years.

    Returns:
        pd.Series: The forecasted values.
    """
    model_fit = joblib.load(load_data('crashes_predictor_model.pkl'))
    if not hasattr(model_fit, 'get_forecast'):
        raise AttributeError("Loaded model is not a valid ARIMA model instance.")

    forecast_result = model_fit.get_forecast(steps=10)
    forecast = forecast_result.predicted_mean
    return forecast


def create_forecast_chart():
    """
    Creates a line chart showing the forecast of total crashes over the next 10 years.

    Returns:
        go.Figure: The plotly figure object.
    """
    forecast = load_and_forecast()
    forecast_index = pd.date_range(start=forecast.index[0], periods=len(forecast), freq='YE-DEC')
    error = forecast * 0.10
    sunsetdark = plotly.colors.sequential.Sunsetdark
    color = sunsetdark[4]

    prediction_trace_with_error = go.Scatter(
        x=forecast_index,
        y=forecast.values,
        error_y=dict(
            type='data',
            symmetric=True,
            array=error.values,
            visible=True
        ),
        mode='lines+markers+text',
        name='Predicted Crashes',
        line=dict(color=color),
        text=[f'{v:.0f}' for v in forecast.values],
        textposition='top right'
    )

    layout = go.Layout(
        title='Forecast of Total Crashes Over the Next 10 Years',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Number of Crashes', range=[20, max(forecast.values) * 1.5]),
        hovermode='closest'
    )

    fig = go.Figure(data=[prediction_trace_with_error], layout=layout)
    standardized_plot_layout(fig)
    return fig
