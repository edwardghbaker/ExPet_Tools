# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 17:45:47 2021

@author: r11403eb

Must be run on python 3.10, due to hyperspy incompatibility
"""

#%%
import os as os
import glob as glob
import numpy as np
import hyperspy.api as hs
from hyperspy.io_plugins.bruker import BCF_reader
from lxml import etree, objectify  # not xml.etree; 
import matplotlib.pyplot as plt
from tqdm import tqdm


#%% define the class
class Bruker:
    
    def plotWithInfo(directory = r'C:\Users\r11403eb\OneDrive - The University of Manchester\meteoriteData\LAR 12156',file = 'LAR12156_position9_001.bcf'):
        
        newdir = os.path.join(directory, file.split(".", 1)[0])
        os.makedirs(newdir,exist_ok=True)
        
        filename = str(directory+'\\'+file)
        data = hs.load(filename, select_type='None')
        elements = data[-1].metadata.Sample.elements
        
        hs.plot.plot_images(data[0])
        plt.savefig(str(newdir+'\\'+'BSE.PNG'),dpi=1200)
        plt.close()
        data[-1].sum().plot(True)
        plt.savefig(str(newdir+'\\'+'Spectrum.PNG'),dpi=1200)
        plt.close()

        EDSdata = data[-1].get_lines_intensity()
        for i in range(len(EDSdata)):
            EDSdata[i].plot()
            plt.savefig(str(newdir+'\\'+elements[i]+'_info'),dpi=1200)
            plt.close()
            
    def plotNoInfo(directory=r'C:\Users\r11403eb\OneDrive - The University of Manchester\meteoriteData\LAR 12156',file='LAR12156_position9_001.bcf'):
        
        newdir = os.path.join(directory, file.split(".", 1)[0])
        os.makedirs(newdir,exist_ok=True)

        filename = str(directory+'\\'+file)
        data = hs.load(filename)
        elements = data[-1].metadata.Sample.elements
        #print(elements)
        EDSdata = data[-1].get_lines_intensity()
        
        for i in range(len(EDSdata)):
            if elements[i] == 'Cl':
                CMAP = 'Greens'
            elif elements[i] == 'Fe':
                CMAP = 'Blues'
            elif elements[i] == 'Si':
                CMAP = 'Reds'
            else:
                CMAP = 'Oranges'
            
            hs.plot.plot_images(hs.transpose(EDSdata[i]),cmap=CMAP, colorbar=None,label=None,tight_layout=True,padding={'wspace':0.0, 'hspace':0.0})
            plt.axis('off')
            plt.savefig(str(newdir+'\\'+elements[i]+'_noInfo'),transparent=True,orientation='landscape',dpi=1200)
            plt.close()

#%% apply the class to my data

def makePics(folder=r'C:\Users\r11403eb\OneDrive - The University of Manchester\meteoriteData\DOM 14021',method='Both'):
    
    
    os.chdir(folder)
    listOfFiles = glob.glob('*.bcf')
    print(listOfFiles)

    
    if method == 'Both':
        
        for i in tqdm(listOfFiles):
            Bruker.plotWithInfo(directory=folder,file=i)

        for i in tqdm(listOfFiles):
            Bruker.plotNoInfo(directory=folder,file=i)

            
    elif method == 'NoInfo':
        
        for i in tqdm(listOfFiles):
            Bruker.plotNoInfo(directory=folder,file=i)
            
            
    elif method == 'Info':
        
        for i in tqdm(listOfFiles):
            Bruker.plotWithInfo(directory=folder,file=i)




#%% Old code to extract header info


# # here we get the single file system handler
# #all file items in this singlefilesystem class instance is held inside
# # dictionary hierarchy, we fetch the header:
# header = file.vfs['EDSDatabase']['HeaderData']  
# #the items in the tree have special method which allows to get selection as BytesIO object:
# bstring = header.get_as_BytesIO_string()
# #rewind:
# bstring.seek(0)
# #for very huge nodes:
# parser = objectify.makeparser(huge_tree=True)
# #the final steps to print the xml to file for examination in text editor:
# xml_thingy = etree.fromstring(bstring.read(), parser)
# xml_root = xml_thingy.getroottree()
# xml_root.write('header_output.xml', pretty_print=True)
# # without pretty_print everything would be in the single line