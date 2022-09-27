from e_SaP_elementaryCommands import *

speed_fast = 1300
speed_slow = 900
first_volume = 80
second_volume = 180
volume_SaP = first_volume + second_volume
bottom_1 = 1.3
bottom_2 = 0.7
bottom_3 = 0.3
vacuum_between_trans = 15

def header_SaP_wl(protocol_file, tiprack, reagentReservoir, filterPlate, desaltingPlate, mount_single_channel, mount_multi_channel):  # ot2=1 means P20 on OT2
    protocol_file.write("from opentrons import protocol_api, types\n"
                        "import serial\n"
                        "metadata = {\'apiLevel\': \'2.3\'}\n")
    protocol_file.write("\n")
    protocol_file.write("def run(protocol: protocol_api.ProtocolContext):\n")
    protocol_file.write("\n")
    protocol_file.write("    p300_single = protocol.load_instrument(\'p300_single_gen2\', \'"+mount_single_channel+"\')\n")
    protocol_file.write("    p300_multi = protocol.load_instrument(\'p300_multi_gen2\', \'"+mount_multi_channel+"\')\n")
    protocol_file.write("\n")
    protocol_file.write("    tiprack_300 = protocol.load_labware(\'"+tiprack[0]+"\', "+tiprack[1]+")\n")
    protocol_file.write("\n")
    protocol_file.write("    FilterPlate = protocol.load_labware(\'"+filterPlate[0]+"\', "+filterPlate[1]+")\n")
    protocol_file.write("\n")
    protocol_file.write("    ReagentReservoir = protocol.load_labware(\'"+reagentReservoir[0]+"\', "+reagentReservoir[1]+")\n")
    protocol_file.write("\n")
    protocol_file.write(
        "    DesaltingPlate = protocol.load_labware(\'" + desaltingPlate[0] + "\', " + desaltingPlate[1] + ")\n")
    protocol_file.write("\n")





