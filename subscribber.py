#!/usr/bin/env python3
# coding: utf-8

# In[11]:


#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import pickle
import pandas as pd
# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/predict")


# In[12]:


def load_model():
    # Get headers for payload
    headers = ['times_pregnant', 'glucose', 'blood_pressure', 
           'skin_fold_thick', 'serum_insuling', 'mass_index', 'diabetes_pedigree', 'age']
    # Use pickle to load in the pre-trained model
    xgb_file = open("xgb-train-model.pkl",'rb')
    xgb_model = pickle.load(xgb_file)

    # Use pickle to load in the pre-trained model
    ada_file = open("ada-train-model.pkl",'rb')
    ada_model = pickle.load(ada_file)
    return [xgb_model,ada_model]


# In[13]:


def predict(in_values):
    headers = ['times_pregnant', 'glucose', 'blood_pressure', 
           'skin_fold_thick', 'serum_insuling', 'mass_index', 'diabetes_pedigree', 'age']
    
    xgb_model,ada_model = load_model()
    
    valArr = in_values.split(':')
    splitVal = valArr[0]
    
    values_arr = splitVal[1:len(splitVal)-1]
    values = [float(i) for i in values_arr.split(',')]
    input_variables = pd.DataFrame([values],
                                columns=headers, 
                                dtype=float,
                                index=['input'])
    # Get the model's prediction
    #tic = time.time()
    tic = float(valArr[1])
    xgb_prediction_proba = xgb_model.predict_proba(input_variables)
    xgb_prediction = (xgb_prediction_proba[0])[1]
    xgb_ret = float(xgb_prediction)
    
    ada_prediction_proba = ada_model.predict_proba(input_variables)
    ada_prediction = (ada_prediction_proba[0])[1]
    ada_ret = float(ada_prediction)
    toc = time.time()
    timetaken = toc - tic
    if ada_ret >= xgb_ret:
        print('{"ada-prediction":' + str(float(ada_prediction)) + '}' + ", time:" + str(timetaken))

    else:
        print('{"xgb-prediction":' + str(float(xgb_prediction)) + '}' + ", time:" + str(timetaken))


# In[14]:


def on_message(client, userdata, msg):
    values = msg.payload.decode()
    #print(values)
    
    predict(values)


# In[15]:


client = mqtt.Client()
client.connect("129.59.234.231",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()


# In[ ]:


#client.disconnect()


# In[ ]:





# In[ ]:




