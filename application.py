import pandas as pd
from geopy.geocoders import Nominatim
import plotly.express as px
import plotly.graph_objects as go
data=pd.read_csv('data/dwb.csv')[0:50]

names=data['Country/Territory'].tolist()


Latitude=[]
Longitude=[]
geolocator = Nominatim(user_agent="worldgeo")
for i in enumerate(names):
    location = geolocator.geocode(i)
    me = location.latitude
    ne = location.longitude
    
    Latitude.append(me)
    Longitude.append(ne)
    


riski=[]

for i in data['rate']:
    if i >= 50:
        riski.append('Extreme')
    elif 40<=i<=50:
        riski.append('Very High')
    elif 30<=i<=40:
        riski.append('High')
    elif 20<=i<=30:
        riski.append('Medium')
    elif 10<=i<=20:
        riski.append('Low')
    elif 0<=i<=10:
        riski.append('Very Low')
        
        
        
data=pd.DataFrame({'Country':data['Country/Territory'],'GDP in Million $':data['GDP(US$million)'],
                   'Risk':data['rate'],'Risk Category':riski,'Latitude':Latitude,'Longitude':Longitude})

data['Risk'] = data['Risk']*(-1)

fig = px.choropleth(locations=data['Country'],
                    hover_name=data['Risk Category'],
                    locationmode="country names",
                    color=data['Risk'],
                    color_continuous_scale=px.colors.diverging.RdYlGn)


fig.update_layout(legend_title_text='uhi',
                  legend=dict(
    orientation="h",
    yanchor="bottom",
 
    y=0.99,
    xanchor="left",
  
    x=1),
    title_text='Risk of Defualt for Top 50 Economies of the World 2020',
    geo=dict(
        
        showframe=False,
        showcoastlines=False,
        
        projection_type='equirectangular'
    )
)

fig.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="RebeccaPurple"
)


fig.show()
