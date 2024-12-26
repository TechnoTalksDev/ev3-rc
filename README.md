# ev3-rc
Remote control EV3 drive motors with a controller


## Setup

1. Install [ev3dev](https://www.ev3dev.org/docs/getting-started/)
2. Connect [EV3 to wifi](https://www.ev3dev.org/docs/networking/)
    - Please note it is **required** that the EV3 has an ip reachable by your computer
    - Bluetooth will not work (atleast on Windows)
3. Make sure your EV3 is discoverable by running `ping ev3dev` or `ping XX.X.X.XXX` with the ip if the EV3
    - If it's not try restarting and manually connecting from the brick
4. Python setup
    - Python 3.6.8 **OTHER VERSIONS DO NOT WORK**
    - `pip install`
      - rpyc==5.0
      - pygame==2.6
5. Connect a controller
    - Any controller pygame supports (tested with Bluetooth Xbox Series X controller)
    - Change axis numbers if they aren't the right ones for you controller
    - Delete the `* -1` when calculating controller values if the signs are flipped
6. Run script
    - Change ports 
      - Change the `OUTPUT_*`
      - ```
        left_motor = ev3dev2_motor.LargeMotor(ev3dev2_motor.OUTPUT_B)
        right_motor = ev3dev2_motor.LargeMotor(ev3dev2_motor.OUTPUT_C)
        ```
    - Tank drive is implemented


## Troubleshooting

### Key errors
Need to update ev3dev rpyc version.
SSH into brick and run

`sudo python -m pip install rpyc==5.0`

If pip is not installed
`sudo apt install python3-pip`

If none of these commands work, look at [step 6.1](https://www.ev3dev.org/docs/getting-started/)

These commands **will** take a while!

### Motor errors
Make sure motors are plugged in and ports are configured correctly

### Controller dosen't do anything
Your axis might be different. Try changing `get_axis(X)` for sticks that dont work
```python
left_stick_y = apply_dead_zone(joystick.get_axis(1) * -1)
right_stick_y = apply_dead_zone(joystick.get_axis(3) * -1)
```

### Help I don't understand these words!
Read this! [ev3dev](https://www.ev3dev.org/docs/getting-started/)

### Other
Try documentation

[ev3dev-wiki](https://github.com/ev3dev/ev3dev/wiki)

[ev3dev networking](https://www.ev3dev.org/docs/networking/)

[rpyc](https://rpyc.readthedocs.io/en/latest/index.html)

[pygame joystick](https://www.pygame.org/docs/ref/joystick.html)