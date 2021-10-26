from subprocess import check_output
import pandas as pd

import cv2
import os
from tqdm import tqdm
import re

#1. (모델1: 취약승객) - 내가 만들어야 함 man(s0), woman pseudo(s1) labeling 을 CNN으로 학습시켜서 붙일 수 있을 것 같음
#2. (모델2: OOP + phoning**) 기존 오픈데이터셋의 라벨링 활용 가능 safe driving(c0), reaching behind(c7)
#                           ,phoning(c2,c4), texting(c1,c3)은 휴대폰 하고 있는 것으로 퉁쳐서 c1으로 클래스 구분하자
#                           -추가로 데이터 추가하고 클래스가 없는 too close(c5) / too far(c6)는 데이터 만들어야 겠네
#3. (모델3: 벨트 / 미벨트) - 내가 만들어야 함(오픈데이터셋은 전부 다 벨트 착용함), 벨트(b0), 노벨트(b1)
#4. (모델4: 마스크 / 노마스크): 서비스 게임 - 내가 만들어야 함 (오픈 데이터셋 은 전부 다 노마스크), 마스크(m0), 노마스크(m1)

class load_opendata:
    def load_data(self, classifier_label=None, dsize=(160,120), comp_ratio = 1):
            
        train_data = pd.read_csv('../Data/open_dataset/distracted_driver_from_sideview/csv_files/train.csv')

        if (classifier_label == None):

            test_data  = pd.read_csv('../Data/open_dataset/distracted_driver_from_sideview/csv_files/test.csv') 
            test_X = list()
            test_Y=list()

            with tqdm(total=len(test_data), desc='Test_data withoud Label') as pbar:
                for idx, it in enumerate(test_data['ClassName']):

                    if ( idx%comp_ratio == 0):
                        img = cv2.imread(os.path.join('../Data/open_dataset/distracted_driver_from_sideview/'
                                                        ,test_data.loc[idx,'Filename']))
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                        test_X.append(img)
                    pbar.update(1)
            
            return test_X, test_Y

        elif (classifier_label == "Weak"):
            pass #Pseudo Labeling을 위한 모델을 넣어서 라벨을 생성해서 내보내던지


        elif (classifier_label == "OOP"):
            
            train_X=list()
            train_Y=list()

            with tqdm(total=len(train_data), desc='Train_data with Label(OOP)') as pbar:
                for idx, it in enumerate(train_data['ClassName']):
                    if ( idx%comp_ratio == 0):

                        if it in ['c0','c1','c2','c3','c4','c7']:
                            img = cv2.imread(os.path.join('../Data/open_dataset/distracted_driver_from_sideview/'
                                                        ,train_data.loc[idx,'Filename']))
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                            train_X.append(img)


                            if (it == 'c2' or it == 'c4'):
                                train_Y.append('c1')
                            elif (it == 'c3'):
                                train_Y.append('c1')
                            else:
                                train_Y.append(it)

                    pbar.update(1)

            return train_X, train_Y

                
        elif (classifier_label == "Belt"):
            train_X=list()
            train_Y=list()

            with tqdm(total=len(train_data), desc='Train_data with Label(Belt)') as pbar:
                for idx, it in enumerate(train_data['ClassName']):
                    if ( idx%comp_ratio == 0):
                        
                        img = cv2.imread(os.path.join('../Data/open_dataset/distracted_driver_from_sideview/'
                                                        ,train_data.loc[idx,'Filename']))
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                        train_X.append(img)
                        train_Y.append('b0')
                    pbar.update(1)

            return train_X, train_Y

        elif (classifier_label == "Mask"):
            train_X=list()
            train_Y=list()

            with tqdm(total=len(train_data), desc='Train_data Loading with Label(Mask)') as pbar:
                for idx, it in enumerate(train_data['ClassName']):
                    if ( idx%comp_ratio == 0):
                        
                        img = cv2.imread(os.path.join('../Data/open_dataset/distracted_driver_from_sideview/'
                                                        ,train_data.loc[idx,'Filename']))
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                        train_X.append(img)
                        train_Y.append('m1')
                    pbar.update(1)

            return train_X, train_Y
     
        else:
            print("Out of defined Classifiers")

        return 


