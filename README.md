# RetroPie Rotate
Python script to perform a soft (no reboot) rotation change on RetroPie and EmulationStation.

Usage:
```
python ./rotate.py [0|1|2|3]
```
Where the rotation is value [0|1|2|3] * 90 degrees

Example:
```
# Rotate the screen 90 degrees
python ./rotate.py 1
```

# Tilt
Tilt.py is a script that reads the tilt value (0 or 1) from a tilt ball switch.  It then calls the rotate.py script to rotate the screen.  I use a bare tilt switch and a 1K restistor in series.  The resistor is optional but highly recommend to prevent a direct short if miswired.  Any value from 100-1000 ohms should be fine.  You could substitute a toggle switch if you prefer.  These are connected to a GPIO pin, like BCM 22 and the 3.3V (see below).  The script uses BCM 22, but you should be able to use most any GPIO pin if you update the "CHANNEL" value in the script.
```
3.3V -> resistor -> tilt switch -> GPIO
```
### Running tilt.py on boot
I run tilt.py on boot.  You will need to edit your rc.local.  I use vi, but you can substitute another editor like nano.
```
sudo vi /etc/rc.local
```
Add this line before the "exit"
```
sudo -u pi python /home/pi/tilt.py &
```

Notes:
- EmulationStation will automatically be restarted to reflect the new rotation.  RetroPie emulators will NOT be restarted, but will be correct on the next execution.
- If you change settings in EmulationStation, it will revert the screen changes.  Running rotate.py again should fix them.
- I wrote/tested this for Pi 4, but it should work on other Pies.

Notes for Tilt:
- I couldn't get the built in debounce code to work the way I liked, so I rolled my own.  There is currently a 1 second delay.  If you are using a toggle switch, you could probably lower this.
- Sometimes my tilt sensor doesn't make a good connection every time.  If you tap around it, it usually corrects itself.
