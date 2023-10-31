import ROOT
import os, array
import sys
# import matplotlib.pylab as plt
import numpy as np
import argparse
import histYearlist

sys.path.append('sampleXsecFiles')
import sample_xsec_run2 as sample_xsec
# ----- command line argument
usage = "python fitQCD_binwise.py -i <input File> -O <output File>"
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-y", "--year", dest="year", default="Year")
parser.add_argument("-c", "--category", dest="category", default="2b")

args = parser.parse_args()

if args.category == None:
    sys.exit()
else:
    category = args.category

runOn2016 = False
runOn2017 = False
runOn2018 = False
if args.year == '2016':
    runOn2016 = True
elif args.year == '2017':
    runOn2017 = True
elif args.year == '2018':
    runOn2018 = True
else:
    print('Please provide on which year you want to run?')

if runOn2016:
  hist_list = histYearlist.for2016
  luminosity = 35.90 * 1000
elif runOn2017:
  hist_list = histYearlist.for2017
  luminosity = 41.5 * 1000
elif runOn2018:
  hist_list = histYearlist.for2018
  luminosity = 59.64 * 1000


file_in = ROOT.TFile('rootFiles/step1_qcdDphi_'+category+'_'+args.year+'.root', 'READ')
file_out = ROOT.TFile('rootFiles/step2_qcdDphi_multibins_'+category+'_'+args.year+'.root', 'RECREATE')

binx_ = np.linspace(0.0, 1.0, num=41)
# binx_ = np.linspace(0.0, 3.14, num=101)

qcdDphiCTS = {}
total_bins = 4

for key in range(1,total_bins+1):
  qcdDphiCTS[key] = ROOT.TH1F('qcdDphiCTS_bin'+str(key),'qcdDphiCTS_bin'+str(key),len(binx_)-1,array.array('d', binx_))

qcdDphiCTS_tot = ROOT.TH1F('qcdDphiCTS_tot','qcdDphiCTS_tot',len(binx_)-1,array.array('d', binx_))
qcdDphiCTS_tot2 = ROOT.TH1F('qcdDphiCTS_tot2','qcdDphiCTS_tot2',len(binx_)-1,array.array('d', binx_))


DYJets_Hits = []
ZJets_Hits = []
WJets_Hists = []
GJets_Hists = []
DIBOSON_Hists = []
STop_Hists = []
Top_Hists = []
QCD_Hists = []
SMH_Hists = []
MET_Hists = []

for histname in hist_list:
    histo_ = file_in.Get(histname)
    histo_total_weight = file_in.Get('h_total_mcweight_'+histname)
    if 'WJetsToLNu' in histname or 'W1JetsToLNu' in histname or 'W2JetsToLNu' in histname or 'WJetsToLNu_Pt' in histname:
        xsec = sample_xsec.getXsec(histname,args.year)
        normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
        histo_.Scale(normlisation)
        WJets_Hists.append(histo_)
    elif 'DYJetsToLL_M-50' in histname or 'DYJetsToLL_Pt' in histname or 'DY1JetsToLL' in histname or 'DY2JetsToLL' in histname or 'DYJetsToLL_Pt' in histname:
        xsec = sample_xsec.getXsec(histname,args.year)
        normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
        histo_.Scale(normlisation)
        DYJets_Hits.append(histo_)
    elif 'ZJetsToNuNu' in histname or 'Z1JetsToNuNu' in histname or 'Z2JetsToNuNu' in histname or 'Z2JetsToNuNU' in histname or 'DYJetsToNuNu_PtZ' in histname:
        xsec = sample_xsec.getXsec(histname,args.year)
        normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
        histo_.Scale(normlisation)
        ZJets_Hits.append(histo_)
    elif 'GJets_HT' in histname:
        xsec = sample_xsec.getXsec(histname,args.year)
        normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
        histo_.Scale(normlisation)
        GJets_Hists.append(histo_)
    elif ('WWTo' in histname) or ('WZTo' in histname) or ('ZZTo' in histname) or ('WW_' in histname) or ('ZZ_' in histname) or ('WZ_' in histname):
        xsec = sample_xsec.getXsec(histname,args.year)
        normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
        histo_.Scale(normlisation)
        DIBOSON_Hists.append(histo_)
    elif ('ST_t' in histname) or ('ST_s' in histname):
        xsec = sample_xsec.getXsec(histname,args.year)
        normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
        histo_.Scale(normlisation)
        STop_Hists.append(histo_)
    elif ('TTTo' in histname) or ('TT_TuneCUETP8M2T4' in histname):
        xsec = sample_xsec.getXsec(histname,args.year)
        normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
        histo_.Scale(normlisation)
        Top_Hists.append(histo_)
    elif ('QCD_HT' in histname) or ('QCD_bEnriched_HT' in histname or ('QCD' in histname and 'BGenFilter' in histname)):
        xsec = sample_xsec.getXsec(histname,args.year)
        normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
        histo_.Scale(normlisation)
        QCD_Hists.append(histo_)
    elif 'HToBB' in histname:
        xsec = sample_xsec.getXsec(histname,args.year)
        normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
        histo_.Scale(normlisation)
        SMH_Hists.append(histo_)
    elif 'MET-Run' in histname:
        MET_Hists.append(histo_)

