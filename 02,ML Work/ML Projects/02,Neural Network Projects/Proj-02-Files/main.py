import numpy as np # Install numpy before importing
import random
import matplotlib.pyplot as plt # Install matplotlib before importing
import utils

# Loading test dataset
X_test = np.loadtxt(r"D:\MPhil\3rd sem\Python work\Practice\Proj-02-Files\cat_test_x.csv", delimiter = ",")/255.0

# Displaying random image from test dataset
index = random.randrange(0, X_test.shape[1])
plt.imshow(X_test[:, index].reshape(64,64,3)) # '64' is 'height', '64' is 'width' and '3' represents 'channels' i.e., red, green, blue.
plt.show()

# Loading the path
path = r"D:\MPhil\3rd sem\Python work\Practice\Proj-02-Files\parameters.npz" # Put the path of 'parameters.npz' file here.

X = X_test[:, index].reshape(X_test.shape[0], 1) # Put an image from test dataset here, fo example, 'X_test[:, index].reshape(X_test.shape[0], 1)' squishing all columns to 1, i.e., the shpe will be, (any number, 1).
parameters = utils.load_parameters(path)

prediction, _ = utils.forward_propagation(X, parameters, "relu")

print(prediction)

# For Binary Classification
if prediction > 0.5:
  print("The Image Is A Cat.")
else:
  print("The Image Is Not A Cat.")


#---------------------------------- ACCURACY: 74 % ---------------------------------

