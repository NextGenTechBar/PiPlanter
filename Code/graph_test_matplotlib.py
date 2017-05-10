import MySQLdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



print("hello wlrd")
#Sets up MySQL connection and reads from table.
conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="TestPiPlanter_DB")
#cursor = conn.cursor()
query = 'SELECT Sample_Number, Time, soil_water FROM DailyTable'
#cursor.execute(query)
#rows = cursor.fetchall()



df = pd.read_sql(query, conn, index_col=['soil_water'])
fig, ax = plt.subplots()
df.plot(ax=ax)
plt.show()

#Closes connections
#cursor.close()
conn.close()



'''
#Sets up panda DataFrame Object
df = pd.DataFrame([[ij for ij in i] for i in rows])
df.rename(columns={0:'Sample_Number', 1: 'Time', 2: 'soil_water'})

my_plot = df.plot(kind="bar")
'''
print("hello wlrd")
