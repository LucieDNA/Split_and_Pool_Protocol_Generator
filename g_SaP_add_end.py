from e_SaP_elementaryCommands import *


def add_end_seq(protocolFile, multi_pipet, single_pipet, labware_list, MARC_COMPORT, pool_well, end_seq):
    if end_seq is not '':
        for base in end_seq:
            add_single_nuc(protocolFile, multi_pipet, single_pipet, labware_list, MARC_COMPORT, pool_well, base)


def add_single_nuc(protocolFile, multi_pipet, single_pipet, labware_list, MARC_COMPORT, pool_well, base):

    #Pipets and labware

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

    #Determining the base

    if base == 'A':
        base_well = 0
        base_tip = 60
    if base == 'C':
        base_well = 1
        base_tip = 61
    if base == 'G':
        base_well = 2
        base_tip = 62
    if base == 'T':
        base_well = 3
        base_tip = 63

    #Elongation start

    comment_WL(protocolFile, "Addition of "+ base)
    ## Nucleotide
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, base_tip)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, base_well, 25, 1.5)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 25 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    return_WL(protocolFile, pipet300_single)
    ## Enzyme
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 68)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 8, 25, 1.5)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 25 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    delay_WL(protocolFile, seconds=50, minutes=3)
    stopStirring(protocolFile, MARC_COMPORT)
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 76)
    delay_WL(protocolFile, seconds=15, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 16, 50, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)

    ## Wash 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 50 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    stopStirring(protocolFile, MARC_COMPORT)
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 84)
    delay_WL(protocolFile, seconds=15, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 28, 50, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)

    ## Deblock 1
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 50 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 28, 50, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    delay_WL(protocolFile, seconds=25, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    # Vacuum
    vacuum(protocolFile, MARC_COMPORT, 25)

    ## Deblock 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 50 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    delay_WL(protocolFile, seconds=20, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)
    # Vacuum
    startVac(protocolFile, MARC_COMPORT)
    pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 92)
    delay_WL(protocolFile, seconds=15, minutes=0)
    startVent(protocolFile, MARC_COMPORT)
    delay_WL(protocolFile, 6, 0)
    stopVac(protocolFile, MARC_COMPORT)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 32, 50, ASP_FLOW_RATE)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
    stopVent(protocolFile, MARC_COMPORT)

    ## Wash 2
    dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 50 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
    blow_out_WL(protocolFile, pipet300_single)
    air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

    # Stir, wait and vacuum
    startStirring(protocolFile, MARC_COMPORT)
    return_WL(protocolFile, pipet300_single)
    delay_WL(protocolFile, seconds=10, minutes=0)
    stopStirring(protocolFile, MARC_COMPORT)

    vacuum(protocolFile, MARC_COMPORT, 25)
