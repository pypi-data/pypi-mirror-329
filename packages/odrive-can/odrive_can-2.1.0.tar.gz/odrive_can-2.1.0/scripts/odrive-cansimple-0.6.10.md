## odrive-cansimple-0.6.10  interface

### ID: 0 - Axis0_Get_Version
- Name: Axis0_Get_Version
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Protocol_Version | 0 | 8 | 1 | 0 | None | None |  | Master |  |
| Hw_Version_Major | 8 | 8 | 1 | 0 | None | None |  | Master |  |
| Hw_Version_Minor | 16 | 8 | 1 | 0 | None | None |  | Master |  |
| Hw_Version_Variant | 24 | 8 | 1 | 0 | None | None |  | Master |  |
| Fw_Version_Major | 32 | 8 | 1 | 0 | None | None |  | Master |  |
| Fw_Version_Minor | 40 | 8 | 1 | 0 | None | None |  | Master |  |
| Fw_Version_Revision | 48 | 8 | 1 | 0 | None | None |  | Master |  |
| Fw_Version_Unreleased | 56 | 8 | 1 | 0 | None | None |  | Master |  |

### ID: 1 - Axis0_Heartbeat
- Name: Axis0_Heartbeat
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Axis_Error | 0 | 32 | 1 | 0 | None | None |  | Master | 0: NONE, 1: INITIALIZING, 2: SYSTEM_LEVEL, 4: TIMING_ERROR, 8: MISSING_ESTIMATE, 16: BAD_CONFIG, 32: DRV_FAULT, 64: MISSING_INPUT, 256: DC_BUS_OVER_VOLTAGE, 512: DC_BUS_UNDER_VOLTAGE, 1024: DC_BUS_OVER_CURRENT, 2048: DC_BUS_OVER_REGEN_CURRENT, 4096: CURRENT_LIMIT_VIOLATION, 8192: MOTOR_OVER_TEMP, 16384: INVERTER_OVER_TEMP, 32768: VELOCITY_LIMIT_VIOLATION, 65536: POSITION_LIMIT_VIOLATION, 16777216: WATCHDOG_TIMER_EXPIRED, 33554432: ESTOP_REQUESTED, 67108864: SPINOUT_DETECTED, 134217728: BRAKE_RESISTOR_DISARMED, 268435456: THERMISTOR_DISCONNECTED, 1073741824: CALIBRATION_ERROR |
| Axis_State | 32 | 8 | 1 | 0 | None | None |  | Master | 0: UNDEFINED, 1: IDLE, 2: STARTUP_SEQUENCE, 3: FULL_CALIBRATION_SEQUENCE, 4: MOTOR_CALIBRATION, 6: ENCODER_INDEX_SEARCH, 7: ENCODER_OFFSET_CALIBRATION, 8: CLOSED_LOOP_CONTROL, 9: LOCKIN_SPIN, 10: ENCODER_DIR_FIND, 11: HOMING, 12: ENCODER_HALL_POLARITY_CALIBRATION, 13: ENCODER_HALL_PHASE_CALIBRATION, 14: ANTICOGGING_CALIBRATION, 5: SENSORLESS_CONTROL |
| Procedure_Result | 40 | 8 | 1 | 0 | None | None |  | Master | 0: SUCCESS, 1: BUSY, 2: CANCELLED, 3: DISARMED, 4: NO_RESPONSE, 5: POLE_PAIR_CPR_MISMATCH, 6: PHASE_RESISTANCE_OUT_OF_RANGE, 7: PHASE_INDUCTANCE_OUT_OF_RANGE, 8: UNBALANCED_PHASES, 9: INVALID_MOTOR_TYPE, 10: ILLEGAL_HALL_STATE, 11: TIMEOUT, 12: HOMING_WITHOUT_ENDSTOP, 13: INVALID_STATE, 14: NOT_CALIBRATED, 15: NOT_CONVERGING |
| Trajectory_Done_Flag | 48 | 1 | 1 | 0 | None | None |  | Master |  |

### ID: 2 - Axis0_Estop
- Name: Axis0_Estop
- Length: 0 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|

