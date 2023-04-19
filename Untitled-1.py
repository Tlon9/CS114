from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
col_name = ['space', 'second']
df = pd.read_csv("http://cs.uit.edu.vn/data.txt", sep = ",", header=None, names = col_name)
df_test = pd.read_csv("http://cs.uit.edu.vn/data3.txt", sep = ",", header = None, names=col_name)
x = df.space
y = df.second
x = x.to_numpy()
x = x.reshape(-1,1)
#y = y.to_numpy()
plt.scatter(x,y)
x_test = df_test.space
y_test = df_test.second
x_test = x_test.to_numpy()
x_test = x_test.reshape(-1,1)
plt.scatter(x_test,y_test)
'''x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.3, random_state=1)
plt.scatter(x_test,y_test)'''
lr = LinearRegression()
lr.fit(x, y)
y_ = lr.predict(x_test)
plt.plot(x_test, y_)
plt.show()
loss = 0
'''index_array = [i for i in range(len(x_test))]
y_test.index = index_array'''
#y_test = y_test.to_numpy()
#print(y_test)
'''for i in range(len(x_test)):
    loss += (y_[i] - y_test[i])**2
loss = loss/ (len(y_test)*2)
print(loss)'''
print(mean_squared_error(y_test, y_))
plt.show()



