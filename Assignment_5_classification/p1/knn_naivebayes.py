from PIL import Image
import numpy as np 
import os
from collections import Counter

def get_test_picture_names(test_path): 
    """
    TODO Description 
    """
    my_path = os.path.abspath(os.path.dirname(__file__))
    test_path = os.path.join(my_path, test_path)  
    test_data_dict = {}    
    for fname in os.listdir(test_path):
        test_data_dict[fname] = '0'
    return test_data_dict


def get_training_set_output(train_path): 
    """
    TODO documentation of function 
    """
    
    my_path = os.path.abspath(os.path.dirname(__file__))
    training_path = os.path.join(my_path, train_path)  
    training_data_dict = {}    
    for fname in os.listdir(training_path):
        if("truth.dsv" in fname): 
            truth_path = os.path.join(training_path, "truth.dsv")
            with open(truth_path) as f:
                lines = f.readlines()
                for line_index in range(len(lines)): 
                    after_semicolon = lines[line_index].partition(":")[2]
                    #Must partition again to remove \n
                    pic_name = lines[line_index].partition(":")[0]
                    pic_id = after_semicolon[0]
                    if pic_id not in training_data_dict: 
                        training_data_dict[pic_id] = [pic_name]
                    else: 
                        training_data_dict[pic_id].append(pic_name)      
        
    return training_data_dict



def get_test_dsv_file(test_dictionary, output_path): 
    """
    TODO documentation of function 
    """
    test_abs_path = os.path.abspath(os.path.dirname(__file__))
    test_path = os.path.join(test_abs_path, output_path)  
    with open(test_path, "w") as tp: 
        for pic_name, predicted_value in test_dictionary.items(): 
            tp.write("%s:%s\n" % (pic_name, predicted_value))

def get_distance(im1, im2):
    """
    Used to get the eucledian distance between two 
    images that are already converted to 2d-numpy arrays.  
    """ 
    diff = im1 - im2
    d2 = np.linalg.norm(diff)
    return d2 

def get_most_likely_value(neighbours_list): 
    """
    Finds the most likely value taken from a list, and returns it. 
    Code taken from here: https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
    """
    occurence_count = Counter(neighbours_list)
    return occurence_count.most_common(1)[0][0]


def classes_probabilities(training_dictionary): 
    """
    Finds the probabilities of each class, and returns it in a dictionary called total_probs. 
    Input: 
        training_dictionary: dictionary used to find the classes and how many occurences of them we have. 
    Output: 
        total_probs: dictionary with the class name as key and the probability of that class as item. 
    
    """
    total_probs = {}
    total = 0
    for key, item in training_dictionary.items(): 
        total_probs[key] = len(item)
        total += len(item)
    for key, item in total_probs.items(): 
        total_probs[key] = item/total
    return total_probs

def get_image_proportions(picture): 
    """
    Opens the picture, and returns it and its width. 
    """
    im = Image.open(picture)
    return im, im.width

