#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install plotly ')
get_ipython().system('pip install dash ')
get_ipython().system('pip install dash_bootstrap_components ')


# In[2]:


get_ipython().system('pip install pandas_datareader ')


# In[3]:


import pandas as pd 
import dash 
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas_datareader.data as web 
import datetime
import plotly.express as px


# In[4]:


# DATA READER IS USED TO ACCESS API OF STOOQ 
#POTBELLY,STARBUCKS,CHIPOTLE,WENDYS,PAPA JOHN'S,DOMINOS
start = datetime.datetime(2021,1,1)
end = datetime.datetime(2021,6,1)
df= web.DataReader(['PBPB','SBUX','CMG','WEN','PIZZA','DPZ'],'stooq', start=start,end = end)
df=df.stack().reset_index()
print(df[:15])


# In[5]:


# in order not to access API everytime , we saved it into CSV on my desktop
df.to_csv("mystockss.csv",index=False)


# In[6]:


df=pd.read_csv("C:/Users/User/Desktop/mystockss.csv")
df.head()


# In[7]:


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
               meta_tags=[{'name':'viewport',
                         'content':'width=device-width,initial-scale=1.0'}])


# In[8]:




app.layout = dbc.Container([
    dbc.Row([
   dbc.Col(html.H1(" RESTAURANTS Stock Market Dashboard",className="text-center text-primary,mb-7"), width=12)
    ]),
    
    
    dbc.Row([
   dbc.Col([
       html.H3("High Daily stocks rates"),
       dcc.Dropdown(id='my-dpdn',multi=False,value='PBPB',
                   options=[{'label':x,'value':x}
                           for x in sorted(df['Symbols'].unique())]),
       dcc.Graph(id='line-fig',figure={})
   ], width={'size':6}),
   
   dbc.Col([
       html.H3("Opening stocks rates"),
       dcc.Dropdown(id='my-dpdn2',multi=True,value=['SBUX','CMG'],
                   options=[{'label':x, 'value':x}
                   for x in sorted(df['Symbols'].unique())]),
       dcc.Graph(id='line-fig2',figure={})
   ], width={'size':6})
    ], no_gutters=False),
    
    
    dbc.Row([
   dbc.Col([
       html.H3("Closing stocks rate per day"),
       html.P("Select Restaurant Stock:", style={'textDecoration':'underline'}),
       dcc.Checklist(id='my-checklist',value=['WEN','DPZ','PIZZA'], 
                    options=[{'label':x,'value':x}
                            for x in sorted(df['Symbols'].unique())],
       labelClassName='mr-3 text-success'),
       dcc.Graph(id='my-hist',figure={})
   ], width={'size':6}),
   
   dbc.Col([
       html.H3("Stocks rate volume"),
       dcc.Dropdown(id='my-pie',multi=False,value='PBPB',
                   options=[{'label':x,'value':x}
                           for x in sorted(df['Symbols'].unique())]),
       dcc.Graph(id='pie-chart',figure={})
   ],width={'size':6})
    ])
    
])

# line chart single - call back 
@app.callback(
    Output('line-fig','figure'),
    Input('my-dpdn','value')
)

def update_graph(stock_slctd):
    dff=df[df['Symbols']==stock_slctd]
    figln=px.line(dff,x='level_0',y='High')
    return figln

# line chart - multiple
@app.callback(
    Output('line-fig2','figure'),
    Input('my-dpdn2','value')
)

def update_graph(stock_slctd):
    dff=df[df['Symbols'].isin(stock_slctd)]
    figln2=px.line(dff,x='level_0',y='Open',color='Symbols')
    return figln2


# histogram
@app.callback(
    Output('my-hist','figure'),
    Input('my-checklist','value')
)

def update_graph(stock_slctd):
    dff=df[df['Symbols'].isin(stock_slctd)]
    dff=dff[dff['level_0']=='04/01/2021']
    fighist=px.histogram(dff,x='Symbols',y='Close')
    return fighist

# pie chart 
@app.callback(
    Output('pie-chart','figure'),
    Input('my-pie','value')
)

def update_graph(stock_slctd):
    dff=df
    piechart=px.pie(dff,names='Symbols',values='Volume')
    return piechart


# In[ ]:


app.run_server(host ='0.0.0.0', debug=False)


# In[ ]:





# In[ ]:




