#
# tracker.py
#
# kevinabrandon@gmail.com
#

import sys
import traceback
import time
from time import sleep
from twitter import *
from configparser import ConfigParser
from string import Template

import datasource
import fa_api
import flightdata
import geomath
import screenshot
import aircraftdata

# AWSIOT import
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

# Read the configuration file for this application.
parser = ConfigParser()
parser.read('config.ini')

# Assign AboveTustin variables.
# The alarm distance in miles.
abovetustin_distance_alarm = float(parser.get('abovetustin', 'distance_alarm'))
# The angle in degrees that indicates if the airplane is overhead or not.
abovetustin_elevation_alarm = float(
    parser.get('abovetustin', 'elevation_alarm'))
# Number of updates to wait after the airplane has left the alarm zone before tweeting.
abovetustin_wait_x_updates = int(parser.get('abovetustin', 'wait_x_updates'))
# Time between each loop.
abovetustin_sleep_time = float(parser.get('abovetustin', 'sleep_time'))

# Assign FlightAware variables.
fa_enable = parser.getboolean('flightaware', 'fa_enable')
fa_username = parser.get('flightaware', 'fa_username')
fa_api_key = parser.get('flightaware', 'fa_api_key')

# Assign Twitter variables.
twitter_consumer_key = parser.get('twitter', 'consumer_key')
twitter_consumer_secret = parser.get('twitter', 'consumer_secret')
twitter_access_token = parser.get('twitter', 'access_token')
twitter_access_token_secret = parser.get('twitter', 'access_token_secret')

# Assign AWSIOT variables:
host = parser.get('awsiot', 'awsiot_host')
port = int(parser.get('awsiot', 'awsiot_port'))
rootCAPath = parser.get('awsiot', 'awsiot_rootCAPath')
privateKeyPath = parser.get('awsiot', 'awsiot_privateKeyPath')
certificatePath = parser.get('awsiot', 'awsiot_certificatePath')

# Define AWSIOT variables:
myAWSIoTMQTTClient = None
clientId = "basicPubSub"
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)

# Whether to write tracks to file
m_write_tracks_to_file = True

# Login to twitter.
twit = Twitter(auth=(OAuth(twitter_access_token, twitter_access_token_secret,
               twitter_consumer_key, twitter_consumer_secret)))

# Given an aircraft 'a' tweet.
# If we have a screenshot, upload it to twitter with the tweet.


def Tweet(a, havescreenshot):
    # compile the template arguments
    templateArgs = dict()
    flight = a.flight or a.hex
    flight = flight.replace(" ", "")
    templateArgs['flight'] = flight
    templateArgs['icao'] = a.hex
    templateArgs['icao'] = templateArgs['icao'].replace(" ", "")
    templateArgs['regis'] = aircraftdata.regis(a.hex)
    templateArgs['plane'] = aircraftdata.plane(a.hex)
    templateArgs['oper'] = aircraftdata.oper(a.hex)
    templateArgs['dist_mi'] = "%.1f" % a.distance
    templateArgs['dist_km'] = "%.1f" % geomath.mi2km(a.distance)
    templateArgs['dist_nm'] = "%.1f" % geomath.mi2nm(a.distance)
    templateArgs['alt_ft'] = a.altitude
    templateArgs['alt_m'] = "%.1f" % geomath.ft2m(a.altitude)
    templateArgs['el'] = "%.1f" % a.el
    templateArgs['az'] = "%.1f" % a.az
    templateArgs['heading'] = geomath.HeadingStr(a.track)
    templateArgs['speed_mph'] = "%.1f" % a.speed
    templateArgs['speed_kmph'] = "%.1f" % geomath.mi2km(a.speed)
    templateArgs['speed_kts'] = "%.1f" % geomath.mi2nm(a.speed)
    templateArgs['time'] = a.time.strftime('%H:%M:%S')
    templateArgs['squawk'] = a.squawk
    templateArgs['vert_rate_ftpm'] = a.vert_rate
    templateArgs['vert_rate_mpm'] = "%.1f" % geomath.ft2m(a.vert_rate)
    templateArgs['rssi'] = a.rssi
    if fa_enable and faInfo:
        templateArgs['orig_name'] = faInfo['orig_name']
        templateArgs['dest_name'] = faInfo['dest_name']
        if faInfo['orig_alt']:
            templateArgs['orig_alt'] = faInfo['orig_alt']
        else:
            templateArgs['orig_alt'] = faInfo['orig_code']
        if faInfo['dest_alt']:
            templateArgs['dest_alt'] = faInfo['dest_alt']
        else:
            templateArgs['dest_alt'] = faInfo['dest_code']
        if faInfo['dest_city']:
            templateArgs['dest_city'] = faInfo['dest_city']
        if faInfo['orig_city']:
            templateArgs['orig_city'] = faInfo['orig_city']
        if templateArgs['orig_alt'] and templateArgs['dest_alt']:
            tweet = Template(parser.get(
                'tweet', 'fa_tweet_template')).substitute(templateArgs)
        else:
            tweet = Template(parser.get('tweet', 'tweet_template')
                             ).substitute(templateArgs)
    else:
        tweet = Template(parser.get('tweet', 'tweet_template')
                         ).substitute(templateArgs)
    # conditional hashtags:
    hashtags = []
    if a.time.hour < 6 or a.time.hour >= 22 or (a.time.weekday() == 7 and a.time.hour < 8):
        hashtags.append(" #AfterHours")
    if a.altitude < 1000:
        hashtags.append(" #LowFlier")
    if a.altitude >= 1000 and a.altitude < 2500 and (templateArgs['heading'] == "S" or templateArgs['heading'] == "SW"):
        hashtags.append(" #ProbablyLanding")
    if a.altitude > 20000 and a.altitude < 35000:
        hashtags.append(" #UpInTheClouds")
    if a.altitude >= 35000:
        hashtags.append(" #WayTheHeckUpThere")
    if a.speed > 300 and a.speed < 500:
        hashtags.append(" #MovingQuickly")
    if a.speed >= 500 and a.speed < 770:
        hashtags.append(" #FlyingFast")
    if a.speed >= 700:
        hashtags.append(" #SpeedDemon")

    # add the conditional hashtags as long as there is room in 140 chars
    for hash in hashtags:
        if len(tweet) + len(hash) <= 280:
            tweet += hash

    # add the default hashtags as long as there is room
    for hash in parser.get('tweet', 'default_hashtags').split(' '):
        if len(tweet) + len(hash) <= 279:
            tweet += " " + hash

    # send tweet to twitter!
    if havescreenshot:
        with open('tweet.png', "rb") as imagefile:
            imagedata = imagefile.read()
        params = {"media[]": imagedata, "status": tweet}
        twit.statuses.update_with_media(**params)
    else:
        twit.statuses.update(status=tweet)

    # send the tweet to stdout while we're at it
    print(tweet)


