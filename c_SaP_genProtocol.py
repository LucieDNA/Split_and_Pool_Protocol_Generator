# from opentrons import protocol_api, types
from d_SaP_commands import *
from math import ceil, log
from f_a_SaP_PSP import *
from f_b_SaP_double_PSP import *
import datetime
from g_SaP_add_end import *
from g_b_SaP_end_seq_double import *


AIR_GAP_VOL = 10
DISPENSE_HEIGHT = str(-1)
ASPIRATION_DEPTH = 1
ASP_FLOW_RATE = 1.5
DISP_FLOW_RATE = 2

def genProtocol(general_parameters, labware_list_and_loc, pipetting_condition, precision_pipetting_param, synthesis_date, start_seq, end_seq, single_psp, double_psp, well_psp, control_synth, vacuum_between_trans):

    MARC_COMPORT = None
    MARC_COMPORT = "/dev/ttyACM0"


    date = datetime.datetime.now().strftime('%y%m%d')

    PROTOCOL_PATH = 'a_SaP_protocol_'+str(synthesis_date.strftime('%y%m%d'))+'.py'

    protocolFile = open(PROTOCOL_PATH, "w")


    # DEFINE USED LABWARES
    # Pipets
    pipet300_multi = "p300_multi" #pipet multi left
    pipet300_single = "p300_single" #pipet single right
    # Plates
    FilterPlate = 'FilterPlate'
    # Reservoirs
    ReagentReservoir = 'ReagentReservoir'
    # Tips
    tips_300 = 'tiprack_300'
    # Desalting plate
    DesaltingPlate = 'DesaltingPlate'
    # Get references from the list
    tiprack = labware_list_and_loc[0]
    reagentReservoir = labware_list_and_loc[1]
    filterPlate = labware_list_and_loc[2]
    desaltingPlate = ["invitek_96_wellplate_on_trash_1000ul", '1']
    #desaltingPlate = ["corning_96_wellplate_360ul_flat", '1']
    mount_single_channel = labware_list_and_loc[3]
    mount_multi_channel = labware_list_and_loc[4]

    # Header
    header_SaP_wl(protocolFile, tiprack, reagentReservoir, filterPlate, desaltingPlate, mount_single_channel,  mount_multi_channel)


    # DEFINE NUMBER OF CYCLE
    number_of_cyle = general_parameters[0]
    current_cycle = 0

    # DEFINE VOLUME FOR THE SPLIT AND POOL
    volume_SaP = general_parameters[1]

    # Define labware list
    labware_list = [FilterPlate, ReagentReservoir, tips_300, pipetting_condition, precision_pipetting_param, volume_SaP, DesaltingPlate, vacuum_between_trans]


    # START HEATING
    startHeating(protocolFile, MARC_COMPORT)
    
    pool_well = 0

    # Addition of an start sequence
    if start_seq != '':
        vacuum(protocolFile, MARC_COMPORT, 25)
        if control_synth:
            add_end_seq_2(protocolFile, pipet300_multi, pipet300_single, labware_list, MARC_COMPORT, pool_well, start_seq)
        else:
            add_end_seq(protocolFile, pipet300_multi, pipet300_single, labware_list, MARC_COMPORT, pool_well, start_seq)

            
    # Full cycle 1
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 0
        work_well = 8
        pool_well = 1
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 2
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 1
        work_well = 16
        pool_well = 2
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 3
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 2
        work_well = 24
        pool_well = 3
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 4
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 3
        work_well = 32
        pool_well = 40
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 5
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 40
        work_well = 48
        pool_well = 41
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 6
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 41
        work_well = 56
        pool_well = 42
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 7
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 42
        work_well = 64
        pool_well = 43
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 8
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 43
        work_well = 72
        pool_well = 80
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 9
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 80
        work_well = 88
        pool_well = 81
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 10
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 81
        work_well = 4
        pool_well = 82
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 11
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 82
        work_well = 12
        pool_well = 83
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 12
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 83
        work_well = 20
        pool_well = 28
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 13
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 28
        work_well = 36
        pool_well = 29
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 14
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 29
        work_well = 44
        pool_well = 30
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 15
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 30
        work_well = 52
        pool_well = 31
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 16
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 31
        work_well = 60
        pool_well = 68
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 17
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 68
        work_well = 76
        pool_well = 69
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 18
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 69
        work_well = 84
        pool_well = 70
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    # Full cycle 19
    current_cycle += 1
    if current_cycle <= number_of_cyle:
        split_well = 70
        work_well = 92
        pool_well = 71
        full_cycle(current_cycle, protocolFile, split_well, work_well, pool_well, pipet300_multi, pipet300_single, labware_list)

    return_WL(protocolFile, pipet300_multi)
    return_WL(protocolFile, pipet300_single)
    
    # Addition of an end sequence
    if end_seq != '':
        vacuum(protocolFile, MARC_COMPORT, 25)
        if control_synth:
            pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 52)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
            aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 65, 200, ASP_FLOW_RATE)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
            dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 200 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
            blow_out_WL(protocolFile, pipet300_single)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
            return_WL(protocolFile, pipet300_single)
            pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, number_of_cyle)
            mix_SaP_WL(protocolFile, pipet300_single, 5, 150, FilterPlate, pool_well, 6)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
            aspirate_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 100, ASP_FLOW_RATE)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
            dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well+1, 100 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
            return_WL(protocolFile, pipet300_single)
            vacuum(protocolFile, MARC_COMPORT, 25)
            add_end_seq_2(protocolFile, pipet300_multi, pipet300_single, labware_list, MARC_COMPORT, pool_well, end_seq)
            
            # Vacuum
            startVac(protocolFile, MARC_COMPORT)
            pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 92)
            delay_WL(protocolFile, seconds=15, minutes=0)
            startVent(protocolFile, MARC_COMPORT)
            delay_WL(protocolFile, 6, 0)
            stopVac(protocolFile, MARC_COMPORT)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
            aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 66, 280, ASP_FLOW_RATE)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
            stopVent(protocolFile, MARC_COMPORT)

            ## Wash 2
            dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 140 + AIR_GAP_VOL, DISP_FLOW_RATE)
            dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well+1, 140 + AIR_GAP_VOL, DISP_FLOW_RATE)
            blow_out_WL(protocolFile, pipet300_single)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

            return_WL(protocolFile, pipet300_single)
        else:
            add_end_seq(protocolFile, pipet300_multi, pipet300_single, labware_list, MARC_COMPORT, pool_well, end_seq)
             # Vacuum
            startVac(protocolFile, MARC_COMPORT)
            pickup_tips_single_WL(protocolFile, pipet300_single, tips_300, 92)
            delay_WL(protocolFile, seconds=15, minutes=0)
            startVent(protocolFile, MARC_COMPORT)
            delay_WL(protocolFile, 6, 0)
            stopVac(protocolFile, MARC_COMPORT)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
            aspirate_SaP_WL(protocolFile, pipet300_single, ReagentReservoir, 66, 100, ASP_FLOW_RATE)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)
            stopVent(protocolFile, MARC_COMPORT)

            ## Wash 2
            dispense_SaP_WL(protocolFile, pipet300_single, FilterPlate, pool_well, 100 + 2 * AIR_GAP_VOL, DISP_FLOW_RATE)
            blow_out_WL(protocolFile, pipet300_single)
            air_gap_WL(protocolFile, pipet300_single, AIR_GAP_VOL)

            return_WL(protocolFile, pipet300_single)
        
    
    if double_psp:
        vacuum(protocolFile, MARC_COMPORT, 25)
        double_psp_for_SaP(protocolFile, pipet300_multi, pipet300_single, labware_list, MARC_COMPORT, pool_well, well_psp)
    if single_psp:
        vacuum(protocolFile, MARC_COMPORT, 25)
        pool_well = 93
        psp_for_SaP(protocolFile, pipet300_multi, pipet300_single, labware_list, MARC_COMPORT, pool_well, well_psp)    
        
    # STOP HEATING
    stopHeating(protocolFile, MARC_COMPORT)


if __name__ == "__main__":
    labware_list_and_loc = [['opentrons_96_tiprack_300ul', '8'], ['usascientific_96_wellplate_2.4ml_deep', '5'], ['nest_96_wellplate_200ul_flat', '2'], 'right', 'left']
    pipetting_condition = [5, 5, '3', '1', 1, 1]
    #well_edges = [(0.79, 0, -1), (-0.76, 0, -1), (0, -0.60, -1), (0, 1.1, -1)]
    losses = '2%'
    precision_pipetting_param = [0, 1]
    genProtocol([10000, 200], labware_list_and_loc, pipetting_condition, precision_pipetting_param)