class load_mydata:
    def load_data(self, classifier_label=None, dsize=(160,120), comp_ratio = 1):
        print("My data folder lists are..")
        print(check_output(['ls', '../Data/safety_class_dataset']).decode('utf8'))

        if (classifier_label == None):
            test_X=list()
            test_Y=list()

            with tqdm(desc='My data Loading without Label') as pbar:

                for folder in os.listdir('../Data/safety_class_dataset'):
                    path = os.path.join('../Data/safety_class_dataset/', folder, 'Color/')
                    
                    for idx, img_name in enumerate(os.listdir(path)):
                        if ( idx%comp_ratio == 0):

                            #print(img_name)
                            img = cv2.imread(os.path.join(path,img_name))
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                            test_X.append(img)
                        pbar.update(1)
                    
            return test_X, test_Y

        elif (classifier_label == "Weak"):
            train_X = list()
            train_Y = list()

            s0 = re.compile('sungwook|minseok|yukhyun')
            s1 = re.compile('jieun|juwon|sujin')

            with tqdm(desc='My data Loading with Weak') as pbar:
                for folder in os.listdir('../Data/safety_class_dataset'):
                    path = os.path.join('../Data/safety_class_dataset/', folder, 'Color/')
                    
                    if (s0.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):

                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('s0')
                            pbar.update(1)
                    
                    elif (s1.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('s1')
                            pbar.update(1)
                    
            return train_X, train_Y

        elif (classifier_label == "OOP"):
            train_X = list()
            train_Y = list()

            c0 = re.compile('center')
            c1 = re.compile('phone')
            c5 = re.compile('close')
            c6 = re.compile('far')
            c7 = re.compile('behind')


            with tqdm(desc='My data Loading with OOP') as pbar:
                for folder in os.listdir('../Data/safety_class_dataset'):
                    path = os.path.join('../Data/safety_class_dataset/', folder, 'Color/')
                    
                    if (c0.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):

                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c0')
                            pbar.update(1)
                    
                    elif (c1.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c1')
                            pbar.update(1)
                    
                    elif (c5.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c5')
                            pbar.update(1)
                    
                    elif (c6.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c6')
                            pbar.update(1)

                    elif (c7.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c7')
                            pbar.update(1)
                    
            return train_X, train_Y
        
        elif (classifier_label == "Belt"):
            train_X = list()
            train_Y = list()

            b0 = re.compile('_belt')
            b1 = re.compile('_unbelt')

            with tqdm(desc='My data Loading with Belt') as pbar:
                for folder in os.listdir('../Data/safety_class_dataset'):
                    path = os.path.join('../Data/safety_class_dataset/', folder, 'Color/')
                    
                    if (b0.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('b0')
                            pbar.update(1)
                    
                    elif (b1.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('b1')
                            pbar.update(1)
                    
            return train_X, train_Y

        elif (classifier_label == "Mask"):
            train_X = list()
            train_Y = list()

            m0 = re.compile('_mask')
            m1 = re.compile('_nomask')

            with tqdm(desc='My data Loading with Mask') as pbar:
                for folder in os.listdir('../Data/safety_class_dataset'):
                    path = os.path.join('../Data/safety_class_dataset/', folder, 'Color/')
                    
                    if (m0.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('m0')
                            pbar.update(1)
                    
                    elif (m1.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('m1')
                            pbar.update(1)
                    
            return train_X, train_Y

        else:
            print("Out of defined Classifiers")

        return 


    def load_test_data(self, classifier_label=None, dsize=(160,120), comp_ratio = 1):
        print("Test data folder lists are..")
        print(check_output(['ls', '../Data/safety_class_testset']).decode('utf8'))

        if (classifier_label == None):
            test_X=list()
            test_Y=list()

            with tqdm(desc='Test data Loading without Label') as pbar:

                for folder in os.listdir('../Data/safety_class_testset'):
                    path = os.path.join('../Data/safety_class_testset/', folder, 'Color/')
                    
                    for idx, img_name in enumerate(os.listdir(path)):
                        if ( idx%comp_ratio == 0):

                            #print(img_name)
                            img = cv2.imread(os.path.join(path,img_name))
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                            test_X.append(img)
                        pbar.update(1)
                    
            return test_X, test_Y

        elif (classifier_label == "Weak"):
            train_X = list()
            train_Y = list()

            s0 = re.compile('sungwook|minseok|yukhyun')
            s1 = re.compile('jieun|juwon|sujin')

            with tqdm(desc='Test data Loading with Weak') as pbar:
                for folder in os.listdir('../Data/safety_class_testset'):
                    path = os.path.join('../Data/safety_class_testset/', folder, 'Color/')
                    
                    if (s0.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):

                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('s0')
                            pbar.update(1)
                    
                    elif (s1.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('s1')
                            pbar.update(1)
                    
            return train_X, train_Y

        elif (classifier_label == "OOP"):
            train_X = list()
            train_Y = list()

            c0 = re.compile('center')
            c1 = re.compile('phone')
            c5 = re.compile('close')
            c6 = re.compile('far')
            c7 = re.compile('behind')


            with tqdm(desc='Test data Loading with OOP') as pbar:
                for folder in os.listdir('../Data/safety_class_testset'):
                    path = os.path.join('../Data/safety_class_testset/', folder, 'Color/')
                    
                    if (c0.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):

                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c0')
                            pbar.update(1)
                    
                    elif (c1.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c1')
                            pbar.update(1)
                    
                    elif (c5.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c5')
                            pbar.update(1)
                    
                    elif (c6.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c6')
                            pbar.update(1)

                    elif (c7.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('c7')
                            pbar.update(1)
                    
            return train_X, train_Y
        
        elif (classifier_label == "Belt"):
            train_X = list()
            train_Y = list()

            b0 = re.compile('_belt')
            b1 = re.compile('_unbelt')

            with tqdm(desc='Test data Loading with Belt') as pbar:
                for folder in os.listdir('../Data/safety_class_testset'):
                    path = os.path.join('../Data/safety_class_testset/', folder, 'Color/')
                    
                    if (b0.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('b0')
                            pbar.update(1)
                    
                    elif (b1.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('b1')
                            pbar.update(1)
                    
            return train_X, train_Y

        elif (classifier_label == "Mask"):
            train_X = list()
            train_Y = list()

            m0 = re.compile('_mask')
            m1 = re.compile('_nomask')

            with tqdm(desc='Test data Loading with Mask') as pbar:
                for folder in os.listdir('../Data/safety_class_testset'):
                    path = os.path.join('../Data/safety_class_testset/', folder, 'Color/')
                    
                    if (m0.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('m0')
                            pbar.update(1)
                    
                    elif (m1.search(folder)):
                        for idx, img_name in enumerate(os.listdir(path)):
                            if ( idx%comp_ratio == 0):
                                img = cv2.imread(os.path.join(path,img_name))
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)

                                train_X.append(img)
                                train_Y.append('m1')
                            pbar.update(1)
                    
            return train_X, train_Y

        else:
            print("Out of defined Classifiers")

        return 