#
# flightdata4.py
#
# PJB 1/28/2022
# Reads on json aircraft.data....
#
#


import json
from time import sleep
import geomath
import math
from datetime import datetime
from configparser import ConfigParser
from colorama import Fore, Back, Style

if __name__ == "__main__":
    import os

    receiver_latitude = 33.635029
    receiver_longitude = -117.842218

    # read on json file
    f = open('/run/readsb/aircraft.json')
    data = json.load(f)
    f.close()

    # 978 is  /run/adsbexchange-978/aircraft.json
    # Summary of json files written to:
    # /run/adsbexchange-978/aircraft.json from 978 SDR (used for 978 webserver)
    # /run/readsb/aircraft.json from both (used for 1090 webserver)
    # /run/adsbexchange-feed/aircraft.json (used for nothing, part of feeder program)

    # f2 = open('/run/adsbexchange-feed/aircraft.json')
    f2 = open('/run/adsbexchange-978/aircraft.json')
    data2 = json.load(f2)
    f2.close()

    # print(data) # json of aircraft.json

    m_aircraft_list = data['aircraft']
    m_icao_list = []
    m_aircraft_list2 = data2['aircraft']
    m_icao_list2 = []
    # print(m_aircraft_list)

    print('1090/978:')
    print("|  icao   | flight  | alt   | dist | rssi  |   type       |  cat | seen  | mesg  | lat        | long      | alert |")
    print("|---------+---------+-------+------+-------+--------------+------+-------+-------+------------+-----------+-------|")
    for m_list_item in m_aircraft_list:  # iterates through all aircraft in list

        m_hex = m_list_item.get('hex') if "hex" in m_list_item else '------'
        m_flight = m_list_item.get(
            'flight') if "flight" in m_list_item else '------- '
        m_alt_geom = m_list_item.get(
            'alt_geom') if "alt_geom" in m_list_item else -1
        m_rssi = m_list_item.get('rssi') if "rssi" in m_list_item else -100
        m_messages = m_list_item.get(
            'messages') if "messages" in m_list_item else '---'
        m_type = m_list_item.get('type') if "type" in m_list_item else '---'
        m_category = m_list_item.get(
            'category') if "category" in m_list_item else '---'
        m_seen = m_list_item.get('seen') if "seen" in m_list_item else '---'
        m_lat = m_list_item.get('lat') if "lat" in m_list_item else 0
        m_lon = m_list_item.get('lon') if "lon" in m_list_item else 0
        m_alert = m_list_item.get('alert') if "alert" in m_list_item else '---'
        m_xyz = m_list_item.get('xyz') if "xyz" in m_list_item else '---'
        m_xyz = m_list_item.get('xyz')

        if "lat" in m_list_item and "lon" in m_list_item:
            m_dist = geomath.distance(
                (receiver_latitude, receiver_longitude), (m_list_item["lat"], m_list_item["lon"]))

        if m_lat != 0 and m_lon != 0 and m_alt_geom != -1:
            print("| {:<7} | {:<7}| {:>5} |{:>5} | {:>5} | {:>12} | {:>4} |  {:>4} | {:>5} | {:>10} |{:>10}| {:>2} |".format(
                m_hex,  # icao {:<7}
                m_flight,  # flight {:<7}
                "%.4d" % m_alt_geom,  # icao {:>5}
                "%.1f" % m_dist,  # {:>5} |
                "%3.1f" % m_rssi,  # icao {:>5}
                m_type,  # icao {:>12}
                m_category,  # {:>4}
                m_seen,  # {:>4}
                m_messages,  # {:>5}
                "%9.6f" % m_lat,
                "%9.6f" % m_lon,
                m_alert))
            m_icao_list.append(m_hex)