### ID: 3 - Axis0_Get_Error
- Name: Axis0_Get_Error
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Active_Errors | 0 | 32 | 1 | 0 | None | None |  | Master | 0: NONE, 1: INITIALIZING, 2: SYSTEM_LEVEL, 4: TIMING_ERROR, 8: MISSING_ESTIMATE, 16: BAD_CONFIG, 32: DRV_FAULT, 64: MISSING_INPUT, 256: DC_BUS_OVER_VOLTAGE, 512: DC_BUS_UNDER_VOLTAGE, 1024: DC_BUS_OVER_CURRENT, 2048: DC_BUS_OVER_REGEN_CURRENT, 4096: CURRENT_LIMIT_VIOLATION, 8192: MOTOR_OVER_TEMP, 16384: INVERTER_OVER_TEMP, 32768: VELOCITY_LIMIT_VIOLATION, 65536: POSITION_LIMIT_VIOLATION, 16777216: WATCHDOG_TIMER_EXPIRED, 33554432: ESTOP_REQUESTED, 67108864: SPINOUT_DETECTED, 134217728: BRAKE_RESISTOR_DISARMED, 268435456: THERMISTOR_DISCONNECTED, 1073741824: CALIBRATION_ERROR |
| Disarm_Reason | 32 | 32 | 1 | 0 | None | None |  | Master | 0: NONE, 1: INITIALIZING, 2: SYSTEM_LEVEL, 4: TIMING_ERROR, 8: MISSING_ESTIMATE, 16: BAD_CONFIG, 32: DRV_FAULT, 64: MISSING_INPUT, 256: DC_BUS_OVER_VOLTAGE, 512: DC_BUS_UNDER_VOLTAGE, 1024: DC_BUS_OVER_CURRENT, 2048: DC_BUS_OVER_REGEN_CURRENT, 4096: CURRENT_LIMIT_VIOLATION, 8192: MOTOR_OVER_TEMP, 16384: INVERTER_OVER_TEMP, 32768: VELOCITY_LIMIT_VIOLATION, 65536: POSITION_LIMIT_VIOLATION, 16777216: WATCHDOG_TIMER_EXPIRED, 33554432: ESTOP_REQUESTED, 67108864: SPINOUT_DETECTED, 134217728: BRAKE_RESISTOR_DISARMED, 268435456: THERMISTOR_DISCONNECTED, 1073741824: CALIBRATION_ERROR |

### ID: 4 - Axis0_RxSdo
- Name: Axis0_RxSdo
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Opcode | 0 | 8 | 1 | 0 | None | None |  |  | 0: READ, 1: WRITE |
| Endpoint_ID | 8 | 16 | 1 | 0 | None | None |  |  |  |
| Reserved | 24 | 8 | 1 | 0 | None | None |  |  |  |
| Value | 32 | 32 | 1 | 0 | None | None |  |  |  |

### ID: 5 - Axis0_TxSdo
- Name: Axis0_TxSdo
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Reserved0 | 0 | 8 | 1 | 0 | None | None |  |  |  |
| Endpoint_ID | 8 | 16 | 1 | 0 | None | None |  |  |  |
| Reserved1 | 24 | 8 | 1 | 0 | None | None |  |  |  |
| Value | 32 | 32 | 1 | 0 | None | None |  |  |  |

### ID: 6 - Axis0_Address
- Name: Axis0_Address
- Length: 8 bytes
- Sender: ['Master', 'ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Node_ID | 0 | 8 | 1 | 0 | None | None |  | ODrive_Axis0 |  |
| Serial_Number | 8 | 48 | 1 | 0 | None | None |  | ODrive_Axis0 |  |

### ID: 7 - Axis0_Set_Axis_State
- Name: Axis0_Set_Axis_State
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Axis_Requested_State | 0 | 32 | 1 | 0 | None | None |  | ODrive_Axis0 | 0: UNDEFINED, 1: IDLE, 2: STARTUP_SEQUENCE, 3: FULL_CALIBRATION_SEQUENCE, 4: MOTOR_CALIBRATION, 6: ENCODER_INDEX_SEARCH, 7: ENCODER_OFFSET_CALIBRATION, 8: CLOSED_LOOP_CONTROL, 9: LOCKIN_SPIN, 10: ENCODER_DIR_FIND, 11: HOMING, 12: ENCODER_HALL_POLARITY_CALIBRATION, 13: ENCODER_HALL_PHASE_CALIBRATION, 14: ANTICOGGING_CALIBRATION, 5: SENSORLESS_CONTROL |

### ID: 9 - Axis0_Get_Encoder_Estimates
- Name: Axis0_Get_Encoder_Estimates
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Pos_Estimate | 0 | 32 | 1 | 0 | None | None | rev | Master |  |
| Vel_Estimate | 32 | 32 | 1 | 0 | None | None | rev/s | Master |  |

### ID: 11 - Axis0_Set_Controller_Mode
- Name: Axis0_Set_Controller_Mode
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Control_Mode | 0 | 32 | 1 | 0 | None | None |  | ODrive_Axis0 | 0: VOLTAGE_CONTROL, 1: TORQUE_CONTROL, 2: VELOCITY_CONTROL, 3: POSITION_CONTROL |
| Input_Mode | 32 | 32 | 1 | 0 | None | None |  | ODrive_Axis0 | 0: INACTIVE, 1: PASSTHROUGH, 2: VEL_RAMP, 3: POS_FILTER, 4: MIX_CHANNELS, 5: TRAP_TRAJ, 6: TORQUE_RAMP, 7: MIRROR, 8: TUNING |

### ID: 12 - Axis0_Set_Input_Pos
- Name: Axis0_Set_Input_Pos
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Input_Pos | 0 | 32 | 1 | 0 | None | None | rev | ODrive_Axis0 |  |
| Vel_FF | 32 | 16 | 0.001 | 0 | None | None | rev/s (default) [#vel-ff-scale]_ | ODrive_Axis0 |  |
| Torque_FF | 48 | 16 | 0.001 | 0 | None | None | Nm (default) [#torque-ff-scale]_ | ODrive_Axis0 |  |

### ID: 13 - Axis0_Set_Input_Vel
- Name: Axis0_Set_Input_Vel
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Input_Vel | 0 | 32 | 1 | 0 | None | None | rev/s | ODrive_Axis0 |  |
| Input_Torque_FF | 32 | 32 | 1 | 0 | None | None | Nm | ODrive_Axis0 |  |

### ID: 14 - Axis0_Set_Input_Torque
- Name: Axis0_Set_Input_Torque
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Input_Torque | 0 | 32 | 1 | 0 | None | None | Nm | ODrive_Axis0 |  |

### ID: 15 - Axis0_Set_Limits
- Name: Axis0_Set_Limits
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Velocity_Limit | 0 | 32 | 1 | 0 | None | None | rev/s | ODrive_Axis0 |  |
| Current_Limit | 32 | 32 | 1 | 0 | None | None | A | ODrive_Axis0 |  |

### ID: 17 - Axis0_Set_Traj_Vel_Limit
- Name: Axis0_Set_Traj_Vel_Limit
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Traj_Vel_Limit | 0 | 32 | 1 | 0 | None | None | rev/s | ODrive_Axis0 |  |

### ID: 18 - Axis0_Set_Traj_Accel_Limits
- Name: Axis0_Set_Traj_Accel_Limits
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Traj_Accel_Limit | 0 | 32 | 1 | 0 | None | None | rev/s^2 | ODrive_Axis0 |  |
| Traj_Decel_Limit | 32 | 32 | 1 | 0 | None | None | rev/s^2 | ODrive_Axis0 |  |

### ID: 19 - Axis0_Set_Traj_Inertia
- Name: Axis0_Set_Traj_Inertia
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Traj_Inertia | 0 | 32 | 1 | 0 | None | None | Nm/(rev/s^2) | ODrive_Axis0 |  |

### ID: 20 - Axis0_Get_Iq
- Name: Axis0_Get_Iq
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Iq_Setpoint | 0 | 32 | 1 | 0 | None | None | A | Master |  |
| Iq_Measured | 32 | 32 | 1 | 0 | None | None | A | Master |  |

### ID: 21 - Axis0_Get_Temperature
- Name: Axis0_Get_Temperature
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| FET_Temperature | 0 | 32 | 1 | 0 | None | None | deg C | Master |  |
| Motor_Temperature | 32 | 32 | 1 | 0 | None | None | deg C | Master |  |

### ID: 22 - Axis0_Reboot
- Name: Axis0_Reboot
- Length: 1 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Action | 0 | 8 | 1 | 0 | None | None |  | ODrive_Axis0 | 0: reboot, 1: save_configuration, 2: erase_configuration, 3: enter_dfu_mode |

### ID: 23 - Axis0_Get_Bus_Voltage_Current
- Name: Axis0_Get_Bus_Voltage_Current
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Bus_Voltage | 0 | 32 | 1 | 0 | None | None | V | Master |  |
| Bus_Current | 32 | 32 | 1 | 0 | None | None | A | Master |  |

### ID: 24 - Axis0_Clear_Errors
- Name: Axis0_Clear_Errors
- Length: 1 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Identify | 0 | 8 | 1 | 0 | None | None |  | ODrive_Axis0 |  |

### ID: 25 - Axis0_Set_Absolute_Position
- Name: Axis0_Set_Absolute_Position
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Position | 0 | 32 | 1 | 0 | None | None | rev | ODrive_Axis0 |  |

### ID: 26 - Axis0_Set_Pos_Gain
- Name: Axis0_Set_Pos_Gain
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Pos_Gain | 0 | 32 | 1 | 0 | None | None | (rev/s) / rev | ODrive_Axis0 |  |

### ID: 27 - Axis0_Set_Vel_Gains
- Name: Axis0_Set_Vel_Gains
- Length: 8 bytes
- Sender: ['Master']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Vel_Gain | 0 | 32 | 1 | 0 | None | None | Nm / (rev/s) | ODrive_Axis0 |  |
| Vel_Integrator_Gain | 32 | 32 | 1 | 0 | None | None | Nm / rev | ODrive_Axis0 |  |

### ID: 28 - Axis0_Get_Torques
- Name: Axis0_Get_Torques
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Torque_Target | 0 | 32 | 1 | 0 | None | None | Nm | Master |  |
| Torque_Estimate | 32 | 32 | 1 | 0 | None | None | Nm | Master |  |

### ID: 29 - Axis0_Get_Powers
- Name: Axis0_Get_Powers
- Length: 8 bytes
- Sender: ['ODrive_Axis0']

| Signal Name | Start Bit | Length | Factor | Offset | Min Value | Max Value | Unit | Receiver | Choices |
|-------------|-----------|--------|--------|--------|-----------|-----------|------|----------|---------|
| Electrical_Power | 0 | 32 | 1 | 0 | None | None | W | Master |  |
| Mechanical_Power | 32 | 32 | 1 | 0 | None | None | W | Master |  |

### ID: 31 - Axis0_Enter_DFU_Mode
- Name: Axis0_Enter_DFU_Mode
- Length: 0 bytes
- Sender: ['Master']

### ID: 32 - Axis1_Get_Version
- Name: Axis1_Get_Version
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 33 - Axis1_Heartbeat
- Name: Axis1_Heartbeat
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 34 - Axis1_Estop
- Name: Axis1_Estop
- Length: 0 bytes
- Sender: ['Master']

### ID: 35 - Axis1_Get_Error
- Name: Axis1_Get_Error
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 36 - Axis1_RxSdo
- Name: Axis1_RxSdo
- Length: 8 bytes
- Sender: ['Master']

### ID: 37 - Axis1_TxSdo
- Name: Axis1_TxSdo
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 38 - Axis1_Address
- Name: Axis1_Address
- Length: 8 bytes
- Sender: ['Master', 'ODrive_Axis1']

### ID: 39 - Axis1_Set_Axis_State
- Name: Axis1_Set_Axis_State
- Length: 8 bytes
- Sender: ['Master']

### ID: 41 - Axis1_Get_Encoder_Estimates
- Name: Axis1_Get_Encoder_Estimates
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 43 - Axis1_Set_Controller_Mode
- Name: Axis1_Set_Controller_Mode
- Length: 8 bytes
- Sender: ['Master']

### ID: 44 - Axis1_Set_Input_Pos
- Name: Axis1_Set_Input_Pos
- Length: 8 bytes
- Sender: ['Master']

### ID: 45 - Axis1_Set_Input_Vel
- Name: Axis1_Set_Input_Vel
- Length: 8 bytes
- Sender: ['Master']

### ID: 46 - Axis1_Set_Input_Torque
- Name: Axis1_Set_Input_Torque
- Length: 8 bytes
- Sender: ['Master']

### ID: 47 - Axis1_Set_Limits
- Name: Axis1_Set_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 49 - Axis1_Set_Traj_Vel_Limit
- Name: Axis1_Set_Traj_Vel_Limit
- Length: 8 bytes
- Sender: ['Master']

### ID: 50 - Axis1_Set_Traj_Accel_Limits
- Name: Axis1_Set_Traj_Accel_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 51 - Axis1_Set_Traj_Inertia
- Name: Axis1_Set_Traj_Inertia
- Length: 8 bytes
- Sender: ['Master']

### ID: 52 - Axis1_Get_Iq
- Name: Axis1_Get_Iq
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 53 - Axis1_Get_Temperature
- Name: Axis1_Get_Temperature
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 54 - Axis1_Reboot
- Name: Axis1_Reboot
- Length: 1 bytes
- Sender: ['Master']

### ID: 55 - Axis1_Get_Bus_Voltage_Current
- Name: Axis1_Get_Bus_Voltage_Current
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 56 - Axis1_Clear_Errors
- Name: Axis1_Clear_Errors
- Length: 1 bytes
- Sender: ['Master']

### ID: 57 - Axis1_Set_Absolute_Position
- Name: Axis1_Set_Absolute_Position
- Length: 8 bytes
- Sender: ['Master']

### ID: 58 - Axis1_Set_Pos_Gain
- Name: Axis1_Set_Pos_Gain
- Length: 8 bytes
- Sender: ['Master']

### ID: 59 - Axis1_Set_Vel_Gains
- Name: Axis1_Set_Vel_Gains
- Length: 8 bytes
- Sender: ['Master']

### ID: 60 - Axis1_Get_Torques
- Name: Axis1_Get_Torques
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 61 - Axis1_Get_Powers
- Name: Axis1_Get_Powers
- Length: 8 bytes
- Sender: ['ODrive_Axis1']

### ID: 63 - Axis1_Enter_DFU_Mode
- Name: Axis1_Enter_DFU_Mode
- Length: 0 bytes
- Sender: ['Master']

### ID: 64 - Axis2_Get_Version
- Name: Axis2_Get_Version
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 65 - Axis2_Heartbeat
- Name: Axis2_Heartbeat
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 66 - Axis2_Estop
- Name: Axis2_Estop
- Length: 0 bytes
- Sender: ['Master']

### ID: 67 - Axis2_Get_Error
- Name: Axis2_Get_Error
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 68 - Axis2_RxSdo
- Name: Axis2_RxSdo
- Length: 8 bytes
- Sender: ['Master']

### ID: 69 - Axis2_TxSdo
- Name: Axis2_TxSdo
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 70 - Axis2_Address
- Name: Axis2_Address
- Length: 8 bytes
- Sender: ['Master', 'ODrive_Axis2']

### ID: 71 - Axis2_Set_Axis_State
- Name: Axis2_Set_Axis_State
- Length: 8 bytes
- Sender: ['Master']

### ID: 73 - Axis2_Get_Encoder_Estimates
- Name: Axis2_Get_Encoder_Estimates
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 75 - Axis2_Set_Controller_Mode
- Name: Axis2_Set_Controller_Mode
- Length: 8 bytes
- Sender: ['Master']

### ID: 76 - Axis2_Set_Input_Pos
- Name: Axis2_Set_Input_Pos
- Length: 8 bytes
- Sender: ['Master']

### ID: 77 - Axis2_Set_Input_Vel
- Name: Axis2_Set_Input_Vel
- Length: 8 bytes
- Sender: ['Master']

### ID: 78 - Axis2_Set_Input_Torque
- Name: Axis2_Set_Input_Torque
- Length: 8 bytes
- Sender: ['Master']

### ID: 79 - Axis2_Set_Limits
- Name: Axis2_Set_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 81 - Axis2_Set_Traj_Vel_Limit
- Name: Axis2_Set_Traj_Vel_Limit
- Length: 8 bytes
- Sender: ['Master']

### ID: 82 - Axis2_Set_Traj_Accel_Limits
- Name: Axis2_Set_Traj_Accel_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 83 - Axis2_Set_Traj_Inertia
- Name: Axis2_Set_Traj_Inertia
- Length: 8 bytes
- Sender: ['Master']

### ID: 84 - Axis2_Get_Iq
- Name: Axis2_Get_Iq
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 85 - Axis2_Get_Temperature
- Name: Axis2_Get_Temperature
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 86 - Axis2_Reboot
- Name: Axis2_Reboot
- Length: 1 bytes
- Sender: ['Master']

### ID: 87 - Axis2_Get_Bus_Voltage_Current
- Name: Axis2_Get_Bus_Voltage_Current
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 88 - Axis2_Clear_Errors
- Name: Axis2_Clear_Errors
- Length: 1 bytes
- Sender: ['Master']

### ID: 89 - Axis2_Set_Absolute_Position
- Name: Axis2_Set_Absolute_Position
- Length: 8 bytes
- Sender: ['Master']

### ID: 90 - Axis2_Set_Pos_Gain
- Name: Axis2_Set_Pos_Gain
- Length: 8 bytes
- Sender: ['Master']

### ID: 91 - Axis2_Set_Vel_Gains
- Name: Axis2_Set_Vel_Gains
- Length: 8 bytes
- Sender: ['Master']

### ID: 92 - Axis2_Get_Torques
- Name: Axis2_Get_Torques
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 93 - Axis2_Get_Powers
- Name: Axis2_Get_Powers
- Length: 8 bytes
- Sender: ['ODrive_Axis2']

### ID: 95 - Axis2_Enter_DFU_Mode
- Name: Axis2_Enter_DFU_Mode
- Length: 0 bytes
- Sender: ['Master']

### ID: 96 - Axis3_Get_Version
- Name: Axis3_Get_Version
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 97 - Axis3_Heartbeat
- Name: Axis3_Heartbeat
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 98 - Axis3_Estop
- Name: Axis3_Estop
- Length: 0 bytes
- Sender: ['Master']

### ID: 99 - Axis3_Get_Error
- Name: Axis3_Get_Error
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 100 - Axis3_RxSdo
- Name: Axis3_RxSdo
- Length: 8 bytes
- Sender: ['Master']

### ID: 101 - Axis3_TxSdo
- Name: Axis3_TxSdo
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 102 - Axis3_Address
- Name: Axis3_Address
- Length: 8 bytes
- Sender: ['Master', 'ODrive_Axis3']

### ID: 103 - Axis3_Set_Axis_State
- Name: Axis3_Set_Axis_State
- Length: 8 bytes
- Sender: ['Master']

### ID: 105 - Axis3_Get_Encoder_Estimates
- Name: Axis3_Get_Encoder_Estimates
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 107 - Axis3_Set_Controller_Mode
- Name: Axis3_Set_Controller_Mode
- Length: 8 bytes
- Sender: ['Master']

### ID: 108 - Axis3_Set_Input_Pos
- Name: Axis3_Set_Input_Pos
- Length: 8 bytes
- Sender: ['Master']

### ID: 109 - Axis3_Set_Input_Vel
- Name: Axis3_Set_Input_Vel
- Length: 8 bytes
- Sender: ['Master']

### ID: 110 - Axis3_Set_Input_Torque
- Name: Axis3_Set_Input_Torque
- Length: 8 bytes
- Sender: ['Master']

### ID: 111 - Axis3_Set_Limits
- Name: Axis3_Set_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 113 - Axis3_Set_Traj_Vel_Limit
- Name: Axis3_Set_Traj_Vel_Limit
- Length: 8 bytes
- Sender: ['Master']

### ID: 114 - Axis3_Set_Traj_Accel_Limits
- Name: Axis3_Set_Traj_Accel_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 115 - Axis3_Set_Traj_Inertia
- Name: Axis3_Set_Traj_Inertia
- Length: 8 bytes
- Sender: ['Master']

### ID: 116 - Axis3_Get_Iq
- Name: Axis3_Get_Iq
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 117 - Axis3_Get_Temperature
- Name: Axis3_Get_Temperature
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 118 - Axis3_Reboot
- Name: Axis3_Reboot
- Length: 1 bytes
- Sender: ['Master']

### ID: 119 - Axis3_Get_Bus_Voltage_Current
- Name: Axis3_Get_Bus_Voltage_Current
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 120 - Axis3_Clear_Errors
- Name: Axis3_Clear_Errors
- Length: 1 bytes
- Sender: ['Master']

### ID: 121 - Axis3_Set_Absolute_Position
- Name: Axis3_Set_Absolute_Position
- Length: 8 bytes
- Sender: ['Master']

### ID: 122 - Axis3_Set_Pos_Gain
- Name: Axis3_Set_Pos_Gain
- Length: 8 bytes
- Sender: ['Master']

### ID: 123 - Axis3_Set_Vel_Gains
- Name: Axis3_Set_Vel_Gains
- Length: 8 bytes
- Sender: ['Master']

### ID: 124 - Axis3_Get_Torques
- Name: Axis3_Get_Torques
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 125 - Axis3_Get_Powers
- Name: Axis3_Get_Powers
- Length: 8 bytes
- Sender: ['ODrive_Axis3']

### ID: 127 - Axis3_Enter_DFU_Mode
- Name: Axis3_Enter_DFU_Mode
- Length: 0 bytes
- Sender: ['Master']

### ID: 128 - Axis4_Get_Version
- Name: Axis4_Get_Version
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 129 - Axis4_Heartbeat
- Name: Axis4_Heartbeat
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 130 - Axis4_Estop
- Name: Axis4_Estop
- Length: 0 bytes
- Sender: ['Master']

### ID: 131 - Axis4_Get_Error
- Name: Axis4_Get_Error
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 132 - Axis4_RxSdo
- Name: Axis4_RxSdo
- Length: 8 bytes
- Sender: ['Master']

### ID: 133 - Axis4_TxSdo
- Name: Axis4_TxSdo
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 134 - Axis4_Address
- Name: Axis4_Address
- Length: 8 bytes
- Sender: ['Master', 'ODrive_Axis4']

### ID: 135 - Axis4_Set_Axis_State
- Name: Axis4_Set_Axis_State
- Length: 8 bytes
- Sender: ['Master']

### ID: 137 - Axis4_Get_Encoder_Estimates
- Name: Axis4_Get_Encoder_Estimates
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 139 - Axis4_Set_Controller_Mode
- Name: Axis4_Set_Controller_Mode
- Length: 8 bytes
- Sender: ['Master']

### ID: 140 - Axis4_Set_Input_Pos
- Name: Axis4_Set_Input_Pos
- Length: 8 bytes
- Sender: ['Master']

### ID: 141 - Axis4_Set_Input_Vel
- Name: Axis4_Set_Input_Vel
- Length: 8 bytes
- Sender: ['Master']

### ID: 142 - Axis4_Set_Input_Torque
- Name: Axis4_Set_Input_Torque
- Length: 8 bytes
- Sender: ['Master']

### ID: 143 - Axis4_Set_Limits
- Name: Axis4_Set_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 145 - Axis4_Set_Traj_Vel_Limit
- Name: Axis4_Set_Traj_Vel_Limit
- Length: 8 bytes
- Sender: ['Master']

### ID: 146 - Axis4_Set_Traj_Accel_Limits
- Name: Axis4_Set_Traj_Accel_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 147 - Axis4_Set_Traj_Inertia
- Name: Axis4_Set_Traj_Inertia
- Length: 8 bytes
- Sender: ['Master']

### ID: 148 - Axis4_Get_Iq
- Name: Axis4_Get_Iq
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 149 - Axis4_Get_Temperature
- Name: Axis4_Get_Temperature
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 150 - Axis4_Reboot
- Name: Axis4_Reboot
- Length: 1 bytes
- Sender: ['Master']

### ID: 151 - Axis4_Get_Bus_Voltage_Current
- Name: Axis4_Get_Bus_Voltage_Current
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 152 - Axis4_Clear_Errors
- Name: Axis4_Clear_Errors
- Length: 1 bytes
- Sender: ['Master']

### ID: 153 - Axis4_Set_Absolute_Position
- Name: Axis4_Set_Absolute_Position
- Length: 8 bytes
- Sender: ['Master']

### ID: 154 - Axis4_Set_Pos_Gain
- Name: Axis4_Set_Pos_Gain
- Length: 8 bytes
- Sender: ['Master']

### ID: 155 - Axis4_Set_Vel_Gains
- Name: Axis4_Set_Vel_Gains
- Length: 8 bytes
- Sender: ['Master']

### ID: 156 - Axis4_Get_Torques
- Name: Axis4_Get_Torques
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 157 - Axis4_Get_Powers
- Name: Axis4_Get_Powers
- Length: 8 bytes
- Sender: ['ODrive_Axis4']

### ID: 159 - Axis4_Enter_DFU_Mode
- Name: Axis4_Enter_DFU_Mode
- Length: 0 bytes
- Sender: ['Master']

### ID: 160 - Axis5_Get_Version
- Name: Axis5_Get_Version
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 161 - Axis5_Heartbeat
- Name: Axis5_Heartbeat
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 162 - Axis5_Estop
- Name: Axis5_Estop
- Length: 0 bytes
- Sender: ['Master']

### ID: 163 - Axis5_Get_Error
- Name: Axis5_Get_Error
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 164 - Axis5_RxSdo
- Name: Axis5_RxSdo
- Length: 8 bytes
- Sender: ['Master']

### ID: 165 - Axis5_TxSdo
- Name: Axis5_TxSdo
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 166 - Axis5_Address
- Name: Axis5_Address
- Length: 8 bytes
- Sender: ['Master', 'ODrive_Axis5']

### ID: 167 - Axis5_Set_Axis_State
- Name: Axis5_Set_Axis_State
- Length: 8 bytes
- Sender: ['Master']

### ID: 169 - Axis5_Get_Encoder_Estimates
- Name: Axis5_Get_Encoder_Estimates
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 171 - Axis5_Set_Controller_Mode
- Name: Axis5_Set_Controller_Mode
- Length: 8 bytes
- Sender: ['Master']

### ID: 172 - Axis5_Set_Input_Pos
- Name: Axis5_Set_Input_Pos
- Length: 8 bytes
- Sender: ['Master']

### ID: 173 - Axis5_Set_Input_Vel
- Name: Axis5_Set_Input_Vel
- Length: 8 bytes
- Sender: ['Master']

### ID: 174 - Axis5_Set_Input_Torque
- Name: Axis5_Set_Input_Torque
- Length: 8 bytes
- Sender: ['Master']

### ID: 175 - Axis5_Set_Limits
- Name: Axis5_Set_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 177 - Axis5_Set_Traj_Vel_Limit
- Name: Axis5_Set_Traj_Vel_Limit
- Length: 8 bytes
- Sender: ['Master']

### ID: 178 - Axis5_Set_Traj_Accel_Limits
- Name: Axis5_Set_Traj_Accel_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 179 - Axis5_Set_Traj_Inertia
- Name: Axis5_Set_Traj_Inertia
- Length: 8 bytes
- Sender: ['Master']

### ID: 180 - Axis5_Get_Iq
- Name: Axis5_Get_Iq
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 181 - Axis5_Get_Temperature
- Name: Axis5_Get_Temperature
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 182 - Axis5_Reboot
- Name: Axis5_Reboot
- Length: 1 bytes
- Sender: ['Master']

### ID: 183 - Axis5_Get_Bus_Voltage_Current
- Name: Axis5_Get_Bus_Voltage_Current
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 184 - Axis5_Clear_Errors
- Name: Axis5_Clear_Errors
- Length: 1 bytes
- Sender: ['Master']

### ID: 185 - Axis5_Set_Absolute_Position
- Name: Axis5_Set_Absolute_Position
- Length: 8 bytes
- Sender: ['Master']

### ID: 186 - Axis5_Set_Pos_Gain
- Name: Axis5_Set_Pos_Gain
- Length: 8 bytes
- Sender: ['Master']

### ID: 187 - Axis5_Set_Vel_Gains
- Name: Axis5_Set_Vel_Gains
- Length: 8 bytes
- Sender: ['Master']

### ID: 188 - Axis5_Get_Torques
- Name: Axis5_Get_Torques
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 189 - Axis5_Get_Powers
- Name: Axis5_Get_Powers
- Length: 8 bytes
- Sender: ['ODrive_Axis5']

### ID: 191 - Axis5_Enter_DFU_Mode
- Name: Axis5_Enter_DFU_Mode
- Length: 0 bytes
- Sender: ['Master']

### ID: 192 - Axis6_Get_Version
- Name: Axis6_Get_Version
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 193 - Axis6_Heartbeat
- Name: Axis6_Heartbeat
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 194 - Axis6_Estop
- Name: Axis6_Estop
- Length: 0 bytes
- Sender: ['Master']

### ID: 195 - Axis6_Get_Error
- Name: Axis6_Get_Error
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 196 - Axis6_RxSdo
- Name: Axis6_RxSdo
- Length: 8 bytes
- Sender: ['Master']

### ID: 197 - Axis6_TxSdo
- Name: Axis6_TxSdo
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 198 - Axis6_Address
- Name: Axis6_Address
- Length: 8 bytes
- Sender: ['Master', 'ODrive_Axis6']

### ID: 199 - Axis6_Set_Axis_State
- Name: Axis6_Set_Axis_State
- Length: 8 bytes
- Sender: ['Master']

### ID: 201 - Axis6_Get_Encoder_Estimates
- Name: Axis6_Get_Encoder_Estimates
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 203 - Axis6_Set_Controller_Mode
- Name: Axis6_Set_Controller_Mode
- Length: 8 bytes
- Sender: ['Master']

### ID: 204 - Axis6_Set_Input_Pos
- Name: Axis6_Set_Input_Pos
- Length: 8 bytes
- Sender: ['Master']

### ID: 205 - Axis6_Set_Input_Vel
- Name: Axis6_Set_Input_Vel
- Length: 8 bytes
- Sender: ['Master']

### ID: 206 - Axis6_Set_Input_Torque
- Name: Axis6_Set_Input_Torque
- Length: 8 bytes
- Sender: ['Master']

### ID: 207 - Axis6_Set_Limits
- Name: Axis6_Set_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 209 - Axis6_Set_Traj_Vel_Limit
- Name: Axis6_Set_Traj_Vel_Limit
- Length: 8 bytes
- Sender: ['Master']

### ID: 210 - Axis6_Set_Traj_Accel_Limits
- Name: Axis6_Set_Traj_Accel_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 211 - Axis6_Set_Traj_Inertia
- Name: Axis6_Set_Traj_Inertia
- Length: 8 bytes
- Sender: ['Master']

### ID: 212 - Axis6_Get_Iq
- Name: Axis6_Get_Iq
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 213 - Axis6_Get_Temperature
- Name: Axis6_Get_Temperature
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 214 - Axis6_Reboot
- Name: Axis6_Reboot
- Length: 1 bytes
- Sender: ['Master']

### ID: 215 - Axis6_Get_Bus_Voltage_Current
- Name: Axis6_Get_Bus_Voltage_Current
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 216 - Axis6_Clear_Errors
- Name: Axis6_Clear_Errors
- Length: 1 bytes
- Sender: ['Master']

### ID: 217 - Axis6_Set_Absolute_Position
- Name: Axis6_Set_Absolute_Position
- Length: 8 bytes
- Sender: ['Master']

### ID: 218 - Axis6_Set_Pos_Gain
- Name: Axis6_Set_Pos_Gain
- Length: 8 bytes
- Sender: ['Master']

### ID: 219 - Axis6_Set_Vel_Gains
- Name: Axis6_Set_Vel_Gains
- Length: 8 bytes
- Sender: ['Master']

### ID: 220 - Axis6_Get_Torques
- Name: Axis6_Get_Torques
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 221 - Axis6_Get_Powers
- Name: Axis6_Get_Powers
- Length: 8 bytes
- Sender: ['ODrive_Axis6']

### ID: 223 - Axis6_Enter_DFU_Mode
- Name: Axis6_Enter_DFU_Mode
- Length: 0 bytes
- Sender: ['Master']

### ID: 224 - Axis7_Get_Version
- Name: Axis7_Get_Version
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 225 - Axis7_Heartbeat
- Name: Axis7_Heartbeat
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 226 - Axis7_Estop
- Name: Axis7_Estop
- Length: 0 bytes
- Sender: ['Master']

### ID: 227 - Axis7_Get_Error
- Name: Axis7_Get_Error
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 228 - Axis7_RxSdo
- Name: Axis7_RxSdo
- Length: 8 bytes
- Sender: ['Master']

### ID: 229 - Axis7_TxSdo
- Name: Axis7_TxSdo
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 230 - Axis7_Address
- Name: Axis7_Address
- Length: 8 bytes
- Sender: ['Master', 'ODrive_Axis7']

### ID: 231 - Axis7_Set_Axis_State
- Name: Axis7_Set_Axis_State
- Length: 8 bytes
- Sender: ['Master']

### ID: 233 - Axis7_Get_Encoder_Estimates
- Name: Axis7_Get_Encoder_Estimates
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 235 - Axis7_Set_Controller_Mode
- Name: Axis7_Set_Controller_Mode
- Length: 8 bytes
- Sender: ['Master']

### ID: 236 - Axis7_Set_Input_Pos
- Name: Axis7_Set_Input_Pos
- Length: 8 bytes
- Sender: ['Master']

### ID: 237 - Axis7_Set_Input_Vel
- Name: Axis7_Set_Input_Vel
- Length: 8 bytes
- Sender: ['Master']

### ID: 238 - Axis7_Set_Input_Torque
- Name: Axis7_Set_Input_Torque
- Length: 8 bytes
- Sender: ['Master']

### ID: 239 - Axis7_Set_Limits
- Name: Axis7_Set_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 241 - Axis7_Set_Traj_Vel_Limit
- Name: Axis7_Set_Traj_Vel_Limit
- Length: 8 bytes
- Sender: ['Master']

### ID: 242 - Axis7_Set_Traj_Accel_Limits
- Name: Axis7_Set_Traj_Accel_Limits
- Length: 8 bytes
- Sender: ['Master']

### ID: 243 - Axis7_Set_Traj_Inertia
- Name: Axis7_Set_Traj_Inertia
- Length: 8 bytes
- Sender: ['Master']

### ID: 244 - Axis7_Get_Iq
- Name: Axis7_Get_Iq
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 245 - Axis7_Get_Temperature
- Name: Axis7_Get_Temperature
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 246 - Axis7_Reboot
- Name: Axis7_Reboot
- Length: 1 bytes
- Sender: ['Master']

### ID: 247 - Axis7_Get_Bus_Voltage_Current
- Name: Axis7_Get_Bus_Voltage_Current
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 248 - Axis7_Clear_Errors
- Name: Axis7_Clear_Errors
- Length: 1 bytes
- Sender: ['Master']

### ID: 249 - Axis7_Set_Absolute_Position
- Name: Axis7_Set_Absolute_Position
- Length: 8 bytes
- Sender: ['Master']

### ID: 250 - Axis7_Set_Pos_Gain
- Name: Axis7_Set_Pos_Gain
- Length: 8 bytes
- Sender: ['Master']

### ID: 251 - Axis7_Set_Vel_Gains
- Name: Axis7_Set_Vel_Gains
- Length: 8 bytes
- Sender: ['Master']

### ID: 252 - Axis7_Get_Torques
- Name: Axis7_Get_Torques
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 253 - Axis7_Get_Powers
- Name: Axis7_Get_Powers
- Length: 8 bytes
- Sender: ['ODrive_Axis7']

### ID: 255 - Axis7_Enter_DFU_Mode
- Name: Axis7_Enter_DFU_Mode
- Length: 0 bytes
- Sender: ['Master']

