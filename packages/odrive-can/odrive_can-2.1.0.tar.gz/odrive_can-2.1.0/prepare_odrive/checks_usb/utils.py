#!/usr/bin/env python3
"""
 utils for odrive testing

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""
from typing import List
import odrive.enums as enums


class OdriveError(Exception):
    """Custom exception for ODrive errors"""


def decode_error_flags(error_value: int, error_enum) -> List[str]:
    """
    Decode an error value into a list of human-readable error names
    by checking each bit against the enum values.
    """
    error_messages = []
    for error in error_enum:
        if error_value & error.value:
            error_messages.append(error.name)
    return error_messages


def check_error(drv) -> None:
    """
    Check if there are any errors and raise OdriveError with decoded error messages.
    Uses odrive.enums to decode error flags into human-readable messages.
    """
    ax = drv.axis0

    error_checks = [
        ("ODrive", ax.error, enums.ODriveError),
        ("Motor", ax.motor.error, enums.MotorError),
        ("Encoder", ax.encoder.error, enums.EncoderError),
        ("Controller", ax.controller.error, enums.ControllerError),
        (
            "Sensorless Estimator",
            ax.sensorless_estimator.error,
            enums.SensorlessEstimatorError,
        ),
    ]

    error_messages: List[str] = []

    for source, error_value, error_enum in error_checks:
        if error_value:
            decoded = decode_error_flags(error_value, error_enum)
            if decoded:
                error_messages.extend(f"{source}: {error}" for error in decoded)

    if error_messages:
        raise OdriveError("Multiple errors detected:\n" + "\n".join(error_messages))
