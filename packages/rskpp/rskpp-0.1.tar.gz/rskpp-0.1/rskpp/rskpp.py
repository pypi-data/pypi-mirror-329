import numpy as np 

def rskmeanspp(data: np.array, k: int, m : int) -> list[int]:
    ''' k-means++ seeding using rejection sampling

    :param data: dataset of shape (n,d)
    :type data: numpy.array 

    :param k: number of clusters
    :type k: int 

    :param m: upper bound on number of rejection sampling iterations
    :type m: int 

    :return: cluster centers of shape (k,d)
    :rtype: numpy.array


    '''
    n, d = data.shape

    # Center the data by subtracting the mean
    mean = np.mean(data, axis=0)
    data_centered = data - mean

    # Precompute norms for sampling
    norms_squared = np.sum(data_centered ** 2, axis=1)
    frobenius_norm_squared = np.sum(norms_squared)

    # Initialize centers
    indices = []
    first_center = np.random.randint(0, n)
    indices.append(first_center)

    # Select remaining k-1 centers
    for _ in range(1, k):
        iter = 0
        sampled = False
        while (sampled == False and iter < m) : 
            iter+=1
            r = np.random.uniform(0, 1)
            r_prime = np.random.uniform(0,1)

            if r <= frobenius_norm_squared / (frobenius_norm_squared + n * norms_squared[first_center]):
                # Sample from Dv
                i = np.random.choice(n, p=norms_squared / frobenius_norm_squared)
            else:
                # Sample uniformly
                i = np.random.randint(0, n)

            # Compute rejection probability
            min_dist_squared = np.linalg.norm(data[i] - data[indices], axis = 1).min() **2
            rejection_prob = 0.5 * min_dist_squared / (norms_squared[i] + norms_squared[first_center])

            if r_prime <= rejection_prob:
                indices.append(i)
                sampled = True 
        
        if sampled == False :
            center = np.random.randint(0,n)
            indices.append(center) 
        
        

    return data[indices] 