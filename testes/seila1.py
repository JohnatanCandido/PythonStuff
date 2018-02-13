from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix

cancer = load_breast_cancer()
cancer.keys()

X = cancer['data']
y = cancer['target']

X_train, X_test, y_train, y_test = train_test_split(X, y)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

mlp = MLPClassifier(hidden_layer_sizes=(40, 50, 60))
mlp.fit(X_train, y_train)

prediction = mlp.predict(X_test)

print(confusion_matrix(y_test, prediction))
print('----------------------------------------------------------------')
print(classification_report(y_test, prediction))
