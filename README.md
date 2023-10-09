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

Notes:
- EmulationStation will automatically be restarted to reflect the new rotation.  RetroPie emulators will NOT be restarted, but will be correct on the next execution.
- I wrote/tested this for Pi 4, but it should work on other Pies.
- tilt.py is a work in progress to perform the rotation based on a tilt switch.
 