print('\n')
print('978 only')
print("|  icao   | flight  | alt   | dist | rssi  |   type       |  cat | seen  | mesg  | lat        | long      | alert |")
print("|---------+---------+-------+------+-------+--------------+------+-------+-------+------------+-----------+-------|")
for m_list_item in m_aircraft_list2:  # iterates through all aircraft in list
        m_hex2 = m_list_item.get('hex') if "hex" in m_list_item else '------'
        if "lat" in m_list_item and "lon" in m_list_item:
            m_dist2 = geomath.distance(
                (receiver_latitude, receiver_longitude), (m_list_item["lat"], m_list_item["lon"]))

        m_flight2 = m_list_item.get(
            'flight') if "flight" in m_list_item else '------- '
        m_alt_geom2 = m_list_item.get(
            'alt_geom') if "alt_geom" in m_list_item else -1
        m_rssi2 = m_list_item.get('rssi') if "rssi" in m_list_item else -100
        m_messages2 = m_list_item.get(
            'messages') if "messages" in m_list_item else '---'
        m_type2 = m_list_item.get('type') if "type" in m_list_item else '---'
        m_category2 = m_list_item.get(
            'category') if "category" in m_list_item else '---'
        m_seen2 = m_list_item.get('seen') if "seen" in m_list_item else '---'
        m_lat2 = m_list_item.get('lat') if "lat" in m_list_item else 0
        m_lon2 = m_list_item.get('lon') if "lon" in m_list_item else 0
        m_alert2 = m_list_item.get(
            'alert') if "alert" in m_list_item else '---'
        m_xyz2 = m_list_item.get('xyz') if "xyz" in m_list_item else '---'
        m_xyz2 = m_list_item.get('xyz')

        if m_lat2 != 0 and m_lon2 != 0 and m_alt_geom2 != -1:
            print("| {:<7} | {:<7}| {:>5} |{:>5} | {:>5} | {:>12} | {:>4} |  {:>4} | {:>5} | {:>10} |{:>10}| {:>2} |".format(
                m_hex2,  # icao {:<7}
                m_flight2,  # flight {:<7}
                "%.4d" % m_alt_geom2,  # icao {:>5}
                "%.1f" % m_dist2,  # {:>5} |
                "%3.1f" % m_rssi2,  # icao {:>5}
                m_type2,  # icao {:>12}
                m_category2,  # {:>4}
                m_seen2,  # {:>4}
                m_messages2,  # {:>5}
                "%9.6f" % m_lat2,
                "%9.6f" % m_lon2,
                m_alert2))
            m_icao_list2.append(m_hex2)


# m_icao_list is the 1090 and 978
# m_icao_list2 is just the 978
# print(m_icao_list)
print('**********************')
print('# of aircraft in 1090/978 = ', len(m_aircraft_list))
print('# of aircraft in 978 only = ', len(m_aircraft_list2))
print('**********************')
print('# of aircraft with position in 1090/978= ', len(m_icao_list))
print('# of aircraft with position in 978 only = ', len(m_icao_list2))
print('# of more in 1090/978 than just 978 = ',
      len(m_icao_list)-len(m_icao_list2))
print('**********************')

list_difference = []
for item in m_icao_list:  # 1090/978
  if item not in m_icao_list2:  # 978 only
    list_difference.append(item)  # 1090/978 only

list_difference2 = []
for item in m_icao_list2:
  if item not in m_icao_list2:
    list_difference2.append(item)  # 978 only


# print('difference:')
# print(list_difference)
print('# of aircraft in 1090/978 not in 978 = ', len(list_difference))
print('# of aircraft in 978 not in 1090/978 = ', len(list_difference2))
print('**********************')


