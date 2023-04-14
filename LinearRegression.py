from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pandas as pd
import numpy as np 
#Read data
csv_url = "http://cs.uit.edu.vn/data.txt"
test_url = "http://cs.uit.edu.vn/data3.txt"
col_name = ['Space','Time']
df = pd.read_csv(csv_url, sep = ",", header=None,names=col_name)
df_test = pd.read_csv(test_url, sep = ",", header=None,names = col_name)
#Change 1D to 2D
x = np.array(df.Space)
y = np.array(df.Time)
x = x.reshape(-1,1)
#y = y.reshape(-1,1)

x_test = np.array(df_test.Space)
x_test = x_test.reshape(-1,1)
y_test = np.array(df_test.Time)
#y_test = y_test.reshape(-1,1)

#Training and test
lr = LinearRegression()
lr = lr.fit(x, y)
y_pred = lr.predict(x_test)
loss = 0
for i in range(len(x_test)):
    loss += (y_pred[i] - y_test[i])**2
loss = loss/ 2*(len(y_test))
print(loss)