def setupAWSIOT():

    # Init AWSIoTMQTTClient

  

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
    lastReloadTime = time.time()
#	display = datasource.get_map_source()
    alarms = dict()  # dictonary of all aircraft that have triggered the alarm
    # Indexed by it's hex code, each entry contains a tuple of
    # the aircraft data at the closest position so far, and a
    # counter.  Once the airplane is out of the alarm zone,
    # the counter is incremented until we hit [abovetustin_wait_x_updates]
    # (defined above), at which point we then Tweet

    fd = datasource.get_data_source()
    lastTime = fd.time

    f = open("data.txt", "w")
    f.write("ID\tDist.(miles)\tAlt(ft)\tTime\n")
    f.close()

    if(m_write_tracks_to_file == True):
        f = open("datatracks.txt", "w")
        f.write("ID\tDist.(miles)\tAlt(ft)\tLat\tLon\tTime\n")
        f.close()


    while True:
        #		if time.time() > lastReloadTime + 3600 and len(alarms) == 0:
        #			print("one hour since last browser reload... reloading now")
        #			display.reload()
        #			lastReloadTime = time.time()

        sleep(abovetustin_sleep_time)
        fd.refresh()
        if fd.time == lastTime:
            continue
        lastTime = fd.time

        # print("Now: {}".format(fd.time))

        current = dict()  # current aircraft inside alarm zone

        # loop on all the aircarft in the receiver
        for a in fd.aircraft: # from aircraft.json
            # if they don't have lat/lon or a heading skip them
            if a.lat == None or a.lon == None or a.track == None:
                continue
            # check to see if it's in the alarm zone:
            if a.distance < abovetustin_distance_alarm and a.altitude < abovetustin_elevation_alarm:
                # add it to the current dictionary
                current[a.hex] = a
                # print("Hornet in the groove!")
                if(m_write_tracks_to_file == True):
                    f = open("datatracks.txt", "w")
