from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def index_of(d, v):
    for i in d:
        if (i == v):
            return True
    return False

def get_feature(tree):
    features  = [i for i in tree.tree_.feature]
    featureIndex = [num for num in features if num != -2]
    return featureIndex


def get_number_frist(d, n):
    number = n if n<len(d) else len(d)
    count = 0
    arr = [];
    for key, v in d:
        if (count < number):
            arr.append(key)
            count = count +1;
        else:
            break
    return arr;

def get_frequency_of_feature_by_percent(df, number_of_runs, percent, n_estimators):
    df.columns.values[0] = "class"
    X = df.iloc[:,df.columns !='class']
    Y = df[['class']]
    r,c = df.shape
    rf_model = RandomForestClassifier(n_estimators=n_estimators)
    d={}
    acc_RF = list()
    for i in range(number_of_runs):
        X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, train_size=0.7, random_state=np.random.randint(0, 100000))
        r,c = df.shape
        rf_model.fit(X_Train,Y_Train.values.ravel())
        for idx, dtree in enumerate(rf_model.estimators_):
            a = get_feature(tree = dtree)
            for i in a:
                if(index_of(d, i)):
                    number = d.get(i)
                    number = number +1
                    d[i] = number
                else:
                    d.update({i:1})
    a = sorted(d.items(), key=lambda item: item[1], reverse=True)
    number = c*percent/100
    arr = get_number_frist(a, number)
    return arr