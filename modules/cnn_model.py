from tensorflow import keras
from tensorflow.keras import layers

# -------------------- CBAM MODULE --------------------
def cbam_block(input_feature, ratio=8):
    """Convolutional Block Attention Module: Channel + Spatial Attention"""
    channel = input_feature.shape[-1]

    # Channel Attention
    avg_pool = layers.GlobalAveragePooling2D()(input_feature)
    max_pool = layers.GlobalMaxPooling2D()(input_feature)
    shared_dense1 = layers.Dense(channel // ratio, activation='relu', kernel_initializer='he_normal')
    shared_dense2 = layers.Dense(channel, kernel_initializer='he_normal')
    avg_out = shared_dense2(shared_dense1(avg_pool))
    max_out = shared_dense2(shared_dense1(max_pool))
    channel_attention = layers.Activation('sigmoid')(avg_out + max_out)
    channel_attention = layers.Reshape((1, 1, channel))(channel_attention)
    x = layers.Multiply()([input_feature, channel_attention])

    # Spatial Attention
    avg_pool_spatial = layers.Lambda(lambda x: keras.backend.mean(x, axis=-1, keepdims=True))(x)
    max_pool_spatial = layers.Lambda(lambda x: keras.backend.max(x, axis=-1, keepdims=True))(x)
    concat = layers.Concatenate(axis=-1)([avg_pool_spatial, max_pool_spatial])
    spatial_attention = layers.Conv2D(1, (7, 7), padding='same', activation='sigmoid', kernel_initializer='he_normal')(concat)
    x = layers.Multiply()([x, spatial_attention])

    return x

# -------------------- BUILD MODEL MỞ RỘNG --------------------
def build_cnn_cbam_extended(input_shape=(64, 64, 3), num_classes=5):
    inputs = keras.Input(shape=input_shape)
    filters = [64, 128, 256, 256, 512]  # 5 block filters

    x = inputs
    for i, f in enumerate(filters):
        x = layers.Conv2D(f, (3,3), padding='same', activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(f, (3,3), padding='same', activation='relu')(x)
        x = layers.MaxPooling2D((2,2))(x)
        x = cbam_block(x)

    # Classifier
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer=keras.optimizers.Adam(0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

# -------------------- TEST --------------------
if __name__ == "__main__":
    model = build_cnn_cbam_extended()
    model.summary()
