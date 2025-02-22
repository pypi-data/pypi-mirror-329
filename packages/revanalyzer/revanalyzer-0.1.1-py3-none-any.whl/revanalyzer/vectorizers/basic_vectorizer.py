# -*- coding: utf-8 -*-
"""Definition of basic vectorizer"""

class BasicVectorizer:
    """
    Base class for vectorizers. (Don't use it directly but derive from it).
    """
    def __init__(self, norm):
        """
        **Input:**
        
        	norm (int): Norm of vectors used in REV analysis. The same, as parameter 'ord' in numpy.linalg.norm function.
        """
        self.norm = norm
