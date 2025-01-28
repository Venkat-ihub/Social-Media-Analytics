import pandas as pd
import json

def charts(chart, metric):
    def load_data():
        # Load the CSV data
        data = pd.read_csv("social_media_metrics.csv")
        return data

    data = load_data()

    platforms = data['Platform'].tolist()

    # Check if the selected chart is 'pie'
    if chart == 'pie':
        # Pie chart data requires each slice to have a 'name' (platform) and 'y' (value)
        series_data = [{
            'name': 'Platforms',
            'colorByPoint': True,
            'data': [{'name': platforms[i], 'y': data[metric].tolist()[i]} for i in range(len(platforms))]
        }]
    else:
        # Bar or column chart structure
        series_data = [{
            'name': metric,
            'data': data[metric].tolist()
        }]

    # Chart data structure with platform names for the x-axis (for non-pie charts)
    chart_data = {
        'chart': {'type': chart},
        'title': {'text': 'Comparison of Social Media Metrics'},
        'series': series_data
    }

    # Add x-axis for bar and column charts only
    if chart != 'pie':
        chart_data['xAxis'] = {
            'categories': platforms,
            'title': {'text': 'Platforms'}
        }
        chart_data['yAxis'] = {
            'title': {'text': 'Values'}
        }

    # Convert chart data to JSON format
    chart_data_json = json.dumps(chart_data)

    # Highcharts HTML template with the JSON data
    highcharts_html = f"""
    <div id="container" style="height: 400px; width: 100%;"></div>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {{
            Highcharts.chart('container', {chart_data_json});
        }});
    </script>
    """
    return highcharts_html
