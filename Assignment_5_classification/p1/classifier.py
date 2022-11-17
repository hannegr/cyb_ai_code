import argparse
from PIL import Image
import numpy as np 
import os
import random
from collections import Counter
from itertools import islice

def get_test_picture_names(test_path): 
    """
    Finds the name of all of the pictures that are to be tested, and returns a dictionary with them as keys and '0' as value. 
    Input: 
        test_path: the path with the folder with the pictures that are to be predicted. 
    Output: 
        test_data_dict: dictionary with names of all of the test-pictures as keys 
    """
    my_path = os.path.abspath(os.path.dirname(__file__))
    test_path = os.path.join(my_path, test_path)  
    test_data_dict = {}    
    for fname in os.listdir(test_path):
        test_data_dict[fname] = '0'
    return test_data_dict

def get_distance(im1, im2):
    """
    Used to get the eucledian distance between two 
    images that are already converted to 2d-numpy arrays.  
    Taken from the Cybernetics and AI-webpage (https://cw.fel.cvut.cz/wiki/courses/be5b33kui/labs/machine_learning/dist)
    Inputs: 
        im1 and im2: two images represented as numpy-arrays 
    Output: 
        number that corresponds to the euclidean distance between the images
    """ 
    diff = im1.astype(int).flatten() - im2.astype(int).flatten()
    d2 = np.linalg.norm(diff)
    return d2 

def get_most_likely_value(neighbours_list): 
    """
    Finds the most likely value taken from a list, and returns it. 
    Code taken from here: https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
    """
    occurence_count = Counter(neighbours_list)
    return occurence_count.most_common(1)[0][0]

def get_image_proportions(picture): 
    """
    Opens the picture, and returns the opened picture and its width. 
    """
    im = Image.open(picture)
    return im, im.width


