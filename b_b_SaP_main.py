import streamlit as st
from math import *
from PIL import Image
from c_SaP_genProtocol import *
import os
from openpyxl import load_workbook
import time
import datetime
import pandas as pd
import numpy as np


st.markdown("<h1 style='text-align: left; color: #ff5843;'>Split and Pool protocol generator</h1>", unsafe_allow_html=True)
#st.title('Split and Pool protocol generator')
#st.markdown('Choose operating parameters')
st.subheader('Automated DNA barcode synthesis on Opentrons')
col1, col2 = st.columns(2)
with col1:
    st.markdown(' 1 - Choose your operating parameters and date for the synthesis <br> 2 - Click on <b>Generate protocol</b> first than on <b>Download protocol</b>', unsafe_allow_html=True)
with col2:
    st.markdown('3 - Upload the python file dowloaded on the [Opentrons App](https://opentrons.com/ot-app/) <br> 4 - Download and fill Excel file for the preparation of reagents and labwares',
        unsafe_allow_html=True)

def convert(min):
    hour, min = divmod(min, 60)
    return "%dh%02d" % (hour, min)

image_SaP = Image.open('images/SaP_theory.png')

image_deck = Image.open('images/DeckMapEmpty.png')
image_pip_single = Image.open("images/Pipettes_single.PNG")
image_pip_multi = Image.open("images/Pipettes_multi.jpg")

image_tiprack = Image.open("images/Tiprack.PNG")
image_reservoir = Image.open("images/USA_reservoir.PNG")

image_filter_pall = Image.open("images/Pall_on_mani.PNG")
image_filter_grenier = Image.open("images/Grenier.PNG")

col1, col1_5, col2, col3, col4 = st.columns([1.5, 1, 1.5, 0.9, 1.4], gap="medium")

with col1:
    number_of_cycle = st.slider('Barcode length', min_value = 0, max_value = 19, value = 18)
    #conc_beads = st.text_input('Concentration of the resin in beads', '100000000', help='in beads/mL')
    #number_beads = st.number_input('Desired number of barcoded beads', 0, max_value=None, value=20000000, step=10000000)

with col1_5:
    support = st.radio('Solid Support', ('Resin', 'Magnetic beads'), index=0)
    
with col2:
    st.markdown('   ')
    #st.markdown("Initial volume of resin to introduce in well 0 &emsp; **" + str(number_beads/int(conc_beads)) + "** &emsp; mL", unsafe_allow_html=True)
    #number_of_cycle = ceil(log(number_beads) / log(4))
    infos = st.container()
    
    #number_beads = 10**(number_of_cycle*log(4))

with col3:
    synthesis_date = st.date_input('Date of the synthesis', datetime.datetime.now())

with col4:
    st.write("Download Excel file [here](https://github.com/LucieDNA/Split_and_Pool_Protocol_Generator/raw/main/Split_And_Pool_Controler_corrected.xlsm)")
    generate_button = st.container()

col1, col2 = st.columns([1.5, 1.5])
with col1:
    start_seq = st.text_input('Addition of sequence at the beginning of the barcodes', 'XTTTTT')
with col2:
    end_seq = st.text_input('Addition of sequence at the end of the barcodes', 'TCGTCGGCAGCGUCAGAUGUGUAUAAGAGACAG')
    
if support == 'Magnetic beads':
    duration = convert(20 * number_of_cycle+10*(len(start_seq)+len(end_seq)))
else:
    duration = convert(18 * number_of_cycle+10*(len(start_seq)+len(end_seq)))
    
with infos:
    st.markdown("Number of Split&Pool cycles &emsp; **" + str(number_of_cycle) + "**", unsafe_allow_html=True)
    st.markdown("Estimated duration &emsp; **" + str(duration) + "**", unsafe_allow_html=True)
    

TiprackList = [
                "opentrons_96_tiprack_300ul",
            ]

