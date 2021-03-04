import abc
import compling.lexicalAnalysis.vectorization

class UnsupervisedLearning(compling.lexicalAnalysis.vectorization.VSM, metaclass=abc.ABCMeta):
    """
    Unsupervised learning is a type of machine learning that looks for previously undetected patterns in a data set with no pre-existing labels and with a minimum of human supervision.
    """

    @abc.abstractmethod
    def run(self, *args) -> object:
        """Runs Unsupervised Learning stage."""
