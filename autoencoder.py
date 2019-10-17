import tensorflow as tf


class Autoencoder(object):
    def __init__(self, inout_dim, encoded_dim):
        learning_rate = 0.001

        # Weights and biases
        hidden_layer_weights = tf.Variable(tf.random_normal([inout_dim, encoded_dim*100]))
        hidden_layer_biases = tf.Variable(tf.random_normal([encoded_dim*100]))
        hidden2_layer_weights = tf.Variable(tf.random_normal([encoded_dim*100, encoded_dim*10]))
        hidden2_layer_biases = tf.Variable(tf.random_normal([encoded_dim*10]))
        hidden3_layer_weights = tf.Variable(tf.random_normal([encoded_dim * 10, encoded_dim]))
        hidden3_layer_biases = tf.Variable(tf.random_normal([encoded_dim]))
        output3_layer_weights = tf.Variable(tf.random_normal([encoded_dim, encoded_dim * 10]))
        output3_layer_biases = tf.Variable(tf.random_normal([encoded_dim * 10]))
        output2_layer_weights = tf.Variable(tf.random_normal([encoded_dim*10, encoded_dim*100]))
        output2_layer_biases = tf.Variable(tf.random_normal([encoded_dim*100]))
        output_layer_weights = tf.Variable(tf.random_normal([encoded_dim*100, inout_dim]))
        output_layer_biases = tf.Variable(tf.random_normal([inout_dim]))

        # Neural network
        self._input_layer = tf.placeholder('float', [None, inout_dim])
        self._hidden_layer = tf.nn.sigmoid(tf.add(tf.matmul(self._input_layer, hidden_layer_weights), hidden_layer_biases))
        self._hidden2_layer = tf.nn.sigmoid(tf.add(tf.matmul(self._hidden_layer, hidden2_layer_weights), hidden2_layer_biases))
        self._hidden3_layer = tf.nn.sigmoid(tf.add(tf.matmul(self._hidden2_layer, hidden3_layer_weights), hidden3_layer_biases))
        self._output3_layer = tf.nn.sigmoid(tf.add(tf.matmul(self._hidden3_layer, output3_layer_weights), output3_layer_biases))
        self._output2_layer = tf.nn.sigmoid(tf.add(tf.matmul(self._output3_layer, output2_layer_weights), output2_layer_biases))
        self._output_layer = tf.add(tf.matmul(self._hidden_layer, output_layer_weights), output_layer_biases)
        self._real_output = tf.placeholder('float', [None, inout_dim])

        self._meansq = tf.reduce_mean(tf.square(self._output_layer - self._real_output))
        self._optimizer = tf.train.AdamOptimizer(learning_rate).minimize(self._meansq)
        self._training = tf.global_variables_initializer()
        self._saver = tf.train.Saver()
        self._session = tf.Session()

    def train(self, input_train, input_test, batch_size, epochs):
        self._session.run(self._training)

        for epoch in range(epochs):
            epoch_loss = 0
            for i in range(int(input_train.shape[0] / batch_size)):
                epoch_input = input_train[i * batch_size: (i + 1) * batch_size]
                _, c = self._session.run([self._optimizer, self._meansq],
                                         feed_dict={self._input_layer: epoch_input, self._real_output: epoch_input})
                epoch_loss += c
                print('Epoch', epoch, '/', epochs, 'Batch loss:', c)
            self._saver.save(self._session, f'./saved_models/model.ckpt')
            print('Epoch', epoch, '/', epochs, 'Epoch loss:', epoch_loss)

    def getEncoded(self, audio):
        encoded = self._session.run(self._hidden3_layer, feed_dict={self._input_layer: [audio]})
        return encoded


