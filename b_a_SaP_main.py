from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
from c_SaP_genProtocol import *
import xlrd
import os
from openpyxl import load_workbook
import time
import datetime

#style = ttk.Style()
#style.theme_use('classic')

os.system("taskkill /F /IM excel.exe")
time.sleep(2)
ExcelPath = r'Split_And_Pool_Controler.xlsx'

wb = xlrd.open_workbook(ExcelPath)
control_sheet = wb.sheet_by_index(0)



number_beads = int(control_sheet.cell_value(7, 3))
tiprack = control_sheet.cell_value(11, 3)
reservoir = control_sheet.cell_value(12, 3)
filterPlate = control_sheet.cell_value(13, 3)
tiprack_loc = int(control_sheet.cell_value(11, 4))
reservoir_loc = int(control_sheet.cell_value(12, 4))
filterPlate_loc = int(control_sheet.cell_value(13, 4))
singleChannel = control_sheet.cell_value(12, 10)
multiChannel = control_sheet.cell_value(13, 10)


# Labware lists

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

Side = ['Left', 'Right']


def convert(min):
    hour, min = divmod(min, 60)
    return "%dh%02d" % (hour, min)

#time_2_percent = ['0h19', '0h37', '0h56', '1h15', '1h33', '1h52', '2h11', '2h29', '2h48', '3h07', '3h25', '3h44', '4h03', '4h21', '4h040', '4h59', '5h17', '5h36', '5h55']
time_2_percent = [convert(15.5*i) for i in range(1, 20)]

# Define default parameter
## Beads
#number_beads = 20000000
total_volume = 270
## Labware
#tiprack =  TiprackList[0]
#reservoir = ReagentReservoirList[0]
#filterPlate = FilterPlateList[1]
#tiprack_loc = LocationList[7]
#reservoir_loc = LocationList[3]
#filterPlate_loc = LocationList[2]
#singleChannel = Side[1]
#multiChannel = Side[0]
## Pipetting
asp_depth = 1
asp_flow_rate = 1.5
disp_flow_rate = 2
## Precision pipetting
#Aspirate depth and flow rate
asp_depth_precision = 0.9
flow_rate = 0.8
#Losses after 19 cycles
number_of_cycle = ceil(log(number_beads)/log(4))
if number_of_cycle > 19:
    number_of_cycle = 19
losses = round((1 - (1 - (10/total_volume)**2 - ((6.7/(total_volume/4))**3)*4)**(int(number_of_cycle)))*100, 3)

duration = time_2_percent[number_of_cycle-1]


#Volumes
volume_nucleotide = round(0.025 * number_of_cycle+0.1, 3)
volume_enzyme = round(0.025 * number_of_cycle+0.1, 3)
volume_W1 = round(0.05 * number_of_cycle+0.1, 3)
volume_D = round(0.1 * number_of_cycle+0.1, 3)
volume_W2 = round(0.05 * number_of_cycle+0.1, 3)
volume_Ps_pool = round(total_volume/1000/4 * number_of_cycle+0.1, 3)
if number_of_cycle <= 6:
    volume_Ps_split_1 = round(total_volume/1000 * number_of_cycle+0.1, 3)
    volume_Ps_split_2 = 0
    volume_Ps_split_3 = 0
if 6 < number_of_cycle <= 12:
    volume_Ps_split_1 = round(total_volume/1000 * 6+0.1, 3)
    volume_Ps_split_2 = round(total_volume/1000 * (number_of_cycle-6)+0.1, 3)
    volume_Ps_split_3 = 0
if 12 < number_of_cycle <= 19:
    volume_Ps_split_1 = round(total_volume/1000 * 6+0.1, 3)
    volume_Ps_split_2 = round(total_volume/1000 * 6+0.1, 3)
    volume_Ps_split_3 = round(total_volume/1000 * (number_of_cycle-6*2)+0.1, 3)

# Define frames

class SaP_MainFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


        self.introFrame = IntroFrame(self, bd=2, relief=GROOVE, padx=10, pady=10)
        self.introFrame.grid(row=0, column=0, sticky='nesw')

        ''' Frame with the choice of the number of beads'''
        self.beadsFrame = BeadsFrame(self, bd=2, relief=GROOVE, padx=10,pady=10)
        self.beadsFrame.grid(row=1, column=0, sticky='nesw')

        '''Frame with the labware choice'''
        self.labwareFrame = LabwareFrame(self, bd=2, relief=GROOVE, padx=10, pady=10)
        self.labwareFrame.grid(row=2, column=0, sticky='nesw')

        '''Frame with the volumes for the reagent reservoir'''
        self.volumeFrame = VolumeFrame(self, bd=2, relief=GROOVE, padx=10, pady=10)
        self.volumeFrame.grid(row=3, column=0, sticky='nesw')

        '''Buttons'''
        self.buttonFrame= ButtonFrame(self, bd=2, relief=GROOVE, padx=10, pady=10)
        self.buttonFrame.grid(row=6, column=0, sticky='nesw')


class IntroFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.MainTitleLabel_font = font.Font(size=12, weight='bold')
        self.MainTitleLabel = Label(self, text="Split And Pool protocol generator", font=self.MainTitleLabel_font, fg='#eb5243')
        self.MainTitleLabel.pack(side = TOP, fill=BOTH, expand=TRUE)

        self.MainTitleLabel_font_2 = font.Font(slant='italic', size=8, weight='normal')
        self.MainTitleLabel = Label(self, text="Choose your operating parameters, click on Generate protocol and upload it on Opentrons app to run it"
                                    , font=self.MainTitleLabel_font_2, fg='#0b1334')
        self.MainTitleLabel.pack(side=BOTTOM, fill=BOTH, expand=TRUE)


class BeadsFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, text="        Initial number of beads     ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.pack(side = LEFT, fill=BOTH, expand=TRUE)

        self.numberBeads = StringVar()
        self.numberBeads.set(number_beads)
        self.entreeBeads = ttk.Entry(self, textvariable=self.numberBeads, width=20)
        self.entreeBeads.pack(side = LEFT, fill=BOTH, expand=TRUE)

        def update_number_of_cycle():
            number_of_cycle = ceil(log(int(self.parent.beadsFrame.entreeBeads.get())) / log(4))
            if number_of_cycle > 19:
                number_of_cycle = 19
            self.parent.beadsFrame.number_of_cycle.set(str(number_of_cycle))
            duration = time_2_percent[number_of_cycle - 1]
            self.parent.beadsFrame.total_duration.set(str(duration))
            #Update the volumes for the reagents
            total_volume = float(self.parent.beadsFrame.entree_total_volume.get())
            volume_nucleotide = 0.025 * number_of_cycle+0.1
            volume_enzyme = 0.025 * number_of_cycle+0.1
            volume_W1 = 0.050 * number_of_cycle+0.1
            volume_D = 0.100 * number_of_cycle+0.1
            volume_W2 = 0.050 * number_of_cycle+0.1
            self.parent.volumeFrame.volume_nucleotide.set(round(volume_nucleotide, 3))
            self.parent.volumeFrame.volume_enzyme.set(round(volume_enzyme, 3))
            self.parent.volumeFrame.volume_W1.set(round(volume_W1, 3))
            self.parent.volumeFrame.volume_D.set(round(volume_D, 3))
            self.parent.volumeFrame.volume_W2.set(round(volume_W2, 3))
            volume_Ps_pool = total_volume / 1000 / 4 * number_of_cycle+0.1
            if number_of_cycle <= 6:
                volume_Ps_split_1 = total_volume / 1000 * number_of_cycle+0.1
                volume_Ps_split_2 = 0
                volume_Ps_split_3 = 0
            if 6 < number_of_cycle <= 12:
                volume_Ps_split_1 = total_volume / 1000 * 6+0.1
                volume_Ps_split_2 = total_volume / 1000 * (number_of_cycle - 6)+0.1
                volume_Ps_split_3 = 0
            if 12 < number_of_cycle <= 19:
                volume_Ps_split_1 = total_volume / 1000 * 6+0.1
                volume_Ps_split_2 = total_volume / 1000 * 6+0.1
                volume_Ps_split_3 = total_volume / 1000 * (number_of_cycle - 6 * 2)+0.1
            self.parent.volumeFrame.volume_Ps_pool.set(round(volume_Ps_pool, 3))
            self.parent.volumeFrame.volume_Ps_split_1.set(round(volume_Ps_split_1, 3))
            self.parent.volumeFrame.volume_Ps_split_2.set(round(volume_Ps_split_2, 3))
            self.parent.volumeFrame.volume_Ps_split_3.set(round(volume_Ps_split_3, 3))
            losses = round((1 - (1 - (10 / total_volume) ** 2 - ((6.7 / (total_volume / 4)) ** 3) * 4) ** (
                int(number_of_cycle))) * 100, 3)
            self.losses.set(str(losses) + ' %')


        self.button_font_1 = font.Font(size=8, weight='bold')
        self.boutton_ok = ttk.Button(self, text="OK",
                               command=lambda:update_number_of_cycle()
                               #fg='#049B5A', bg='#9BF9E0',
                               #font=self.button_font_1
                                     )
        self.boutton_ok.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=5)

        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, text="Total volume for the split and pool", font=self.MainTitleLabel_font)
        #self.MainTitleLabel.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.total_volume = StringVar()
        self.total_volume.set(total_volume)
        self.entree_total_volume = Entry(self, textvariable=self.total_volume, width=2, justify='center')
        #self.entree_total_volume.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.MainTitleLabel = Label(self, text="ul   ")
        #self.MainTitleLabel.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, text="                            Number of cycles")
        self.MainTitleLabel.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.number_of_cycle = StringVar()
        self.number_of_cycle.set(str(number_of_cycle))
        self.MainTitleLabel = Label(self, textvariable=self.number_of_cycle, font=self.MainTitleLabel_font)
        self.MainTitleLabel.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.MainTitleLabel = Label(self, text="                            Total losses")
        self.MainTitleLabel.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.losses = StringVar()
        self.losses.set(str(losses) + ' %')
        self.MainTitleLabel = Label(self, textvariable=self.losses, font=self.MainTitleLabel_font)
        self.MainTitleLabel.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.MainTitleLabel = Label(self, text="                            Estimated duration")
        self.MainTitleLabel.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.total_duration = StringVar()
        self.total_duration.set(str(duration))
        self.MainTitleLabel = Label(self, textvariable=self.total_duration, font=self.MainTitleLabel_font)
        self.MainTitleLabel.pack(side=LEFT, fill=BOTH, expand=TRUE)


class LabwareFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, text="Choice of labware and location on deck", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=1)

        self.MainTitleLabel = Label(self, text="Labware used")
        self.MainTitleLabel.grid(row=1, column=2)

        self.MainTitleLabel = Label(self, text="Location on deck")
        self.MainTitleLabel.grid(row=1, column=3, padx=10)

        self.MainTitleLabel = Label(self, text="Tiprack")
        self.MainTitleLabel.grid(row=2, column=1)

        self.tiprack = StringVar()
        self.tiprack.set(tiprack)
        self.opt_tiprack = ttk.OptionMenu(self, self.tiprack, tiprack, *TiprackList)
        self.opt_tiprack.grid(row=2, column=2)

        self.loc_tiprack = StringVar()
        self.loc_tiprack.set(tiprack_loc)
        self.opt_loc_tiprack = ttk.OptionMenu(self, self.loc_tiprack, tiprack_loc, *LocationList)
        self.opt_loc_tiprack.grid(row=2, column=3)

        self.MainTitleLabel = Label(self, text="ReagentReservoir")
        self.MainTitleLabel.grid(row=3, column=1)

        self.Reservoir = StringVar()
        self.Reservoir.set(reservoir)
        self.opt_Reservoir = ttk.OptionMenu(self, self.Reservoir, reservoir, *ReagentReservoirList)
        self.opt_Reservoir.grid(row=3, column=2)

        self.loc_Reservoir = StringVar()
        self.loc_Reservoir.set(reservoir_loc)
        self.opt_loc_Reservoir = ttk.OptionMenu(self, self.loc_Reservoir, reservoir_loc, *LocationList)
        self.opt_loc_Reservoir.grid(row=3, column=3)

        self.MainTitleLabel = Label(self, text="FilterPlate")
        self.MainTitleLabel.grid(row=4, column=1)

        self.FilterPlate = StringVar()
        self.FilterPlate.set(filterPlate)
        self.opt_FilterPlate = ttk.OptionMenu(self, self.FilterPlate, filterPlate, *FilterPlateList)
        self.opt_FilterPlate.grid(row=4, column=2)

        self.loc_FilterPlate = StringVar()
        self.loc_FilterPlate.set(filterPlate_loc)
        self.opt_loc_FilterPlate = ttk.OptionMenu(self, self.loc_FilterPlate, filterPlate_loc, *LocationList)
        self.opt_loc_FilterPlate.grid(row=4, column=3)

        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, text="Pipet placement", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=4, padx=10)

        self.MainTitleLabel = Label(self, text="SingleChannel")
        self.MainTitleLabel.grid(row=2, column=4)

        self.singleChannel = StringVar()
        self.singleChannel.set(singleChannel)
        self.opt_singleChannel = ttk.OptionMenu(self, self.singleChannel, singleChannel, *Side)
        self.opt_singleChannel.grid(row=2, column=5)

        self.MainTitleLabel = Label(self, text="MultiChannel")
        self.MainTitleLabel.grid(row=3, column=4)

        self.multiChannel = StringVar()
        self.multiChannel.set(multiChannel)
        self.opt_multiChannel = ttk.OptionMenu(self, self.multiChannel, multiChannel, *Side)
        self.opt_multiChannel.grid(row=3, column=5)

        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, text="Pipetting conditions", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=6, padx=20)

        self.MainTitleLabel = Label(self, text="Aspirate flow rate")
        self.MainTitleLabel.grid(row=2, column=6)

        self.asp_flow_rate = StringVar()
        self.asp_flow_rate.set(asp_flow_rate)
        self.entree_asp_flow_rate = ttk.Entry(self, textvariable=self.asp_flow_rate, width=4, justify='center')
        self.entree_asp_flow_rate.grid(row=2, column=7)

        self.MainTitleLabel = Label(self, text="Dispense flow rate")
        self.MainTitleLabel.grid(row=3, column=6)

        self.disp_flow_rate = StringVar()
        self.disp_flow_rate.set(disp_flow_rate)
        self.entree_disp_flow_rate = ttk.Entry(self, textvariable=self.disp_flow_rate, width=4, justify='center')
        self.entree_disp_flow_rate.grid(row=3, column=7)

        self.MainTitleLabel = Label(self, text="Aspirate height (mm)\n(above the bottom of the well)")
        self.MainTitleLabel.grid(row=4, column=6, padx=10)


        self.asp_depth = StringVar()
        self.asp_depth.set(asp_depth)
        self.entreeAsp_depth = ttk.Entry(self, textvariable=self.asp_depth, width=4, justify='center')
        self.entreeAsp_depth.grid(row=4, column=7)


        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, text="Precision pipetting", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=9)

        self.MainTitleLabel = Label(self, text="Aspirate height (mm)\n(above the bottom of the well)")
        self.MainTitleLabel.grid(row=3, column=9, padx=10)


        self.asp_depth = StringVar()
        self.asp_depth.set(asp_depth_precision)
        self.entreeAsp_depth = ttk.Entry(self, textvariable=self.asp_depth, width=4, justify='center')
        self.entreeAsp_depth.grid(row=3, column=10)

        self.MainTitleLabel = Label(self, text="Aspirate flow rate")
        self.MainTitleLabel.grid(row=2, column=9)

        self.flow_rate = StringVar()
        self.flow_rate.set(flow_rate)
        self.entree_flow_rate = ttk.Entry(self, textvariable=self.flow_rate, width=4, justify='center')
        self.entree_flow_rate.grid(row=2, column=10)


class VolumeFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, text=" ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=0, column=0)

        #Nucleotide A--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="A")
        self.MainTitleLabel.grid(row=1, column=0)

        self.MainTitleLabel = Label(self, text="Well 0")
        self.MainTitleLabel.grid(row=1, column=1)

        self.volume_nucleotide = StringVar()
        self.volume_nucleotide.set(volume_nucleotide)
        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_nucleotide, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=0)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=1)

        # Nucleotide C--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="C")
        self.MainTitleLabel.grid(row=3, column=0)

        self.MainTitleLabel = Label(self, text="Well 1")
        self.MainTitleLabel.grid(row=3, column=1)


        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_nucleotide, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=0)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=1)

        # Nucleotide G--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="G")
        self.MainTitleLabel.grid(row=5, column=0)

        self.MainTitleLabel = Label(self, text="Well 2")
        self.MainTitleLabel.grid(row=5, column=1)

        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_nucleotide, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=0)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=1)

        # Nucleotide T--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="T")
        self.MainTitleLabel.grid(row=7, column=0)

        self.MainTitleLabel = Label(self, text="Well 3")
        self.MainTitleLabel.grid(row=7, column=1)

        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_nucleotide, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=0)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=1)

        # Colonne vide --------------------------------------------------------------------------------------------------

        self.MainTitleLabel = Label(self, text="    ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=2)

        # Enzyme --------------------------------------------------------------------------------------------------
        # Enzyme 1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="E")
        self.MainTitleLabel.grid(row=1, column=3)

        self.MainTitleLabel = Label(self, text="Well 8")
        self.MainTitleLabel.grid(row=1, column=4)

        self.volume_enzyme = StringVar()
        self.volume_enzyme.set(volume_enzyme)
        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_enzyme, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=3)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=4)

        # Enzyme 2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="E")
        self.MainTitleLabel.grid(row=3, column=3)

        self.MainTitleLabel = Label(self, text="Well 9")
        self.MainTitleLabel.grid(row=3, column=4)

        self.MainTitleLabel = Label(self, textvariable=self.volume_enzyme, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=3)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=4)

        # Enzyme 3--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="E")
        self.MainTitleLabel.grid(row=5, column=3)

        self.MainTitleLabel = Label(self, text="Well 10")
        self.MainTitleLabel.grid(row=5, column=4)

        self.MainTitleLabel = Label(self, textvariable=self.volume_enzyme, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=3)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=4)

        # Enzyme 4--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="E")
        self.MainTitleLabel.grid(row=7, column=3)

        self.MainTitleLabel = Label(self, text="Well 11")
        self.MainTitleLabel.grid(row=7, column=4)

        self.MainTitleLabel = Label(self, textvariable=self.volume_enzyme, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=3)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=4)

        # Colonne vide --------------------------------------------------------------------------------------------------

        self.MainTitleLabel = Label(self, text="    ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=5)

        # Wash 1 --------------------------------------------------------------------------------------------------
        # Wash 1.1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="W1")
        self.MainTitleLabel.grid(row=1, column=6)

        self.MainTitleLabel = Label(self, text="Well 16")
        self.MainTitleLabel.grid(row=1, column=7)

        self.volume_W1 = StringVar()
        self.volume_W1.set(volume_W1)
        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_W1, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=6)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=7)

        # Wash 1.2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="W1")
        self.MainTitleLabel.grid(row=3, column=6)

        self.MainTitleLabel = Label(self, text="Well 17")
        self.MainTitleLabel.grid(row=3, column=7)

        self.MainTitleLabel = Label(self, textvariable=self.volume_W1, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=6)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=7)

        # Wash 1.3--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="W1")
        self.MainTitleLabel.grid(row=5, column=6)

        self.MainTitleLabel = Label(self, text="Well 18")
        self.MainTitleLabel.grid(row=5, column=7)

        self.MainTitleLabel = Label(self, textvariable=self.volume_W1, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=6)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=7)

        # Wash 1.4--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="W1")
        self.MainTitleLabel.grid(row=7, column=6)

        self.MainTitleLabel = Label(self, text="Well 19")
        self.MainTitleLabel.grid(row=7, column=7)

        self.MainTitleLabel = Label(self, textvariable=self.volume_W1, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=6)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=7)

        # Colonne vide --------------------------------------------------------------------------------------------------

        self.MainTitleLabel = Label(self, text="    ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=8)

        # Deblock --------------------------------------------------------------------------------------------------
        # Deblock 1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="D")
        self.MainTitleLabel.grid(row=1, column=9)

        self.MainTitleLabel = Label(self, text="Well 24")
        self.MainTitleLabel.grid(row=1, column=10)

        self.volume_D = StringVar()
        self.volume_D.set(volume_D)
        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_D, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=9)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=10)

        # Deblock 2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="D")
        self.MainTitleLabel.grid(row=3, column=9)

        self.MainTitleLabel = Label(self, text="Well 25")
        self.MainTitleLabel.grid(row=3, column=10)

        self.MainTitleLabel = Label(self, textvariable=self.volume_D, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=9)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=10)

        # Deblock 3--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="D")
        self.MainTitleLabel.grid(row=5, column=9)

        self.MainTitleLabel = Label(self, text="Well 26")
        self.MainTitleLabel.grid(row=5, column=10)

        self.MainTitleLabel = Label(self, textvariable=self.volume_D, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=9)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=10)

        # Deblock 4--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="D")
        self.MainTitleLabel.grid(row=7, column=9)

        self.MainTitleLabel = Label(self, text="Well 27")
        self.MainTitleLabel.grid(row=7, column=10)

        self.MainTitleLabel = Label(self, textvariable=self.volume_D, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=9)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=10)

        # Colonne vide --------------------------------------------------------------------------------------------------

        self.MainTitleLabel = Label(self, text="    ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=11)

        # Wash 2 --------------------------------------------------------------------------------------------------
        # Wash 2.1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="W2")
        self.MainTitleLabel.grid(row=1, column=12)

        self.MainTitleLabel = Label(self, text="Well 32")
        self.MainTitleLabel.grid(row=1, column=13)

        self.volume_W2 = StringVar()
        self.volume_W2.set(volume_W2)
        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_W2, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=12)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=13)

        # Wash 2.2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="W2")
        self.MainTitleLabel.grid(row=3, column=12)

        self.MainTitleLabel = Label(self, text="Well 33")
        self.MainTitleLabel.grid(row=3, column=13)

        self.MainTitleLabel = Label(self, textvariable=self.volume_W2, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=12)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=13)

        # Wash 2.3--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="W2")
        self.MainTitleLabel.grid(row=5, column=12)

        self.MainTitleLabel = Label(self, text="Well 34")
        self.MainTitleLabel.grid(row=5, column=13)

        self.MainTitleLabel = Label(self, textvariable=self.volume_W2, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=12)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=13)

        # Wash 2.4--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="W2")
        self.MainTitleLabel.grid(row=7, column=12)

        self.MainTitleLabel = Label(self, text="Well 35")
        self.MainTitleLabel.grid(row=7, column=13)

        self.MainTitleLabel = Label(self, textvariable=self.volume_W2, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=12)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=13)

        # Colonne vide --------------------------------------------------------------------------------------------------

        self.MainTitleLabel = Label(self, text="                                              Volumes for reagents                                              ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=0, column=14)

        # Pooling solution --------------------------------------------------------------------------------------------------
        # Pooling solution 1.1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=1, column=15)

        self.MainTitleLabel = Label(self, text="Well 64")
        self.MainTitleLabel.grid(row=1, column=16)

        self.volume_Ps_pool = StringVar()
        self.volume_Ps_pool.set(volume_Ps_pool)
        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=15)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=16)

        # Pooling solution 1.2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=3, column=15)

        self.MainTitleLabel = Label(self, text="Well 65")
        self.MainTitleLabel.grid(row=3, column=16)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=15)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=16)

        # Pooling solution 1.3--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=5, column=15)

        self.MainTitleLabel = Label(self, text="Well 66")
        self.MainTitleLabel.grid(row=5, column=16)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=15)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=16)

        # Pooling solution 1.4--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=7, column=15)

        self.MainTitleLabel = Label(self, text="Well 67")
        self.MainTitleLabel.grid(row=7, column=16)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=15)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=16)

        # Colonne vide --------------------------------------------------------------------------------------------------

        self.MainTitleLabel = Label(self, text="    ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=17)

        # Pooling solution --------------------------------------------------------------------------------------------------
        # Pooling solution 1.1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=1, column=18)

        self.MainTitleLabel = Label(self, text="Well 72")
        self.MainTitleLabel.grid(row=1, column=19)


        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=18)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=19)

        # Pooling solution 1.2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=3, column=18)

        self.MainTitleLabel = Label(self, text="Well 73")
        self.MainTitleLabel.grid(row=3, column=19)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=18)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=19)

        # Pooling solution 1.3--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=5, column=18)

        self.MainTitleLabel = Label(self, text="Well 74")
        self.MainTitleLabel.grid(row=5, column=19)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=18)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=19)

        # Pooling solution 1.4--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=7, column=18)

        self.MainTitleLabel = Label(self, text="Well 75")
        self.MainTitleLabel.grid(row=7, column=19)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=18)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=19)

        # Colonne vide --------------------------------------------------------------------------------------------------

        self.MainTitleLabel = Label(self, text="    ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=20)

        # Pooling solution --------------------------------------------------------------------------------------------------
        # Pooling solution 1.1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=1, column=21)

        self.MainTitleLabel = Label(self, text="Well 80")
        self.MainTitleLabel.grid(row=1, column=22)


        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=21)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=22)

        # Pooling solution 1.2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=3, column=21)

        self.MainTitleLabel = Label(self, text="Well 81")
        self.MainTitleLabel.grid(row=3, column=22)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=21)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=22)

        # Pooling solution 1.3--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=5, column=21)

        self.MainTitleLabel = Label(self, text="Well 82")
        self.MainTitleLabel.grid(row=5, column=22)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=21)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=22)

        # Pooling solution 1.4--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=7, column=21)

        self.MainTitleLabel = Label(self, text="Well 83")
        self.MainTitleLabel.grid(row=7, column=22)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_pool, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=21)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=22)

        # Colonne vide --------------------------------------------------------------------------------------------------

        self.MainTitleLabel = Label(self, text="    ", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=1, column=23)

        # Pooling solution for split --------------------------------------------------------------------------------------------------
        # Pooling solution for split 1.1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=1, column=24)

        self.MainTitleLabel = Label(self, text="Well 88")
        self.MainTitleLabel.grid(row=1, column=25)

        self.volume_Ps_split_1 = StringVar()
        self.volume_Ps_split_1.set(volume_Ps_split_1)
        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_split_1, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=24)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=2, column=25)

        # Pooling solution for split 1.2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=3, column=24)

        self.MainTitleLabel = Label(self, text="Well 89")
        self.MainTitleLabel.grid(row=3, column=25)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_split_1, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=24)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=4, column=25)

        # Pooling solution for split 2.1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=5, column=24)

        self.MainTitleLabel = Label(self, text="Well 90")
        self.MainTitleLabel.grid(row=5, column=25)

        self.volume_Ps_split_2 = StringVar()
        self.volume_Ps_split_2.set(volume_Ps_split_2)
        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_split_2, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=24)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=6, column=25)

        # Pooling solution for split 2.2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=7, column=24)

        self.MainTitleLabel = Label(self, text="Well 91")
        self.MainTitleLabel.grid(row=7, column=25)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_split_2, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=24)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=8, column=25)

        # Pooling solution for split 3.1--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=9, column=24)

        self.MainTitleLabel = Label(self, text="Well 92")
        self.MainTitleLabel.grid(row=9, column=25)

        self.volume_Ps_split_3 = StringVar()
        self.volume_Ps_split_3.set(volume_Ps_split_3)
        self.MainTitleLabel_font = font.Font(size=9, weight='bold')
        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_split_3, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=10, column=24)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=10, column=25)

        # Pooling solution for split 3.2--------------------------------------------------------------------------------------------------
        self.MainTitleLabel = Label(self, text="Ps")
        self.MainTitleLabel.grid(row=11, column=24)

        self.MainTitleLabel = Label(self, text="Well 93")
        self.MainTitleLabel.grid(row=11, column=25)

        self.MainTitleLabel = Label(self, textvariable=self.volume_Ps_split_3, font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=12, column=24)

        self.MainTitleLabel = Label(self, text="ml", font=self.MainTitleLabel_font)
        self.MainTitleLabel.grid(row=12, column=25)



class ButtonFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.big_button_font_1 = font.Font(size=12, weight='bold')
        self.gen_prot = Button(self, text="Generate protocol",
                               command=lambda: [genProtocol([int(self.parent.beadsFrame.entreeBeads.get()), int(self.parent.beadsFrame.entree_total_volume.get())],
                                                            [[self.parent.labwareFrame.tiprack.get(),
                                                              self.parent.labwareFrame.loc_tiprack.get()],
                                                             [self.parent.labwareFrame.Reservoir.get(),
                                                              self.parent.labwareFrame.loc_Reservoir.get()],
                                                             [self.parent.labwareFrame.FilterPlate.get(),
                                                              self.parent.labwareFrame.loc_FilterPlate.get()],
                                                             self.parent.labwareFrame.singleChannel.get(),
                                                             self.parent.labwareFrame.multiChannel.get()
                                                             ],
                                                            [self.parent.labwareFrame.entreeAsp_depth.get(),
                                                             self.parent.labwareFrame.entree_asp_flow_rate.get(),
                                                             self.parent.labwareFrame.entree_disp_flow_rate.get()
                                                             ]
                                                            ,
                                                            [
                                                                float(self.parent.labwareFrame.entreeAsp_depth.get()),
                                                                float(self.parent.labwareFrame.entree_flow_rate.get())
                                                            ]
                                                            )
                                   #, popUpbox()
                                    , update_number_of_cycle()
                                                ],
                               fg='#FFFFFF', bg='#eb5243', font=self.big_button_font_1, padx=10, pady=10)
        #self.gen_prot.grid(row=1, column=1, sticky='w')
        self.gen_prot.pack(side = LEFT, fill=BOTH, expand=TRUE)

        def update_number_of_cycle():
            number_of_cycle = ceil(log(int(self.parent.beadsFrame.entreeBeads.get())) / log(4))
            if number_of_cycle > 19:
                number_of_cycle = 19
            self.parent.beadsFrame.number_of_cycle.set(str(number_of_cycle))
            duration = time_2_percent[number_of_cycle - 1]
            self.parent.beadsFrame.total_duration.set(str(duration))
            # Update the volumes for the reagents
            total_volume = float(self.parent.beadsFrame.entree_total_volume.get())
            volume_nucleotide = 0.025 * number_of_cycle
            volume_enzyme = 0.025 * number_of_cycle
            volume_W1 = 0.050 * number_of_cycle
            volume_D = 0.100 * number_of_cycle
            volume_W2 = 0.050 * number_of_cycle
            self.parent.volumeFrame.volume_nucleotide.set(round(volume_nucleotide, 3))
            self.parent.volumeFrame.volume_enzyme.set(round(volume_enzyme, 3))
            self.parent.volumeFrame.volume_W1.set(round(volume_W1, 3))
            self.parent.volumeFrame.volume_D.set(round(volume_D, 3))
            self.parent.volumeFrame.volume_W2.set(round(volume_W2, 3))
            volume_Ps_pool = total_volume / 1000 / 4 * number_of_cycle
            if number_of_cycle <= 6:
                volume_Ps_split_1 = total_volume / 1000 * number_of_cycle
                volume_Ps_split_2 = 0
                volume_Ps_split_3 = 0
            if 6 < number_of_cycle <= 12:
                volume_Ps_split_1 = total_volume / 1000 * 6
                volume_Ps_split_2 = total_volume / 1000 * (number_of_cycle - 6)
                volume_Ps_split_3 = 0
            if 12 < number_of_cycle <= 19:
                volume_Ps_split_1 = total_volume / 1000 * 6
                volume_Ps_split_2 = total_volume / 1000 * 6
                volume_Ps_split_3 = total_volume / 1000 * (number_of_cycle - 6 * 2)
            self.parent.volumeFrame.volume_Ps_pool.set(round(volume_Ps_pool, 3))
            self.parent.volumeFrame.volume_Ps_split_1.set(round(volume_Ps_split_1, 3))
            self.parent.volumeFrame.volume_Ps_split_2.set(round(volume_Ps_split_2, 3))
            self.parent.volumeFrame.volume_Ps_split_3.set(round(volume_Ps_split_3, 3))
            losses = round((1 - (1 - (10 / total_volume) ** 2 - ((6.7 / (total_volume / 4)) ** 3) * 4) ** (
                int(number_of_cycle))) * 100, 3)
            self.parent.beadsFrame.losses.set(str(losses) + ' %')

        def reset():
            # beadsFrame
            self.parent.beadsFrame.entreeBeads.delete(0, END)
            self.parent.beadsFrame.entreeBeads.insert(0,number_beads)
            self.parent.beadsFrame.entree_total_volume.delete(0, END)
            self.parent.beadsFrame.entree_total_volume.insert(0, total_volume)
            self.parent.beadsFrame.number_of_cycle.set(number_of_cycle)
            self.parent.beadsFrame.losses.set(str(losses) + ' %')
            # labwareFrame
            self.parent.labwareFrame.tiprack.set(tiprack)
            self.parent.labwareFrame.Reservoir.set(reservoir)
            self.parent.labwareFrame.FilterPlate.set(filterPlate)
            self.parent.labwareFrame.loc_tiprack.set(tiprack_loc)
            self.parent.labwareFrame.loc_Reservoir.set(reservoir_loc)
            self.parent.labwareFrame.loc_FilterPlate.set(filterPlate_loc)
            self.parent.labwareFrame.singleChannel.set(singleChannel)
            self.parent.labwareFrame.multiChannel.set(multiChannel)
            # pipettingFrame
            self.parent.labwareFrame.entreeAsp_depth.delete(0, END)
            self.parent.labwareFrame.entreeAsp_depth.insert(0, asp_depth)
            # precisionPipettingFrame
            self.parent.labwareFrame.entreeAsp_depth.delete(0, END)
            self.parent.labwareFrame.entreeAsp_depth.insert(0, asp_depth_precision)
            self.parent.labwareFrame.entree_flow_rate.delete(0, END)
            self.parent.labwareFrame.entree_flow_rate.insert(0, flow_rate)
            self.parent.beadsFrame.total_duration.set(duration)
            self.parent.labwareFrame.entree_disp_flow_rate.delete(0, END)
            self.parent.labwareFrame.entree_disp_flow_rate.insert(0, disp_flow_rate)
            self.parent.labwareFrame.entree_asp_flow_rate.delete(0, END)
            self.parent.labwareFrame.entree_asp_flow_rate.insert(0, asp_flow_rate)
            # Volume frame
            volume_nucleotide = round(0.025 * number_of_cycle + 0.1, 3)
            volume_enzyme = round(0.025 * number_of_cycle + 0.1, 3)
            volume_W1 = round(0.05 * number_of_cycle + 0.1, 3)
            volume_D = round(0.1 * number_of_cycle + 0.1, 3)
            volume_W2 = round(0.05 * number_of_cycle + 0.1, 3)
            volume_Ps_pool = round(total_volume / 1000 / 4 * number_of_cycle + 0.1, 3)
            if number_of_cycle <= 6:
                volume_Ps_split_1 = round(total_volume / 1000 * number_of_cycle + 0.1, 3)
                volume_Ps_split_2 = 0
                volume_Ps_split_3 = 0
            if 6 < number_of_cycle <= 12:
                volume_Ps_split_1 = round(total_volume / 1000 * 6 + 0.1, 3)
                volume_Ps_split_2 = round(total_volume / 1000 * (number_of_cycle - 6) + 0.1, 3)
                volume_Ps_split_3 = 0
            if 12 < number_of_cycle <= 19:
                volume_Ps_split_1 = round(total_volume / 1000 * 6 + 0.1, 3)
                volume_Ps_split_2 = round(total_volume / 1000 * 6 + 0.1, 3)
                volume_Ps_split_3 = round(total_volume / 1000 * (number_of_cycle - 6 * 2) + 0.1, 3)
            self.parent.volumeFrame.volume_Ps_pool.set(round(volume_Ps_pool, 3))
            self.parent.volumeFrame.volume_Ps_split_1.set(round(volume_Ps_split_1, 3))
            self.parent.volumeFrame.volume_Ps_split_2.set(round(volume_Ps_split_2, 3))
            self.parent.volumeFrame.volume_Ps_split_3.set(round(volume_Ps_split_3, 3))


        self.buttun_reset = Button(self, text="Reset to default parameters", command=lambda: reset(), fg='#FFFFFF', bg='#0b1334', font=self.big_button_font_1, padx=10, pady=10)
        self.buttun_reset.pack(side = RIGHT, fill=BOTH, expand=TRUE)

        def popUpbox():
            messagebox.showinfo(title="Information", message="Protocol generated, upload on Opentrons app to run it")

        def update_excel():
            os.system("taskkill /F /IM excel.exe")
            time.sleep(1)
            workbook = load_workbook(filename="Split_And_Pool_Controler.xlsx")
            sheet = workbook.active

            sheet["D8"] = self.parent.beadsFrame.entreeBeads.get()
            sheet["D12"] = self.parent.labwareFrame.tiprack.get()
            sheet["D13"] = self.parent.labwareFrame.Reservoir.get()
            sheet["D14"] = self.parent.labwareFrame.FilterPlate.get()
            sheet["K13"] = self.parent.labwareFrame.singleChannel.get()
            sheet["K14"] = self.parent.labwareFrame.multiChannel.get()

            date = datetime.datetime.now().strftime('%y%m%d')

            workbook.save(filename="Split_And_Pool_Controler_Updated_"+str(date)+".xlsx")
            os.startfile("Split_And_Pool_Controler_Updated_"+str(date)+".xlsx")

            #workbook.save(filename="Split_And_Pool_Controler_Updated_test.xlsx")
            #os.startfile("Split_And_Pool_Controler_Updated_test.xlsx")

        self.buttun_update = Button(self, text="Update and Open Excel file", command=lambda: update_excel(), fg='#FFFFFF',
                                       bg='#4cbc7c', font=self.big_button_font_1, padx=10, pady=10)
        self.buttun_update.pack(side=RIGHT, fill=BOTH, expand=TRUE)



if __name__ == "__main__":
    # GUI root implementation
    root = Tk()
    root.title("Split And Pool")
    SaP_MainFrame(root).grid(row=0, column=0, sticky='ns', padx=25, pady=15)

    root.grid_rowconfigure(3, minsize=20)

    root.mainloop()
