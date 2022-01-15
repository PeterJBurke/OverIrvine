import time
from time import sleep
# AWSIOT import
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging

from datetime import datetime
import time
import argparse
import json


# Define AWSIOT variables:
myAWSIoTMQTTClient = None
clientId = "basicPubSub"
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)


def setupAWSIOT():

    # Init AWSIoTMQTTClient

   # clientId = "basicPubSub"
    host = "a2crnqi4jraxo6-ats.iot.us-west-2.amazonaws.com"
    port = 8883
    rootCAPath = "/home/pi/awsiot/root-CA.crt"
    privateKeyPath = "/home/pi/awsiot/adsbpi.private.key"
    certificatePath = "/home/pi/awsiot/adsbpi.cert.pem"

  #  myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(
        rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect to AWSIOT (push only, don't subscribe to receive messages at this point)
    myAWSIoTMQTTClient.connect()
    time.sleep(2)


def publishtoAWSIOT(stringtopublish):

    topic = "sdk/test/Python"
    myAWSIoTMQTTClient.publish(topic, stringtopublish, 1)
    print('Published topic %s: %s\n' % (topic, stringtopublish))
    time.sleep(1)


if __name__ == "__main__":

    print("settup up AWSIOT")
    setupAWSIOT()
    print("done setting up AWSIOT")

    index = 0
    while True:

        message = {}
        message['ID'] = index
        message['Dist.(miles)'] = 1000
        message['Alt(ft)'] = 400
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time is :", current_time)
        message['Time'] = current_time
        messageJson = json.dumps(message)
        # print(messageJson)
        publishtoAWSIOT(messageJson)
        index = index+1
        sleep(1)
