
def pickup_tips_multi_WL(protocolFile, pipet, tipLabware, well):
    protocolFile.write("    " + pipet + ".pick_up_tip(" + tipLabware + ".wells()[" + str(well) + "], 1, 1.0)\n")


def pickup_tips_single_WL(protocolFile, pipet, tipLabware, well):
    protocolFile.write("    " + pipet + ".pick_up_tip(" + tipLabware + ".wells()[" + str(well) + "], 1, 1.0)\n")


def pipet_Zaxis_speed_WL(protocolFile, speed):
    protocolFile.write("    protocol.max_speeds['Z'] = " + str(speed) + "\n")  # only for left Pipette


def pipet_Xaxis_speed_WL(protocolFile, speed):
    protocolFile.write("    protocol.max_speeds['X'] = " + str(speed) + "\n")


def pipet_Yaxis_speed_WL(protocolFile, speed):
    protocolFile.write("    protocol.max_speeds['Y'] = " + str(speed) + "\n")


def aspirate_SaP_WL(protocolFile, pipet, labware, well, volume, flow_rate):
    if volume != 0:
        protocolFile.write("    " + pipet + ".aspirate(" + str(volume) + ", " + labware + ".wells()[" + str(well) + "], "+ str(flow_rate)
                           + ")\n")

def dispense_SaP_WL(protocolFile, pipet, labware, well, volume, flow_rate):
    if volume != 0:
        protocolFile.write("    " + pipet + ".dispense(" + str(volume) + ", " + labware + ".wells()[" + str(well) + "].top(3), "+ str(flow_rate)
                           + ")\n")


def consolidate_SaP_WL(protocolFile, pipet, volume, list_of_source_well, dest_well):
    if volume != 0:
        protocolFile.write(
            "    " + pipet + ".consolidate(" + str(volume) + ", " + str(list_of_source_well) + ", " + str(
                dest_well)
            + ")\n")

def distribute_SaP_WL(protocolFile, pipet, volume, list_of_source_well, dest_well):
    if volume != 0:
        protocolFile.write(
            "    " + pipet + ".distribute(" + str(volume) + ", " + str(list_of_source_well) + ", " + str(
                dest_well)
            + ")\n")


def air_gap_WL(protocolFile, pipet, air_vol):
    protocolFile.write("    " + pipet + ".air_gap(" + str(air_vol) + ", 20)\n")


def return_WL(protocolFile, pipet):
    protocolFile.write("    " + pipet + ".return_tip()\n")


def drop_WL(protocolFile, pipet):
    protocolFile.write("    " + pipet + ".drop_tip()\n")


def mix_SaP_WL(protocolFile, pipet, repetitions, volume, labware, well, flow_rate):
    protocolFile.write("    " + pipet + ".mix(" + str(repetitions) + ", " + str(volume) + ", " + labware + ".wells()[" + str(well) + "], "
                       + str(flow_rate)+")\n")


def blow_out_WL(protocolFile, pipet, location=""):
    protocolFile.write("    " + pipet + ".blow_out(" + location + ")\n")


def touch_tip_WL(protocolFile, pipet, location, radius=1, offset=-1):
    protocolFile.write("    " + pipet + ".touch_tip(" + location + ", radius=" + str(radius) + ", v_offset=" + str(offset) + ")\n")

def touch_tip_SaP_WL(protocolFile, pipet, labware, well, radius=1, offset=-3):
    protocolFile.write("    " + pipet + ".touch_tip(" + labware + ".wells()[" + str(well) + "], radius=" + str(radius) + ", v_offset=" + str(offset) + ")\n")


def move_to_WL(protocolFile, pipet, location):
    protocolFile.write("    " + pipet + ".move_to(" + str(location) + ")\n")


def delay_WL(protocolFile, seconds=0, minutes=0):
    protocolFile.write("    protocol.delay(seconds=" + str(seconds) + ", minutes=" + str(minutes) + ")\n")
    protocolFile.write("\n")


def comment_WL(protocolFile: object, msg: object) -> object:
    protocolFile.write("    protocol.comment(\"" + msg + "\")\n")


def pause_WL(protocolFile):
    protocolFile.write("    protocol.pause()\n")



# Arduino elementary functions
def sendSerial(protocolFile, COMPORT, intToTransfer):
    protocolFile.write("    ser = serial.Serial(\"" + str(COMPORT) + "\", 9600)\n")
    protocolFile.write("    ser.write(b\'" + str(intToTransfer) + "\\r\\n\')\n")
    protocolFile.write("    ser.close()\n")
    protocolFile.write("\n")


def startStirring_variable(protocolFile, COMPORT, speed):
    comment_WL(protocolFile, "Start Stirring")
    sendSerial(protocolFile, COMPORT, speed)

def startStirring(protocolFile, COMPORT):
    comment_WL(protocolFile, "Start Stirring")
    sendSerial(protocolFile, COMPORT, 900)


def stopStirring(protocolFile, COMPORT):
    comment_WL(protocolFile, "Stop Stirring")
    sendSerial(protocolFile, COMPORT, 1)


def startVac(protocolFile, COMPORT):
    comment_WL(protocolFile, "Start Vac")
    sendSerial(protocolFile, COMPORT, 2500)


def stopVac(protocolFile, COMPORT):
    comment_WL(protocolFile, "Stop Vac")
    sendSerial(protocolFile, COMPORT, 3000)


def startHeating(protocolFile, COMPORT):
    comment_WL(protocolFile, "Start heating")
    sendSerial(protocolFile, COMPORT, 1500)


def stopHeating(protocolFile, COMPORT):
    comment_WL(protocolFile, "Stop heating")
    sendSerial(protocolFile, COMPORT, 2000)


def startVent (protocolFile, COMPORT):
    comment_WL(protocolFile, "Start vent")
    sendSerial(protocolFile, COMPORT, 3500)


def stopVent (protocolFile, COMPORT):
    comment_WL(protocolFile, "Stop vent")
    sendSerial(protocolFile, COMPORT, 4000)



def vacuum(protocolFile, COMPORT, VacSeconds=0, VacMinutes=0, VentSeconds=12, VentMinutes=0):
    startVac(protocolFile, COMPORT)
    delay_WL(protocolFile, VacSeconds-6, VacMinutes)
    startVent(protocolFile, COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, COMPORT)
    delay_WL(protocolFile, VentSeconds-6, VentMinutes)
    stopVent(protocolFile, COMPORT)


def vent(protocolFile, COMPORT, seconds=0, minutes=0):
    startVent(protocolFile, COMPORT)
    delay_WL(protocolFile, seconds, minutes)
    stopVent(protocolFile, COMPORT)
