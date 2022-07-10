import ROOT
import os, array
import sys
import matplotlib.pylab as plt
import numpy as np
import sampleXsecFiles.sample_xsec_2017_GenXSecAnalyser_nlo as sample_xsec
luminosity = 41.5 * 1000


file_in = ROOT.TFile(sys.argv[1], 'READ')
file_out = ROOT.TFile('dk_plot_'+sys.argv[1].split('/')[-1], 'RECREATE')

binx_ = np.linspace(0.0, 1.0, num=41)
# binx_ = np.linspace(0.0, 3.14, num=101)

qcdDphiCTS = {}
total_bins = 5

for key in range(1,total_bins+1):
  qcdDphiCTS[key] = ROOT.TH1F('qcdDphiCTS_bin'+str(key),'qcdDphiCTS_bin'+str(key),len(binx_)-1,array.array('d', binx_))

qcdDphiCTS_tot = ROOT.TH1F('qcdDphiCTS_tot','qcdDphiCTS_tot',len(binx_)-1,array.array('d', binx_))
qcdDphiCTS_tot2 = ROOT.TH1F('qcdDphiCTS_tot2','qcdDphiCTS_tot2',len(binx_)-1,array.array('d', binx_))

hist_list = ['DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'DY1JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'DY1JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'DY2JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'DY2JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8',
            'GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
            'GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8',
            'GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',
            'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8',
            'QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8',
            'QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8',
            'QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8',
            'QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8',
            'QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8',
            'QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8',
            'QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8',
            'ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8',
            'ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8',
            'ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8',
            'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
            'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
            'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',
            'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',
            'W1JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'W1JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'W2JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'WW_TuneCP5_13TeV-pythia8',
            'WZ_TuneCP5_13TeV-pythia8',
            'Z1JetsToNuNu_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'Z1JetsToNuNu_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'Z1JetsToNuNu_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'Z1JetsToNuNu_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'Z2JetsToNuNu_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'Z2JetsToNuNu_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'Z2JetsToNuNu_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'Z2JetsToNuNu_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
            'ZZ_TuneCP5_13TeV-pythia8',
            'combined_data_MET',
            'combined_data_SE',
            'crab_TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8',
            'crab_WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8',
            'crab_WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8',
            'crab_ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8',
            'crab_ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8',
            'crab_ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8',
            'crab_ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8',
            'ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8'
            ]

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
    xsec = sample_xsec.getXsec(histname)
    normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
    histo_.Scale(normlisation)
    WJets_Hists.append(histo_)
  elif 'DYJetsToLL_M-50' in histname or 'DYJetsToLL_Pt' in histname or 'DY1JetsToLL' in histname or 'DY2JetsToLL' in histname or 'DYJetsToLL_Pt' in histname:
    xsec = sample_xsec.getXsec(histname)
    normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
    histo_.Scale(normlisation)
    DYJets_Hits.append(histo_)
  elif 'ZJetsToNuNu' in histname or 'Z1JetsToNuNu' in histname or 'Z2JetsToNuNu' in histname or 'DYJetsToNuNu_PtZ' in histname:
    xsec = sample_xsec.getXsec(histname)
    normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
    histo_.Scale(normlisation)
    ZJets_Hits.append(histo_)
  elif 'GJets_HT' in histname:
    xsec = sample_xsec.getXsec(histname)
    normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
    histo_.Scale(normlisation)
    GJets_Hists.append(histo_)
  elif ('WWTo' in histname) or ('WZTo' in histname) or ('ZZTo' in histname) or ('WW_' in histname) or ('ZZ_' in histname) or ('WZ_' in histname):
    xsec = sample_xsec.getXsec(histname)
    normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
    histo_.Scale(normlisation)
    DIBOSON_Hists.append(histo_)
  elif ('ST_t' in histname) or ('ST_s' in histname):
    xsec = sample_xsec.getXsec(histname)
    normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
    histo_.Scale(normlisation)
    STop_Hists.append(histo_)
  elif ('TTTo' in histname) or ('TT_TuneCUETP8M2T4' in histname):
    xsec = sample_xsec.getXsec(histname)
    normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
    histo_.Scale(normlisation)
    Top_Hists.append(histo_)
  elif ('QCD_HT' in histname) or ('QCD_bEnriched_HT' in histname or ('QCD' in histname and 'BGenFilter' in histname)):
    xsec = sample_xsec.getXsec(histname)
    normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
    histo_.Scale(normlisation)
    QCD_Hists.append(histo_)
  elif 'HToBB' in histname:
    xsec = sample_xsec.getXsec(histname)
    normlisation = (xsec*luminosity)/(histo_total_weight.Integral())
    histo_.Scale(normlisation)
    SMH_Hists.append(histo_)
  elif 'combined_data_MET' in histname:
    MET_Hists.append(histo_)

print(MET_Hists)
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
    Top.Add(Top_Hists[i])
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

QCD = MET
QCD.Add(Tot_Bkg,-1)


binVal = {}
bin_integral = {}
integral = QCD.Integral()
for key in range(1,total_bins+1):
  ibin = 1
  binVal[key] = 0
  bin_integral[key] = sum([QCD.GetBinContent(x, key) for x in range(1, QCD.GetXaxis().GetNbins()+1)])
  for x in range(1,QCD.GetXaxis().GetNbins()+1):
    binVal[key] += QCD.GetBinContent(x, key)
    qcdDphiCTS[key].SetBinContent(ibin, bin_integral[key]-binVal[key])
    ibin+=1
  qcdDphiCTS[key].GetXaxis().SetTitle('minimum #Delta#phi(Jet,MET)')
  qcdDphiCTS[key].GetYaxis().SetTitle('Yield of bin'+str(key)+'(MET)')


ibin = 1
total_bin = 0
for x in range(1,QCD.GetXaxis().GetNbins()+1):
  total_bin += sum([QCD.GetBinContent(x, i) for i in range(1,QCD.GetXaxis().GetNbins()+1)])
  yVal_tot = integral-total_bin
  qcdDphiCTS_tot.SetBinContent(ibin, yVal_tot)
  qcdDphiCTS_tot2.SetBinContent(ibin, yVal_tot)
  ibin+=1
qcdDphiCTS_tot.GetXaxis().SetTitle('minimum #Delta#phi(Jet,MET)')
qcdDphiCTS_tot.GetYaxis().SetTitle('MET Yield')


file_out.cd()
for key in range(1,total_bins+1):
  qcdDphiCTS[key].Write()
qcdDphiCTS_tot.Write()
qcdDphiCTS_tot2.Write()
file_out.Close()