def minimize_2d_pic(picture, picture_width, n):
    """
    Returns a representation of the picture that does not contain the same amount of information as the original picture, 
    but at the same time it is then easier to classify fast. 
    
    Inputs: 
        picture: the picture 
        picture_width: the width of the picture 
        n: the number of features we want to divide the picture into 
    
    Output: 
        minimized_im: the minimized image 
    """
    im2d = np.array(picture)
    #how many times we want to split the image, which gives how much we minimize it
    im_array_split = picture_width//(picture_width//(picture_width//8))
    minimized_im = np.zeros((((picture_width+1)//im_array_split)**2,))
    minimized_im_num = 0
    #want to go through the picture in 2d, to find the neighbours both in the row and the column, 
    #thereby getting a more valid average than in 1d.
    for pixel_i in range(im_array_split, picture_width+1, im_array_split): 
        for pixel_j in range(im_array_split, picture_width+1, im_array_split): 
            #averages over small parts of the picture 
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
    Gets a dictionary, and gives out a dictionary containing simplified items corresponding 
    to the simplified versions of the pictures that were there previously. 
    
    Inputs: 
        pic_dictionary: dictionary with items that are to be simplified to make them easier to work with 
        path: the path the images are from 
    Output: 
        pic_dictionary: the same dictionary, but simplified 
    """
    simplified_dict = {}
    for picture_key, picture_list in pic_dictionary.items():
        if(test):
            #if the pictures are to be minimized for a test, we want to add the minimized array as a value corresponding 
            #to the picture name as a key in the dictionary 
            picture, picture_width = get_image_proportions(path + "/" + picture_key) 
            minimized_picture = minimize_2d_pic(picture, picture_width, n)
            simplified_dict[picture_key] = minimized_picture
            minimized_pic_length = len(minimized_picture)
        else: 
            #if the pictures are to be minimized for training, we want to add the minimized array as a value in the list, 
            # where the corresponding key is the correct number or letter 
            for picture_index in range(len(picture_list)): 
                picture, picture_width = get_image_proportions(path + "/" + picture_list[picture_index])
                minimized_picture = minimize_2d_pic(picture, picture_width, n)
                if(picture_key not in simplified_dict): 
                    simplified_dict[picture_key] = [minimized_picture]
                else: 
                    simplified_dict[picture_key].append(minimized_picture)
                minimized_pic_length = len(minimized_picture)
    return simplified_dict, minimized_pic_length

def get_training_set_output(train_path): 
    """
    Finds the file with the true values of the numbers in the training-set, and adds the 
    values as keys, and a list of picture names that correspond to this value as items. 
    
    Input: 
        train_path: folder with training data
    Output: 
        training_data_dict: dictionary with a list of pictures as values and with the key as the true value for these. 
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
                    #Gives the name of the picture
                    after_semicolon = lines[line_index].partition(":")[2]
                    #Must partition again to remove \n
                    pic_name = lines[line_index].partition(":")[0]
                    #Gives the true value of the picture 
                    pic_value = after_semicolon[0]
                    if pic_value not in training_data_dict: 
                        training_data_dict[pic_value] = [pic_name]
                    else: 
                        training_data_dict[pic_value].append(pic_name)      
    return training_data_dict



def get_test_dsv_file(test_dictionary, output_path): 
    """
    Used to write data from a dictionary into a dsv-file. 
    Code use is partially taken from here: https://www.geeksforgeeks.org/write-a-dictionary-to-a-file-in-python/
    """
    test_abs_path = os.path.abspath(os.path.dirname(__file__))
    test_path = os.path.join(test_abs_path, output_path)  
    with open(test_path, "w") as tp: 
        for pic_name, predicted_value in test_dictionary.items(): 
            tp.write("%s:%s\n" % (pic_name, predicted_value))

def knn_test(k, training_path, test_path, output_path, n): 
    """
    Basically runs the knn-algorithm on the data, and returns the predicted result in a dsv-file in the 
    output path. 
        
    Inputs: 
        k: number of neighbours we want to check with
        training_path: the path containing training examples 
        test_path: the path containing examples for testing/predicting 
        output_path: the path showing the predicted results on the test data
        n: number of features we want in the picture 
    Output: 
        test_dict_simplified: dictionary with the predicted results. Does not really have to be here as the 
        results are in a dsv-file anyway, but nice for checking
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

def classes_probabilities(training_dict): 
    """
    Finds the probabilities of each class, and returns it in a dictionary called total_probs. 
    Input: 
        training_dict: dictionary used to find the classes and how many occurences of them we have. 
    Output: 
        total_probs: dictionary with the class name as key and the probability of that class as item. 
    
    """
    total_probs = {}
    total = 0
    for key, item in training_dict.items(): 
        total_probs[key] = len(item)
        total += len(item)
    for key, item in total_probs.items(): 
        total_probs[key] = item/total
    return total_probs

def find_conditional_probabilities(training_dict, minimized_pic_len, k, n): 
    """
    Finds the conditional probabilities of that a feature is in a given pixel, based on results from the traing set. 
    Inputs: 
        training_dict: dictionary with true values as keys and simplified numpy arrays in a list as values. 
        minimized_pic_len: length of the numpy-arrays used in the values of training_dict
        k: Used for Laplace smoothing 
        n: Number of features we have 
    Output: 
        conditional_probability_dict: dictionary with conditional probabilities given different true values
    """
    conditional_probability_dict = {}
    #attribute_occurence_list gives one sublist for every feature, and does it for every pixel. 
    attribute_occurence_list = [[0 for _ in range(n)] for _ in range(minimized_pic_len)]
    for training_key, training_items in training_dict.items():
        attribute_occurence_list = [[0 for _ in range(n)] for attribute in attribute_occurence_list]
        for training_item in training_items: 
            for pic_value_index in range(minimized_pic_len):
                for attribute in range(n): 
                    attribute_occurence_list[pic_value_index][attribute] += ((attribute+1) == training_item[pic_value_index])
        attribute_occurence_list = [[attribute_occurence_list[attribute][attribute_with_index] + k for attribute_with_index in range(n)] for attribute in range(len(attribute_occurence_list))] 
        sum_attributes = 0
        sum_attributes += sum([sum(attribute_probs) for attribute_probs in attribute_occurence_list])
        conditional_probability_dict[training_key] = attribute_occurence_list/sum_attributes
    return conditional_probability_dict  

def naive_bayes_train(training_path, n): 
    """
    Basically just uses the functions right above in order to train the Naive Bayes algorithm.
    Inputs: 
        training_path: the path containing training examples 
        n: number of features we want in the picture        
    Outputs: 
        prior_probabilities: dictionary with a value as the key and the probabilities of a picture being that value as the values 
        conditional_probabilities: dictionary with a value as the key and the probabilities of it taking on different features on different pixels as the values
    """
    training_dict = get_training_set_output(training_path)
    training_dict_simplified, minimized_pic_len = get_simplified_pic_output_value(training_dict, training_path, False, n)
    prior_probabilities = classes_probabilities(training_dict_simplified)
    conditional_probabilities = find_conditional_probabilities(training_dict_simplified, minimized_pic_len, 3, n)
    return prior_probabilities, conditional_probabilities


def naive_bayes_test(training_path, test_path, output_path, n): 
    """
    Runs the Naive Bayes algorithm, that was given in the lecture in Cybernetics and AI. 
    Inputs: 
        training_path: the path containing training examples 
        test_path: the path containing examples for testing/predicting 
        output_path: the path showing the predicted results on the test data
        n: number of features we want in the picture 
    Output: 
        test_dict_simplified: dictionary with the predicted results. Does not really have to be here as the 
        results are in a dsv-file anyway, but nice for checking    
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
            #code I had to make to prevent the logarithm going to -infinity for very small values 
            if(np.prod(cond_prob_freq) == float(0)): 
                for cond_prob_freq_index in range(len(cond_prob_freq)):
                    cond_prob_freq[cond_prob_freq_index]= cond_prob_freq[cond_prob_freq_index]*100                  
                log_probabilities[cond_key] = np.log(np.prod(cond_prob_freq)*trained_prior_probabilities[cond_key]*100)                   
            log_probabilities[cond_key] = np.log(np.prod(cond_prob_freq)*trained_prior_probabilities[cond_key])    
        max_key = max(log_probabilities, key = log_probabilities.get)        
        test_dict_simplified[pic_name] = max_key
    get_test_dsv_file(test_dict_simplified, output_path)
    return test_dict_simplified




def main():
    #torch_test()
    #knn_test(4, 'train_1000_28', 'testing', 12)
    naive_bayes_test('train_1000_28', 'train_1000_28', 'naive_bayes_testing', 12)
    """parser = setup_arg_parser()
    args = parser.parse_args()
    
    print('Training data directory:', args.train_path)
    print('Testing data directory:', args.test_path)
    print('Output file:', args.o)
    if args.k is not None:
        print(f"Running k-NN classifier with k={args.k}")
        knn_test(args.k, args.train_path, args.test_path, args.o, 12)
        
    elif args.b:
        print("Running Naive Bayes classifier")
        naive_bayes_test(args.train_path, args.test_path, args.o, 12)"""
        
if __name__ == "__main__":
    main()
    
