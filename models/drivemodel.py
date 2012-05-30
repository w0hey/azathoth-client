from gtkmvc import Model

class DriveModel(Model):
    estop_act = "N/A"
    estop_cmd = "N/A"
    select_act = "N/A"
    select_cmd = "N/A"
    moving = "Unknown"
    xpos = 0
    ypos = 0
    xval = 0
    yval = 0
    cal_initial_x = 0
    cal_initial_y = 0
    cal_current_x = 0
    cal_current_y = 0
    cal_eeprom_x = 0
    cal_eeprom_y = 0
    deadman = True
    counting = True
    looper = None

    __observables__ = ("estop_act", "estop_cmd", "select_act", "select_cmd", "moving",
                        "xpos", "ypos", "xval", "yval", "cal_initial_x", "cal_initial_y",
                        "cal_current_x", "cal_current_y", "cal_eeprom_x", "cal_eeprom_y",
                        "deadman")

    def __init__(self, parent):
        Model.__init__(self)
        self.parent = parent
        self.factory = self.parent.factory

    def joystickCommand(self, x, y):
        if not self.counting and (x | y != 0):
            self.looper = task.LoopingCall(self.joystickCommand, (x, y))
            self.looper.start(0.2) # Run every 200ms
        self.factory.control.send_joystick_command(x, y)
        self.parent.joy_x = x
        self.parent.joy_y = y
        if self.counting:
            self.looper.reset()
            if (x | y = 0):
                self.looper.stop()

    def onStatusUpdate(self, status, xpos, ypos, xval, yval):
        self.estop_act = 'RUN' if (status & 0x01 == 0x01) else 'STOP'
        self.estop_cmd = 'RUN' if (status & 0x02 == 0x02) else 'STOP'
        self.select_act = 'ROBOT' if (status & 0x04 == 0x04) else 'CHAIR'
        self.select_cmd = 'ROBOT' if (status & 0x08 == 0x08) else 'CHAIR'
        self.moving = 'MOVING' if (status & 0x10 == 0x10) else 'STOPPED'

    def onReceiveInitialCalibration(self, d):
        self.cal_initial_x = d['current_x']
        self.cal_initial_y = d['current_y']
        return d

    def onReceiveCalibration(self, d):
        self.cal_current_x = d['current_x']
        self.cal_current_y = d['current_y']
        self.cal_eeprom_x = d['eeprom_x']
        self.cal_eeprom_y = d['eeprom_y']
        return d

    def select(self):
        self.factory.control.send_select_command(True)

    def deselect(self):
        self.factory.control.send_select_command(False)

    def estop(self):
        self.factory.control.send_estop_command()

    def reset(self):
        self.factory.control.send_reset_command()

    def requestCalibration(self):
        d = self.factory.control.req_cal_values()
        d.addCallback(self.onReceiveInitialCalibration)
        d.addCallback(self.onReceiveCalibration)
