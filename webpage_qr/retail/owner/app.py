import pandas as pd
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Create a Flask app
app = dash.Dash(__name__)

# Load your DataFrame (df) or create a sample DataFrame
df = pd.DataFrame(...)  # Replace with your data

app.layout = html.Div([
    dcc.Graph(id='histogram'),
])

@app.callback(
    Output('histogram', 'figure'),
    Input('histogram', 'relayoutData')
)
def update_histogram(relayoutData):
    lw =  # Define your threshold values
    diss =  # Define your threshold values
    up =  # Define your threshold values
    new_prediction =  # Define your prediction value

    fig = plt.figure(figsize=(8, 6))
    plt.hist(df['sales'], bins=200)
    plt.axvline(x=lw, color='r', linestyle='dashed', linewidth=2, label="(re)move threshold)")
    plt.axvline(x=diss, color='m', linestyle='dashed', linewidth=2, label="discount recommendation")
    plt.axvline(x=up, color='g', linestyle='dashed', linewidth=2, label="recommend to keep")
    plt.axvline(x=new_prediction, color='y', linestyle='solid', linewidth=2)
    plt.legend(loc='upper right')

    return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)
