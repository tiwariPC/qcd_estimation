import os, sys
#//--------------------------------------------------------------------------------------
def getXsec(samplename):
    samplename = str(samplename)

    if 'QCD_HT1000to1500'   in samplename: Xsec  =	1094
    elif 'QCD_HT1500to2000'   in samplename: Xsec  =	98.99
    elif 'QCD_HT2000toInf'   in samplename: Xsec  =	20.23
    elif 'QCD_HT500to700'   in samplename: Xsec  =	29990
    elif 'QCD_HT700to1000'   in samplename: Xsec  =	6351
    elif 'QCD_HT200to300' in samplename: Xsec  =  1735000
    elif 'QCD_HT300to500' in samplename: Xsec  =  366800
    elif 'QCD_HT100to200' in samplename:Xsec = 23700000.

    # gamma+jets are reupdated based on twiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Gamma_jets
    elif 'GJets_HT-100To200'   in samplename: Xsec  =   9238#8622
    elif 'GJets_HT-200To400'   in samplename: Xsec  =   2305#2193
    elif 'GJets_HT-400To600'   in samplename: Xsec  =   274.4#258.5
    elif 'GJets_HT-40To100'   in samplename: Xsec  =    20790#18620
    elif 'GJets_HT-600ToInf'   in samplename: Xsec  =   93.46#85.21

    elif 'QCD_bEnriched_HT200to300'  in samplename: Xsec = 88240.00		
    elif 'QCD_bEnriched_HT300to500'  in samplename: Xsec = 17950.00
    elif 'QCD_bEnriched_HT500to700'  in samplename: Xsec = 1594.00
    elif 'QCD_bEnriched_HT700to1000'  in samplename: Xsec = 321.30
    elif 'QCD_bEnriched_HT1000to1500'  in samplename: Xsec = 51.61
    elif 'QCD_bEnriched_HT1500to2000'  in samplename: Xsec = 4.45
    elif 'QCD_bEnriched_HT2000toInf'  in samplename: Xsec = 0.78

    elif 'ST_s-channel_4f_leptonDecays'   in samplename: Xsec  =	10.32
    elif 'ST_t-channel_antitop_4f_inclusiveDecays'   in samplename: Xsec  =	80.95
    elif 'ST_t-channel_top_4f_inclusiveDecays'   in samplename: Xsec  =	 136.02
    elif 'ST_tW_antitop_5f_inclusiveDecays'   in samplename: Xsec  =	35.85#38.06
    elif 'ST_tW_top_5f_inclusiveDecays'   in samplename: Xsec  =	35.85#38.09
    elif 'TTTo2L2Nu'   in samplename: Xsec  =	88.29#687.1*0.105
    elif 'TTToHadronic'   in samplename: Xsec  =	377.96#687.1*0.457
    elif 'TTToSemiLeptonic'   in samplename: Xsec  =	365.34#687.1*0.438


    elif 'WW_TuneCP5_13TeV'   in samplename: Xsec  =	75.9
    elif 'WZ_TuneCP5_13TeV'   in samplename: Xsec  =	27.57


    elif 'ZZ_TuneCP5'   in samplename: Xsec  =	12.14

    elif 'DY1JetsToLL_M-50_LHEZpT_50-150_' in samplename: Xsec  = 315.1
    elif 'DY1JetsToLL_M-50_LHEZpT_150-250_' in samplename: Xsec  = 9.5
    elif 'DY1JetsToLL_M-50_LHEZpT_250-400_' in samplename: Xsec  = 1.097
    elif 'DY1JetsToLL_M-50_LHEZpT_400-inf' in samplename: Xsec  = 0.1207
    elif 'DY2JetsToLL_M-50_LHEZpT_50-150_' in samplename: Xsec  = 169
    elif 'DY2JetsToLL_M-50_LHEZpT_150-250_' in samplename: Xsec  = 15.73
    elif 'DY2JetsToLL_M-50_LHEZpT_250-400_' in samplename: Xsec  = 2.74
    elif 'DY2JetsToLL_M-50_LHEZpT_400-inf' in samplename: Xsec  = 0.4492


    elif 'W1JetsToLNu_LHEWpT_100-150_' in samplename: Xsec  = 284.06
    elif 'W1JetsToLNu_LHEWpT_150-250_' in samplename: Xsec  = 71.71
    elif 'W1JetsToLNu_LHEWpT_250-400_' in samplename: Xsec  = 8.06
    elif 'W1JetsToLNu_LHEWpT_400-inf_' in samplename: Xsec  = 0.89
    elif 'W2JetsToLNu_LHEWpT_100-150_' in samplename: Xsec  = 281.63
    elif 'W2JetsToLNu_LHEWpT_150-250_' in samplename: Xsec  = 108.59
    elif 'W2JetsToLNu_LHEWpT_250-400_' in samplename: Xsec  = 18.03
    elif 'W2JetsToLNu_LHEWpT_400-inf_' in samplename: Xsec  = 3

    elif 'Z1JetsToNuNu_M-50_LHEZpT_50-150_' in samplename: Xsec  = 598.9
    elif 'Z1JetsToNuNu_M-50_LHEZpT_150-250_' in samplename: Xsec  = 18.04
    elif 'Z1JetsToNuNu_M-50_LHEZpT_250-400_' in samplename: Xsec  = 2.051
    elif 'Z1JetsToNuNu_M-50_LHEZpT_400-inf_' in samplename: Xsec  = 0.2251
    elif 'Z2JetsToNuNu_M-50_LHEZpT_50-150_' in samplename: Xsec  = 326.3
    elif 'Z2JetsToNuNu_M-50_LHEZpT_150-250_' in samplename: Xsec  = 29.6
    elif 'Z2JetsToNuNu_M-50_LHEZpT_250-400_' in samplename: Xsec  = 5.174
    elif 'Z2JetsToNuNu_M-50_LHEZpT_400-inf_' in samplename: Xsec  = 0.8472

    elif 'ggZH_HToBB_ZToNuNu_M125'  in samplename: Xsec = 0.01222#*0.588
    elif 'ggZH_HToBB_ZToLL_M125'    in samplename: Xsec = 0.006185#*0.588
    elif 'WminusH_HToBB_WToQQ_M125' in samplename: Xsec = 0.3654#*0.588
    elif 'WplusH_HToBB_WToLNu_M125' in samplename: Xsec = 0.2819#*0.588
    elif 'ZH_HToBB_ZToLL_M125'      in samplename and 'ggZH_HToBB_ZToLL_M125' not in samplename:   Xsec = 0.07924#*0.588
    elif 'ZH_HToBB_ZToNuNu_M125'    in samplename and 'ggZH_HToBB_ZToNuNu_M125' not in samplename: Xsec = 0.1565#*0.588
    return Xsec
