import numpy as np
def histvec(X, bins, density = False):
	"""
		Create a histogram of X on bins. 
		items placed in the bin eith the lowest absolute difference.
	"""

	D = np.atleast_2d(bins).transpose() - np.atleast_2d(np.array(X)) 
	D = np.abs(D)
	assignment = np.argmin(D, axis=0)
	counts = [np.sum(assignment==i) for i in range(len(bins))]
	counts = np.array(counts)
	
	if density:
	    counts = counts / float(np.sum(counts))
	
	return counts