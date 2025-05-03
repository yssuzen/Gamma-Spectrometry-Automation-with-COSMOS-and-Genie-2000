# This file is part of the Gamma Spectrometry Automation Program project.
#
# Copyright (C) 2025 Yavuz Selim Suzen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import serial
import time

def move_to_position(User_position, speed=put/your/speed/here, port="put/your/port/here", baud=put/your/baud/here):
    reference = put/your/reference/position/here #slides's reference position - absolute position
    position = reference - (User_position*1000)
    abs_pos_str = str(abs(position))
    spd_str = str(speed)

    #opening the serial port
    with serial.Serial(port, baudrate=baud, timeout=1) as ser:
        #slight delay to let port open
        time.sleep(0.2)

        #F
        ser.write(b"F,\r")
        time.sleep(0.1)

        #C
        ser.write(b"C,\r")
        time.sleep(0.1)

        #Setting speed to put/your/speed/here
        cmd_speed = f"S1M{spd_str},".encode("utf-8")
        ser.write(cmd_speed)
        time.sleep(0.1)

        # Absolute Movement => IA1M-#####
        # Pause => P##### (in seconds)
        # Run => R        
        if position > 0:
            move_line = f"IA1M-{abs_pos_str},R,".encode("utf-8")
        else:
            move_line = f"IA1M{abs_pos_str},R,".encode("utf-8")

        ser.write(move_line)
        time.sleep(0.1)

        #Poll with 'V' until we get 'R'
        is_busy = True
        while is_busy:
            #Sending 'V' to query status
            ser.write(b"V,\r")
            time.sleep(0.1)

            #reading resposne from VXM
            response = ser.read_until(b"\r")
            #response = ser.readline()  - will use this if the device sends newlines

            if b"R" in response:
                # R means ready -> move completed
                is_busy = False
            elif b"B" in response:
                #B means busy -> keep waiting
                time.sleep(0.3)
            else:
                #If unexpected commands come from the vxm
                time.sleep(0.3)
        
        return True

def setReference(port="put/your/port/here", baud=put/your/baud/here):
    # Try to move by 100000
    move_to_position(200, speed=put/your/speed/here, port="put/your/port/here", baud=put/your/baud/here)
    # Reset Reference
    cmd = (
        "F,"
        "C,"
        "IA1M-0,"
        "R,"
    )
    with serial.Serial(port="put/your/port/here", baudrate=put/your/baud/here, timeout=1) as ser:
        time.sleep(0.2)
        ser.write(cmd.encode("utf-8")+b"\r")
        time.sleep(0.1)

def return_to_reference(speed=put/your/speed/here):
    cmd = (
        "F,"
        "C,"
        f"S1M{speed},"
        "IA1M0,"
        "R,"
    )

    with serial.Serial(port="put/your/port/here", baudrate=put/your/baud/here, timeout=1) as ser:
        time.sleep(0.2)
        ser.write(cmd.encode("utf-8")+b"\r")
        time.sleep(0.1)

        #Poll until done
        done = False
        while not done:
            ser.write(b"V,\r")
            time.sleep(0.1)
            resp = ser.read_until(b"\r")
            if b"R" in resp:
                done=True
            else:
                time.sleep(0.2)

def kill_motion(port="put/your/port/here", baud=put/your/baud/here):
    try:
        with serial.Serial(port=port, baudrate=baud, timeout=1) as ser:
            time.sleep(0.2)
            ser.write(b"K,\r")
    except serial.SerialException as e:
        print(f"[kill_motion] could not open port {port}: {e}")


def get_position():
    with serial.Serial(port="put/your/port/here", baudrate=put/your/baud/here, timeout=1) as ser:
        ser.write(b"X,\r")
        time.sleep(0.2)
        position = ser.readline().decode('utf-8').strip()
        return position
