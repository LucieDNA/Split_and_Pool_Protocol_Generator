from e_SaP_elementaryCommands import *


def double_psp_for_SaP(protocolFile, multi_pipet, single_pipet, labware_list, MARC_COMPORT, pool_well, well_psp):

    sample_well = int(well_psp[0])
    control_well = int(well_psp[1])

    # Pipets and labware definition

    pipet300_multi = multi_pipet
    pipet300_single = single_pipet

    FilterPlate = labware_list[0]
    ReagentReservoir = labware_list[1]
    tips_300 = labware_list[2]
    DesaltingPlate = labware_list[6]

    # Pipetting parameter

    AIR_GAP_VOL = 10
    DISPENSE_HEIGHT = str(-1)
    ASPIRATION_DEPTH = labware_list[3][0]
    ASP_FLOW_RATE = labware_list[3][1]
    DISP_FLOW_RATE = labware_list[3][2]
    DISPENSE_HEIGHT_PSP = '24'

    # Volume for split and pool

    volume_SaP = labware_list[5]

    # Precision pipetting

    precision_asp_depth = labware_list[4][0]
    precision_flow_rate = labware_list[4][1]

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

    def dispense_PSP_SaP_WL(protocolFile, pipet, labware, well, volume, flow_rate):
        if volume != 0:
            protocolFile.write("    " + pipet + ".dispense(" + str(volume) + ", " + labware + ".wells()[" + str(
                well) + "].top("+DISPENSE_HEIGHT_PSP+"), " + str(flow_rate)
                               + ")\n")

    def aspirate_PSP_SaP_WL(protocolFile, pipet, labware, well, volume, flow_rate):
        if volume != 0:
            protocolFile.write(
                "    " + pipet + ".aspirate(" + str(volume) + ", " + labware + ".wells()[" + str(well) + "].top("+DISPENSE_HEIGHT_PSP+"), "+ str(
                    flow_rate)
                + ")\n")

    def aspirate_split_SaP_WL(protocolFile, pipet, labware, well, volume, asp_depth, flow_rate):
        if volume != 0:
            protocolFile.write(
                "    " + pipet + ".aspirate(" + str(volume) + ", " + labware + ".wells()[" + str(well) + "].bottom("+str(asp_depth)+"), "+ str(
                    flow_rate)
                + ")\n")


    # PSP start
    comment_WL(protocolFile, "PSP start ")
    pause_WL(protocolFile)
    comment_WL(protocolFile, "Fill well "+str(pool_well+1)+" with resin on FilterPlate")
    delay_WL(protocolFile, seconds=2)
    vacuum(protocolFile, MARC_COMPORT, 25)
    startHeating(protocolFile, MARC_COMPORT)

    # Post synthesis washes
    comment_WL(protocolFile, "Post synthesis washes")
    # H20
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 40)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 7, 200, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well+1, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    delay_WL(protocolFile, seconds=20, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)

    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 48)
    delay_WL(protocolFile, seconds=15, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 15, 100, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)

    # TSTPK 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 50 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well+1, 50 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=30, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    startVac(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=19, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 15, 200, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)
    # TSTPK 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well+1, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    delay_WL(protocolFile, seconds=50, minutes=4)
    stopStirring(protocolFile, MARC_COMPORT)
    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 56)
    delay_WL(protocolFile, seconds=15, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 23, 200, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)
    # TH1X 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well+1, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=30, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    startVac(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=19, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 23, 200, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)
    # TH1X 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well+1, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=30, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    startVac(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=19, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 23, 200, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)
    # TH1X 3
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well+1, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    delay_WL(protocolFile, seconds=20, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 64)
    delay_WL(protocolFile, seconds=15, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 31, 200, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)

    # Cleavage
    comment_WL(protocolFile, "Cleavage")
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well+1, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)


    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    delay_WL(protocolFile, seconds=30, minutes=29)
    pickup_tips_multi_WL(protocolFile, pipet300_multi, tips_300, 23)
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 72)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    stopStirring(protocolFile, MARC_COMPORT)


    # DNA precipitation
    comment_WL(protocolFile, "DNA precipitation")
    # Isop in desalting plate
    dispense_SaP_WL(protocolFile, pipet300_multi, DesaltingPlate, sample_well, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_multi, DesaltingPlate, control_well, 100 + 1 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_multi)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, DesaltingPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    # Isop in filter plate, synthesis beads
    # First transfer
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, 100, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, pool_well, 100 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, FilterPlate, pool_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    mix_SaP_WL(protocolFile, pipet300_single, 3, 70, FilterPlate, pool_well, 3)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 200, precision_asp_depth,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 25, 0.4,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 25, 0.1,
                          precision_flow_rate)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, sample_well, 250 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, sample_well)
    blow_out_WL(protocolFile, pipet300_single)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    # Second transfer
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, 100, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, pool_well, 100 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, FilterPlate, pool_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    mix_SaP_WL(protocolFile, pipet300_single, 3, 70, FilterPlate, pool_well, 3)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 200, precision_asp_depth,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 25, 0.4,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 25, 0.1,
                          precision_flow_rate)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, sample_well, 250 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, sample_well)
    blow_out_WL(protocolFile, pipet300_single)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)

    return_WL(protocolFile, pipet300_single)
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 80)

    # Isop in filter plate, control beads
    # First transfer
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, 100, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, pool_well + 1, 100 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, FilterPlate, pool_well + 1, AIR_GAP_VOL, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    mix_SaP_WL(protocolFile, pipet300_single, 3, 70, FilterPlate, pool_well + 1, 3)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, 200, precision_asp_depth,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, 25, 0.4,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, 25, 0.1,
                          precision_flow_rate)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, control_well, 250 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, control_well)
    blow_out_WL(protocolFile, pipet300_single)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    # Second transfer
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, 100, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, ReagentReservoir, 39, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_multi, FilterPlate, pool_well + 1, 100 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_multi, FilterPlate, pool_well + 1, AIR_GAP_VOL, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    mix_SaP_WL(protocolFile, pipet300_single, 3, 70, FilterPlate, pool_well + 1, 3)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, 200, precision_asp_depth,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, 25, 0.4,
                          precision_flow_rate)
    aspirate_split_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, 25, 0.1,
                          precision_flow_rate)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well + 1, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, control_well, 250 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    touch_tip_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, control_well)
    blow_out_WL(protocolFile, pipet300_single)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, DesaltingPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)

    return_WL(protocolFile, pipet300_single)

    # Exchange DesaltingPlate and FilterPlate
    pause_WL(protocolFile)
    comment_WL(protocolFile, 'Exchange DesaltingPlate and FilterPlate')
    delay_WL(protocolFile, 2, 0)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=180, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    vacuum(protocolFile, MARC_COMPORT, 25)

    # Ethanol wash
    # Ethanol wash 1
    comment_WL(protocolFile, 'Ethanol wash 1')
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 88)
    # Synthesis beads
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 47, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 47, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 47, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 47, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    # Control beads
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 55, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 55, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 55, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, seconds=30, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    vacuum(protocolFile, MARC_COMPORT, 25)
    # Ethanol wash 2
    comment_WL(protocolFile, 'Ethanol wash 2')
    # Synthesis beads
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 47, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 47, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 47, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 47, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, sample_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    # Control beads
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 55, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 55, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 55, 200, ASP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    dispense_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    aspirate_PSP_SaP_WL(protocolFile, pipet300_single, FilterPlate, control_well, AIR_GAP_VOL, ASP_FLOW_RATE)
    
    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    return_WL(protocolFile, pipet300_multi)
    delay_WL(protocolFile, seconds=30)
    stopStirring(protocolFile, MARC_COMPORT)
    vacuum(protocolFile, MARC_COMPORT, 900)
