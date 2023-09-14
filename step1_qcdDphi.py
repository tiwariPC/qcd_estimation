import ROOT
import os, math
import sys, argparse
import numpy as np
from glob import glob
from root_pandas import read_root
import array
## ----- command line argument
usage = "python step1_qcdDphi.py -i <input Directory> -o <output File>"
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-i", "--inputDir", dest="inputDir", default="inputDir")
parser.add_argument("-o", "--outputfile", dest="outputfile", default="step1_qcdDphi_output.root")
args = parser.parse_args()
if args.inputDir == None:
    sys.exit()
else:
    inputDir = args.inputDir

if args.outputfile == None:
    sys.exit()
else:
    outputfile = args.outputfile


files = glob(inputDir+'/*.root')
file_out = ROOT.TFile('rootFiles/'+outputfile, 'RECREATE')
# file_out.cd()
histo_list = []
for file_in in files:
  binx_ = np.linspace(0.0, 1.0, num = 41)
  # binx_ = np.linspace(0.0, 0.5, num=21)
  # binx_ = np.linspace(0.0, 3.14, num=101)
  biny_ = [0.0 , 0.25, 0.50 , 0.75, 1.0] ## for bbdm
  # biny_ = [200., 250., 290., 360., 420., 1000.] ## for monoH
  qcdDphi = ROOT.TH2F(file_in.split('/')[-1].strip('.root'),file_in.split('/')[-1].strip('.root'),len(binx_)-1,array.array('d', binx_),len(biny_)-1,array.array('d', biny_))
  h_total_mcweight = ROOT.TH1F('h_total_mcweight_'+file_in.split('/')[-1].strip('.root'), 'h_total_mcweight_'+file_in.split('/')[-1].strip('.root'), 2, 0, 2)

  print(h_total_mcweight)
  f_temp = ROOT.TFile.Open(file_in, 'READ')
  h_tmp_weight = f_temp.Get('h_total_mcweight')
  print(file_in.split('/')[-1].strip('.root'), h_tmp_weight.Integral())
  h_total_mcweight.Add(h_tmp_weight)

  hist_list = []
  # for df in read_root(file_in, 'bbDM_QCDbCR_1b', columns=['min_dPhi', 'MET', 'weight'], chunksize=125000):
  #   for dPhi_jetMET, MET, weight in zip(df.min_dPhi, df.MET, df.weight):
  #     if dPhi_jetMET == -9999: continue
  #     # ctsValue = abs(math.tanh(dEtaJet12/2))
  #     #print(dPhi_jetMET,ctsValue,weight)
  #     hist_list.append([dPhi_jetMET,MET,weight])
  #     #qcdDphi.Fill(dPhi_jetMET,ctsValue,weight)

  for df in read_root(file_in, 'bbDM_QCDbCR_2b', columns=['dPhi_jetMET', 'dEtaJet12', 'weight'], chunksize=125000):
    for dPhi_jetMET, dEtaJet12, weight in zip(df.dPhi_jetMET, df.dEtaJet12, df.weight):
      if dPhi_jetMET == -9999: continue
      ctsValue = abs(math.tanh(dEtaJet12/2))
      #print(dPhi_jetMET,ctsValue,weight)
      hist_list.append([dPhi_jetMET,ctsValue,weight])
      #qcdDphi.Fill(dPhi_jetMET,ctsValue,weight)

  # for df in read_root(file_in, 'bbDM_SR_2b', columns=['dPhi_jetMET', 'dEtaJet12', 'weight'], chunksize=125000):
  #   for dPhi_jetMET, dEtaJet12, weight in zip(df.dPhi_jetMET, df.dEtaJet12, df.weight):
  #     if dPhi_jetMET == -9999: continue
  #     ctsValue = abs(math.tanh(dEtaJet12/2))
  #     #print(dPhi_jetMET,ctsValue,weight)
  #     hist_list.append([dPhi_jetMET,ctsValue,weight])
  #     #qcdDphi.Fill(dPhi_jetMET,ctsValue,weight)

  #print(hist_list)
  for i in range(len(hist_list)):
    qcdDphi.Fill(hist_list[i][0],hist_list[i][1],hist_list[i][2])
  #qcdDphi.Write()

  histo_list.append(qcdDphi)
  histo_list.append(h_total_mcweight)

file_out.cd()
for hist in histo_list:
  hist.Write()
file_out.Close()
