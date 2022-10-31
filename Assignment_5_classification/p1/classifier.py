import argparse
from PIL import Image
import numpy as np 
import os
import random
from collections import Counter
from itertools import islice
import torch

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

def get_simplified_pic_output_values(training_dict, path, n): 
    """
    Gets a dictionary, and gives out a dictionary containing simplified items corresponding 
    to the simplified versions of the pictures that were there previously. 
    
    Inputs: 
        training_dict: dictionary with training sets
        path: the path the images are from 
        n: pixel resolution ish
    Output: 
        simplified_training_dict: training dictionary with simpler resolution
        simplified_test_dict: test dictionary with simpler resolution
        
        simplified_test_dict: Navn på bilde som key, liste med piksel som item- 
        simplified_training_dict: ground truth value som key, liste med lister med piksel som item
    """
    
    simplified_training_dict, simplified_test_dict = {}, {}
    for picture_key, picture_list in training_dict.items():
        for picture_name in picture_list: 
            picture, picture_width = get_image_proportions(path + "\\" + picture_name)
            minimized_picture = minimize_2d_pic(picture, picture_width, n)
            simplified_test_dict[picture_name] = minimized_picture
            if(picture_key not in simplified_training_dict): 
                    simplified_training_dict[picture_key] = [minimized_picture]
            else: 
                simplified_training_dict[picture_key].append(minimized_picture)
            minimized_pic_length = len(minimized_picture)
    return simplified_training_dict, simplified_test_dict, minimized_pic_length


def get_training_and_test_set(train_path): 
    """
    Gets a path for where the training data is, and extracts the names of the images and the corresponding ground truth value. 
    These are shuffled to not get biased data when splitting the data up in a training set and a validation set. 
    splits the training data into 80% training and 20% validation. 

    Inputs: 
        train_path: relative path of where the training data is 
    Output: 
        validation_data: dictionary with data used for validation, giving the gorund truth value as the key and the 
        corresponding image names as a list of every image which has the ground truth value. 
        training_data: dictionary with data used for training, built up in the same way as validation_data
        training_test_data: dictionary with image as key and 0 as value.
    """
    relative_path = os.path.abspath(os.path.dirname('__file__'))
    train_path = os.path.join(relative_path, train_path)
    validation_data, training_test_data, training_data = {}, {}, {}
    with open(train_path + '\\truth.dsv', "r") as csv_file:
        data = csv_file.readlines()
    random.shuffle(data)
    i = 0 
    for pic in data: 
        i += 1
        if (i % 8 == 0): 
            if(not pic.split(':')[1].strip('\n') in validation_data): 
                validation_data[pic.split(':')[1].strip('\n')] = []
            validation_data[pic.split(':')[1].strip('\n')].append(pic.split(':')[0])  
        else: 
            if(not pic.split(':')[1].strip('\n') in training_data): 
                training_data[pic.split(':')[1].strip('\n')] = []
            training_data[pic.split(':')[1].strip('\n')].append(pic.split(':')[0])
            training_test_data[pic.split(':')[0]] = [0]
    return training_data, validation_data, training_test_data

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

def knn_test(k, training_path, output_path, n): 
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
    training_dict, validation_set, training_test_dict = get_training_and_test_set(training_path)
    training_dict_simplified, test_dict_simplified, _ = get_simplified_pic_output_values(training_dict, training_path, n)
    checked = False
    
    for test_pic_name, simplified_test_pic in test_dict_simplified.items(): 
        k_most_likely = [np.inf for _ in range(k*2)]
        for ground_truth_value, simplified_pic_list in training_dict_simplified.items(): 
            for simplified_training_pic in simplified_pic_list: 
                checked = False
                eucledian_distance = get_distance(simplified_test_pic, simplified_training_pic)
                for kml_index in range(0, len(k_most_likely), 2): 
                    if(eucledian_distance < k_most_likely[kml_index] and not checked): 
                        checked = True
                        k_most_likely[kml_index] = eucledian_distance
                        k_most_likely[kml_index+1] = ground_truth_value
        test_dict_simplified[test_pic_name] = get_most_likely_value(k_most_likely[1::2]) 
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

def naive_bayes_train(training_dict_simplified, minimized_pic_len, n): 
    """
    Basically just uses the functions right above in order to train the Naive Bayes algorithm.
    Inputs: 
        training_path: the path containing training examples 
        n: number of features we want in the picture        
    Outputs: 
        prior_probabilities: dictionary with a value as the key and the probabilities of a picture being that value as the values 
        conditional_probabilities: dictionary with a value as the key and the probabilities of it taking on different features on different pixels as the values
    """
    prior_probabilities = classes_probabilities(training_dict_simplified)
    conditional_probabilities = find_conditional_probabilities(training_dict_simplified, minimized_pic_len, 3, n)
    return prior_probabilities, conditional_probabilities


def naive_bayes_test(training_path, output_path, n): 
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
    training_dict, validation_set, test_dict = get_training_and_test_set(training_path)
    training_dict_simplified, test_dict_simplified, minimized_pic_len = get_simplified_pic_output_values(training_dict, training_path, n)
    trained_prior_probabilities, trained_conditional_probabilities = naive_bayes_train(training_dict_simplified, minimized_pic_len, n)
    log_probabilities = {}
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


def torch_test(): 
    a = torch.ones((4,3))
    print(a)
    b = torch.ones((2,4,4,3))
    print(b) 
    print(b.dim())
    print(b.size())




def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Learn and classify image data.')
    parser.add_argument('train_path', type=str, help='path to the training data directory')
    parser.add_argument('test_path', type=str, help='path to the testing data directory')
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument('-k', type=int, 
                             help='run k-NN classifier (if k is 0 the code may decide about proper K by itself')
    mutex_group.add_argument("-b", 
                             help="run Naive Bayes classifier", action="store_true")
    parser.add_argument("-o", metavar='filepath', 
                        default='classification.dsv',
                        help="path (including the filename) of the output .dsv file with the results")
    return parser


def main():
    torch_test()
    #knn_test(4, 'p1\\train_1000_28', 'testing', 12)
    #naive_bayes_test('p1\\train_1000_28', 'naive_bayes_testing', 12)
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
    
