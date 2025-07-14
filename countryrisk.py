import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------------------------

"""
Country-specific risk is a key factor in both corporate finance and investment decisions.
Large firms operating globally must assess the financial and political stability of 
target countries to evaluate project risks. Differences in country risk can also create 
short-term speculation opportunities, often monitored by macro funds.

Country risk includes macroeconomic, political, and socio-cultural factors. While 
macroeconomic indicators are easier to quantify, political and socio-cultural risks 
remain challenging to measure. In this project, I used a K-Nearest Neighbors (KNN) 
algorithm (https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) to classify 
countries based on macroeconomic indicators. The data, sourced from FactSet, covers 
the world’s top 30 economies.

With access to richer (though typically paid) databases like:
https://www.quandl.com/data/SGE-Trading-Economics,
the model can be expanded and updated dynamically. It can also be trained with broader 
datasets and enhanced by incorporating political and social developments via news APIs.
"""
# ##Define and train the model
train_df=pd.read_excel('train.xlsx', skiprows=(0,1,2,3,4,5,7),skipfooter=3,index_col=0,na_values='-')
train_df=train_df.drop(labels=['World Total','Developed Countries','Emerging Countries','United Arab Emirates'],axis=0)
train_df = train_df.dropna(axis=1, how='all').replace(np.nan, 0)
train_df['Risk_Category']=['Low','Low','Low','Low','Low','Low','Low','Low','Low','Satisfactory','Satisfactory','Low','Reasonable'
                            ,'Low','Very_Low','Very_Low','Low','Very_Low','Low','Very_Low','Low','Low','Low','Very_Low','Satisfactory'
                            ,'Low','Fairly_High','Satisfactory','Fairly_High','Reasonable','Satisfactory','Fairly_High','Fairly_High',
                            'Satisfactory','Fairly_High','Reasonable','Satisfactory','Fairly_High','Reasonable','Reasonable','Reasonable',
                            'Satisfactory','Fairly_High','Fairly_High','Low','Reasonable','High']
IV=train_df.drop(columns=['Risk_Category'])
DV=train_df['Risk_Category']
KNN_model=KNeighborsClassifier(n_neighbors=6)
KNN_model.fit(IV, DV)

##importing and cleaning datasets


#-----------------------------------------------------------------------------------

option_selected=st.selectbox('Select the Quarter',[
    'Q4_2018',
    'Q1_2019',
    'Q2_2019',
    'Q3_2019',
    'Q4_2019',
    'Q1_2020',
    'Q2_2020',
    'Q3_2020'])

@st.cache(persist=True)

def country_risk(option_selected):

    dff = option_selected+'.xlsx'
    data=pd.read_excel(dff, skiprows=(0,1,2,3,4,5,7),skipfooter=3,index_col=0,na_values='-')
    data=data.drop(labels=['World Total','Developed Countries','Emerging Countries','United Arab Emirates'],axis=0)
    data = data.dropna(axis=1, how='all').replace(np.nan, 0)
    knn1=KNN_model.predict(data)
    data['Risk_Category']=knn1

    return data
data=country_risk(option_selected)

fig = px.choropleth(
        data_frame=data,
        locations=data.index,
        locationmode='country names',
        color='Risk_Category',
        hover_data=['Govt Budg Bal', 'Unemployment Rate',
        'Real GDP', 'CPI','FX Reserves'],
        width=1200, height=1000,
         color_discrete_map={

            "High": "red",
            "Fairly_High": "darkorange",
            "Reasonable": "orange",
            "Satisfactory": "yellow",
            "Low": "yellowgreen",
            "Very_Low": "green"},
        category_orders={"Default Risk": ["Very_Low"
                                           "Low",
                                          "Satisfactory",
                                          "Reasonable",
                                          "Fairly High",
                                          "High"
                                          ]},

        )
fig.update_geos(
        visible=False,showcountries=True)
st.plotly_chart(fig)