for i in range(len(WJets_Hists)):
    if i == 0:
        WJets = WJets_Hists[i]
    else:
        WJets.Add(WJets_Hists[i])
WJets.Sumw2()

for i in range(len(DYJets_Hits)):
  if i == 0:
    DYJets = DYJets_Hits[i]
  else:
    DYJets.Add(DYJets_Hits[i])
DYJets.Sumw2()

for i in range(len(ZJets_Hits)):
    if i == 0:
        ZJets = ZJets_Hits[i]
    else:
        ZJets.Add(ZJets_Hits[i])
ZJets.Sumw2()

for i in range(len(GJets_Hists)):
    if i == 0:
        GJets = GJets_Hists[i]
    else:
        GJets.Add(GJets_Hists[i])
GJets.Sumw2()

for i in range(len(DIBOSON_Hists)):
    if i == 0:
        DIBOSON = DIBOSON_Hists[i]
    else:
        DIBOSON.Add(DIBOSON_Hists[i])
DIBOSON.Sumw2()

for i in range(len(STop_Hists)):
    if i == 0:
        STop = STop_Hists[i]
    else:
        STop.Add(STop_Hists[i])
STop.Sumw2()

for i in range(len(Top_Hists)):
    if i == 0:
        Top = Top_Hists[i]
    else:
        Top.Add(top_Hists[i])
Top.Sumw2()

for i in range(len(QCD_Hists)):
    if i == 0:
        QCD_MC = QCD_Hists[i]
    else:
        QCD_MC.Add(QCD_Hists[i])
QCD_MC.Sumw2()

for i in range(len(SMH_Hists)):
    if i == 0:
        SMH = SMH_Hists[i]
    else:
    SMH.Add(SMH_Hists[i])
SMH.Sumw2()

for i in range(len(MET_Hists)):
    if i == 0:
        MET = MET_Hists[i]
    else:
        MET.Add(MET_Hists[i])
MET.Sumw2()

Tot_Bkg = WJets
Tot_Bkg.Add(DYJets)
Tot_Bkg.Add(ZJets)
Tot_Bkg.Add(GJets)
Tot_Bkg.Add(DIBOSON)
Tot_Bkg.Add(STop)
Tot_Bkg.Add(Top)
Tot_Bkg.Add(SMH)

Tot_Bkg.Sumw2()

QCD = MET.Clone()
QCD.Add(Tot_Bkg,-1)

for i in range(1,QCD.GetXaxis().GetNbins()+1):
    for j in range(1,5):
        if QCD.GetBinContent(i,j) <= 0.0:
            QCD.SetBinContent(i,j,0.0)
            QCD.SetBinError(i,j,0.0)

print("Y-Axis Bins",QCD.GetYaxis().GetNbins())
binVal = {}
bin_integral = {}
integral = QCD.Integral()
print(integral)
for key in range(1,total_bins+1):
    ibin = 1
    binVal[key] = 0
    bin_integral[key] = sum([QCD.GetBinContent(x, key) for x in range(1, QCD.GetXaxis().GetNbins()+1)])
    for x in range(1,QCD.GetXaxis().GetNbins()+1):
        binVal[key] += QCD.GetBinContent(x, key)
        qcdDphiCTS[key].SetBinContent(ibin, bin_integral[key]-binVal[key])
        ibin+=1
    qcdDphiCTS[key].GetXaxis().SetTitle('minimum #Delta#phi(Jet,MET)')
    if '1b' in category:
        qcdDphiCTS[key].GetYaxis().SetTitle('bin'+str(key)+' #bf{p_{T}^{miss} Yield}')
    elif '2b' in category:
        qcdDphiCTS[key].GetYaxis().SetTitle('bin'+str(key)+' cos(#theta)* Yield')


ibin = 1
total_bin = 0
for x in range(1,QCD.GetXaxis().GetNbins()+1):
    total_bin += sum([QCD.GetBinContent(x, i) for i in range(1,5)])
    yVal_tot = integral-total_bin
    qcdDphiCTS_tot.SetBinContent(ibin, yVal_tot)
    qcdDphiCTS_tot2.SetBinContent(ibin, yVal_tot)
    ibin+=1
qcdDphiCTS_tot.GetXaxis().SetTitle('minimum #Delta#phi(Jet,MET)')
if '1b' in category:
    qcdDphiCTS_tot.GetYaxis().SetTitle('#bf{p_{T}^{miss} Yield}')
elif '2b' in category:
    qcdDphiCTS_tot.GetYaxis().SetTitle('cos(#theta)* Yield')


file_out.cd()
for key in range(1,total_bins+1):
    qcdDphiCTS[key].Write()
qcdDphiCTS_tot.Write()
qcdDphiCTS_tot2.Write()
file_out.Close()