ReagentReservoirList = [
                "usascientific_96_wellplate_2.4ml_deep",
                "nest_96_wellplate_2ml_deep",
                "axygen_96_reservoir_2000ul"
            ]

FilterPlateList = [
                "pall_96_wellplate_350ul_test",
                "pall_96_wellplate_350ul_manifold",
                "greiner_96_wellplate_350ul",
                "corning_96_wellplate_360ul_flat"
            ]

LocationList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

st.markdown('   ')
st.markdown('   ')
st.markdown('**Choose Opentrons set up**')

col1, col1_5, col2, col3 = st.columns([1.5, 0.5, 1, 1.2])

with col1:
    tiprack = st.selectbox('Tiprack', TiprackList, 0)
    reservoir = st.selectbox('ReagentReservoir', ReagentReservoirList, 0)
    filterPlate = st.selectbox('FilterPlate', FilterPlateList, 1)
    
    #with open('pall_96_wellplate_350ul_manifold.json') as file:
    #        st.download_button('Download filterPlate labware file', data=file, file_name='pall_96_wellplate_350ul_manifold.json')
    #st.write("[Custom Labware Creator](https://labware.opentrons.com/create/)")

with col1_5:
    st.image(image_tiprack) #, width=120)
    st.image(image_reservoir) #, width=120)
    if filterPlate == 'pall_96_wellplate_350ul_manifold':
        st.image(image_filter_pall) #, width=120)
    else :
        st.image(image_filter_grenier) #, width=120)

with col2:
    error_labware = st.container()
    tiprack_loc = st.select_slider('Tiprack location', LocationList, '7')
    reservoir_loc = st.select_slider('ReagentReservoir location', LocationList, '4')
    filterPlate_loc = st.select_slider('FilterPlate location', LocationList, '6')
    with error_labware:
        if tiprack_loc == reservoir_loc or tiprack_loc == filterPlate_loc or reservoir_loc == filterPlate_loc:
            st.warning("Labware must be on different locations")

with col3:
    image_deck_2 = Image.open('images/'+str(tiprack_loc)+'_'+str(reservoir_loc)+'_'+str(filterPlate_loc)+'.png')
    st.image(image_deck_2)#, width=310)
    

#st.write("Dowload filterPlate labware file and import it on the Opentrons App")
col1, col2, col3 = st.columns([1.7, 1.5, 4])
with col1 : 
     with open('pall_96_wellplate_350ul_manifold.json') as file:
           st.download_button('Download filterPlate labware file', data=file, file_name='pall_96_wellplate_350ul_manifold.json')
    
with col2:
    st.write("[Custom Labware Creator](https://labware.opentrons.com/create/)")


error_pipette = st.container()
    
col1, col2, col3, col4 = st.columns([1, 2.5, 1, 2.5])

with col1:
    st.image(image_pip_single)#, width=140)

with col2:
    singleChannel = st.radio('Pipette SingleChannel placement', ('Right', 'Left'), index=0)
    st.radio('Pipette SingleChannel generation', ('GEN2', 'GEN1'), index=0)

with col4:
    multiChannel = st.radio('Pipette MultiChannel placement', ('Right', 'Left'), index=1)
    st.radio('Pipette MultiChannel generation', ('GEN2', 'GEN1'), index=0)

with col3:
    st.image(image_pip_multi)#, width=140)
    
with error_pipette:
    if singleChannel == multiChannel:
        st.warning("Both pipettes can't be on the same side")

