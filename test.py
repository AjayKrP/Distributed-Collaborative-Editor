import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report


data = pd.read_csv('trip.csv')

# pre-processing steps
data = data.dropna()


data = data.drop(['Start date', 'End date'], axis=1)
columns = data.columns

le = LabelEncoder()
for i in range(len(columns)):
    data[columns[i]] = le.fit_transform(data[columns[i]])

X = data.drop(['Member type'], axis=1)
y = data['Member type']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

knn = KNeighborsClassifier(n_neighbors=20)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)
accuracy = 100 * round(accuracy_score(y_test, pred), 3)
print('Accuracy of the Model is: {}'.format(accuracy))
print(classification_report(y_test, pred))