print('aircraft in both 978 and 1090/978')
print(Fore.GREEN + 'GREEN = 1090/978')
print(Fore.RED + 'RED = 978 ONLY')
print(Style.RESET_ALL +  "|  icao   | flight  | alt   | dist | rssi  |   type       |  cat | seen  | mesg  | lat        | long      | alert |")
print("|---------+---------+-------+------+-------+--------------+------+-------+-------+------------+-----------+-------|")
for m_list_item in m_aircraft_list:  # iterates through all aircraft in list 1090/978

    m_hex = m_list_item.get('hex') if "hex" in m_list_item else '------'
    m_flight = m_list_item.get(
        'flight') if "flight" in m_list_item else '------- '
    m_alt_geom = m_list_item.get(
        'alt_geom') if "alt_geom" in m_list_item else -1
    m_rssi = m_list_item.get('rssi') if "rssi" in m_list_item else -100
    m_messages = m_list_item.get(
        'messages') if "messages" in m_list_item else '---'
    m_type = m_list_item.get('type') if "type" in m_list_item else '---'
    m_category = m_list_item.get(
        'category') if "category" in m_list_item else '---'
    m_seen = m_list_item.get('seen') if "seen" in m_list_item else '---'
    m_lat = m_list_item.get('lat') if "lat" in m_list_item else 0
    m_lon = m_list_item.get('lon') if "lon" in m_list_item else 0
    m_alert = m_list_item.get('alert') if "alert" in m_list_item else '---'
    m_xyz = m_list_item.get('xyz') if "xyz" in m_list_item else '---'
    m_xyz = m_list_item.get('xyz')
    if "lat" in m_list_item and "lon" in m_list_item:
        m_dist = geomath.distance(
            (receiver_latitude, receiver_longitude), (m_list_item["lat"], m_list_item["lon"]))

    if not (m_hex in list_difference):  # plane in 1090/978 and 978
        if m_lat != 0 and m_lon != 0 and m_alt_geom != -1:
            print(Fore.GREEN + "| {:<7} | {:<7}| {:>5} |{:>5} | {:>5} | {:>12} | {:>4} |  {:>4} | {:>5} | {:>10} |{:>10}| {:>2} |".format(
                m_hex,  # icao {:<7}
                m_flight,  # flight {:<7}
                "%.4d" % m_alt_geom,  # icao {:>5}
                "%.1f" % m_dist,  # {:>5} |
                "%3.1f" % m_rssi,  # icao {:>5}
                m_type,  # icao {:>12}
                m_category,  # {:>4}
                m_seen,  # {:>4}
                m_messages,  # {:>5}
                "%9.6f" % m_lat,
                "%9.6f" % m_lon,
                m_alert))
            #print('finding same plane in 978 only')
            # find
            for m_list_item2 in m_aircraft_list2:  # iterates through all aircraft in list 978
                m_hex2 = m_list_item2.get('hex') if "hex" in m_list_item2 else '------'
                if "lat" in m_list_item2 and "lon" in m_list_item2:
                    m_dist2 = geomath.distance(
                    (receiver_latitude, receiver_longitude), (m_list_item2["lat"], m_list_item2["lon"]))
                m_flight2 = m_list_item2.get('flight') if "flight" in m_list_item2 else '------- ' 
                m_alt_geom2=m_list_item2.get('alt_geom') if "alt_geom" in m_list_item2 else -1
                m_rssi2=m_list_item2.get('rssi') if "rssi" in m_list_item2 else -100            
                m_messages2=m_list_item2.get('messages') if "messages" in m_list_item2 else '---'
                m_type2=m_list_item2.get('type') if "type" in m_list_item2 else '---' 
                m_category2=m_list_item2.get('category') if "category" in m_list_item2 else '---'    
                m_seen2=m_list_item2.get('seen') if "seen" in m_list_item2 else '---'            
                m_lat2=m_list_item2.get('lat') if "lat" in m_list_item2 else 0
                m_lon2=m_list_item2.get('lon') if "lon" in m_list_item2 else 0
                m_alert2=m_list_item2.get('alert') if "alert" in m_list_item2 else '---'
                if m_hex2 == m_hex: # print
                    print(Fore.RED + "| {:<7} | {:<7}| {:>5} |{:>5} | {:>5} | {:>12} | {:>4} |  {:>4} | {:>5} | {:>10} |{:>10}| {:>2} |".format(
                    m_hex2,  # icao {:<7}
                    m_flight2,  # flight {:<7}
                    "%.4d" % m_alt_geom2,  # icao {:>5}
                    "%.1f" % m_dist2,  # {:>5} |
                    "%3.1f" % m_rssi2,  # icao {:>5}
                    m_type2,  # icao {:>12}
                    m_category2,  # {:>4}
                    m_seen2,  # {:>4}
                    m_messages2,  # {:>5}
                    "%9.6f" % m_lat2,
                    "%9.6f" % m_lon2,
                    m_alert2))
                    #print(Style.RESET_ALL)
                    print(Style.RESET_ALL + "|---------+---------+-------+------+-------+--------------+------+-------+-------+------------+-----------+-------|")


# Fields: https://www.adsbexchange.com/version-2-api-wip/

# print(Fore.RED + 'some red text')
# print(Fore.BLUE + 'some blue text')
# print(Fore.GREEN + 'some green text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')