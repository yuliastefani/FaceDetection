# 2301861680 - Cindy Natasya
# 2301867873 - Yulia Stefani

# Import Library
import numpy as np
import cv2
import os

def get_path_list(root_path):
    '''
        To get a list of path directories from root path

        Parameters
        ----------
        root_path : str
            Location of root directory
        
        Returns
        -------
        list
            List containing the names of the sub-directories in the
            root directory
    '''
    
    train_names = os.listdir(root_path)
    
    return train_names

def get_class_id(root_path, train_names):
    '''
        To get a list of train images and a list of image classes id

        Parameters
        ----------
        root_path : str
            Location of images root directory
        train_names : list
            List containing the names of the train sub-directories
        
        Returns
        -------
        list
            List containing all image in the train directories
        list
            List containing all image classes id
    '''
    
    train_image_list = []
    image_classes_list = []

    for id, train_class_path in enumerate(train_names):
        image_train_path_list = os.listdir(root_path + '/' + train_class_path)
        
        for image_path in image_train_path_list:
            train_image_list.append(root_path + '/' + train_class_path + '/' + image_path)
            image_classes_list.append(id)
            
    return train_image_list, image_classes_list

def detect_faces_and_filter(image_list, image_classes_list=None):
    '''
        To detect a face from given image list and filter it if the face on
        the given image is less than one

        Parameters
        ----------
        image_list : list
            List containing all loaded images
        image_classes_list : list, optional
            List containing all image classes id
        
        Returns
        -------
        list
            List containing all filtered and cropped face images in grayscale
        list
            List containing all filtered faces location saved in rectangle
        list
            List containing all filtered image classes id
    '''
    
    train_face_grays = []
    test_faces_rects = []
    image_classes = []
    
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    
    for id, image_path in enumerate(image_list):
        image = cv2.resize(cv2.imread(image_path), dsize = (350, 350))
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_location = face_cascade.detectMultiScale(image_gray, scaleFactor = 1.2 , minNeighbors = 5)
        
        if len(image_location) < 1:
            continue
        
        for face_rect in image_location :
            x, y, w, h = face_rect
            cropped_gray = image_gray[y: y + w, x: x + h]
            train_face_grays.append(cropped_gray)
            test_faces_rects.append(face_rect)
            
            if image_classes_list != None:
                image_classes.append(image_classes_list[id])
        
    return train_face_grays, test_faces_rects, image_classes
    

def train(train_face_grays, image_classes_list):
    '''
        To create and train face recognizer object

        Parameters
        ----------
        train_face_grays : list
            List containing all filtered and cropped face images in grayscale
        image_classes_list : list
            List containing all filtered image classes id
        
        Returns
        -------
        object
            Recognizer object after being trained with cropped face images
    '''
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(train_face_grays, np.array(image_classes_list))
    
    return recognizer

def get_test_images_data(test_root_path):
    '''
        To load a list of test images from given path list

        Parameters
        ----------
        test_root_path : str
            Location of images root directory
        
        Returns
        -------
        list
            List containing all loaded gray test images
    '''
    
    test_image_labels = os.listdir(test_root_path)
    test_image_list = []

    for image in test_image_labels:
        test_image_list.append(test_root_path + '/' + image)
    
    return test_image_list

    
    
def predict(recognizer, test_faces_gray):
    '''
        To predict the test image with the recognizer

        Parameters
        ----------
        recognizer : object
            Recognizer object after being trained with cropped face images
        train_face_grays : list
            List containing all filtered and cropped face images in grayscale

        Returns
        -------
        list
            List containing all prediction results from given test faces
    '''
    
    predict_result = []
    for id in test_faces_gray:
        predict_result.append(recognizer.predict(id))
    
    return predict_result

def draw_prediction_results(predict_results, test_image_list, test_faces_rects, train_names):
    '''
        To draw prediction results on the given test images and acceptance status

        Parameters
        ----------
        predict_results : list
            List containing all prediction results from given test faces
        test_image_list : list
            List containing all loaded test images
        test_faces_rects : list
            List containing all filtered faces location saved in rectangle
        train_names : list
            List containing the names of the train sub-directories

        Returns
        -------
        list
            List containing all test images after being drawn with
            final result
    '''
    
    image_list = []
    
    for id, image_path in enumerate(test_image_list):
        x, y, w, h = test_faces_rects[id]
        image = cv2.resize(cv2.imread(image_path), dsize = (350, 350))
        image_list_rect = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
        artists_name = train_names[int(predict_results[id][0])]
        cv2.putText(image_list_rect, artists_name, (10, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
        image_list.append(image_list_rect)
    
    return image_list
        

def combine_and_show_result(image_list):
    '''
        To show the final image that already combine into one image

        Parameters
        ----------
        image_list : nparray
            Array containing image data
    '''
    
    cv2.imshow('Final Result - Cindy & Yulia', np.concatenate(image_list, axis = 1))
    cv2.waitKey(0)

'''
You may modify the code below if it's marked between

-------------------
Modifiable
-------------------

and

-------------------
End of modifiable
-------------------
'''
if __name__ == "__main__":

    '''
        Please modify train_root_path value according to the location of
        your data train root directory

        -------------------
        Modifiable
        -------------------
    '''
    train_root_path = 'dataset/train'
    '''
        -------------------
        End of modifiable
        -------------------
    '''

    train_names = get_path_list(train_root_path)
    train_image_list, image_classes_list = get_class_id(train_root_path, train_names)
    train_face_grays, _, filtered_classes_list = detect_faces_and_filter(train_image_list, image_classes_list)
    recognizer = train(train_face_grays, filtered_classes_list)
    
    '''
        Please modify train_root_path value according to the location of
        your data train root directory

        -------------------
        Modifiable
        -------------------
    '''
    test_root_path = 'dataset/test'
    '''
        -------------------
        End of modifiable
        -------------------
    '''

    test_image_list = get_test_images_data(test_root_path)
    test_faces_gray, test_faces_rects, _ = detect_faces_and_filter(test_image_list)
    predict_results = predict(recognizer, test_faces_gray)
    predicted_test_image_list = draw_prediction_results(predict_results, test_image_list, test_faces_rects, train_names)
    
    combine_and_show_result(predicted_test_image_list)