import numpy as np # Install numpy befor importing

# Supporting functions
def relu(x):
    return np.maximum(x, 0)

def tanh(x):
    np.tanh(x)

def sigmoid(z):
    A = 1/(1 + np.exp(-z))
    return A

def softmax(z):
    expZ = np.exp(z)
    return expZ/np.sum(expZ, axis = 0)

# Loading parameters function
def load_parameters(path):
    # Loading the file
    npz_file = np.load(path)

    # Rebuild it back into a standard Python dictionary
    loaded_parameters = {key: npz_file[key] for key in npz_file.files}

    return loaded_parameters


# Prediction function
def forward_propagation(X, parameters, activation = 'relu'):
    L = len(parameters)//2
    forward_cache = {}
    forward_cache["A0"] = X

    # Hidden layers functionality
    for l in range(1, L):
        # Z_l = W_l * A_(l-1) + B_l
        forward_cache["Z" + str(l)] = np.dot(parameters["W" + str(l)], forward_cache["A" + str(l-1)]) + parameters["B" + str(l)]

        if activation == "relu":
            # A_l = ReLU(Z_l)
            forward_cache["A" + str(l)] = relu(forward_cache["Z" + str(l)])
        else:
            # A_l = Tanh(Z_l)
            forward_cache["A" + str(l)] = tanh(forward_cache["Z" + str(l)])

    # Output layer functionality
    # Z_L = W_L * A_(L-1) + B_L
    forward_cache["Z" + str(L)] = np.dot(parameters["W" + str(L)], forward_cache["A" + str(L-1)]) + parameters["B" + str(L)]

    if forward_cache["Z" + str(L)].shape[0] == 1:
        # A_L = Sigmoid(Z_L)
        forward_cache["A" + str(L)] = sigmoid(forward_cache["Z" + str(L)])
    else:
        # A_L = Softmax(Z_L)
        forward_cache["A" + str(L)] = softmax(forward_cache["Z" + str(L)])

    return forward_cache["A" + str(L)], forward_cache