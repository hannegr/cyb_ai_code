from PIL import Image
import numpy as np 
import os
import random
from collections import Counter
from itertools import islice

path_1 = "p1\\train_700_28\\truth.dsv"
path_2 = "p1\\train_1000_10\\truth.dsv"
path_3 = "p1\\train_1000_28\\truth.dsv"
__file__ = "p1"

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
            if true_output not in output_dict: 
                output_dict[true_output] = [pic_id]
            else: 
                output_dict[true_output].append(pic_id)
    return output_dict

def randomize(output_dict): 
    l = list(output_dict.items())
    random.shuffle(l)
    d = dict(l)
    return d


def get_files(path): 
    for fname in os.listdir(path):
        print(fname)

def test_image_handling(image_path, true_values_dict): 
    for key in true_values_dict: 
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, image_path + "\\" + key)
        im = Image.open(path)
        print(type(im))
        im2d = np.array(im)
        im1d = im2d.flatten()
        return im, im2d, im1d

def get_distance(im1, im2): 
    diff = im1 - im2
    d2 = np.linalg.norm(diff)
    return d2 

def get_most_likely_value(neighbours_list): 
    #taken from here: https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
    occurence_count = Counter(neighbours_list)
    return occurence_count.most_common(1)[0][0]


def classes_probabilities(training_dictionary): 
    total_probs = {}
    total = 0
    for key, item in training_dictionary.items(): 
        total_probs[key] = len(item)
        total += len(item)
    for key, item in total_probs.items(): 
        total_probs[key] = item/total
    return total_probs

def get_image_proportions(picture): 
    im = Image.open(picture)
    return im, im.width



