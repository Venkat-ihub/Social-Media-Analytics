from pyfacebook import GraphAPI
import pandas as pd

# Function to convert JSON insights to a DataFrame and save as CSV
def json_to_table(json_input, output_file):
    # Ensure 'insights' and 'data' exist in JSON
    if 'insights' in json_input and 'data' in json_input['insights']:
        insights_data = json_input['insights']['data']

        # Prepare rows for DataFrame
        rows = []
        for metric in insights_data:
            metric_name = metric.get('title', metric['name'])  # Fallback to 'name'
            period = metric['period']

            # Extract values for each metric period
            for value in metric['values']:
                end_time = value.get('end_time', 'N/A')
                row = {
                    'Metric': metric_name,
                    'Period': period,
                    'Value': value['value'],
                    'End Time': end_time
                }
                rows.append(row)

        # Create DataFrame from rows
        df = pd.DataFrame(rows)

        # Save DataFrame to CSV without index
        df.to_csv(output_file, index=False)
        print(f"Table saved to {output_file}")
    else:
        print("No insights data found in the JSON.")

# Initialize the API with your access token
api = GraphAPI(access_token="EAAkIrqqRsBIBOZCD0qXYCGwfZB8NMZARPqFjDVwog2sihZCTFW0liZAJUKUXCYrBXAL12ZAWQ0frZBzeFZAa2Xh9qcFAsUFZCZAmYcDlwDoWuX0c1y3zv1ay2SpmJE59NHG5PMN7uJV8OAH7atILhLSW4XZB3pb65EYjuNLV2hIKSSK9cj49UZC3yPM6Xt7wNir1hlgZD")

# Fetch page ID and insights
page_id = "110454791874065"
try:
    facebook_page_info = api.get_object(object_id=page_id)  # Fetch page info
    print(f"Page Info: {facebook_page_info}")

    # Fetch insights data
    metrics = "page_preview_total"
    insights = api.get_object(object_id=page_id, fields=f"insights.metric({metrics})")
    print(f"Insights: {insights}")

    # Convert JSON to table and save as CSV
    json_to_table(insights, "facebook_insights.csv")

except Exception as e:
    print(f"Error: {e}")
