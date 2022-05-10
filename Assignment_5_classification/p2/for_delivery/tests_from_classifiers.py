import os 
from matplotlib import pyplot as plt

__file__ = "p2"
in_folder = os.path.abspath(__file__) 

def find_classifiers():
    """
    Gets all of the classifiers in a list.
    """
    classifiers = []
    for fname in os.listdir(in_folder):
        if "C" in fname: 
            classifiers.append(fname)
    return classifiers


def get_gt_vals(): 
    """
    Returns Ground truth values in a list.
    """
    with open(in_folder + "\\" + "GT.dsv") as f:
        lines = f.read()
        gt_vals = lines.split('\n')
    return gt_vals
    
def read_lines(classifier):
    """
    Reads the lines in the given text, and returns a list of the lines and the length of that list. 
    """
    with open(in_folder + '\\' + classifier, encoding='utf-8', errors='ignore') as classifier_file: 
        lines = classifier_file.read()
        str_numbers = lines.split('\n')
    return(str_numbers, len(str_numbers))

def get_tp_fp_tn_fn(classifier_lines, gt_vals):
    alpha_tp_fp_tn_fn_count = [[0, 0, 0, 0] for _ in range(50)]
    line = 0 
    for numbers in classifier_lines[0]:
        numbers = numbers.replace(',', '')
        for number_index in range(len(numbers)): 
            #correctly classified as 1 - True Positive (TP)
            if(numbers[number_index] == gt_vals[line] and gt_vals[line] == '1'):
                alpha_tp_fp_tn_fn_count[number_index][0]+=1
            #Incorrectly classified as 1 - False Positive (FP)
            elif(numbers[number_index] != gt_vals[line] and gt_vals[line] == '0'):
                alpha_tp_fp_tn_fn_count[number_index][1] += 1 
            #Correctly classified as 0 - True negative (TN)
            elif(numbers[number_index] == gt_vals[line] and gt_vals[line] == '0'):
                alpha_tp_fp_tn_fn_count[number_index][2] += 1 
            #Incorrectly classified as negative - False negative (FN)
            elif(numbers[number_index] != gt_vals[line] and gt_vals[line] == '1'):
                alpha_tp_fp_tn_fn_count[number_index][3]+=1                        
        line += 1 
    return alpha_tp_fp_tn_fn_count 

def get_precision(alpha_tp_fp_tn_fn_count): 
    """
    precision = TP/(TP + FP)
    Returns a list with the precision of each alpha in a classifier. 
    Here I assume that Positive is 1 and Negative is 0 
    """
    alpha_precision_count = [0 for _ in range(50)]
    alpha_precision_counter = 0
    for tp_fp_tn_fn in alpha_tp_fp_tn_fn_count: 
        try:
            #precision = TP/(TP + FP)
            alpha_precision_count[alpha_precision_counter] = tp_fp_tn_fn[0]/(tp_fp_tn_fn[0]+tp_fp_tn_fn[1])
        except: #in case of division by 0
            alpha_precision_count[alpha_precision_counter] = 0 
        alpha_precision_counter += 1
    return alpha_precision_count

def get_specificity(alpha_tp_fp_tn_fn_count): 
    """
    Specificity = TN/(TN + FP)
    Returns a list with the specificity of each alpha in a classifier. 
    """
    alpha_specificity_count = [0 for _ in range(50)]
    alpha_specificity_counter = 0
    for tp_fp_tn_fn in alpha_tp_fp_tn_fn_count: 
        #Specificity = TN/(TN + FP)
        alpha_specificity_count[alpha_specificity_counter] = tp_fp_tn_fn[2]/(tp_fp_tn_fn[2]+tp_fp_tn_fn[1])
        alpha_specificity_counter += 1
    return alpha_specificity_count  
 
def get_fpr(specificity_count):
    """
    Returns a list with the False Positive Rate (FPR) of each alpha in a classifier. 
    """ 
    fpr = [0 for _ in range(50)]
    for specificity_index in range(len(specificity_count)):
        #FPR = 1 - specificity
        fpr[specificity_index] = 1 - specificity_count[specificity_index]
    return fpr
         
        
def get_recall(alpha_tp_fp_tn_fn_count): 
    """
    recall = TP/(TP + FN)
    Returns a list with the recall of each alpha in a classifier. 
    """
    alpha_recall_count = [0 for _ in range(50)]
    alpha_recall_counter = 0
    for tp_fp_tn_fn in alpha_tp_fp_tn_fn_count: 
        #recall = TP/(TP + FN)
        alpha_recall_count[alpha_recall_counter] = tp_fp_tn_fn[0]/(tp_fp_tn_fn[0]+tp_fp_tn_fn[3])
        alpha_recall_counter += 1
    return alpha_recall_count  

def draw_ROC(specificity, recall): 
    """
    Draws the ROC-curve for the given classifier.
    """
    plt.title('ROC curve')
    fpr = get_fpr(specificity)
    best_index = find_best_index(specificity, recall)
    plt.plot(fpr, recall, marker='^', markeredgecolor='green', color='blue')
    plt.plot(fpr[best_index], recall[best_index], marker='*', markersize = 30,  markeredgecolor = 'pink',  markerfacecolor='red')
    plt.text(0.025, 0.9, ('optimal point, alpha'+ str(best_index) + ", fpr: " + str((fpr[best_index])) + ", recall: " + str(recall[best_index])), fontsize=14)
    plt.xlabel('False Positive Rate (1-specificity)')
    plt.ylabel('True Positive Rate (recall)')
    plt.show()
    
def find_best_index(specificity, recall): 
    """
    Finds the best alpha for the classifier, and returns the index of this alpha.
    """
    max_rate_index = 0
    max_rate = 0 
    for rates_index in range(len(specificity)): 
        sum_recall_specificity = specificity[rates_index]+recall[rates_index]
        #use this if-statement if you want the optimal point that has a trade-off between the FPR and the TPR
        #if (recall_fpr>max_rate):
        #use this if-statement you want the best points with no false positives 
        if (sum_recall_specificity>max_rate) and (specificity[rates_index] >= 1): 
            max_rate = sum_recall_specificity
            max_rate_index = rates_index
    return max_rate_index

def compare_classifiers(): 
    """
    Compares an old with classifier with the new classifier, and checks which one is best 
    if we want a FPR of 0. Returns True if C6 is best and False if C6 is worst. 
    """
    classifiers = find_classifiers()
    #ground truth values 
    gt_vals = get_gt_vals()
    #assuming we want classifier 4 (C4) here.
    C4 = read_lines(classifiers[3])
    #assuming the new classifier (C6) is last in the list of classifiers
    C6 = read_lines(classifiers[-1])
    #Find TP, TN, FP and FN for each classifier to be able to find specificity and recall 
    C4_tp_fp_tn_fn = get_tp_fp_tn_fn(C4, gt_vals)
    C6_tp_fp_tn_fn = get_tp_fp_tn_fn(C6, gt_vals)
    C4_specificity = get_specificity(C4_tp_fp_tn_fn)
    C4_recall = get_recall(C4_tp_fp_tn_fn)
    C6_specificity = get_specificity(C6_tp_fp_tn_fn)
    C6_recall = get_recall(C6_tp_fp_tn_fn)
    
    C4_best_index = find_best_index(C4_specificity, C4_recall)
    C6_best_index = find_best_index(C6_specificity, C6_recall)
    
    if(C6_specificity[C6_best_index] != 1) or (C4_recall[C4_best_index] >= C6_recall[C6_best_index]): 
        return False 
    return True 
    
            

  

   


if __name__ == '__main__': 
    print(compare_classifiers())
