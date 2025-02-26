#!/usr/bin/env python3
"""
 Send data to UDP server, used for plotting with plotjuggler

 Copyright (c) 2024 ROX Automation - Jev Kuznetsov


"""
import os
import time
import socket
import json
import logging
import math

# set this to the IP address of the machine running plotjuggler =


class UDP_Client:
    """send data to UDP server, used for plotting with plotjuggler

    Set the UDP_DATA_DEST environment variable to the IP address of the machine running plotjuggler

    """

    def __init__(self, host: str | None = None, port: int = 5005):

        if host is not None:
            self._host = host
        else:
            host = os.getenv("UDP_DATA_DEST", "localhost")
            self._host = host

        self._port = port

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._log = logging.getLogger(self.__class__.__name__)
        self._log.info("UDP client created, sending to %s:%d", host, port)

    def send(self, data: dict, add_timestamp: bool = True):
        """send data to UDP server"""
        if add_timestamp:
            data["ts"] = time.time()

        try:
            self._sock.sendto(json.dumps(data).encode(), (self._host, self._port))
        except Exception as e:  # pylint: disable=broad-except
            self._log.error("Failed to send data: %s", e)


def demo(period: float = 2.0) -> None:
    """demo, send x and y values to plotjuggler
    x is sawtooth, y is sine wave"""
    client = UDP_Client()

    start_time = time.time()  # Record the start time
    while True:
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        sine_value = math.sin(
            2 * math.pi * elapsed_time / period
        )  # Calculate sine value
        time.sleep(0.01)  # Small delay to control output frequency (adjust as needed)

        client.send({"x": elapsed_time % period, "y": sine_value})


if __name__ == "__main__":
    demo()
