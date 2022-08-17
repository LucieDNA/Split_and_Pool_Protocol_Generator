import streamlit as st
from math import *
from PIL import Image
from c_SaP_genProtocol import *
import os
from openpyxl import load_workbook
import time
import datetime

st.markdown("<h1 style='text-align: left; color: #ff5843;'>Split and Pool protocol generator</h1>", unsafe_allow_html=True)
#st.title('Split and Pool protocol generator')
#st.markdown('Choose operating parameters')
st.subheader('Automomated DNA barcode synthesis on Opentrons')
col1, col2 = st.columns(2)
with col1:
    st.markdown(' 1 - Choose your operating parameters and date for the synthesis <br> 2 - Click on <b>Generate protocol</b> first than on <b>Download protocol</b>', unsafe_allow_html=True)
with col2:
    st.markdown('3 - Upload the python file dowloaded on the [Opentrons App](https://opentrons.com/ot-app/) <br> 4 - Download and fill Excel file for the preparation of reagents and labwares',
        unsafe_allow_html=True)

def convert(min):
    hour, min = divmod(min, 60)
    return "%dh%02d" % (hour, min)

image_deck = Image.open('images/DeckMapEmpty.png')
image_pip_single = Image.open("images/Pipettes_single.PNG")
image_pip_multi = Image.open("images/Pipettes_multi.jpg")

image_tiprack = Image.open("images/Tiprack.PNG")
image_reservoir = Image.open("images/USA_reservoir.PNG")

image_filter_pall = Image.open("images/Pall_on_mani.PNG")
image_filter_grenier = Image.open("images/Grenier.PNG")

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
    st.write("Download Excel file [here](https://github.com/LucieDNA/Split_and_Pool_Protocol_Generator/raw/main/Split_And_Pool_Controler.xlsm)")
    generate_button = st.container()

col1, col2 = st.columns([1.5, 1.5])
with col1:
    start_seq = st.text_input('Addition of sequence at the beginning of the barcodes', '')
with col2:
    end_seq = st.text_input('Addition of sequence at the end of the barcodes', 'ATCGAATCGA')

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
    tiprack_loc = st.select_slider('Tiprack location', LocationList, '7')
    reservoir_loc = st.select_slider('ReagentReservoir location', LocationList, '4')
    filterPlate_loc = st.select_slider('FilterPlate location', LocationList, '6')

with col3:
    st.image(image_deck)#, width=310)
    

st.write("Dowload filterPlate labware file and import it on the Opentrons App")
col1, col2, col3 = st.columns([1.7, 1.5, 4])
with col1 : 
     with open('pall_96_wellplate_350ul_manifold.json') as file:
           st.download_button('Download filterPlate labware file', data=file, file_name='pall_96_wellplate_350ul_manifold.json')
    
with col2:
    st.write("[Custom Labware Creator](https://labware.opentrons.com/create/)")


    
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

with st.sidebar:
    st.header('Advanced parameters')
    st.subheader('For classic pipetting')
    asp_depth = st.text_input('Aspirate height above the bottom of the well', '1', help='in mm')
    asp_flow_rate = st.text_input('Aspirate flow rate', '1.5', help='relative')
    disp_flow_rate = st.text_input('Dispense flow rate', '2', help='relative')
    st.subheader('For precision pipetting')
    asp_depth_precision = st.text_input('Aspirate height above the bottom of the well', '0.9', help='in mm', key='1')
    flow_rate = st.text_input('Aspirate flow rate', '0.8', help='relative', key='2')


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
