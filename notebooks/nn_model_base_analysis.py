import numpy as np
import random
import sys
from utils import randmatrix, progress_bar

__author__ = "Christopher Potts"
__version__ = "CS224u, Stanford, Spring 2018"


class NNModelBase(object):
    def __init__(self,
            vocab,
            embedding=None,
            embed_dim=10,
            hidden_dim=20,
            eta=0.01,
            max_iter=10,
            tol=1e-6,
            display_progress=True):
        #> map each word in vocab to some i.
        self.vocab = dict(zip(vocab, range(len(vocab))))
        if embedding is None:
            embedding = self._define_embedding_matrix(
                len(self.vocab), embed_dim)
        self.embedding = embedding
        self.embed_dim = self.embedding.shape[1]
        self.hidden_dim = hidden_dim
        self.eta = eta
        self.max_iter = max_iter
        self.tol = tol
        self.display_progress = display_progress
        self.params = [
            'embedding', 'embed_dim', 'hidden_dim', 'eta', 'max_iter']

    def initialize_parameters(self):
        raise NotImplementedError

    def update_parameters(self, gradients):
        raise NotImplementedError

    def forward_propagation(self):
        raise NotImplementedError

    def backward_propagation(self):
        raise NotImplementedError

    def fit(self, X, y):
        """Train the network.

        Parameters
        ----------
        X : list of lists
           Each element should be a list of elements in `self.vocab`.
        y : list
           The one-hot label vector.

        """
        #> get a one-hot representation for the correct classification.
        y = self.prepare_output_data(y)
        self.initialize_parameters()
        # Unified view for training
        #> matching examples to correct classification, now one-hot form.
        training_data = list(zip(X, y))
        # SGD:
        iteration = 0
        for iteration in range(1, self.max_iter+1):
            error = 0.0
            random.shuffle(training_data)
            for ex, labels in training_data:
                hidden_states, predictions = self.forward_propagation(ex)
                # Cross-entropy error reduces to -log(prediction-for-correct-label):
                error += -np.log(predictions[np.argmax(labels)])
                # Back-prop:
                gradients = self.backward_propagation(
                    hidden_states, predictions, ex, labels)
                self.update_parameters(gradients)
            error /= len(training_data)
            #> there seems to be some redundancy here, as we check for error threshold after updating the weights.
            #> still, you need to forward prop to get the predictions, and this is used in backpropping, so unclear what a better method would be.
            if error <= self.tol:
                if self.display_progress:
                    progress_bar(
                        "Converged on iteration {} with error {}".format(
                            iteration, error))
                break
            else:
                if self.display_progress:
                    progress_bar(
                        "Finished epoch {} of {}; error is {}".format
                        (iteration, self.max_iter, error))

    @staticmethod
    def _define_embedding_matrix(vocab_size, embed_dim):
        return np.random.uniform(
            low=-1.0, high=1.0, size=(vocab_size, embed_dim))

    def predict_one_proba(self, seq):
        """Softmax predictions for a single example.

        Parameters
        ----------
        seq : list
            Variable length sequence of elements in the vocabulary.

        Returns
        -------
        np.array

        """
        hidden_states, predictions = self.forward_propagation(seq)
        return predictions

    def predict_proba(self, X):
        """Softmax predictions for a list of examples.

        Parameters
        ----------
        X : list of lists
            List of examples.

        Returns
        -------
        list of np.array

        """
        return [self.predict_one_proba(seq) for seq in X]

    def predict(self, X):
        """Predictions for a list of examples.

        Parameters
        ----------
        X : list of lists
            List of examples.

        Returns
        -------
        list

        """
        return [self.predict_one(ex) for ex in X]

    def predict_one(self, x):
        """Predictions for a single example.

        Parameters
        ----------
        seq : list
            Variable length sequence of elements in the vocabulary.

        Returns
        -------
        int
            The index of the highest probability class according to
            the model.

        """
        probs = self.predict_one_proba(x)
        return self.classes[np.argmax(probs)]

    def get_word_rep(self, w):
        """For getting the input representation of word `w` from
        `self.embedding`.

        Parameters
        ----------
        w : str

        Returns
        -------
        np.array, dimension `self.embed_dim`

        """
        if w in self.vocab:
            word_index = self.vocab[w]
        else:
            word_index = self.vocab['$UNK']
        return self.embedding[word_index]

    @staticmethod
    def weight_init(m, n):
        """Uses the Xavier Glorot method for initializing the weights
        of an `m` by `n` matrix.

        Parameters
        ----------
        m : int
            Row dimension
        n : int
            Column dimension

        Returns
        -------
        np.array, shape `(m, n)`

        """
        x = np.sqrt(6.0/(m+n))
        return randmatrix(m, n, lower=-x, upper=x)

    def prepare_output_data(self, y):
        """Format `y` into a vector of one-hot encoded vectors.

        Parameters
        ----------
        y : list

        Returns
        -------
        np.array with length the same as y and each row the
        length of the number of classes

        """
        #> y is a vector of correct outputs. So, taking a set gets the different types of output, and sorting this gives it a canonical form, which is going to be used for the one-hot encoding.
        self.classes = sorted(set(y))
        # out_dim then stores the length.
        self.output_dim = len(self.classes)
        y = self._onehot_encode(y)
        return y

    def _onehot_encode(self, y):
        """Maps a single label `y` to a one-hot encoding with 1.0 in
        the position of y and 0.0 for all other classes.

        Parameters
        ----------
        y : object
            Typically a str, int, or bool

        Returns
        -------
        np.array, dimension `len(self.classes)`

        """
        """
        if y = ['y', 'n', 'n'] then we get something like
        [[1,0],
         [0,1],
         [0,1]]
        with the knowledge that each row is an example, column 0 correspond to y, and 1 to n.
        """
        #> range gives a list from 0 up to n.
        #> zip then matches class to element in list.
        #> dict makes a dictionary out of this.
        classmap = dict(zip(self.classes, range(self.output_dim)))
        #> create a len(y) by self.output_dim array of zeroes
        y_ = np.zeros((len(y), self.output_dim))
        #> enumerate y make an iterable object out of y.
        for i, cls in enumerate(y):
            #> so, we update y_ so that for each row (example) one class is chosen, where we lookup the right column for the class by the dictionary created above.
            y_[i][classmap[cls]] = 1.0
        return y_

    def prepare_output_data(self, y):
        """Format `y` so that Tensorflow can deal with it, by turning
        it into a vector of one-hot encoded vectors.

        Parameters
        ----------
        y : list

        Returns
        -------
        np.array with length the same as y and each row the
        length of the number of classes

        """
        self.classes = sorted(set(y))
        self.output_dim = len(self.classes)
        y = self._onehot_encode(y)
        return y

    def get_params(self, deep=True):
        """Gets the hyperparameters for the model, as given by the
        `self.params` attribute. This is called `get_params` for
        compatibility with sklearn.

        Returns
        -------
        dict
            Map from attribute names to their values.

        """
        return {p: getattr(self, p) for p in self.params}

    def set_params(self, **params):
        for key, val in params.items():
            setattr(self, key, val)
        return self
