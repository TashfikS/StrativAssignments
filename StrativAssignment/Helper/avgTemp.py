import pandas as pd

def getAvgTemp(values):
    
    filtered_df = values[values['date'].dt.strftime('%H:%M:%S') == '14:00:00']
    if not filtered_df.empty:
        average_temperature = filtered_df['temperature_2m'].mean()
        return average_temperature
    else:
        print("No data available at 14:00:00")
        return None