#				f.write("ID\tDist.(miles)\tAlt(ft)\tTime")
#               f.write("ID\tDist.(miles)\tAlt(ft)\tLat\tLon\tTime\n")
                    txt = "{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    a.ident_desc(), "%.2f" % a.distance, "%.0f" % a.altitude, "%.8f" % a.lat, "%.8f" % a.lon, (fd.time))
                    f.write(txt)
                    f.close()
                    #print(txt)
                    # now push to AWSIOT
                    # Try to make a dictionary:
                    message = {}
                    message['ID'] = a.ident_desc()
                    message['distance'] = a.distance
                    message['altitude'] = a.altitude
                    message['latitude'] = a.lat
                    message['longitude'] = a.lon
                    message['tUTC'] = "{}".format(fd.time)
                    messageJson = json.dumps(message)
                    #print(messageJson)
                    publishtoAWSIOT(messageJson)



                # print("{}: {}mi, {}az, {}el, {}alt, {}dB, {}seen".format(
                #	a.ident_desc(), "%.1f" % a.distance, "%.1f" % a.az, "%.1f" % a.altitude,
                #	a.altitude, "%0.1f" % a.rssi, "%.1f" % (a.seen or 0)))
                if a.hex in alarms:
                    # if it's already in the alarms dict, check to see if we're closer
                    if a.distance < alarms[a.hex][0].distance:
                        # if we're closer than the one already there, then overwrite it
                        alarms[a.hex] = (a, 0)
                else:
                    # add it to the alarms
                    alarms[a.hex] = (a, 0)

        finishedalarms = []
        # loop on all the aircraft in the alarms dict
        for h, a in alarms.items():
            # test code on a[0] here:
            m_debug=False
            if(m_debug==True):
                # Try to make a dictionary:
                message = {}
                message['ID'] = a[0].ident_desc()
                message['distance'] = a[0].distance
                message['altitude'] = a[0].altitude
                message['latitude'] = a[0].lat
                message['longitude'] = a[0].lon
                message['time'] = "{}".format(fd.time)
                messageJson = json.dumps(message)
                # print(messageJson)
                publishtoAWSIOT(messageJson)

            found = False

            # check to see if it's in the current set of aircraft
            for h2, a2 in current.items():
                # print("{}: {}mi, {}alt".format(a[0].ident_desc(),"%.1f" % a[0].distance,"%.0f" % a[0].altitude))

                #				f = open("data.txt", "a")
                #				f.write("ID\tDist.(miles)\tAlt(ft)\tTime")
                #				txt = "{}\t{}\t{}\t{}\n".format(a[0].ident_desc(),"%.1f" % a[0].distance,"%.0f" % a[0].altitude,(fd.time))
                #				f.write(txt)
                #				f.close()
                #				print(txt)

                #				print("{}: {}mi, {}alt, {}".format(a[0].ident_desc(),"%.1f" % a[0].distance,"%.0f" % a[0].altitude,(fd.time)))
                if h2 == h:
                    # print("{} not yet, dist, elv: {}, {}".format(h, "%.1f" % a[0].distance, "%.1f" % a[0].el))
                    # havescreenshot = display.clickOnAirplane(h)
                    # print('took screenshot of')
                    # print(h)
                    found = True
                    break
            # if it wasn't in the current set of aircraft, that means it's time to tweet!
            if not found:
                if a[1] < abovetustin_wait_x_updates:
                    alarms[h] = (a[0], a[1]+1)
                else:
                    havescreenshot = False
                    # if display != None:
                    # print("time to create screenshot of {}:".format(a[0]))
                    # print("Plane spotted {}:".format(a[0]))
                    # hexcode = a[0].hex
                    # hexcode = hexcode.replace(" ", "")
                    # hexcode = hexcode.replace("~", "")
                    # havescreenshot = display.clickOnAirplane(hexcode)
                    if fa_enable:
                        print("Getting FlightAware flight details")
                        faInfo = fa_api.FlightInfo(
                            a[0].flight, fa_username, fa_api_key)
                    else:
                        faInfo = False
                    f = open("data.txt", "a")
#				f.write("ID\tDist.(miles)\tAlt(ft)\tTime")
                    txt = "{}\t{}\t{}\t{}\n".format(
                        a[0].ident_desc(), "%.1f" % a[0].distance, "%.0f" % a[0].altitude, (fd.time))
                    f.write(txt)
                    f.close()
                    print(txt)
                    # now push to AWSIOT
                    # Try to make a dictionary:
                    message = {}
                    message['ID'] = a[0].ident_desc()
                    message['distance'] = a[0].distance
                    message['altitude'] = a[0].altitude
                    message['latitude'] = a[0].lat
                    message['longitude'] = a[0].lon
                    message['tUTC'] = "{}".format(fd.time)
                    messageJson = json.dumps(message)
                    # print(messageJson)
                    publishtoAWSIOT(messageJson)

                    # print("time to tweet!!!!!")
                    # print("Hornet LEFT the groove!")
#					print("Now: {}".format(fd.time))
#					print("{}: {}mi, {}el, {}alt, {}dB, {}seen".format(a[0].ident_desc(), "%.1f" % a[0].distance,
#											    "%.1f" % a[0].altitude,
#												   "%0.1f" % a[0].rssi,
#												  "%.1f" % (a[0].seen or 0)))
#					with open('filename.txt', 'w') as f:
#						print('This message will be written to a file.', file=f)
#					print("{}: {}mi, {}alt, {}".format(a[0].ident_desc(),"%.1f" % a[0].distance,"%.0f" % a[0].altitude,(fd.time)))
                    # try:
                    # Tweet(a[0], havescreenshot)
                    # print("banned from twitter!!!!!")
                    # except Exception:
                    # print("exception in Tweet():")
                    # traceback.print_exc()
                    finishedalarms.append(a[0].hex)

        # for each alarm that is finished, delete it from the dictionary
        for h in finishedalarms:
            del(alarms[h])

        # flush output for following in log file
        sys.stdout.flush()