with st.sidebar:
    st.header('Advanced parameters')
    st.subheader('Control synthesis')
    control_synth = st.checkbox('Control sample in well 71')
    st.subheader('Post Synthesis Process')
    well_psp = None
    warning = st.container()
    simple_psp = st.checkbox('Simple PSP')
    if simple_psp:
          well_psp = st.text_input('Well for the sample on the desalting plate', "1")
    double_psp = st.checkbox('Double PSP')
    if double_psp:
        well_psp_sample = st.text_input('Well for the sample on the desalting plate', "0")
        well_psp_control = st.text_input('Well for the control on the desalting plate', "1")
        well_psp = [well_psp_sample, well_psp_control]
    if simple_psp and double_psp:
        with warning:
            st.warning('Choose only one option')
    with st.form('my_form'):
        st.subheader('For classic pipetting')
        asp_depth = st.text_input('Aspirate height above bottom of the well', '1', help='in mm')
        asp_flow_rate = st.text_input('Aspirate flow rate', '1.5', help='relative')
        disp_flow_rate = st.text_input('Dispense flow rate', '2', help='relative')
        submitted = st.form_submit_button("Submit")
    with st.form('my_form_2'):
        st.subheader('For precision pipetting')
        asp_depth_precision = st.text_input('Aspirate height above the bottom of the well', '0.9', help='in mm', key='1')
        flow_rate = st.text_input('Aspirate flow rate', '0.8', help='relative', key='2')
        submitted = st.form_submit_button("Submit")

if support == 'Magnetic beads':
    vacuum_between_trans = 60
else :
    vacuum_between_trans = 15
with generate_button:
    gen_button = st.button('Generate protocol', on_click=genProtocol, args=[[number_of_cycle, 270],
                                                               [[tiprack, tiprack_loc], [reservoir, reservoir_loc],
                                                                [filterPlate, filterPlate_loc], singleChannel,
                                                                multiChannel],
                                                               [asp_depth, asp_flow_rate, disp_flow_rate],
                                                               [asp_depth_precision, flow_rate], synthesis_date, start_seq, end_seq, simple_psp, double_psp, well_psp, control_synth, vacuum_between_trans])
    if gen_button:
        st.success('Protocol successfully generated, click on **Download protocol**')

def update_excel():
    workbook = load_workbook(filename="Split_And_Pool_Controler.xlsx")
    sheet = workbook.active

    sheet["D7"] = conc_beads
    sheet["D8"] = number_beads
    sheet["D12"] = tiprack
    sheet["D13"] = reservoir
    sheet["D14"] = filterPlate
    sheet["E12"] = tiprack_loc
    sheet["E13"] = reservoir_loc
    sheet["E14"] = filterPlate_loc
    sheet["K13"] = singleChannel
    sheet["K14"] = multiChannel

    workbook.save(filename="Split_And_Pool_Controler_Updated_" + str(synthesis_date.strftime('%y%m%d')) + ".xlsx")
    os.startfile("Split_And_Pool_Controler_Updated_" + str(synthesis_date.strftime('%y%m%d')) + ".xlsx")

    # workbook.save(filename="Split_And_Pool_Controler_Updated_test.xlsx")
    # os.startfile("Split_And_Pool_Controler_Updated_test.xlsx")

with generate_button:
    #st.button('Open Excel file', on_click=update_excel)
    if gen_button:
        with open('a_SaP_protocol_'+str(synthesis_date.strftime('%y%m%d'))+'.py') as file:
            st.download_button('Download protocol', data=file, file_name=str(synthesis_date.strftime('%y%m%d'))+'_'+str(number_of_cycle)+'_mers_barcodes.py')

   
#st.image(image_SaP)

volume_nucleotide = int((0.025 * number_of_cycle+0.1)*1000)
volume_enzyme = int((0.025 * number_of_cycle+0.1)*1000)
volume_W1 = int((0.05 * number_of_cycle+0.15)*1000)
volume_D =int((0.1 * number_of_cycle+0.2)*1000)
volume_W2 = int((0.05 * number_of_cycle+0.15)*1000)


if number_of_cycle <= 6:
    volume_Ps_split_1 = str(int(270* number_of_cycle+200))
    volume_Ps_split_2 = str(0)
    volume_Ps_split_3 = str(0)
if 6 < number_of_cycle <= 12:
    volume_Ps_split_1 = str(int(270 * 6+200))
    volume_Ps_split_2 = str(int(270 * (number_of_cycle-6)+200))
    volume_Ps_split_3 = str(0)
if 12 < number_of_cycle <= 19:
    volume_Ps_split_1 = str(int(270*6+200))
    volume_Ps_split_2 = str(int(270* 6+200))
    volume_Ps_split_3 = str(int(270* (number_of_cycle-6*2)+200))

volume_Ps_pool = str(int(270/4 * number_of_cycle+150))
volume_Ps_pool_1 = str(int(270/4 * number_of_cycle+150+270))
pooling_solution = 'W2'

volume_A = 0
volume_C = 0
volume_G = 0
volume_T = 0
volume_E_2 = 0
volume_W1_2 = 0
volume_D_2 = 0
volume_W2_2 = 0
volume_U = 0
volume_X = 0
if end_seq != '' or start_seq != '':
    nb_A = end_seq.count('A')
    nb_A += start_seq.count('A')
    volume_A = nb_A*25
    nb_C = end_seq.count('C')
    nb_C += start_seq.count('C')
    volume_C = nb_C*25
    nb_G = end_seq.count('G')
    nb_G += start_seq.count('G')
    volume_G = nb_C*25
    nb_T = end_seq.count('T')
    nb_T += start_seq.count('T')
    volume_T = nb_T*25
    nb_add = len(end_seq) + len(start_seq)
    volume_E_2 = 25*nb_add + 100
    volume_W1_2 = 50*nb_add + 100
    volume_D_2 = 50*nb_add + 100
    volume_W2_2 = 50*nb_add + 100
    nb_U = end_seq.count('U')
    nb_U += start_seq.count('U')
    volume_U = nb_U*25 + 100
    nb_X = end_seq.count('X')
    nb_X += start_seq.count('X')
    volume_X = nb_X*25 + 100
volume_eau = 150
volume_TSTPK = 250
volume_TH1X = 400
volume_LB = 200
volume_Isop = 450
volume_Eth = 1400
        

text_A = "A = " + str(volume_nucleotide+volume_A) +" µL"
text_C = "C = " + str(volume_nucleotide+volume_C) +" µL"
text_G = "G = " + str(volume_nucleotide+volume_G) +" µL"
text_T = "T = " + str(volume_nucleotide+volume_T) +" µL"
text_U = "U = " + str(volume_U) +" µL"
text_X = "X = " + str(volume_X) +" µL"
text_E = "E = " + str(volume_enzyme)+" µL"
text_W1 = "W1 = " + str(volume_W1)+" µL"
text_D = "D = " + str(volume_D)+" µL"
text_W2 = "W2 = " + str(volume_W2)+" µL"
text_E_2 = "E = " + str(volume_E_2)+" µL"
text_W1_2 = "W1 = " + str(volume_W1_2)+" µL"
text_D_2 = "D = " + str(volume_D_2)+" µL"
text_W2_2 = "W2 = " + str(volume_W2_2)+" µL"

nb_psp = 0
if simple_psp:
    nb_psp = 1
if double_psp:
    nb_psp = 2
text_eau = "H2O = " + str(volume_eau*nb_psp) +" µL"
text_TSTPK = "TSTPK = " + str(volume_TSTPK*nb_psp) +" µL"
text_TH1X = "TH1X = " + str(volume_TH1X*nb_psp) +" µL"
text_LB = "LB = " + str(volume_LB*nb_psp) +" µL"
text_Isop = "Isop = " + str(volume_LB*nb_psp) +" µL"
text_Eth = "Isop = " + str(volume_Eth) +" µL"
    

color_enzyme = 'background-color: green'

table_volume = np.full((8,12), '                  ')
table_volume[0,0] = text_A
table_volume[1,0] = text_C
table_volume[2,0] = text_G
table_volume[3,0] = text_T

table_volume[7,0] = text_eau
table_volume[7,1] = text_TSTPK
table_volume[7,2] = text_TH1X
table_volume[7,3] = text_LB
table_volume[7,4] = text_Isop
table_volume[7,5] = text_Eth
if nb_psp == 2:
    table_volume[7,6] = text_Eth

table_volume[0,11] = pooling_solution+" = " +volume_Ps_split_1+" µL"
table_volume[1,11] = pooling_solution+" = " +volume_Ps_split_1+" µL"
table_volume[2,11] = pooling_solution+" = " +volume_Ps_split_1+" µL"
table_volume[3,11] = pooling_solution+" = " +volume_Ps_split_2+" µL"
table_volume[4,11] = pooling_solution+" = " +volume_Ps_split_2+" µL"
table_volume[5,11] = pooling_solution+" = " +volume_Ps_split_2+" µL"
table_volume[6,11] = pooling_solution+" = " +volume_Ps_split_3+" µL"
table_volume[7,11] = pooling_solution+" = " +volume_Ps_split_3+" µL"
table_volume[7,10] = pooling_solution+" = " +volume_Ps_split_3+" µL"
for i in range(4):
    table_volume[i,1] = text_E
    table_volume[i,2] = text_W1
    table_volume[i,3] = text_D
    table_volume[i,4] = text_W2
    table_volume[i,8] = pooling_solution+" = " +volume_Ps_pool+" µL"
    table_volume[i,9] = pooling_solution+" = " +volume_Ps_pool+" µL"
    table_volume[i,10] = pooling_solution+" = " +volume_Ps_pool+" µL"
table_volume[0,8] = pooling_solution+" = " +volume_Ps_pool_1+" µL"

if end_seq != '' or start_seq != '':
    table_volume[4,1] = text_E_2
    table_volume[4,2] = text_W1_2
    table_volume[4,3] = text_D_2
    table_volume[5,3] = text_D_2
    table_volume[4,4] = text_W2_2
    if end_seq.count('U') != 0 or start_seq.count('U') != 0:
        table_volume[4,0] = text_U
    if end_seq.count('X') != 0 or start_seq.count('X') != 0:
        table_volume[5,0] = text_X

def color_reageants(cell):
    if cell == '                  ':
        return 'background-color: #ffffff'
    if cell == text_A:
        return 'background-color: #ebe7f2'
    if cell == text_C:
        return 'background-color: #d7cee6'
    if cell == text_G:
        return 'background-color: #c4b6d9'
    if cell == text_T:
        return 'background-color: #9c85c0'
    if cell == text_U:
        return 'background-color: #8d59b3'
    if cell == text_X:
        return 'background-color: #d5d8fb'
    if cell == text_E or cell == text_E_2:
        return 'background-color: #e3beca'
    if cell == text_W1 or cell == text_W1_2:
        return 'background-color: #f1d77f'
    if cell == text_D or cell == text_D_2:
        return 'background-color: #c9d3be'
    if cell == text_W2 or cell == text_W2_2:
        return 'background-color: #f8c891'
    if cell == pooling_solution+" = " +volume_Ps_pool+" µL" or pooling_solution+" = " +volume_Ps_split_1+" µL" or pooling_solution+" = " +volume_Ps_split_2+" µL" or pooling_solution+" = " +volume_Ps_split_3+" µL" or pooling_solution+" = " +volume_Ps_pool_1+" µL":
         return 'background-color: #b3c5da'

df = pd.DataFrame(
    table_volume,
    index=('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'),
    columns=(str(i) for i in range(1,13)))

tableau_1, tableau_2 = st.tabs(['Reagents plate', 'Tip rack'])
with tableau_1:
    table = st.dataframe(df.style.applymap(color_reageants), width=1500)

    
table_tip = np.full((8,12), '                      ')
for i in range(number_of_cycle+1):
    table_tip[i%8, i//8] = "Transfer " + str(i)

enzyme = '          E'
wash_1 = '        W1'
deblock = '          D'
wash_2 = '        W2'
A = '          A'
C = '          C'
G = '          G'
T = '          T'
U = '          U'
X = '          X'
eau = '       H2O'
TSTPK = '       TSTPK'
TH1X = '      TH1X'
LB = '         LB'
Isop = '       Isop'
Eth = '        Eth'


for i in range(4):
    table_tip[4+i, 6] = 'W2 (transfer)'
    table_tip[4+i, 8] = enzyme
    table_tip[4+i, 9] = wash_1
    table_tip[4+i, 10] = deblock
    table_tip[4+i, 11] = wash_2
table_tip[4, 7] = A
table_tip[5, 7] = C
table_tip[6, 7] = G
table_tip[7, 7] = T
if end_seq.count('U') != 0 or start_seq.count('U') != 0:
    table_tip[7, 5] = U
if end_seq.count('X') != 0 or start_seq.count('X') != 0:
    table_tip[6, 5] = X
if simple_psp or double_psp:
    table_tip[0, 5] = eau
    table_tip[0, 6] = TSTPK
    table_tip[0, 7] = TH1X
    table_tip[0, 8] = LB
    table_tip[0, 9] = Isop
    table_tip[7, 2] = Isop
    table_tip[0, 11] = Eth
if double_psp:
    table_tip[0, 10] = Isop

df = pd.DataFrame(
    table_tip,
    index=('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'),
    columns=(str(i) for i in range(1,13)))

color_for_tips = ['background-color: #d9d9d9']
color_for_tips.append('background-color: #e6ecf3')
color_for_tips.append('background-color: #ccd8e7')
color_for_tips.append('background-color: #b3c5da')
color_for_tips.append('background-color: #809ec2')
color_for_tips.append('background-color: #ebe7f2')
color_for_tips.append('background-color: #d7cee6')
color_for_tips.append('background-color: #c4b6d9')
color_for_tips.append('background-color: #9c85c0')
color_for_tips.append('background-color: #f6e9ed')
color_for_tips.append('background-color: #ecd3dc')
color_for_tips.append('background-color: #e3beca')
color_for_tips.append('background-color: #d092a7')
color_for_tips.append('background-color: #faf2d4')
color_for_tips.append('background-color: #f5e4a9')
color_for_tips.append('background-color: #f1d77f')
color_for_tips.append('background-color: #e7bc29')
color_for_tips.append('background-color: #fdedda')
color_for_tips.append('background-color: #fadbb5')
color_for_tips.append('background-color: #f8c891')


def color_tips(cell):
    if cell == '                      ':
        return 'background-color: #ffffff'
    for i in range(number_of_cycle+1):
        if cell == "Transfer " + str(i):
            return color_for_tips[i]
    if cell == A:
        return 'background-color: #ebe7f2'
    if cell == C:
        return 'background-color: #d7cee6'
    if cell == G:
        return 'background-color: #c4b6d9'
    if cell == T:
        return 'background-color: #9c85c0'
    if cell == 'W2 (transfer)':
        return 'background-color: #b3c5da'
    if cell == enzyme:
        return 'background-color: #e3beca'
    if cell == wash_1:
        return 'background-color: #f1d77f'
    if cell == deblock:
        return 'background-color: #c9d3be'
    if cell == wash_2:
        return 'background-color: #f8c891'
    if cell == U:
        return 'background-color: #8d59b3'
    if cell == X:
        return 'background-color: #d5d8fb'
    if cell == eau:
        return 'background-color: #ff5843'
    if cell == TSTPK:
        return 'background-color: #ff6956'
    if cell == TH1X:
        return 'background-color: #ff7969'
    if cell == LB:
        return 'background-color: #ff8a7b'
    if cell == Isop:
        return 'background-color: #ff9b8e'
    if cell == Eth:
        return 'background-color: #ffaca1'

nombre_tip = 0
for row in table_tip:
    for cell in row:
        if cell != '                      ':
            nombre_tip += 1

with tableau_2:
    table_2 = st.dataframe(df.style.applymap(color_tips), width=2000)

st.text('Number of tips = '+ str(nombre_tip))
