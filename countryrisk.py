import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------------------------
# ##Define and train the model
train_df=pd.read_excel('data/train.xlsx', skiprows=(0,1,2,3,4,5,7),skipfooter=3,index_col=0,na_values='-')
train_df=train_df.drop(labels=['World Total','Developed Countries','Emerging Countries','United Arab Emirates'],axis=0)
train_df=train_df.dropna(1,how='all').replace(np.nan, 0)
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
    data=pd.read_excel(data/dff, skiprows=(0,1,2,3,4,5,7),skipfooter=3,index_col=0,na_values='-')
    data=data.drop(labels=['World Total','Developed Countries','Emerging Countries','United Arab Emirates'],axis=0)
    data=data.dropna(1,how='all').replace(np.nan, 0)
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
