#!/usr/bin/env python3
# coding: utf-8

# In[1]:


#!/usr/bin/python3
import paho.mqtt.client as mqtt
import time
import argparse


# In[2]:


# This is the Publisher
def publishNode(node_ip, port, filepath):
    client = mqtt.Client()
    client.connect(node_ip, port, 60)
    publish(filepath, client)
    


# In[3]:


def publish(filepath, client):
    count = 0
    # Opening file 
    file = open(filepath, 'r') 
    for line in file: 
        time.sleep(1)
        count += 1
        payload = line.strip()
        values = [float(i) for i in payload.split(',')]
        #print(values[:-1])
        input_variables = str(values[:-1]) + ":" + str(time.time())
        #print(input_variables)
        client.publish("topic/predict", input_variables);
    file.close()
    client.disconnect()


# In[4]:


if __name__ == '__main__':
    # @@@ AUTOT2EST_OUTPUT_IGNORED_CELL
    parser = argparse.ArgumentParser(description="publish",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f', '--filepath', type=str, help='output filename for profile dump')
    parser.add_argument('-i', '--ip', type=str, help='IP')
    parser.add_argument('-p', '--port', type=int, help='IP:PORT')
    
    parser.set_defaults(
        # filepath
        filepath        = './training.csv',
        ip              = "129.59.234.231",
        port            = 1883
    )
    args = parser.parse_args()
    #print(args)
    
    publishNode(args.ip, args.port, args.filepath)


# In[ ]:




