import MySQLdb
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='Socrates315', api_key='qb1ZvuyQPjQAMFr7Cg08')


#Sets up MySQL connection and reads from table.
conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="TestPiPlanter_DB")
cursor = conn.cursor()
cursor.execute('SELECT Sample_Number, Time, soil_water FROM DailyTable')
rows = cursor.fetchall()


#Sets up panda DataFrame Object
df = pd.DataFrame([[ij for ij in i] for i in rows])
df.rename(columns={0:'Sample_Number', 1: 'Time', 2: 'soil_water'})


#Makes Trace (dataset) #1. Should be only one needed
trace1 = go.Scatter(
    x=df[0],
    y=df[2],
    mode='lines'
    )

#Sets Axies titles
layout= dict(
    title = 'Water level in Soil over time',
    xaxis = dict(title='Sample Number'),
    yaxis = dict(title='Water level')
    )

#Graphs
data = [trace1]
fig = dict(data=data, layout=layout)
py.plot(fig, filename='Water levels over time')




