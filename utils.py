import numpy as np
import csv
import math

def average(item_ratings):
    '''
        Receives a list of item_ratings and returns
        the mean of said list
        @param item_ratings is the list of item_ratings
        @return mean of list in float64 format
    '''
    arr = np.array(item_ratings)
    return np.mean(arr)

def least_misery(item_ratings):
    '''
        Receives a list of item_ratings and returns
        the min element of said list
        @param item_ratings is the list of item_ratings
        @return minimal value of list as a scalar value 
    '''
    arr = np.array(item_ratings)
    return np.amin(arr)

def disagreement_variance(item_ratings):
    '''
        Receives a list of item_ratings and returns
        the variance of said list
        @param item_ratings is the list of item_ratings
        @return variance of the list
    '''
    arr = np.array(item_ratings)
    return np.var(arr,dtype=np.float64)

def average_pairwise_disagreement(item_ratings):
    '''
        Receives a list of item_ratings and returns
        the average pairwise disagreement of said list
        @param item_ratings is the list of item_ratings
        @return average_pairwise_disagreement of the list
    '''
    G = len(item_ratings)
    k = 2/(G*(G-1))
    pair_wise_diff = 0
    for i in range(0,G):
        for j in range(i+1,G):
            pair_wise_diff += abs(item_ratings[i] - item_ratings[j])
    return pair_wise_diff/k

def get_function_switch(key,map_of_functions):
    '''
        Receives a string with the name of the function you want
        and a dict with the function name and the function object,
        returns the function object or throws an error if the function
        was not found.
        @param key string corresponding to the strategy chosen
        @return the functions correspondent with the chosen strategies
    '''

    func = map_of_functions.get(key,"None")

    if ( func == "None"):
        raise("No corresponding function.")

    return func

def cosine_similarity(item1,item2):
    '''
        Receives two lists with all the ratings for item 1 and
        item 2 and returns the cosine_similarity
        @param item1 the list with all the ratings for item 1
        @param item2 the list with all the ratings for item 2
        @return the cosine similarity of the two items
    '''
    return np.dot(item1,item2)/(np.linalg.norm(item1)*np.linalg.norm(item2))

def append_collumn_to_matrix(M):
    '''
        Receives a matrix and appends a collumn to it
        @param M the matrix to append the collumn to
        @returns the matrix with the collumn appended
    '''
    return [ row + [-1] for row in M]

def append_row_to_matrix(M):
    '''
     Receives a matrix and appends a row to it
        @param M the matrix to append the row to
        @returns the matrix with the row appended
    '''
    if(len(M) == 0):
        return [[(-1)]]
    M.append([-1 for collumn in M[0]])
    return M

def get_user_item_index(user_dict,item_dict,user_elem,item_elem,M):

    if(user_dict.get(user_elem) == None):
        M = append_row_to_matrix(M)
        user_dict[user_elem] = (len(M) - 1)

    if(item_dict.get(item_elem) == None):
        M = append_collumn_to_matrix(M)
        item_dict[item_elem] = (len(M[0]) - 1)

    return M,user_dict.get(user_elem),item_dict.get(item_elem)

def get_user_item_matrix(dataset):

    user_dict = dict()
    item_dict = dict()
    M = list()
    with open(dataset,'r') as ds:
        in_reader = csv.reader(ds)
        first_el = next(in_reader)
        user_dict[first_el[0]] = 0
        item_dict[first_el[1]] = 0
        M.append([float(first_el[2])])
        for row in in_reader:
            user_elem = row[0]
            item_elem = row[1]
            review = row[2]

            M,user_index , item_index = get_user_item_index(user_dict,item_dict,user_elem,item_elem,M)
            M[user_index][item_index] = float(review)
    return M,item_dict

def get_mean_of_each_item(M):
    '''
        Receives the user-item matrix and retrieves the mean
        for all item-ratings.
        @param M user-item matrix
        @return the list with the mean for each item
    '''
    M = np.transpose(M)
def replace_missing_values(M,avg_rev):
    '''
        Receives the user-item matrix with the missing values
        and the avg-rev of users and replace the missing values
        by the avg_rev.
        @param M the user-item matrix
        @param avg_rev the average of that review
        @return the new user-item matrix with the values replaced
    '''
    for i in range(0,len(M)):
        for j in range(0,len(avg_rev)):
            if(np.isnan(M[i][j])):
                M[i][j] = avg_rev[j]
    return M

def euclidean_with_nan(x, y):
    x = np.array(x)
    y = np.array(y)
    x_index = [not math.isnan(a) for a in x]
    y_index = [not math.isnan(a) for a in y]
    inter = [a[0] and a[1] for a in list(zip(x_index, y_index))]
    pairs = list(zip(x[inter],y[inter]))
    mapped = list(map((lambda x: (x[0]-x[1])**2), pairs))
    return sum(mapped)

def nearest_neighbor(M, index, forb_ind):
    item = M[index]
    search_M = M
    min_dist = np.Inf
    min_ind = 0
    for it in range(len(search_M)):
        if it in forb_ind:
            continue
        dist = euclidean_with_nan(item, search_M[it])
        if dist < min_dist:
            min_ind = it
            min_dist = dist
    return search_M[min_ind], min_ind

def replace_missing_values_nn(M):
    for i in range(len(M)):
        if np.any(np.isnan(M[i])):
            forb_ind = {i}
            union = [False]
            found = True
            while not np.all(union):
                neighbor, n_ind = nearest_neighbor(M, i, forb_ind)
                n_index = [not math.isnan(a) for a in neighbor]
                m_index = [not math.isnan(a) for a in M[i]]
                union = [a[0] or a[1] for a in list(zip(n_index, m_index))]
                forb_ind.add(n_ind)
                if(len(forb_ind) == len(M)):
                    found = False
                    break
            if found:
                for j in range(len(M[i])):
                    if math.isnan(M[i][j]):
                        M[i][j] = neighbor[j]
            else:
                mean = np.nanmean(M[i])
                for j in range(len(M[i])):
                    if math.isnan(M[i][j]):
                        M[i][j] = mean
    return M