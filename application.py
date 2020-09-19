import plotly
import plotly.express as px
import pandas as pd



data=pd.read_csv('data/data.csv',index_col=0,na_values='-')
#df = data.iloc[:,1:-1]
#df1 = data.iloc[:,-1:].fillna(0)

data.fillna(method='ffill',inplace=True)

fig = px.choropleth(
            data_frame=data,
            locations='Country/Territory',
            locationmode='country names',
            color='Default Risk',
            title="COUNTRY RISK ASSESSMENT",
            hover_data=['GDP(US$million)', 'Unemployment',
            'Real GDP(% Growth)', 'Interest Rate(%)'],
             color_discrete_map={
                "Extreme": "maroon",
                "Very High": "orangered",
                "High": "darkorange",
                "Fairly High": "orange",
                "Reasonable": "yellow",
                "Satisfactory": "yellowgreen",
                "Low": "green"},
            
            )

fig.update_layout(legend_title="Default Risk")

fig.show()
