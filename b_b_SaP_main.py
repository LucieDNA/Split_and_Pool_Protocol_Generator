import streamlit as st
from math import *
from PIL import Image
from c_SaP_genProtocol import *
import os
from openpyxl import load_workbook
import time
import datetime


## Unmoved parameters
asp_depth = '1'
asp_flow_rate = '1.5'
disp_flow_rate = '2'
asp_depth_precision = '0.9'
flow_rate = '0.8'


st.markdown("<h1 style='text-align: left; color: #ff5843;'>Split and Pool protocol generator</h1>", unsafe_allow_html=True)
#st.title('Split and Pool protocol generator')
#st.markdown('Choose operating parameters')
st.markdown('Choose your operating parameters and date for the synthesis, click on Generate protocol first than on Download protocol')

def convert(min):
    hour, min = divmod(min, 60)
    return "%dh%02d" % (hour, min)

image_deck = Image.open('images/DeckMapEmpty.png')
image_pip_single = Image.open("images/Pipettes_single.PNG")
image_pip_multi = Image.open("images/Pipettes_multi.jpg")

image_tiprack = Image.open("images/Tiprack.PNG")
image_reservoir = Image.open("images/USA_reservoir.PNG")
image_filter = Image.open("images/Pall_on_mani.PNG")

col1, col2, col3, col4 = st.columns([1, 1.5, 0.7, 1], gap="medium")

with col1:
    conc_beads = st.text_input('Concentration of the resin in beads', '100000000', help='in beads/mL')
    number_beads = st.number_input('Desired number of barcoded beads', 0, max_value=None, value=20000000, step=10000000)

with col2:
    st.markdown('   ')
    st.markdown('   ')
    st.markdown("Initial volume of resin to introduce in well 0 &emsp; **" + str(number_beads/int(conc_beads)) + "** &emsp; mL", unsafe_allow_html=True)
    number_of_cycle = ceil(log(number_beads) / log(4))
    duration = convert(15.25 * number_of_cycle)


    st.markdown("Number of cycles &emsp; **" + str(number_of_cycle) + "**", unsafe_allow_html=True)
    st.markdown("Estimated duration &emsp; **" + str(duration) + "**", unsafe_allow_html=True)

with col3:
    st.markdown('   ')
    st.markdown('   ')
    st.markdown('   ')
    synthesis_date = st.date_input('Date of the synthesis', datetime.datetime.now())

with col4:
    st.markdown('   ')
    st.markdown('   ')
    generate_button = st.container()

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
st.markdown('Choose Opentrons set up')

col1, col1_5, col2, col3 = st.columns([1.5, 0.5, 1, 1.2])

with col1:
    tiprack = st.selectbox('Tiprack', TiprackList, 0)
    reservoir = st.selectbox('ReagentReservoir', ReagentReservoirList, 0)
    filterPlate = st.selectbox('FilterPlate', FilterPlateList, 1)

with col1_5:
    st.image(image_tiprack) #, width=120)
    st.image(image_reservoir) #, width=120)
    st.image(image_filter) #, width=120)

with col2:
    tiprack_loc = st.select_slider('Tiprack location', LocationList, '7')
    reservoir_loc = st.select_slider('ReagentReservoir location', LocationList, '4')
    filterPlate_loc = st.select_slider('FilterPlate location', LocationList, '6')

with col3:
    st.image(image_deck)#, width=310)

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

with generate_button:
    gen_button = st.button('Generate protocol', on_click=genProtocol, args=[[number_beads, 270],
                                                               [[tiprack, tiprack_loc], [reservoir, reservoir_loc],
                                                                [filterPlate, filterPlate_loc], singleChannel,
                                                                multiChannel],
                                                               [asp_depth, asp_flow_rate, disp_flow_rate],
                                                               [asp_depth_precision, flow_rate], synthesis_date])


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
            st.download_button('Download protocol', data=file, file_name='a_SaP_protocol_'+str(synthesis_date.strftime('%y%m%d'))+'.py')