def full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, multi_pipet, single_pipet, labware_list):
    MARC_COMPORT = None
    MARC_COMPORT = "/dev/ttyACM0"


    # Pipets and labware definition

    pipet300_multi = multi_pipet
    pipet300_single = single_pipet

    FilterPlate = labware_list[0]
    ReagentReservoir = labware_list[1]
    tips_300 = labware_list[2]

    # Pipetting parameter

    AIR_GAP_VOL = 10
    DISPENSE_HEIGHT = str(-1)
    ASPIRATION_DEPTH = labware_list[3][0]
    ASP_FLOW_RATE = labware_list[3][1]
    DISP_FLOW_RATE = labware_list[3][2]

    # Volume for split and pool

    volume_SaP = labware_list[5]

    # Precision pipetting

    precision_asp_depth = labware_list[4][0]
    precision_flow_rate = labware_list[4][1]
    precision_flow_rate_2 = '2'

    # Define functions dispense and aspirate

    def dispense_SaP_WL(protocolFile, pipet, labware, well, volume, flow_rate):
        if volume != 0:
            protocolFile.write("    " + pipet + ".dispense(" + str(volume) + ", " + labware + ".wells()[" + str(
                well) + "].top("+DISPENSE_HEIGHT+"), " + str(flow_rate)
                               + ")\n")

    def aspirate_SaP_WL(protocolFile, pipet, labware, well, volume, flow_rate):
        if volume != 0:
            protocolFile.write(
                "    " + pipet + ".aspirate(" + str(volume) + ", " + labware + ".wells()[" + str(well) + "].bottom("+ASPIRATION_DEPTH+"), "+ str(
                    flow_rate)
                + ")\n")

    def aspirate_split_SaP_WL(protocolFile, pipet, labware, well, volume, asp_depth, flow_rate):
        if volume != 0:
            protocolFile.write(
                "    " + pipet + ".aspirate(" + str(volume) + ", " + labware + ".wells()[" + str(well) + "].bottom("+str(asp_depth)+"), "+ str(
                    flow_rate)
                + ")\n")

    def home_made_airgap(protocolFile, pipet, labware, well, volume):
        protocolFile.write(
            "    " + pipet + ".aspirate(" + str(volume) + ", " + labware + ".wells()[" + str(well) + "].top(" + str(
                30) + "), " + str(
                1)
            + ")\n")

    # Start full cycle
    comment_WL(protocolFile, "Full cycle " + str(current_cycle))
    # Split
    comment_WL(protocolFile, "Split")
    split_tip = current_cycle - 1

    if current_cycle <= 6:
        res_split_1 = 88
        res_split_2 = 89
        res_split_3 = 90

    if 7 <= current_cycle <= 12:
        res_split_1 = 91
        res_split_2 = 92
        res_split_3 = 93

    if 13 <= current_cycle <= 19:
        res_split_1 = 94
        res_split_2 = 95
        res_split_3 = 87

    if current_cycle == 1:
        # Empty first well and pickup first tips
        startVac(protocolFile, MARC_COMPORT)
        pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 0)
        pickup_tips_multi_WL(protocolFile, pipet300_multi, tips_300, 55)
        delay_WL(protocolFile, 30, 0)
        startVent(protocolFile, MARC_COMPORT)
        delay_WL(protocolFile, 20, 0)
        stopVac(protocolFile, MARC_COMPORT)
        air_gap_WL(protocolFile, pipet300_multi, 10)
        aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 64, volume_SaP - 20, 1.5)
        air_gap_WL(protocolFile, pipet300_multi, 10)
        stopVent(protocolFile, MARC_COMPORT)

        # First fill of split well
        dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, first_volume + 10, 2)
        air_gap_WL(protocolFile, pipet300_multi, 10)
        startStirring_variable(protocolFile, MARC_COMPORT, speed_fast)
        delay_WL(protocolFile, seconds=8, minutes=0)
        stopStirring(protocolFile, MARC_COMPORT)

        dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, second_volume + 20, 2)
        blow_out_WL(protocolFile, pipet300_multi)
        air_gap_WL(protocolFile, pipet300_multi, 10)
    
    

    # First split
    # Stir
    startStirring_variable(protocolFile, MARC_COMPORT, speed_slow)
    delay_WL(protocolFile, seconds=5, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    # Mix
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    mix_SaP_WL(protocolFile, pipet300_single, 2, 200, FilterPlate, split_well, 8)
    mix_SaP_WL(protocolFile, pipet300_single, 2, 220, FilterPlate, split_well, 8)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, volume_SaP - 40, bottom_1,
                          precision_flow_rate_2)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 20, bottom_2,
                          precision_flow_rate)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, split_well, AIR_GAP_VOL)
    # Dispense well 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well, (volume_SaP - 20) / 4 + AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well)
    # Dispense well 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1, (volume_SaP - 20) / 4,
                    DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1)
    # Dispense well 3
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2, (volume_SaP - 20) / 4,
                    DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2)
    # Dispense well 4
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3, (volume_SaP - 20) / 4 + AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3)
    blow_out_WL(protocolFile, pipet300_single)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, work_well + 3, AIR_GAP_VOL)

    # Fill up the split well
    startVac(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_1, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, res_split_1, volume_SaP, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_1, AIR_GAP_VOL)
    stopVac(protocolFile, MARC_COMPORT)

    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, first_volume + 10, 2)
    air_gap_WL(protocolFile, pipet300_multi, 10)
    startStirring_variable(protocolFile, MARC_COMPORT, speed_fast)
    delay_WL(protocolFile, seconds=8, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=2, minutes=0)

    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, second_volume + 20, 2)
    blow_out_WL(protocolFile, pipet300_multi)
    air_gap_WL(protocolFile, pipet300_multi, 10)

    # Stir
    startStirring_variable(protocolFile, MARC_COMPORT, speed_slow)
    delay_WL(protocolFile, seconds=5, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)

    # Second aspiration in split well
    air_gap_WL(protocolFile, pipet300_single, 5)
    mix_SaP_WL(protocolFile, pipet300_single, 2, 200, FilterPlate, split_well, 8)
    mix_SaP_WL(protocolFile, pipet300_single, 2, 220, FilterPlate, split_well, 10)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, volume_SaP - 10 - 20,
                          bottom_1,
                          precision_flow_rate_2)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 20 + 10, bottom_2,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 10 + 5, bottom_3,
                          precision_flow_rate)
    # Dispense well 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3,
                    volume_SaP / 4 + 20, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3)
    # Dispense well 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2, volume_SaP / 4, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2)
    # Dispense well 3
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1, volume_SaP / 4, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1)
    # Dispense well 4
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well, volume_SaP / 4 + AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well)
    blow_out_WL(protocolFile, pipet300_single)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, work_well, AIR_GAP_VOL)

    # Refill split well
    startVac(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_2, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, res_split_2, volume_SaP, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_2, AIR_GAP_VOL)
    stopVac(protocolFile, MARC_COMPORT)

    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, first_volume + 10, 2)
    air_gap_WL(protocolFile, pipet300_multi, 10)
    startStirring_variable(protocolFile, MARC_COMPORT, speed_fast)
    delay_WL(protocolFile, seconds=8, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=2, minutes=0)

    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, second_volume + 20, 2)
    blow_out_WL(protocolFile, pipet300_multi)
    air_gap_WL(protocolFile, pipet300_multi, 10)

    # Stir
    startStirring_variable(protocolFile, MARC_COMPORT, speed_slow)
    delay_WL(protocolFile, seconds=5, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)

    # Third aspiration in split well
    air_gap_WL(protocolFile, pipet300_single, 5)
    mix_SaP_WL(protocolFile, pipet300_single, 2, 200, FilterPlate, split_well, 8)
    mix_SaP_WL(protocolFile, pipet300_single, 2, 220, FilterPlate, split_well, 10)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, volume_SaP - 10 - 20,
                          bottom_1,
                          precision_flow_rate_2)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 20 + 10, bottom_2,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 10 + 5, bottom_3,
                          precision_flow_rate)
    # Dispense well 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3,
                    volume_SaP / 4 + AIR_GAP_VOL + 20, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3)
    # Dispense well 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2, volume_SaP / 4, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2)
    # Dispense well 3
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1, volume_SaP / 4, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1)
    # Dispense well 4
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well, volume_SaP / 4 + AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well)
    blow_out_WL(protocolFile, pipet300_single)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, work_well, AIR_GAP_VOL)

    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_3, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, res_split_3, volume_SaP - 20, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_3, AIR_GAP_VOL)
    stopVac(protocolFile, MARC_COMPORT)

    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, first_volume + 10, 2)
    air_gap_WL(protocolFile, pipet300_multi, 10)
    startStirring_variable(protocolFile, MARC_COMPORT, speed_fast)
    delay_WL(protocolFile, seconds=8, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=2, minutes=0)

    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, second_volume + 20, 2)
    blow_out_WL(protocolFile, pipet300_multi)
    air_gap_WL(protocolFile, pipet300_multi, 10)

    # Stir
    startStirring_variable(protocolFile, MARC_COMPORT, speed_slow)
    delay_WL(protocolFile, seconds=5, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)

    # Forth aspiration in split well
    air_gap_WL(protocolFile, pipet300_single, 5)
    mix_SaP_WL(protocolFile, pipet300_single, 2, 200, FilterPlate, split_well, 8)
    mix_SaP_WL(protocolFile, pipet300_single, 2, 220, FilterPlate, split_well, 10)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, volume_SaP - 10 - 20,
                          bottom_1,
                          precision_flow_rate_2)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 20 + 10, bottom_2,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 10 + 5, bottom_3,
                          precision_flow_rate)
    # Dispense well 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3,
                    volume_SaP / 4 + 20,
                    DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3)
    # Dispense well 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2, volume_SaP / 4, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2)
    # Dispense well 3
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1, volume_SaP / 4, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1)
    # Dispense well 4
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well, volume_SaP / 4 + AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well)
    blow_out_WL(protocolFile, pipet300_single)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, work_well, AIR_GAP_VOL)

    #Return pipets
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    return_WL(protocolFile, pipet300_multi)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    pickup_tips_multi_WL(protocolFile, pipet300_multi, tips_300, 60)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 0, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 0, 25, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 0, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)



    # Cycle to add a nucleotide
    comment_WL(protocolFile, "Cycle " + str(current_cycle) + " starts")
    ## Elongation
    comment_WL(protocolFile, "Elongation" + "- Cycle " + str(current_cycle))
    # Nucleotide
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, work_well, 25+2*AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, work_well, AIR_GAP_VOL)
    return_WL(protocolFile, pipet300_multi)
    # Enzyme
    pickup_tips_multi_WL(protocolFile, pipet300_multi, tips_300, 68)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 8, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 8, 25, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 8, AIR_GAP_VOL)
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, work_well, 25+2*AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, work_well, AIR_GAP_VOL)


    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_multi)
    delay_WL(protocolFile, seconds=50, minutes=3)
    stopStirring(protocolFile, MARC_COMPORT)
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_multi_WL(protocolFile, pipet300_multi, tips_300, 76)
    delay_WL(protocolFile, seconds=15, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 16, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 16, 50, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 16, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)


    ## Wash 1
    comment_WL(protocolFile, "Wash 1" + "- Cycle " + str(current_cycle))
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, work_well, 50+2*AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, work_well, AIR_GAP_VOL)


    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_multi)
    stopStirring(protocolFile, MARC_COMPORT)
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_multi_WL(protocolFile, pipet300_multi, tips_300, 84)
    delay_WL(protocolFile, seconds=15, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 24, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 24, 50, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 24, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)



    ## Deblock 1
    comment_WL(protocolFile, "Deblock 1" + "- Cycle " + str(current_cycle))
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, work_well, 50+2*AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, work_well, AIR_GAP_VOL)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 24, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 24, 50, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 24, AIR_GAP_VOL)
    delay_WL(protocolFile, seconds=25, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    # Vacuum
    vacuum(protocolFile, MARC_COMPORT, 25)



    ## Deblock 2
    comment_WL(protocolFile, "Deblock 2" + "- Cycle " + str(current_cycle))
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, work_well, 50+2*AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, work_well, AIR_GAP_VOL)


    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_multi)
    delay_WL(protocolFile, seconds=20, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_multi_WL(protocolFile, pipet300_multi, tips_300, 92)
    delay_WL(protocolFile, seconds=15, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 32, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 32, 50, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 32, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)


    ## Wash 2
    comment_WL(protocolFile, "Wash 2" + "- Cycle " + str(current_cycle))
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, work_well, 50+2*AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, work_well, AIR_GAP_VOL)



    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_multi)
    delay_WL(protocolFile, seconds=10, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_multi_WL(protocolFile, pipet300_multi, tips_300, 52)
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, split_tip + 1)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 64, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 64, volume_SaP / 4, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 64, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)



    comment_WL(protocolFile, "Cycle ends" + "- Cycle " + str(current_cycle))
    # Pool
    comment_WL(protocolFile, "Pool" + "- Cycle " + str(current_cycle))

    def transfer_whole_wells(protocolFile, well, pool_well, volume):
        # Aspirate and dispense
        air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL / 4)
        ## Aspirate well 1
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well, volume / 4 - 10, precision_asp_depth,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well, AIR_GAP_VOL / 4 + 10, 0.7,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well, AIR_GAP_VOL / 4, 0.4,
                              precision_flow_rate)
        ## Aspirate well 2
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well + 1, volume / 4 - 10,
                              precision_asp_depth,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well + 1, AIR_GAP_VOL / 4 + 10, 0.7,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well + 1, AIR_GAP_VOL / 4, 0.4,
                              precision_flow_rate)
        ## Aspirate well 3
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well + 2, volume / 4 - 10,
                              precision_asp_depth,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well + 2, AIR_GAP_VOL / 4 + 10, 0.7,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well + 2, AIR_GAP_VOL / 4, 0.4,
                              precision_flow_rate)
        ## Aspirate well 4
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well + 3, volume / 4 - 10,
                              precision_asp_depth,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well + 3, AIR_GAP_VOL / 4 + 10, 0.7,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well + 3, AIR_GAP_VOL / 4, 0.4,
                              precision_flow_rate)
        home_made_airgap(protocolFile, pipet300_single, FilterPlate, well + 3, AIR_GAP_VOL / 4)
        ## Dispense in the pool well
        dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, volume + 10 * AIR_GAP_VOL / 4,
                        DISP_FLOW_RATE)
        blow_out_WL(protocolFile, pipet300_single)
        touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well)
        blow_out_WL(protocolFile, pipet300_single)
        home_made_airgap(protocolFile, pipet300_single, FilterPlate, pool_well, AIR_GAP_VOL / 4)

    def transfer_whole_wells_mix(protocolFile, pool_well, volume, well_1, well_2, well_3, well_4):
        # Aspirate and dispense
        air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL / 4)
        mix_SaP_WL(protocolFile, pipet300_single, 2, 50, FilterPlate, well_1, 8)
        ## Aspirate well 1
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_1, 57.5, bottom_1,
                              precision_flow_rate_2)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_1, 20, bottom_2,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_1, 20, bottom_3,
                              precision_flow_rate)
        dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_2, 115, 8)
        mix_SaP_WL(protocolFile, pipet300_single, 3, 125, FilterPlate, well_2, 8)
        ## Aspirate well 2
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_2, 115,
                              bottom_1,
                              precision_flow_rate_2)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_2, 20, bottom_2,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_2, 20, bottom_3,
                              precision_flow_rate)
        dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_3, 160, 8)
        mix_SaP_WL(protocolFile, pipet300_single, 2, 180, FilterPlate, well_3, 8)
        ## Aspirate well 3
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_3, 172.5,
                              bottom_1,
                              precision_flow_rate_2)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_3, 20, bottom_2,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_3, 20, bottom_3,
                              precision_flow_rate)
        dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_4, 220, 8)
        mix_SaP_WL(protocolFile, pipet300_single, 2, 235, FilterPlate, well_4, 8)
        ## Aspirate well 4
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_4, 230,
                              bottom_1,
                              precision_flow_rate_2)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_4, 20, bottom_2,
                              precision_flow_rate)
        aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, well_4, 20, bottom_3,
                              precision_flow_rate)
        home_made_airgap(protocolFile, pipet300_single, FilterPlate, well_4, AIR_GAP_VOL / 4)
        ## Dispense in the pool well
        dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 300,
                        DISP_FLOW_RATE)
        blow_out_WL(protocolFile, pipet300_single)
        touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well)
        blow_out_WL(protocolFile, pipet300_single)
        home_made_airgap(protocolFile, pipet300_single, FilterPlate, pool_well, AIR_GAP_VOL / 4)

    # Fill the wells
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, work_well, 270 / 4 + 2 * AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, work_well, AIR_GAP_VOL)
    # Stir
    startStirring_variable(protocolFile, MARC_COMPORT, speed_fast)
    delay_WL(protocolFile, seconds=10, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    # Transfer 1
    transfer_whole_wells_mix(protocolFile, pool_well, volume_SaP, work_well, work_well + 1, work_well + 2,
                             work_well + 3)
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    startStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=vacuum_between_trans, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 72, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 72, 270 / 4, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 72, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)
    # Fill the wells
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, work_well, 270 / 4 + 2 * AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, work_well, AIR_GAP_VOL)
    # Stir
    startStirring_variable(protocolFile, MARC_COMPORT, speed_fast)
    delay_WL(protocolFile, seconds=15, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    # Transfer 2
    transfer_whole_wells_mix(protocolFile, pool_well, volume_SaP, work_well + 3, work_well + 2, work_well + 1,
                             work_well)
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    startStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=vacuum_between_trans, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 80, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 80, 270 / 4, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, 80, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)
    # Fill the wells
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, work_well, volume_SaP / 4 + 2 * AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, work_well, AIR_GAP_VOL)
    # Stir
    startStirring_variable(protocolFile, MARC_COMPORT, speed_fast)
    delay_WL(protocolFile, seconds=15, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    # Transfer 3
    transfer_whole_wells_mix(protocolFile, pool_well, volume_SaP, work_well + 2, work_well, work_well + 3,
                             work_well + 1)


    # Return tips
    return_WL(protocolFile, pipet300_multi)
    pickup_tips_multi_WL(protocolFile, pipet300_multi, tips_300, 55)



def last_transfer(current_cycle, protocolFile, split_well, multi_pipet, single_pipet, labware_list):
    MARC_COMPORT = "/dev/ttyACM0"

    # Pipets and labware definition

    pipet300_multi = multi_pipet
    pipet300_single = single_pipet

    FilterPlate = labware_list[0]
    ReagentReservoir = labware_list[1]
    tips_300 = labware_list[2]

    # Pipetting parameter

    AIR_GAP_VOL = 10
    DISPENSE_HEIGHT = str(-1)
    ASPIRATION_DEPTH = labware_list[3][0]
    ASP_FLOW_RATE = labware_list[3][1]
    DISP_FLOW_RATE = labware_list[3][2]

    # Volume for split and pool

    volume_SaP = labware_list[5]

    # Precision pipetting

    precision_asp_depth = labware_list[4][0]
    precision_flow_rate = labware_list[4][1]


    # Define functions dispense and aspirate

    def dispense_SaP_WL(protocolFile, pipet, labware, well, volume, flow_rate):
        if volume != 0:
            protocolFile.write("    " + pipet + ".dispense(" + str(volume) + ", " + labware + ".wells()[" + str(
                well) + "].top(" + DISPENSE_HEIGHT + "), " + str(flow_rate)
                               + ")\n")


    def aspirate_SaP_WL(protocolFile, pipet, labware, well, volume, flow_rate):
        if volume != 0:
            protocolFile.write(
                "    " + pipet + ".aspirate(" + str(volume) + ", " + labware + ".wells()[" + str(
                    well) + "].bottom(" + ASPIRATION_DEPTH + "), " + str(
                    flow_rate)
                + ")\n")


    def aspirate_split_SaP_WL(protocolFile, pipet, labware, well, volume, asp_depth, flow_rate):
        if volume != 0:
            protocolFile.write(
                "    " + pipet + ".aspirate(" + str(volume) + ", " + labware + ".wells()[" + str(well) + "].bottom(" + str(
                    asp_depth) + "), " + str(
                    flow_rate)
                + ")\n")


    def home_made_airgap(protocolFile, pipet, labware, well, volume):
        protocolFile.write(
            "    " + pipet + ".aspirate(" + str(volume) + ", " + labware + ".wells()[" + str(well) + "].top(" + str(
                30) + "), " + str(
                1)
            + ")\n")

    split_tip = current_cycle - 1

    if current_cycle <= 5:
        res_split_1 = 88
        res_split_2 = res_split_1 + 1

    if 6 <= current_cycle <= 12:
        res_split_1 = 90
        res_split_2 = res_split_1 + 1

    if 13 <= current_cycle <= 19:
        res_split_1 = 92
        res_split_2 = res_split_1 + 1

    work_well = 92

    # First split
    # Mix
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    mix_SaP_WL(protocolFile, pipet300_single, 3, 100, FilterPlate, split_well, 4)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, split_well, AIR_GAP_VOL)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, volume_SaP - 40, 1,
                          precision_flow_rate)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, split_well, AIR_GAP_VOL)
    # Dispense well 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well, (volume_SaP - 40) / 4 + AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well)
    # Dispense well 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1, (volume_SaP - 40) / 4, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1)
    # Dispense well 3
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2, (volume_SaP - 40) / 4, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2)
    # Dispense well 4
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3, (volume_SaP - 40) / 4 + AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3)
    blow_out_WL(protocolFile, pipet300_single)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, work_well + 3, AIR_GAP_VOL)

    # Fill up the split well
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_1, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, res_split_1, volume_SaP - 40, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_1, AIR_GAP_VOL)
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, volume_SaP - 40 + 2 * AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, split_well, AIR_GAP_VOL)

    # Second aspiration in split well
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    mix_SaP_WL(protocolFile, pipet300_single, 3, 100, FilterPlate, split_well, 4)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL / 4)
    blow_out_WL(protocolFile, pipet300_single)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, split_well, AIR_GAP_VOL)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, volume_SaP - 10 - 20,
                          precision_asp_depth,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 20 + 10, 0.7,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 10, 0.4,
                          precision_flow_rate)
    # Dispense well 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3, volume_SaP / 4 - 2.5 + AIR_GAP_VOL + 30,
                    DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3)
    # Dispense well 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2, volume_SaP / 4 - 2.5, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2)
    # Dispense well 3
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1, volume_SaP / 4 - 2.5, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1)
    # Dispense well 4
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well, volume_SaP / 4 - 2.5 + AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well)
    blow_out_WL(protocolFile, pipet300_single)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, work_well, AIR_GAP_VOL)

    # Refill split well
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_2, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, res_split_2, volume_SaP - 20, ASP_FLOW_RATE)
    home_made_airgap(protocolFile, pipet300_multi, ReagentReservoir, res_split_2, AIR_GAP_VOL)
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, split_well, volume_SaP - 15 + 2 * AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    home_made_airgap(protocolFile, pipet300_multi, FilterPlate, split_well, AIR_GAP_VOL)

    # Third aspiration in split well
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    mix_SaP_WL(protocolFile, pipet300_single, 3, 100, FilterPlate, split_well, 4)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL / 4)
    blow_out_WL(protocolFile, pipet300_single)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, split_well, AIR_GAP_VOL)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, volume_SaP - 10 - 20,
                          precision_asp_depth,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 20 + 10, 0.7,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, split_well, 10, 0.4,
                          precision_flow_rate)
    # Dispense well 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3, volume_SaP / 4 - 2.5 + AIR_GAP_VOL + 30,
                    DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 3)
    # Dispense well 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2, volume_SaP / 4 - 2.5, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 2)
    # Dispense well 3
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1, volume_SaP / 4 - 2.5, DISP_FLOW_RATE)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well + 1)
    # Dispense well 4
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well, volume_SaP / 4 - 2.5 + AIR_GAP_VOL,
                    DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, FilterPlate, work_well)
    blow_out_WL(protocolFile, pipet300_single)
    home_made_airgap(protocolFile, pipet300_single, FilterPlate, work_well, AIR_GAP_VOL)

    # Return pipets
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    return_WL(protocolFile, pipet300_multi)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVent(protocolFile, MARC_COMPORT)
