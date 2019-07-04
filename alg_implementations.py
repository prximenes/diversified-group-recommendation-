import utils
import constants
import csv
import numpy as np

def get_utility_score(M,group_utility,disagreement,w):
    '''
        Receives the user-item matrix, the strings with the names
        of the group-utility and disagreement strategies and a 
        contant w for the
        @param M the user X item matrix, the matrix should have 
        @param group_utility string with the name of the group-utility strategy
        @param disagreement string with the name of the dis. strategy
        @param w weight used to control the proportion between group-utility and disagreement
        @returns an array with the overall utility-score for each item 
    '''
    pref = utils.get_function_switch(group_utility,constants.GROUP_UTILITY_SWITCH)
    dis = utils.get_function_switch(disagreement,constants.DISAGREEMENT_SWITCH)

    M = utils.np.transpose(M)
    r = list()
    utility_score = 0
    w1 = w
    w2 = -w
    
    for row in M:
        utility_score = w1*pref(row) + w2*(1 - dis(row)) 
        r.append(utility_score)
    return r

def get_similarity_matrix(M,similarity):
    '''
        Receives the user-item matrix and the name of the similarity
        function and returns the similarity matrix
        @param M the user-item matrix
        @param similarity string of the similarity function to be used
        @returns the similarity matrix
    '''
    M = utils.np.transpose(M)
    S = utils.get_function_switch(similarity,constants.SIMILARITY_SWITCH)
    return [ [S(item1,item2) for item2 in M] for item1 in M]

def update_ranking_score(rank,r,w,s,last_item_index):
    '''
        Receives the rank array, the utility score, a weight,
        the similarity matrix and the last inserted item index
        @param rank an array with the rank of all items
        @param r the utility score of all items
        @param w the weight of the function
        @param s the similarity matrix
        @param last_item_index the index of the last inserted item at the M array
        @returns the updated rank
    '''
    for i in range(0,len(rank)):
        rank[i] = rank[i] - w*r[i]*s[i][last_item_index]*r[last_item_index]
    return rank

def get_weight_factor(M,r,s):
    '''
        Receives the user-item matrix, the utility score
        and the similarity matrix, returns the weight_factor
        array
        @param M the user-item matrix
        @param r the utility score array
        @param s the similarity matrix
        @return the weight_factor array
    '''
    M = utils.np.transpose(M)
    q = list()
    weight_factor = 0

    for i in range(0,len(M)):
        for j in range(0,len(M)):
            weight_factor += s[i][j]*r[i]

        q.append(weight_factor)
        weight_factor = 0

    return q



def gen_csv_from_list(M,fp):

    with open(fp,'w') as fil:
        wr = csv.writer(fil)
        for row in M:
            wr.writerow(row)


def refined_pre_processing(fp,similarity="cosine"):
    M,item_dict = utils.get_user_item_matrix(fp)
    print("user-item-matrix [x]")
    fp1 = fp[:-4] + "-user-item.csv"
    gen_csv_from_list(M,fp1)
    fp2 = fp[:-4] + "-item-item.csv"    
    print("similarity-matrix [x]")
    M = [[int(collumn) for collumn in row] for row in M]
    S = get_similarity_matrix(M,similarity)
    gen_csv_from_list(S,fp2)


def get_list_from_csv(fp):
    
    l = list()
    with open(fp,'r') as fil:
        in_reader = csv.reader(fil,delimiter=",")
        for row in in_reader:
            l.append(row)
    return l 
    
def diversify_group_recommendation_the_algorithm(fp,k,group_utility="average",disagreement="variance",similarity="cosine",w=2):

    fp1 = fp[:-4] + "-user-item.csv"
    fp2 = fp[:-4] + "-item-item.csv"    

    M,item_dict = utils.get_user_item_matrix(fp)
    M = get_list_from_csv(fp1)
    M = M[:20]
    M = [[float(collumn) for collumn in row] for row in M]
    print("user-item-matrix [x]")
    print(" dimensions: " + str(len(M)) + "x" + str(len(M[0])))
    
    S = get_list_from_csv(fp2)
    S = [[float(collumn) for collumn in row] for row in S]
    print("similarity-matrix [x]")
    print(" dimensions: " + str(len(S)) + "x" + str(len(S[0])))

    #avg_rev = [np.nanmean(row) for row in S] < -- apenas se formos fazer o preenchimento usando média
    #avg_rev = [np.nan_to_num(x) for x in avg_rev]
    S = utils.replace_missing_values_nn(S)

    print(S)
    
    r = get_utility_score(M,group_utility,disagreement,w)
    print("utility-score [x] len= #" + str(len(r)))
    print(" dimensions: " + str(len(r)))

    q = get_weight_factor(M,r,S)
    print("weight-factor [x] len= #" + str(len(q)))
    print(" dimensions: " + str(len(q)))
    
    rank = [w*x*y for x,y in zip(q,r)]    
    I = list()

    for i in range(0,k):
        x = np.max(rank)
        last_item_idex = rank.index(x)
        I.append(last_item_idex)

        rank = update_ranking_score(rank,r,w,S,last_item_idex)    

        rank.pop(last_item_idex)
        r.pop(last_item_idex)
        S.pop(last_item_idex)
        [s.pop(last_item_idex) for s in S]


    for i in range(0,len(I)):
        print("Item #"+ str(i) + " = " +  str([k for k,v in item_dict.items() if v == I[i]]))

#refined_pre_processing("databases/parsed-databases/movie-lenz.csv")
#diversify_group_recommendation_the_algorithm("databases/parsed-databases/movie-lenz.csv",5)