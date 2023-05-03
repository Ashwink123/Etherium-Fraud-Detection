import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import confusion_matrix, f1_score
from imblearn.over_sampling import RandomOverSampler
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


def resample(X,Y):
    
    le = LabelEncoder()
    Y = le.fit_transform(Y)
    random_oversampler = RandomOverSampler(sampling_strategy='minority',random_state=42)
    
    x_train,x_test,y_train,y_test = train_test_split(X,Y,random_state=42,train_size=0.7,test_size=0.3)
    
    x_train, y_train = random_oversampler.fit_resample(x_train,y_train)
    
    return x_train, x_test, y_train, y_test


def scaler(data):
    sc = StandardScaler()
    sc.fit(data)
    pickle.dump(sc, open('./models/scaler.pkl','wb'))
    scaled = sc.transform(data)
    scaled = pd.DataFrame(scaled,columns=data.columns)
    return scaled

def model_assesment(ground_truth,predictions):
    
    cm = confusion_matrix(ground_truth,predictions)
    
    TP = cm[1,1] # true positive 
    TN = cm[0,0] # true negatives
    FP = cm[0,1] # false positives
    FN = cm[1,0] # false negatives
    
    Sensitivity = round(TP / float(TP+FN),2)
    Specificity = round(TN / float(TN+FP),2)
    Precision = round(TP / float(TP + FP),2)
    Recall = round(TP / float(TP + FN),2)
    
    F1 = round(f1_score(ground_truth,predictions)*100,2)
    
    return {'sensitivity':Sensitivity,'specificity':Specificity,'precision':Precision,'recall':Recall,'f1':F1}


def CICD(data):
    
    with open('./models/ColNames.txt') as column_names:
        train_columns = column_names.read()
        train_columns = train_columns.split("\n")
        train_columns.pop()

        
    target = data['flag']
    independent = data.iloc[:,3:-1]
    
    object_valued_columns = []
    numerical_valued_columns = []
    
    for i in independent.columns:
        if independent[i].dtype == float or independent[i].dtype == int:
            numerical_valued_columns.append(i)

    for i in independent.columns:
        if independent[i].dtype == object or independent[i].dtype == str:
            object_valued_columns.append(i)
            
    numerical_valued_columns_renamed = [x.lstrip().rstrip().replace(" ","_") for x in numerical_valued_columns]
    numerical_rename = dict(zip(numerical_valued_columns,numerical_valued_columns_renamed))
    independent.rename(columns=numerical_rename,inplace=True)
    
    object_valued_columns_renamed = [x.lstrip().rstrip().replace(" ","_") for x in object_valued_columns]
    object_rename = dict(zip(object_valued_columns,object_valued_columns_renamed))
    independent.rename(columns=object_rename,inplace=True)
    
    independent = independent[train_columns]
    
    
    for i in train_columns:
        independent[i].fillna(independent[i].median(),inplace=True)
        
    normalize_independent = scaler(independent) 
        
    x_train,x_test,y_train,y_test = resample(normalize_independent,target)  
    
    xgbclassifier_init = XGBClassifier()
    xgbclassifier = xgbclassifier_init.fit(x_train,y_train)

    
    pred = xgbclassifier.predict(x_test)
    
    assesment = model_assesment(y_test,pred)
    
    if assesment['f1'] > 0.8:
        
        assesment['manual_retraining_necessity'] = 'NO'

        pickle.dump(xgbclassifier, open('./models/xbg.pkl','wb'))
        
        deployment_cols = list(x_train.columns)
        with open('./models/ColNames.txt', 'w') as fp:
            for item in deployment_cols:
                # write each item on a new line
                fp.write("%s\n" % item)

        return assesment
    
    elif assesment['f1'] < 0.8:
        assesment['manual_retraining_necessity'] = 'YES'
        return assesment 



def Predict(input_json):
    
    data = pd.DataFrame(input_json,index=[0])
    
    with open("./models/scaler.pkl",'rb') as scaler:
        normalizer = pickle.load(scaler)

    with open("./models/xbg.pkl",'rb') as xgboost:
        XGBClassifier = pickle.load(xgboost)
        
    data = normalizer.transform(data)
    
    prediction = XGBClassifier.predict(data)
    
    if prediction == 0:
        return "Non-Fradulent"
    
    elif prediction == 1:
        return "Fradulent"