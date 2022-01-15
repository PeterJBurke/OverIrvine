# OverIrvine

Fork of OverPutney.
Updated.
Pushes data to AWSIOT.
Tweet, screenshot not yet working. FA also not working.
Saves data.txt file of nearest distance, time, alt., ID of each plane within range.
Changed to alt instead of angle above horizon.

[OverPutney](https://twitter.com/overputney) is an ADS-B Twitter Bot running on a Raspberry Pi 4.  It tracks airplanes and then tweets whenever an airplane flies overhead. It is a fork of the original AboveTustin bot, modified to work on a Piaware with Flightaware's fork of dump1090 and adding support for [Josh Douch's free ICAO lookup APIs](https://api.joshdouch.me/). It also uses chromedriver for browser interactions rather than the deprecated PhantomJS webdriver.

 * Uses [tar1090](https://github.com/wiedehopf/tar1090) for ADSB message decoding, airplane tracking, and webserving.
 * Built on the [Flightaware Piaware distribution](https://flightaware.com/adsb/piaware/build).
 * Works with Chromium chromedriver webdriver on Raspberry Pi.
 * It tweets an image of a map with the airplane's track and the decoded aircraft data displayed by tar1090.
 * It displays the flight name if available, or the reported icao code.
 * It displays altitude, ground speed and heading information of the airplane at it's closest point to the bot.
 * Gives different hashtags depending on altitude, speed and time of day.
 * Adds aircraft registration, type, and owner using [Josh Douch's ICAO hex lookup APIs](https://api.joshdouch.me/).

## Dependencies
* Uses [tar1090](https://github.com/wiedehopf/tar1090) for ADSB message decoding, airplane tracking, and webserving.
* Uses [twitter](https://pypi.python.org/pypi/twitter) for tweeting.
* Uses [selenium](https://pypi.python.org/pypi/selenium) for screenshots with Chromedriver and Chromium.
* Uses [pillow](https://python-pillow.org/) for image processing.
* Uses [requests](https://pypi.org/project/requests/) for API calls.
* Uses [Chromedriver](https://chromedriver.chromium.org/) for headless web browsing.
* Builds on a running [Piaware](https://flightaware.com/adsb/piaware/build) Raspberry Pi-based ADS-B receiver and decoder with MLAT support, with web server and local databases.

## Instructions to get up and running:
* Create SD card from ADSBexchange, configure it, get it running.
* Download needed packages:

  sudo apt update
sudo apt upgrade
  pip3 install twitter
  pip3 install requests
  pip3 install selenium
  pip3 install cryptography
  pip3 install Pillow
  sudo apt-get install chromium-chromedriver
  pip3 install --upgrade requests
* clone it
git clone https://github.com/PeterJBurke/OverIrvine.git
* Run it (manually)!
   python3 tracker.py 
**Gives output and tweets every time a plane in view. Then got banned from twitter….


## Alternative webcam configuration:

While raspimjpeg is the easiest user interface, the latency can be large (up to 700 ms) for 4G connection. An alternative is to stream the bits directly out using netcat, and play them on the desktop. Here is how to do that, assuming you have a linux desktop with a monitor:
### 1) Stop raspimjpeg (on Pi  terminal)
Stop the raspimjpeg screen, if installed and running. See screen manual for insructions how to kill a screen.

### 2) SSH Pi to AWS for webcam  (on Pi terminal)
SSH into AWS for webcam traffic (sets up a reverse ssh tunnel so if you log into localhost:8901 on desktop, it will take you to AWSIPADDRESS:8080, which has the webcam data):
```
ssh -R 8080:localhost:8090 -i "AWSKEY.pem" ubuntu@AWSIPADDRESS
```
so whatever AW sees at its port 8080 goes to Pi port 8090.

### 3) Push bits out from Pi (on Pi terminal):
Push bits out from pi using netcat. Type this command on a terminal on the pi:
```
sudo raspivid -t 0 -w 1280 -h 720 -ih -vf -hf -fps 20 -b 1000000 -a 12 -o - | nc   -k -l 8090
```
OR:
```
sudo raspivid -t 0 -w 1280 -h 720 -ih -vf -hf -fps 20 -b 1000000 -a 12 -l -o tcp://0.0.0.0:8090
```


## Notes

Add your Twitter keys and location in lat/long to `config` and rename as `config.ini` before running. The `./runbot.sh` script will launch the looping script `run_tracker.sh` (which ensures the tracker python code is running) as a background task with no interaction. Use `tail -f nohup.out` to monitor operations. `pkill -f tracker` will shut down the bot.

## Forked from the [AboveTustin](https://github.com/kevinabrandon/AboveTustin) code written by
* [Kevin Brandon](https://github.com/kevinabrandon)
* [Joseph Prochazka](https://github.com/jprochazka)
