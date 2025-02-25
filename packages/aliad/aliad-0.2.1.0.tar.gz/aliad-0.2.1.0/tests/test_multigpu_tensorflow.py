import tensorflow as tf
import unittest

def get_compiled_model():
    # Make a simple 2-layer densely-connected neural network.
    inputs = tf.keras.Input(shape=(784,))
    x = tf.keras.layers.Dense(256, activation="relu")(inputs)
    x = tf.keras.layers.Dense(256, activation="relu")(x)
    outputs = tf.keras.layers.Dense(10)(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )
    return model


def get_dataset():
    batch_size = 32
    num_val_samples = 10000

    # Return the MNIST dataset in the form of a `tf.data.Dataset`.
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # Preprocess the data (these are Numpy arrays)
    x_train = x_train.reshape(-1, 784).astype("float32") / 255
    x_test = x_test.reshape(-1, 784).astype("float32") / 255
    y_train = y_train.astype("float32")
    y_test = y_test.astype("float32")

    # Reserve num_val_samples samples for validation
    x_val = x_train[-num_val_samples:]
    y_val = y_train[-num_val_samples:]
    x_train = x_train[:-num_val_samples]
    y_train = y_train[:-num_val_samples]
    return (
        tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(batch_size),
        tf.data.Dataset.from_tensor_slices((x_val, y_val)).batch(batch_size),
        tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(batch_size),
    )


class TestMultiGPUTraining(unittest.TestCase):
    
    def test_multi_gpu_training(self):
        # Create a MirroredStrategy.
        strategy = tf.distribute.MirroredStrategy()
        print("Number of devices: {}".format(strategy.num_replicas_in_sync))

        # Open a strategy scope.
        with strategy.scope():
            # Everything that creates variables should be under the strategy scope.
            # In general this is only model construction & `compile()`.
            model = get_compiled_model()

        # Train the model on all available devices.
        train_dataset, val_dataset, test_dataset = get_dataset()

        # Check if model trains without any errors
        try:
            model.fit(train_dataset, epochs=2, validation_data=val_dataset)
            model.evaluate(test_dataset)
            trained_successfully = True
        except Exception as e:
            trained_successfully = False
            print("Error during training:", e)

        self.assertTrue(trained_successfully, "Model training failed on multiple GPUs.")

if __name__ == '__main__':
    unittest.main()