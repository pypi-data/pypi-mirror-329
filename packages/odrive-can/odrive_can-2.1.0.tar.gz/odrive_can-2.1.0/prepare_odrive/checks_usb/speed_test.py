#!/usr/bin/env python3
"""
 simple test of velocity control

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""
import asyncio
import os
import odrive  # type: ignore
import odrive.enums as enums  # type: ignore
from utils import check_error

from odrive_can.tools import UDP_Client

SETPOINT = 50
DURATION = 20

drv = odrive.find_any()

print(f"Found ODrive {drv.serial_number}")

drv.clear_errors()
check_error(drv)

ax = drv.axis0


ax.controller.config.control_mode = enums.ControlMode.VELOCITY_CONTROL
ax.controller.config.input_mode = enums.InputMode.VEL_RAMP
ax.requested_state = enums.AxisState.CLOSED_LOOP_CONTROL

ax.config.enable_watchdog = False

# limit acceleration
ax.controller.config.vel_ramp_rate = 60
ax.motor.config.current_lim = 20

# set positiion to zero
ax.encoder.set_linear_count(0)

# disable limits
ax.controller.config.enable_vel_limit = True
ax.controller.config.vel_limit = 100


# ignore hall errors
ax.encoder.config.ignore_illegal_hall_state = False


async def feedback_loop() -> None:
    udp_dest = os.getenv("UDP_DATA_DEST", "localhost")

    print(f"sending data to {udp_dest}")
    udp = UDP_Client(host=udp_dest)

    counter = 0

    while True:
        check_error(drv)

        sp_rpm = int(ax.controller.input_vel * 60)
        vel_rpm = int(ax.encoder.vel_estimate * 60)

        data = {
            "sp": sp_rpm,
            "vel": vel_rpm,
            "pos": ax.encoder.pos_estimate,
        }

        udp.send(data)
        await asyncio.sleep(0.05)

        if counter % 100 == 0:
            print(f"sp: {data['sp']}, vel: {data['vel']}")

        counter += 1


async def setpoint_loop() -> None:
    print("Starting setpoint loop")
    ax.controller.input_vel = 0
    await asyncio.sleep(1)
    while True:
        ax.controller.input_vel = SETPOINT
        print(f"Setpoint set to {ax.controller.input_vel} ({SETPOINT*60} RPM)")
        await asyncio.sleep(DURATION)

        ax.controller.input_vel = 0
        print(f"Setpoint set to {ax.controller.input_vel}")
        await asyncio.sleep(5)


async def main() -> None:
    await asyncio.gather(feedback_loop(), setpoint_loop())


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
finally:
    ax.controller.input_vel = 0
    ax.requested_state = enums.AxisState.IDLE
