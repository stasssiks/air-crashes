import os
import sys
import pandas as pd
import pytest
import threading
import time
import requests
from flask import Flask
from plotly.graph_objs import Figure

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import dash_app

from pages.analysis import (
    create_yearly_incidents_figure,
    create_seasonal_distribution_figure,
    create_location_graph,
    create_top_locations_figure,
    create_most_crashes_by_destination_figure,
    create_top_causes_figure,
    create_casualties_by_cause_figure,
    create_operator_figure,
    create_aircraft_figure,
    create_survival_figure,
    create_casualty_season_plots,
    create_forecast_chart,
    load_data
)

flask_app = Flask(__name__)


@pytest.fixture(scope='module')
def start_dash_app():
    """Start the Dash app in a separate thread."""
    app_thread = threading.Thread(target=dash_app.run_server, kwargs={'debug': False, 'use_reloader': False})
    app_thread.start()
    time.sleep(2)

    yield dash_app

    # Ensure proper shutdown
    try:
        response = requests.post('http://127.0.0.1:8050/_shutdown')
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error during shutdown: {e}")

    app_thread.join(timeout=10)
    if app_thread.is_alive():
        print("Thread did not finish, forcing exit.")
        os._exit(1)


def test_dash_app(start_dash_app):
    """Test if the Dash app is running."""
    response = requests.get('http://127.0.0.1:8050')
    assert response.status_code == 200


def test_home_page(start_dash_app):
    """Test if the Home page is running."""
    response = requests.get('http://127.0.0.1:8050/')
    assert response.status_code == 200


def test_hypothesis_page(start_dash_app):
    """Test if the Hypothesis page is running."""
    response = requests.get('http://127.0.0.1:8050/about')
    assert response.status_code == 200


def test_analysis_page(start_dash_app):
    """Test if the Analysis page is running."""
    response = requests.get('http://127.0.0.1:8050/analysis')
    assert response.status_code == 200


def test_conclusion_page(start_dash_app):
    """Test if the Conclusion page is running."""
    response = requests.get('http://127.0.0.1:8050/conclusion')
    assert response.status_code == 200


def test_initial_data_page(start_dash_app):
    """Test if the Initial Data page is running."""
    response = requests.get('http://127.0.0.1:8050/data')
    assert response.status_code == 200


def load_data(filename):
    """Load CSV data from the specified file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, '..', 'src', 'data'))
    file_path = os.path.join(parent_dir, filename)
    return pd.read_csv(file_path)


def test_load_data_raw():
    """Test loading of raw data."""
    data = load_data('crashes-raw.csv')
    assert data.shape == (28536, 24), "Raw data shape mismatch"
    assert not data.empty, "Data should not be empty"


def test_load_data_processed():
    """Test loading of processed data."""
    data = load_data('crashes-processed.csv')
    assert not data.empty, "Data should not be empty"
    assert data.shape == (28536, 11), "Processed data shape mismatch"


def test_export_csv(start_dash_app):
    """Test clicking the export CSV button."""
    response = requests.post('http://127.0.0.1:8050/_dash-update-component', json={
        'output': 'download-csv.data',
        'inputs': [
            {'id': 'export-csv-button', 'property': 'n_clicks'}
        ],
        'state': [
            {'id': 'raw-button', 'property': 'n_clicks_timestamp'},
            {'id': 'processed-button', 'property': 'n_clicks_timestamp'}
        ],
        'changedPropIds': ['export-csv-button.n_clicks']
    })
    assert os.path.exists(os.path.join(os.path.expanduser('~'), 'Downloads', 'exported_data.csv'))


def test_export_pdf(start_dash_app):
    """Test clicking the export PDF button."""
    # Simulate clicking the export PDF button
    response = requests.post('http://127.0.0.1:8050/_dash-update-component', json={
        'output': 'download-pdf.data',
        'inputs': [
            {'id': 'export-pdf-button', 'property': 'n_clicks'}
        ],
        'state': [
            {'id': 'raw-button', 'property': 'n_clicks_timestamp'},
            {'id': 'processed-button', 'property': 'n_clicks_timestamp'}
        ],
        'changedPropIds': ['export-pdf-button.n_clicks']
    })
    assert os.path.exists(os.path.join(os.path.expanduser('~'), 'Downloads', 'exported_data.pdf'))


def test_create_yearly_incidents_figure():
    data = load_data('crashes-processed.csv')
    fig = create_yearly_incidents_figure(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_seasonal_distribution_figure():
    data = load_data('crashes-processed.csv')
    fig = create_seasonal_distribution_figure(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_location_graph():
    data = load_data('crashes-processed.csv')
    fig = create_location_graph(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_top_locations_figure():
    data = load_data('crashes-processed.csv')
    fig = create_top_locations_figure(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_most_crashes_by_destination_figure():
    data = load_data('crashes-processed.csv')
    fig = create_most_crashes_by_destination_figure(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_top_causes_figure():
    data = load_data('crashes-processed.csv')
    fig = create_top_causes_figure(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_casualties_by_cause_figure():
    data = load_data('crashes-processed.csv')
    fig = create_casualties_by_cause_figure(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_operator_figure():
    data = load_data('crashes-processed.csv')
    fig = create_operator_figure(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_aircraft_figure():
    data = load_data('crashes-processed.csv')
    fig = create_aircraft_figure(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_survival_figure():
    data = load_data('crashes-processed.csv')
    fig = create_survival_figure(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()


def test_create_casualty_season_plots():
    data = load_data('crashes-processed.csv')
    fig = create_casualty_season_plots(data)
    assert isinstance(fig, Figure)
    assert 'data' in fig.to_plotly_json()
