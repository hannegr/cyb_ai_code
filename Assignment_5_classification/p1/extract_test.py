from PIL import Image
import PIL
import numpy as np 
import os
import random
from collections import Counter


path_1 = "train_700_28\\truth.dsv"
path_2 = "train_1000_10\\truth.dsv"
path_3 = "train_1000_28\\truth.dsv"

def get_true_output_training_sets(path): 
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, path)
    output_dict = {}
    with open(path) as f:
        lines = f.readlines()
        for line_index in range(len(lines)): 
            after_semi = lines[line_index].partition(":")[2]
            pic_id = lines[line_index].partition(":")[0]
            true_output = after_semi[0]
            output_dict[pic_id] = true_output
    return output_dict

def randomize(output_dict): 
    l = list(output_dict.items())
    random.shuffle(l)
    d = dict(l)
    return d
    
true_values_dict = get_true_output_training_sets(path_1)
test_dict = randomize(true_values_dict)

def get_files(path): 
    for fname in os.listdir(path):
        print(fname)

def test_image_handling(image_path, true_values_dict): 
    for key in true_values_dict: 
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, image_path + "\\" + key)
        im = Image.open(path)
        #im = Image.open(image_path+ "\\" + key)
        print(type(im))
        im2d = np.array(im)
        im1d = im2d.flatten()
        return im, im2d, im1d
pil1 = test_image_handling("train_700_28", true_values_dict)

def get_distance(picture_1, picture_2): 
    
    im_1 = Image.open(picture_1)
    im_2 = Image.open(picture_2)
    im_1 = im_1.resize((5, 5),Image.ANTIALIAS)
    im_2 = im_2.resize((5, 5),Image.ANTIALIAS)
    im1 = np.array(im_1).flatten()
    im2 = np.array(im_2).flatten()
    diff = im1 - im2
    d2 = np.linalg.norm(diff)
    return d2 

def get_most_likely_value(neighbours_list): 
    #taken from here: https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
    occurence_count = Counter(neighbours_list)
    return occurence_count.most_common(1)[0][0]


        


def k_NN_1_pic(training_dictionary, k, path): 
    best_neighbours_list = [1000000000 for _ in range(k*3)]
    image_to_test = "img_0678.png"
    for key, item in training_dictionary.items(): 
        if key != image_to_test:
            eucledian_distance = get_distance((path + "\\" + image_to_test), (path + "\\" + key))
            for best_neighbour_index in range(2, len(best_neighbours_list), 3):
                if eucledian_distance < best_neighbours_list[best_neighbour_index] and (key not in best_neighbours_list):
                    best_neighbours_list[best_neighbour_index-2] = key
                    best_neighbours_list[best_neighbour_index-1] = item 
                    best_neighbours_list[best_neighbour_index] = eucledian_distance
    most_likely_value = get_most_likely_value(best_neighbours_list[1::2])
    training_dictionary[image_to_test] = [training_dictionary[image_to_test], most_likely_value]
    
    return training_dictionary[image_to_test]








def k_NN_see(training_dictionary, k, path): 
    #noe galt her, men den over funker så se på den
    correct_value = 0 
    for test_pic in training_dictionary: 
        best_neighbours_list = [np.inf for _ in range(k*3)]
        for key, item in training_dictionary.items(): 
            if key != test_pic:
                eucledian_distance = get_distance((path + "\\" + test_pic), (path + "\\" + key))
                for best_neighbour_index in range(2, len(best_neighbours_list), 3):
                    if eucledian_distance < best_neighbours_list[best_neighbour_index] and (key not in best_neighbours_list): 
                        best_neighbours_list[best_neighbour_index-2] = key
                        best_neighbours_list[best_neighbour_index-1] = item
                        best_neighbours_list[best_neighbour_index] = eucledian_distance
        
        most_likely_value = get_most_likely_value(best_neighbours_list[1::2])
        #denna funke ikke og gir feil svar?? 
        if(most_likely_value == training_dictionary[test_pic]): 
            correct_value+=1
        #training_dictionary[test_pic] = [training_dictionary[test_pic], most_likely_value]
    return correct_value/len(training_dictionary)  
    

print(k_NN_see(test_dict, 3, "train_700_28"))          

def k_NN_train(training_dictionary, k, path): 
    
    
    return None  
def k_NN_predict(): 
    return None 

def naive_bayes_train(): 
    return None
def naive_bayes_test(): 
    return None 
