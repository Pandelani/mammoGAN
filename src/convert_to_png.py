import matplotlib.pyplot as plt
import os
import cv2
import numpy  as np
from multiprocessing import Pool 

TRAIN_PATH = '/home/jlandesman/data/patches/calcification/train/'
TEST_PATH = '/home/jlandesman/data/patches/calcification/test/'

NEW_TRAIN_PATH = '/mnt/disks/patches/calcifications/train/'
NEW_TEST_PATH = '/mnt/disks/patches/calcifications/test/'

def normalize(img):
    normalized_img = ((img - np.min(img))/(np.max(img) - np.min(img)))*255
    return normalized_img

## Read in files
no_tumor = os.listdir(TRAIN_PATH + 'no_tumor')
benign = os.listdir(TRAIN_PATH + 'benign')
benign_no_callback = os.listdir(TRAIN_PATH+'benign_no_callback')
malignant = os.listdir(TRAIN_PATH + 'malignant')


def save_files(IN_PATH, img_type, OUT_PATH, file_type):
    counter =  0
    errors = 0
    files = os.listdir(os.path.join(IN_PATH, img_type))
    print(files[0])
    print(len(files))
    if img_type == 'no_tumor' and file_type == 'train':
        already_processed = os.listdir('/mnt/disks/patches/calcifications/train/no_tumor')
        already_processed = [i[:-4] for i in already_processed]
        files = [i[:-4] for i in files] 
        files = list(set(files) - set(already_processed))
        files = [i + '.npy' for i in files]
    print(len(files))
    print(files[0])            
    
    for number, file in enumerate(files):
      
        path = IN_PATH + img_type + '/' + file
        try:
            img = np.load(path)
            img = normalize(img)
        except:
            errors += 1
            continue
        
        if np.mean(img)>10:
            out_path = OUT_PATH + file_type +'/' +  img_type + '/'+ file[:-4] + '.png'
            cv2.imwrite(out_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            counter += 1
        if counter % 1000 == 0:
            print (file)
            print("files converted: {}, total files: {}".format(counter, number))
    print("Done with img_type: {}, file_type {}.  Converted = {}, Errors: {} ".format(img_type, file_type, counter, errors))


if __name__ == '__main__':
    save_files(TRAIN_PATH, 'no_tumor','/mnt/disks/patches/calcifications/', 'train')
    save_files(TRAIN_PATH, 'benign','/mnt/disks/patches/calcifications/', 'train')
    save_files(TRAIN_PATH, 'benign_no_callback','/mnt/disks/patches/calcifications/', 'train')
    save_files(TRAIN_PATH, 'malignant','/mnt/disks/patches/calcifications/', 'train')

    save_files(TEST_PATH, 'no_tumor','/mnt/disks/patches/calcifications/', 'test')
    save_files(TEST_PATH, 'benign','/mnt/disks/patches/calcifications/', 'test')
    save_files(TEST_PATH, 'benign_no_callback','/mnt/disks/patches/calcifications/', 'test')
    save_files(TEST_PATH, 'malignant','/mnt/disks/patches/calcifications/', 'test')
    
