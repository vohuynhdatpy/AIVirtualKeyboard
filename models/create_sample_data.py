import numpy as np
import os

os.makedirs("../data/train", exist_ok=True)
os.makedirs("../data/test", exist_ok=True)

def create(n):
    return np.random.rand(n, 42).astype('float32')

# train: 400 each
np.save("../data/train/click.npy", create(400))
np.save("../data/train/none.npy", create(400))
# test: 100 each
np.save("../data/test/click.npy", create(100))
np.save("../data/test/none.npy", create(100))

print("Sample data created in data/train and data/test")
