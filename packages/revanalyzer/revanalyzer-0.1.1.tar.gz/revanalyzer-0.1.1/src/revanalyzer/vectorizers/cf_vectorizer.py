# -*- coding: utf-8 -*-
"""Definition of CF vectorizer"""

import numpy as np
from .basic_vectorizer import BasicVectorizer


class CFVectorizer(BasicVectorizer):
    """
    Class describing CF vectorizer.
    """   
    def __init__(self, norm=2, mode='max'):
        """
        **Input:**
        
        	mode (str): can be 'all' or 'max'. If mode = 'all', CF calculated for 'x', 'y' and 'z' directions are concatenated into one vector during vectorization. If mode = 'max', CF calculared for different directions are vectorizes  independently. 
        	Then at the analisys step, maximal differences and deviations over 3 directions are taking for REV sizes calculation. Default: 'max';
        	
        	norm (int): Norm of vectors used in REV analysis. The same, as parameter 'ord' in numpy.linalg.norm function, default: 2.
        """      
        super().__init__(norm)
        self.mode = mode

    def vectorize(self, v1, v2):
        """
        Vectorize the vector metric values for a given pair of subsamples. 
        
        **Input:**
        
        	v1 (list(dtype = float)): data for the first subsample;
        	
        	v2 (list(dtype = float)): data for the second subsample.
        
        **Output:**
        
        Depends on the chosen mode.
        
        	If mode = 'all':
        
        		(list(dtype = float), list(dtype = float), float) - a tuple, in which the first two elements are vectorized metric values for a given pair of subsamples, and the last one is the normalized distance between these vectors. 
        
        	If mode = 'max:
        
        		(list(list(dtype = float)), list(list(dtype = float)), list(float)) - a tuple, in which the first two elements are vectorized metric values in 'x', 'y' and 'z' directions for a given pair of subsamples, and the last one is a list of normalized distances between these vectors.        
        """
        if not (self.mode == 'max' or self.mode == 'all'):
            raise ValueError("Mode should be 'max' or 'all'.")
        n = min(len(v1[0]), len(v2[0]))
        if self.mode == 'max':
            v_res1 = []
            v_res2 = []
            deltas = []
            for i in range(3):
                v_norm1 = np.linalg.norm(v1[i][:n], ord=self.norm)
                v_norm2 = np.linalg.norm(v2[i][:n], ord=self.norm)
                d = np.linalg.norm(np.array(v1[i][:n]) -
                                   np.array(v2[i][:n]), ord=self.norm)
                deltas.append(2 * d/(v_norm1 + v_norm2))
                vi1 = np.array(v1[i][:n])/v_norm1
                vi2 = np.array(v2[i][:n])/v_norm2
                v_res1.append(vi1.tolist())
                v_res2.append(vi2.tolist())
        if self.mode == 'all':
            v_res1 = np.concatenate([v1[0][:n], v1[1][:n], v1[2][:n]]).tolist()
            v_res2 = np.concatenate([v2[0][:n], v2[1][:n], v2[2][:n]]).tolist()
            v_norm1 = np.linalg.norm(np.array(v_res1), ord=self.norm)
            v_norm2 = np.linalg.norm(np.array(v_res2), ord=self.norm)
            deltas = 2 * \
                np.linalg.norm(np.array(v_res1) - np.array(v_res2),
                               ord=self.norm)/(v_norm1 + v_norm2)
            v_res1 = (v_res1/v_norm1).tolist()
            v_res2 = (v_res2/v_norm2).tolist()
        return v_res1, v_res2, deltas
