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
### Create SD card from ADSBexchange, configure it, get it running.
### Download needed packages:
```
  sudo apt update 
  sudo apt upgrade 
  pip3 install twitter 
  pip3 install requests 
  pip3 install selenium 
  pip3 install cryptography 
  pip3 install Pillow 
  sudo apt-get install chromium-chromedriver 
  pip3 install --upgrade requests
  ```
### clone it
```
git clone https://github.com/PeterJBurke/OverIrvine.git
```
### Run it (manually)!
```
   python3 tracker.py 
```
**Gives output and tweets every time a plane in view. Then got banned from twitter….

## Notes

Add your Twitter keys and location in lat/long to `config` and rename as `config.ini` before running. The `./runbot.sh` script will launch the looping script `run_tracker.sh` (which ensures the tracker python code is running) as a background task with no interaction. Use `tail -f nohup.out` to monitor operations. `pkill -f tracker` will shut down the bot.

## Forked from the [AboveTustin](https://github.com/kevinabrandon/AboveTustin) code written by
* [Kevin Brandon](https://github.com/kevinabrandon)
* [Joseph Prochazka](https://github.com/jprochazka)
