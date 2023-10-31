import ROOT
import os, math
import sys, argparse
import numpy as np
from glob import glob
from root_pandas import read_root
import pandas as pd
from array import array

## ----- command line argument
usage = "python step1_qcdDphi.py -i <input Directory> -o <output File>"
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-i", "--inputDir", dest="inputDir", default="inputDir")
parser.add_argument("-y", "--year", dest="year", default="Year")

args = parser.parse_args()
if args.inputDir == None:
    sys.exit()
else:
    inputDir = args.inputDir

if args.year == None:
    sys.exit()
else:
    year = args.year

def dataframe_concat(original_dataframe,input_filename):
    if '-Run2018A-' in input_filename or '-Run2018B-' in input_filename:
        # print('original_dataframe', original_dataframe.shape[0])
        return original_dataframe
    elif '-Run2018C-' in input_filename or '-Run2018D-' in input_filename:
        # print(input_filename,'original_dataframe',original_dataframe.shape[0])
        original_dataframe = original_dataframe[original_dataframe.isak4JetBasedHemEvent == 0]
        original_dataframe = original_dataframe[original_dataframe.ismetphiBasedHemEvent2 == 0]
        # print(input_filename,'original_dataframe',original_dataframe.shape[0])
        return original_dataframe
    else:
        # Set the random seed for reproducibility
        np.random.seed(12345)
        # Calculate the number of rows for 65% and 35% split
        split_ratio = 0.6469398078
        num_rows_AB = original_dataframe.shape[0]
        num_rows_CD = int(num_rows_AB * split_ratio)
        # Create a boolean mask for selecting 65% of the rows
        mask = np.random.rand(num_rows_AB) < split_ratio
        # Split the DataFrame into two parts based on the mask
        dataframe_CD = original_dataframe[mask]
        dataframe_AB = original_dataframe[~mask]
        # Perform some operations on part1 (for example, Vetoing some events)
        dataframe_CD = dataframe_CD[dataframe_CD.isak4JetBasedHemEvent == 0]
        dataframe_CD = dataframe_CD[dataframe_CD.ismetphiBasedHemEvent2 == 0]
        # Combine the parts
        final_dataframe = pd.concat([dataframe_AB, dataframe_CD], ignore_index=True)
        return final_dataframe


files = glob(inputDir+'/*.root')
file_out = ROOT.TFile('rootFiles/step1/step1_qcdDphi_'+year+'.root', 'RECREATE')

crs = ['bbDM_QCDbCR_1b', 'bbDM_QCDbCR_2b', 'bbDM_ZeeQCDCR_2j', 'bbDM_ZeeQCDCR_3j', 'bbDM_ZmumuQCDCR_2j', 'bbDM_ZmumuQCDCR_3j', 'bbDM_WenuQCDCR_1b', 'bbDM_WmunuQCDCR_1b', 'bbDM_TopenuQCDCR_2b', 'bbDM_TopmunuQCDCR_2b']
# crs=['bbDM_QCDbCR_1b']

histo_list = {}
for file_in in files:
    # binx_ = np.linspace(0.0, 1.0, num = 41)
    binx_ = array('d',np.append(np.linspace(0.0, 3.10, num = 125), 3.14))
    # binx_ = np.linspace(0.0, 3.15, num = 127)

    h_total_mcweight = ROOT.TH1F('h_total_mcweight_'+file_in.split('/')[-1].strip('.root'), 'h_total_mcweight_'+file_in.split('/')[-1].strip('.root'), 2, 0, 2)

    f_temp = ROOT.TFile.Open(file_in, 'READ')
    h_tmp_weight = f_temp.Get('h_total_mcweight')
    print(file_in.split('/')[-1].strip('.root'), h_tmp_weight.Integral())
    h_total_mcweight.Add(h_tmp_weight)
    for cr in crs:
        hist_list = []
        if ('1b' in cr) or ('2j' in cr):
            biny_ = [250, 300, 400, 550, 1000]
            qcdDphi = ROOT.TH2F(file_in.split('/')[-1].strip('.root')+cr.replace('bbDM_','_'),file_in.split('/')[-1].strip('.root')+cr.replace('bbDM_','_'),len(binx_)-1,array('d', binx_),len(biny_)-1,array('d', biny_))
            if 'bbDM_QCDbCR_1b' in cr:
                for df in read_root(file_in, cr, columns=['dPhi_jetMET', 'MET', 'weight', 'isak4JetBasedHemEvent', 'ismetphiBasedHemEvent2'], chunksize=125000):
                    if '2018' in year: df = dataframe_concat(df,file_in)
                    for dPhi_jetMET, MET, weight in zip(df.dPhi_jetMET, df.MET, df.weight):
                        if dPhi_jetMET == -9999: continue
                        hist_list.append([dPhi_jetMET,MET,weight])
            else:
                for df in read_root(file_in, cr, columns=['dPhi_jetMET', 'Recoil', 'weight', 'isak4JetBasedHemEvent', 'ismetphiBasedHemEvent2'], chunksize=125000):
                    if '2018' in year: df = dataframe_concat(df,file_in)
                    for dPhi_jetMET, Recoil, weight in zip(df.dPhi_jetMET, df.Recoil, df.weight):
                        if dPhi_jetMET == -9999: continue
                        hist_list.append([dPhi_jetMET,Recoil,weight])
        elif ('2b' in cr) or ('3j' in cr):
            biny_ = [0.0 , 0.25, 0.50 , 0.75, 1.0]
            qcdDphi = ROOT.TH2F(file_in.split('/')[-1].strip('.root')+cr.replace('bbDM_','_'),file_in.split('/')[-1].strip('.root')+cr.replace('bbDM_','_'),len(binx_)-1,array('d', binx_),len(biny_)-1,array('d', biny_))
            for df in read_root(file_in, cr, columns=['dPhi_jetMET', 'dEtaJet12', 'weight', 'isak4JetBasedHemEvent', 'ismetphiBasedHemEvent2'], chunksize=125000):
                if '2018' in year: df = dataframe_concat(df,file_in)
                for dPhi_jetMET, dEtaJet12, weight in zip(df.dPhi_jetMET, df.dEtaJet12, df.weight):
                    if dPhi_jetMET == -9999: continue
                    ctsValue = abs(math.tanh(dEtaJet12/2))
                    hist_list.append([dPhi_jetMET,ctsValue,weight])
        for i in range(len(hist_list)):
            qcdDphi.Fill(hist_list[i][0],hist_list[i][1],hist_list[i][2])
        file_out.cd()
        qcdDphi.Write()
        qcdDphi.Reset()
        # histo_list.update({file_in.split('/')[-1].strip('.root')+cr.replace('bbDM_','_'):qcdDphi})
    file_out.cd()
    h_total_mcweight.Write()
file_out.Close()
