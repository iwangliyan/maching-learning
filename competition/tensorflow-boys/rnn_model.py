import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import json
import datetime


HIDDEN_SIZE = 30
NUM_LAYERS = 2
TIMESTEPS = 66
TRAINING_STEPS = 20000
BATCH_SIZE = 32


def lstm_model(X, y, is_training):
    cell = tf.nn.rnn_cell.MultiRNNCell([
        tf.nn.rnn_cell.BasicLSTMCell(HIDDEN_SIZE)
        for _ in range(NUM_LAYERS)])
    outputs, _ = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
    # output = outputs[:, -1, 1：16]
    output = outputs[:, -1, :]
    predictions = tf.contrib.layers.fully_connected(
        output, 1, activation_fn=None)
    if not is_training:
        return predictions, None, None
    loss = tf.losses.mean_squared_error(labels=y, predictions=predictions)
    train_op = tf.contrib.layers.optimize_loss(
        loss, tf.train.get_global_step(),
        optimizer="Adagrad", learning_rate=0.1)
    return predictions, loss, train_op


def run_eval(sess, test_X, test_y):
    ds = tf.data.Dataset.from_tensor_slices((test_X, test_y))
    ds = ds.batch(1)
    X, y = ds.make_one_shot_iterator().get_next()
    with tf.variable_scope("model", reuse=True):
        prediction, _, _ = lstm_model(X, [0.0], False)
    predictions = []
    labels = []
    for i in range(len(test_y)):
        p, l = sess.run([prediction, y])
        predictions.append(p)
        labels.append(l)
    predictions = np.array(predictions).squeeze()
    labels = np.array(labels).squeeze()
    rmse = np.sqrt(((predictions - labels) ** 2).mean(axis=0))
    print("Root Mean Square Error is: %f" % rmse)
    plt.figure()
    plt.scatter(predictions[1], labels[1], color='r', s=20)
    plt.show()

fid = open("data/trains.json")
data_raw = json.load(fid)
fid.close()
start_time = datetime.datetime.strptime("2017-10-17", "%Y-%m-%d")
feats_raw = []
labs = []
for data in data_raw:
    data_time = datetime.datetime.strptime(data["date"], "%Y-%m-%d:%H")
    if data_time > start_time:
        feats_raw.append([data["holiday"], data["week"]-1, data["place"]-1, data_time.hour])
        labs.append(data["people"])

from sklearn import preprocessing
ohcoder = preprocessing.OneHotEncoder()
ohcoder.fit(feats_raw)
print(ohcoder.n_values_)
feats = ohcoder.transform(feats_raw).toarray()

from sklearn.model_selection import train_test_split
train_feats, val_feats, train_labs, val_labs = train_test_split(feats, labs, test_size = 0.2, random_state = 0)

train_labs = np.reshape(np.array(train_labs),[-1,1]).astype("float32")
val_labs = np.reshape(np.array(val_labs),[-1,1]).astype("float32")
train_feats = np.reshape(train_feats,[22101, 1,66]).astype("float32")
val_feats = np.reshape(val_feats,[-1, 1,66]).astype("float32")

CUDA_VISIBLE_DEVICE = 5
ds = tf.data.Dataset.from_tensor_slices((train_feats, train_labs))
ds = ds.repeat().shuffle(50).batch(BATCH_SIZE)
X, y = ds.make_one_shot_iterator().get_next()

with tf.variable_scope("model"):
    _, loss, train_op = lstm_model(X, y, True)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for i in range(TRAINING_STEPS):
        _, l = sess.run([train_op, loss])
        if i % 1000 == 0:
            print("train step: " + str(i) + ", loss: " + str(l))

    print("Evaluate model after training.")
    run_eval(sess, val_feats, val_labs)