def minimize_2d_pic(picture, picture_width, n):
    """
    Returns a representation of the picture that does not contain the same amount of information, but at the
    same time is then easier to classify fast. 
    
    Inputs: 
        picture: the picture 
        picture_width: the width of the picture 
    
    Output: 
        minimized_im: the minimized image 
    """
    im2d = np.array(picture)
    #how many times we want to split the image, which gives how much we minimize it
    im_array_split = picture_width//(picture_width//(picture_width//8))
    minimized_im = np.zeros((((picture_width+1)//im_array_split)**2,))
    minimized_im_num = 0
    #want to go through the picture in 2d, to find the neighbours both in the row and the column, 
    # thereby getting a more valid average, thank if we were to only find the neighbours in the rows for instance
    for pixel_i in range(im_array_split, picture_width+1, im_array_split): 
        for pixel_j in range(im_array_split, picture_width+1, im_array_split): 
            pixel_average = np.average(im2d[pixel_j-im_array_split:pixel_j,pixel_i-im_array_split:pixel_i])
            pixel_feature = features_in_pic(pixel_average, n)
            minimized_im[minimized_im_num] = pixel_feature  
            minimized_im_num += 1 
    return minimized_im


def features_in_pic(pixel_average, n): 
    """
    Returns a number between 1 and n, based on what number between 0 and 255 the numbers of the pixel average is. 
    Input: 
        pixel_average: The average of some pixels that is to be classified 
    Output: 
        pixel_class: a number between 1 and n
    """
    for pixel_class in range(1, n+1): 
        if(pixel_average < 256*pixel_class/n): 
            return pixel_class
    return n 

def get_simplified_pic_output_value(pic_dictionary, path, test, n): 
    """
    Gets in a dictionary, and gives out the same dictionary, containing simplifies items corresponding 
    to the simplified versions of the pictures that were there previously. 
    
    Inputs: 
        pic_dictionary: dictionary with items that are to be simplified to make them easier to work with 
        path: the path the images are from 
    Output: 
        pic_dictionary: the same dictionary, but simplified 
    """
    new_dict = {}
    for picture_key, picture_list in pic_dictionary.items():
        if(test):
            picture, picture_width = get_image_proportions(path + "\\" + picture_key) 
            minimized_picture = minimize_2d_pic(picture, picture_width, n)
            new_dict[picture_key] = minimized_picture
            minimized_pic_length = len(minimized_picture)
        else: 
            for picture_index in range(len(picture_list)): 
                picture, picture_width = get_image_proportions(path + "\\" + picture_list[picture_index])
                minimized_picture = minimize_2d_pic(picture, picture_width, n)
                if(picture_key not in new_dict): 
                    new_dict[picture_key] = [minimized_picture]
                else: 
                    new_dict[picture_key].append(minimized_picture)
                minimized_pic_length = len(minimized_picture)
    return new_dict, minimized_pic_length
        


def find_conditional_probabilities(training_dict, k, n): 
    """
    k used for laplace smoothing!
    """
    conditional_probability_dict = {}
    attribute_occurence_list = [0 for _ in range(n)]
    for key, items in training_dict.items(): 
        for item in items: 
             for attribute in range(n): 
                frequency_count = np.count_nonzero(item == float(attribute))
                attribute_occurence_list[attribute] = frequency_count + k
        conditional_probability_dict[key] = np.divide(attribute_occurence_list, sum(attribute_occurence_list))     
    return conditional_probability_dict

def complex_find_conditional_probabilities(training_dict, minimized_pic_len, k, n): 
    """
    TODO better documentation of function
    Finds the probabilities 
    k used for laplace smoothing!
    Instead of doing it like this, I can add the frequencyes of ever index on that place of each number! 
    """     
    conditional_probability_dict = {}
    attribute_occurence_list = [[0 for _ in range(n)] for _ in range(minimized_pic_len)]
    for training_key, training_items in training_dict.items(): 
        for training_item in training_items: 
            for pic_value_index in range(len(training_item)):
                for attribute in range(n): 
                    attribute_occurence_list[pic_value_index][attribute] = k + ((attribute + 1) == training_item[pic_value_index])
        sum_attributes = 0
        sum_attributes += sum([sum(attribute_probs) for attribute_probs in attribute_occurence_list])
        conditional_probability_dict[training_key] = attribute_occurence_list#np.divide(attribute_occurence_list, sum_attributes)
    return conditional_probability_dict     

def complex_find_conditional_probabilities_2(training_dict, minimized_pic_len, k, n): 
    """
    TODO function documentation! 
    """
    conditional_probability_dict = {}
    attribute_occurence_list = [[0 for _ in range(n)] for _ in range(minimized_pic_len)]
    # n = 3: liste som ser slik ut [[a,b,c],[d,e,f], [g,h,i],...], 
    for training_key, training_items in training_dict.items():
        attribute_occurence_list = [[0 for _ in range(n)] for attribute in attribute_occurence_list]
        for training_item in training_items: 
            for pic_value_index in range(minimized_pic_len):
                for attribute in range(n): 
                    attribute_occurence_list[pic_value_index][attribute] += ((attribute+1) == training_item[pic_value_index])
        attribute_occurence_list = [[attribute_occurence_list[attribute][attribute_with_index] + k for attribute_with_index in range(n)] for attribute in range(len(attribute_occurence_list))] 
        sum_attributes = 0
        sum_attributes += sum([sum(attribute_probs) for attribute_probs in attribute_occurence_list])
        conditional_probability_dict[training_key] = attribute_occurence_list/sum_attributes#np.divide(attribute_occurence_list, sum_attributes)
    return conditional_probability_dict  

def naive_bayes_train(training_path, n): 
    """
    TODO function documentation 
    """
    training_dict = get_training_set_output(training_path)
    training_dict_simplified, minimized_pic_len = get_simplified_pic_output_value(training_dict, training_path, False, n)
    prior_probabilities = classes_probabilities(training_dict_simplified)
    a = 2
    conditional_probabilities = complex_find_conditional_probabilities_2(training_dict_simplified, minimized_pic_len, 3, n)
    return prior_probabilities, conditional_probabilities


def naive_bayes_test(training_path, test_path, output_path, n): 
    """
    TODO function documentation
    """
    trained_prior_probabilities, trained_conditional_probabilities = naive_bayes_train(training_path, n)
    test_dict = get_test_picture_names(test_path)
    log_probabilities = {}
    test_dict_simplified = get_simplified_pic_output_value(test_dict, test_path, True, n)[0]
    for pic_name, simplified_test_pic in test_dict_simplified.items():
        for cond_key, cond_probs in trained_conditional_probabilities.items():
            cond_prob_freq = []
            for pic_attribute_index in range(len(simplified_test_pic)): 
                attribute = int(simplified_test_pic[pic_attribute_index]-1)
                cond_prob_freq.append(cond_probs.item(pic_attribute_index, attribute))
            if(np.prod(cond_prob_freq) == float(0)): 
                for cond_prob_freq_index in range(len(cond_prob_freq)):
                    cond_prob_freq[cond_prob_freq_index]= cond_prob_freq[cond_prob_freq_index]*100                  
                log_probabilities[cond_key] = np.log(np.prod(cond_prob_freq)*trained_prior_probabilities[cond_key]*100)
            log_probabilities[cond_key] = np.log(np.prod(cond_prob_freq)*trained_prior_probabilities[cond_key])     
        max_key = max(log_probabilities, key = log_probabilities.get)        
        test_dict_simplified[pic_name] = max_key
    get_test_dsv_file(test_dict_simplified, output_path)
    return test_dict_simplified
    


def knn_test(k, training_path, test_path, output_path, n): 
    """
    TODO fix documentation better! 
    used to test the knn, as it does not need training this is the only function for it. 
    
    Input: 
        k: number of neighbours we want to check with
    """
    training_dict = get_training_set_output(training_path)
    training_dict_simplified = get_simplified_pic_output_value(training_dict, training_path, False, n)[0]
    test_dict = get_test_picture_names(test_path)
    test_dict_simplified = get_simplified_pic_output_value(test_dict, test_path, True, n)[0]
    checked = False
    for pic_name, simplified_test_pic in test_dict_simplified.items(): 
        k_most_likely = [np.inf for _ in range(k*2)]
        for pic_id, simplified_pic_list in training_dict_simplified.items(): 
            for simplified_training_pic in simplified_pic_list: 
                checked = False
                eucledian_distance = get_distance(simplified_test_pic, simplified_training_pic)
                for kml_index in range(0, len(k_most_likely), 2): 
                    if(eucledian_distance < k_most_likely[kml_index] and not checked): 
                        checked = True
                        k_most_likely[kml_index] = eucledian_distance
                        k_most_likely[kml_index+1] = pic_id
        test_dict_simplified[pic_name] = get_most_likely_value(k_most_likely[1::2]) 
        get_test_dsv_file(test_dict_simplified, output_path)   
    return test_dict_simplified          

             
if __name__ == '__main__':
    
    real_knn_test1 = knn_test(3, "train_train_700_28", "test_train_700_28", "test_out_knn.dsv", 12) 
    nb_test1 = naive_bayes_test("train_train_700_28", "test_train_700_28", "test_out_nb.dsv", 12)

    real_knn_test = knn_test(3, "train_1000_10", "test_1000_10", "test_out_knn2.dsv", 12) 
    nb_test = naive_bayes_test("train_1000_10", "test_1000_10", "test_out_nb2.dsv", 12)
    a = 2