import numpy as np
import tflearn

# download titanic set
from tflearn.datasets import titanic

# titanic.download_dataset()

# Load CSV file, indicate that the first column represents labels
from tflearn.data_utils import load_csv

data, labels = load_csv('titanic_dataset.csv', target_column=0,
                        categorical_labels=True, n_classes=2)


# Pre processing function
def preprocess(passengers, columns_to_delete):
    # Sort by descending id and delete columns
    for column_to_delete in sorted(columns_to_delete, reverse=True):
        [passenger.pop(column_to_delete) for passenger in passengers]
    for i in range(len(passengers)):
        # Converting 'sex' field to float (id is 1 after removing labels column)
        passengers[i][1] = 1. if passengers[i][1] == 'female' else 0.
    return np.array(passengers, dtype=np.float32)


# Ignore 'name' and 'ticket' columns (id 1 & 6 of data array)
to_ignore = [1, 6]

# Pre process data
data = preprocess(data, to_ignore)

# build the neural network
net = tflearn.input_data(shape=[None, 6])
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 32)
net = tflearn.fully_connected(net, 2, activation='softmax')
net - tflearn.regression(net)

# define the model
model = tflearn.DNN(net)
# start training
model.fit(data, labels, n_epoch=10, batch_size=16)

# prediction
dicaprio = [3, 'Jack Dawson', 'male', 19, 0, 0, 'N/A', 5.0000]
winslet = [1, 'Rose DeWitt Bukater', 'female', 17, 1, 2, 'N/A', 100.0000]

# Preprocess data
dicaprio, winslet = preprocess([dicaprio, winslet], to_ignore)

# Predict surviving chances (class 1 results)
pred = model.predict([dicaprio, winslet])
print("DiCaprio Surviving Rate:", pred[0][1])
print("Winslet Surviving Rate:", pred[1][1])

devon = [3, 'Devon Martin', 'male', 22, 0, 0, 'N/A', 20.]
devon = preprocess([devon], to_ignore)
pred = model.predict(devon)
print("My Surviving Rate:", pred[0][1])
