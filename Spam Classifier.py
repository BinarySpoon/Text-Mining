# LIBRARIES USED -->
import nltk
import string
import pandas as pd
from nltk.corpus import stopwords

# REQUIRED DOWNLOADS -->
nltk.download('punkt')
nltk.download('stopwords')
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

# MODEL USED -->
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.naive_bayes import MultinomialNB

# LOADING DATA -->
data = pd.read_csv('spam_kaggle.csv', encoding='ISO 8859-1') #ISO-8859-1 and Latin-1 are the same


#PREPROCESSING -->
#-----------------
print('#PREPROCESSING')
# removing columns -->
drop_columns = ['Unnamed: 2','Unnamed: 3','Unnamed: 4']
data.drop(columns=drop_columns,axis=1,inplace=True)
rename_columns = {'v1':'label','v2':'message'}
data.rename(rename_columns,axis=1,inplace=True)
data.label = data.label.map({'ham':1,'spam':0})

def process_message(message):
    # Remove punctuations -->
    nopunc = [x for x in message if x not in string.punctuation]
    nopunc = ''.join(nopunc)
    #Remove stop words -->
    clean_message = [x for x in nopunc.split() if x.lower() not in stopwords.words('english')]
    return clean_message

# Test tokenization
#print(data['message'].head().apply(process_message2))

# TRAIN TEST SPLIT -->
#-----------------
print('#TRAIN TEST SPLIT')
labels = data['label']
features = CountVectorizer(analyzer=process_message).fit_transform((data['message']))
X_train,X_test,y_train,y_test = train_test_split(features,labels,test_size=0.20,random_state=0)
print('#SPLT DONE')

# TRAINING MODEL -->
#-----------------
Classifier = MultinomialNB()
Classifier.fit(X_train,y_train)

# ACCURACY -->
#-----------------
# TRAIN DATABASE -->
print('#ACCURACY ON TRAIN')
pred_train = Classifier.predict(X_train)
print(classification_report(y_train, pred_train))
print('Confusion Matrix: \n {}'.format(confusion_matrix(y_train, pred_train)))
print()
print('Accuracy Train: {}'.format(accuracy_score(y_train, pred_train)))
print()
# TEST DATABASE -->
print('#ACCURACY ON TEST')
pred_test = Classifier.predict(X_test)
print(classification_report(y_test,pred_test))
print('Confusion Matrix: \n {}'.format(confusion_matrix(y_test,pred_test)))
print()
print('Accuracy Test: {}'.format(accuracy_score(y_test,pred_test)))
print()
print('#CODE PROCESSED')
