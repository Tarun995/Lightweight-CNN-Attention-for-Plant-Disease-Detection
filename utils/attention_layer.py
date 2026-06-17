import tensorflow as tf
from keras.saving import register_keras_serializable

@register_keras_serializable(package="CustomLayers")
class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self, input_shape):
        feat = int(input_shape[-1])
        self.att_w = self.add_weight(
            name='att_w', shape=(feat, 1), initializer='normal', trainable=True
        )
        self.att_b = self.add_weight(
            name='att_b', shape=(1,), initializer='zeros', trainable=True
        )
        super().build(input_shape)

    def call(self, x):
        # x is expected to have shape (batch, timesteps, features)
        e = tf.tanh(tf.matmul(x, self.att_w) + self.att_b)   # (batch, timesteps, 1)
        a = tf.nn.softmax(e, axis=1)                         # (batch, timesteps, 1)
        out = tf.reduce_sum(x * a, axis=1)                   # (batch, features)
        return out

    def get_config(self):
        config = super().get_config()
        return config
