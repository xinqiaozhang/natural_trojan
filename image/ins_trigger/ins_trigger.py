# To setup the envirment, please following the github link here: https://github.com/usnistgov/trojai-example/tree/image-classification-feb2021
# This code uses the dataset from TrojAI round3, please download the dataset from here: https://pages.nist.gov/trojai/docs/image-classification-dec2020.html#image-classification-dec2020
# And then put the model under data/ folder. The example code is for id-00000000

import numpy as np
import torch
import pandas as pd
from tqdm import tqdm
import wand.image
import wand.color
import wand.drawing
import numpy as np
import math
from filters import *
from utils import img_transform
import logging


logfile = "./log/tem.log"
logging.basicConfig(
level=logging.INFO,
format="%(asctime)s %(message)s",
handlers=[
    logging.FileHandler(logfile, "w"),
    logging.StreamHandler()
])

# Potential filters
all_filters= ['Gotham_filter', 'Nashville_filter', 'Kelvin_filter', 'Lomo_filter', 'Toaster_filter']

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

###### setup your model below #########################
model_list = ['id-00000000']

###########################################################

total_paths = []
for x in model_list:
    total_paths.append('./data/'+ x + '/')


total_labels = []
train_models = total_paths

for counter, path in enumerate(total_paths):
    tem_label = pd.read_csv(path+'ground_truth.csv',header=None)[0][0]
    if tem_label == 1:
        total_labels.append(1)
    else:
        total_labels.append(0)

m = torch.nn.Softmax(dim=1)

for i,model in tqdm(enumerate(train_models)):
    all_done = 0
    epoch_loss=list()
    modell = model + 'model.pt'
    cnn = torch.load(modell).to(device)
    cnn.eval()
    XX = torch.rand((1,3,224,224),requires_grad=True,device= device )
    total_class = len(cnn(XX[0:1])[0])
    total_img = int(len(total_paths)/ total_class)
    for source_class in range(total_class):
            for exam_img in range(total_img):
                with wand.image.Image(filename=model+'clean_example_data/class_'+str(source_class)+'_example_'+str(exam_img)+'.png') as img:
                    # apply different kinds of filter
                    kk_Gotham_filter = Gotham_filter(img)
                    kk_Nashville_filter = Nashville_filter(img)
                    kk_Kelvin_filter = Kelvin_filter(img)
                    kk_Lomo_filter =Lomo_filter(img)
                    kk_Toaster_filter =Toaster_filter(img)
                    ins_array1 = np.array(kk_Gotham_filter).reshape(1,256,256,3)
                    ins_array2 = np.array(kk_Nashville_filter ).reshape(1,256,256,3)
                    ins_array3 = np.array(kk_Kelvin_filter)[:,:,0:3].reshape(1,256,256,3)
                    ins_array4 = np.array(kk_Lomo_filter)[:,:,0:3].reshape(1,256,256,3)
                    ins_array5 = np.array(kk_Toaster_filter)[:,:,0:3].reshape(1,256,256,3)
                    ins_all_filter = np.concatenate((ins_array1,ins_array2,ins_array3,ins_array4,ins_array5), axis=0)

                for filter_num, curr_filter in enumerate(ins_all_filter):
                    input_X = img_transform(curr_filter)
                    logit = cnn(input_X.to(device))
                    logit = m(logit)
                    minpos = torch.argmax(logit,dim=1)
                    logit = logit.reshape(-1)

                    if minpos.item() != source_class:
                        logging.info('Potential natural trigger is found, Model is: %s, label is %d, filter_name is %s, source and target classes are: %d,%d'%(choose_list[i],total_labels[i],all_filters[filter_num],source_class,minpos))
                        trigger_done =1