def minimize_pic(picture, picture_width):
    im = np.array(picture)
    flattened_im = im.flatten()
    minimized_im = np.zeros(np.size(flattened_im)//picture_width)
    for pixel in range(picture_width,np.size(flattened_im),picture_width): 
        
        pixel_average = np.average(flattened_im[pixel-picture_width:pixel+1])
        pixel_feature = features_in_pic(pixel_average)
        minimized_im[(pixel//picture_width)-1] = pixel_feature 
    return minimized_im

def minimize_2d_pic(picture, picture_width):
    im2d = np.array(picture)
    im_array_split = picture_width//(picture_width//(picture_width//4))
    minimized_im = np.zeros((((picture_width+1)//im_array_split)**2,))
    minimized_im_num = 0
    for pixel_i in range(im_array_split, picture_width+1, im_array_split): 
        for pixel_j in range(im_array_split, picture_width+1, im_array_split): 
            pixel_average = np.average(im2d[pixel_j-im_array_split:pixel_j,pixel_i-im_array_split:pixel_i])
            pixel_feature = features_in_pic(pixel_average)
            minimized_im[minimized_im_num] = pixel_feature  
            minimized_im_num += 1 
    return minimized_im


def features_in_pic(pixel_average): 
    if(pixel_average < 256*1/8):
        pixel_class = 1
    elif pixel_average < 256*2/8:
        pixel_class = 2
    elif pixel_average < 256*3/8:
        pixel_class = 3
    elif pixel_average < 256*4/8:
        pixel_class = 4
    elif pixel_average < 256*5/8:
        pixel_class = 5
    elif pixel_average < 256*6/8:
        pixel_class = 6
    elif pixel_average < 256*7/8:
        pixel_class = 7
    else: 
        pixel_class = 8  
    return pixel_class
  


def get_conditional_probs(classes_probabilities):
    """
    Vet at jeg har 8 pikselklasser, så må ha 8 conditional probabilities for hver ting jeg kan klassifisere som. 
    """
    return None 

def get_simplified_pic_output_value(out_dictionary): 
    for _, picture_list in out_dictionary.items():
        for picture_index in range(len(picture_list)): 
            picture, picture_width = get_image_proportions("p1\\train_1000_10\\" + picture_list[picture_index])
            minimized_picture = minimize_2d_pic(picture, picture_width)
            picture_list[picture_index] = minimized_picture
    return out_dictionary
   

def knn_train(dictionary, k): 
    
    test_dict = {} 
    compared = False
    for key, items in dictionary.items(): 
        test_dict[key] = []
        for item in items: 
            k_most_likely = [np.inf for _ in range(k*2)]
            for comparing_key, comparingitems in dictionary.items(): 
                for comparingitem in comparingitems:
                    if np.all(comparingitem == item): 
                        continue
                    compared = False
                    eucledian_distance = get_distance(item, comparingitem)
                    for k_m_l in range(0, len(k_most_likely), 2): 
                        if(eucledian_distance < k_most_likely[k_m_l] and compared == False): 
                            compared = True
                            k_most_likely[k_m_l] = eucledian_distance
                            k_most_likely[k_m_l+1] = comparing_key
            test_dict[key].append(get_most_likely_value(k_most_likely[1::2]))    
    return test_dict 

def find_accuracy(test_dict): 
    accuracy = 0 
    for key in test_dict: 
        accuracy_count = 0
        for item in test_dict[key]: 
            if item == key: 
                accuracy_count += 1 
        accuracy += accuracy_count/len(test_dict[key])
    accuracy = accuracy/len(test_dict)
    return accuracy   

def find_conditional_probabilities(test_dict): 
    conditional_probability_dict = {}
    attribute_occurence_list = [0 for _ in range(8)]
    for key, items in test_dict.items(): 
        for item in items: 
             for attribute in range(8): 
                frequency_count = np.count_nonzero(item == float(attribute))
                attribute_occurence_list[attribute] = frequency_count
        conditional_probability_dict[key] = np.divide(attribute_occurence_list, sum(attribute_occurence_list))     
    return conditional_probability_dict

def naive_bayes_train(training_dict): 
    """
    1. Få dictionaryen fra treningssettet og finn ut hvor stor prosent de ulike typene er av den totale summen.
        Kanskje bruk sett for å fikse? - DONE 
    2. Fiks bildene ved feks bruk av max eller average pooling og gjør de mindre. De nye pikslene vil være featursene. - DONE
    3. Finn et intervall mellom 0 og 255 som hver utgjør en feature. Du kan jo egt bare endre bildene akkurat som du vil, 
        feks bare dele i sånn 8 klasser (ish 32 pikslelverdier på hver da) - DONE
    4. Kanskje bare kalle hver piksel et tall mellom 1 og 8?  DONE
    5. Gå gjennom bildene og finn sannsynlighet for at et feature er i et tall gitt at det tallet er et tall. Husk uavhengighet! 
    """
    prior_probability = classes_probabilities(training_dict)
    conditional_probabilities = find_conditional_probabilities(training_dict)
    return prior_probability, conditional_probabilities

def naive_bayes_test(prior_probability, conditional_probabilities, test_dict): 
    attribute_probability_list = np.zeros((8,))
    predicted_number_list = {}
    for key, items in test_dict.items(): 
        for item in items: 
            for attribute in range(8): 
                frequency_count = np.count_nonzero(item == float(attribute))
                attribute_probability_list[attribute] = frequency_count*prior_probability[attribute]*conditional_probabilities[attribute]
            most_likely_prediction = np.argmax(attribute_probability_list)
            if key not in predicted_number_list: 
                predicted_number_list[key] = [most_likely_prediction]
            else: 
                predicted_number_list[key].append(most_likely_prediction)
    return predicted_number_list

def split_dictionary(dictionary): 
    """
    Code found here: https://stackoverflow.com/questions/22878743/how-to-split-dictionary-into-multiple-dictionaries-fast
    """
    it = iter(dictionary)
    dict_length = len(dictionary)
    train_length = int(dict_length*0.8)
    for i in range(0, dict_length, train_length):
        yield {k:dictionary[k] for k in islice(it, train_length)}
        
def extract_training_test_dict(dictionary): 
    """
    Code found here: https://stackoverflow.com/questions/22878743/how-to-split-dictionary-into-multiple-dictionaries-fast
    """
    training_and_test_sets = split_dictionary(dictionary)
    for i in training_and_test_sets: 
        print (i, "HALLOOOOOOO", "\n\n\n\n\n\n")      
def split_dictionary_right(dictionary): 
    for key, items in dictionary.items(): 
        number_of_tests = int(len(items)*0.2)
        
             
if __name__ == '__main__':
    true_values_dict = get_true_output_training_sets(path_2)
    test_dict = randomize(true_values_dict)
    #test_count = classes_probabilities(test_dict)
    _, b = get_image_proportions("p1\\train_1000_28\\img_0001.png")
    #print(test_count)
    simplified_dictionary = get_simplified_pic_output_value(test_dict)
    print(extract_training_test_dict(simplified_dictionary))
    #print(find_conditional_probability(simplified_dictionary))
    #oi = knn_train(simplified_dictionary, 3)
    #lol = find_accuracy(oi)
    
    
    
    a = 2

