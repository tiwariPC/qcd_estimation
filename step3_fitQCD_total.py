import ROOT as ROOT
from array import array
import os, sys
import numpy as np
import argparse

## ----- command line argument
usage = "python step3_fitQCD_total.py -i <input File> -O <output Directory>"
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-y", "--year", dest="year", default="Year")
parser.add_argument("-c", "--category", dest="category", default="2b")

args = parser.parse_args()

if args.category == None:
    sys.exit()
else:
    category = args.category

if not os.path.exists(args.year):
    os.makedirs(args.year)

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
  luminosity_ = '{0:.1f}'.format(35.90)
elif runOn2017:
  luminosity_ = '{0:.1f}'.format(41.50)
elif runOn2018:
  luminosity_ = '{0:.1f}'.format(59.64)

ROOT.gStyle.SetOptFit(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetFrameLineWidth(3)
ROOT.gStyle.SetLineWidth(2)

def myCanvas1D():
    c = ROOT.TCanvas("myCanvasName", "The Canvas Title", 650, 600)
    c.SetBottomMargin(0.11)
    c.SetRightMargin(0.020)
    c.SetLeftMargin(0.19)
    c.SetTopMargin(0.074)
    return c

def ExtraText(text_, x_, y_):
    if not text_:
        print("nothing provided as text to ExtraText, function crashing")
    ltx = ROOT.TLatex(x_, y_, text_)

    if len(text_) > 0:
        ltx.SetTextFont(42)
        ltx.SetTextSize(0.049)
        #ltx.Draw(x_,y_,text_)
        ltx.Draw('same')
    return ltx

c = myCanvas1D()

def leg():
    leg = ROOT.TLegend(0.65, 0.55, 0.88,0.850,'',"brNDC")
    leg.SetTextSize(0.052)
    leg.SetBorderSize(0)
    leg.SetLineStyle(8)
    leg.SetLineWidth(4)
    # sig_leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    return leg

def HistStyle(hist, title):
    hist.SetLineWidth(3)
    hist.SetMarkerStyle(20)
    hist.SetLineColor(1)
    hist.GetXaxis().SetTitle("minimum #Delta#phi(Jet,MET)")
    # hist.GetXaxis().SetRange(0,1)
    hist.GetXaxis().SetNdivisions(508)
    hist.GetXaxis().SetLabelFont(42)
    hist.GetXaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleSize(0.05)
    hist.GetXaxis().SetTitleOffset(1)
    hist.GetXaxis().SetTitleFont(42)
    hist.GetYaxis().SetTitle(title)
    hist.GetYaxis().CenterTitle(1)
    hist.GetYaxis().SetNdivisions(505)
    hist.GetYaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetYaxis().SetTitleSize(0.06)
    hist.GetYaxis().SetTitleOffset(1.4)
    hist.GetYaxis().SetTitleFont(42)
    hist.GetZaxis().SetLabelFont(42)
    hist.GetZaxis().SetTitleOffset(1)
    hist.GetZaxis().SetTitleFont(42)
    return hist

def drawenergy1D(is2017, text_="Work in progress 2018", data=True):
    #pt = ROOT.TPaveText(0.0877181,0.9,0.9580537,0.96,"brNDC")
    pt = ROOT.TPaveText(0.0877181, 0.95, 0.9580537, 0.96, "brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(52)

    cmstextSize = 0.07
    preliminarytextfize = cmstextSize * 0.7
    lumitextsize = cmstextSize * 0.7
    pt.SetTextSize(cmstextSize)
    text = pt.AddText(0.03, 0.57, "#font[61]{CMS}")

    #pt1 = ROOT.TPaveText(0.0877181,0.9,0.9580537,0.96,"brNDC")
    pt1 = ROOT.TPaveText(0.0877181, 0.95, 0.9580537, 0.96, "brNDC")
    pt1.SetBorderSize(0)
    pt1.SetTextAlign(12)
    pt1.SetFillStyle(0)
    pt1.SetTextFont(52)

    pt1.SetTextSize(preliminarytextfize)
    #text1 = pt1.AddText(0.215,0.4,text_)
    text1 = pt1.AddText(0.15, 0.4, text_)

    #pt2 = ROOT.TPaveText(0.0877181,0.9,0.9580537,0.96,"brNDC")
    pt2 = ROOT.TPaveText(0.0877181, 0.95, 0.9580537, 0.96, "brNDC")
    pt2.SetBorderSize(0)
    pt2.SetTextAlign(12)
    pt2.SetFillStyle(0)
    pt2.SetTextFont(52)
    pt2.SetTextFont(42)
    pt2.SetTextSize(lumitextsize)

    pavetext = ''
    if is2017 and data:
        pavetext = str(luminosity_)+' fb^{-1}'+" (13 TeV)"
    if (not is2017) and data:
        pavetext = str(luminosity_)+' fb^{-1}'+"(13 TeV)"

    if is2017 and not data:
        pavetext = "13 TeV"
    if (not is2017) and not data:
        pavetext = "13 TeV"

    if data:
        text3 = pt2.AddText(0.65, 0.5, pavetext)
    if not data:
        text3 = pt2.AddText(0.65, 0.5, pavetext)

    return [pt, pt1, pt2]


def fitWorkflow(mainhisto,myFunc,parameter,fitUptoBin):
    total_bins = np.linspace(0.0, 1.0, num=41)
    binsInUse = [i for i in total_bins if i <= fitUptoBin]

    tobeFitHisto = ROOT.TH1F('tobeFitHisto', 'tobeFitHisto', len(binsInUse)-1, array('d', binsInUse))
    for i in range(1,len(binsInUse)+1):
        tobeFitHisto.SetBinContent(i, mainhisto.GetBinContent(i))

    PrevFitTMP = ROOT.TF1("PrevFitTMP", myFunc, 0, fitUptoBin)
    PrevFitTMP.SetParLimits(0, 0, 1.E7) # Set a lower limit of 0 for parameter [0]
    # PrevFitTMP.SetParLimits(2, 0, 1.E7) # Set a lower limit of 0 for parameter [2]
    if '1b' in category:
        tobeFitHisto = HistStyle(tobeFitHisto, "#bf{p_{T}^{miss} Yield}")
        mainhisto = HistStyle(mainhisto, "#bf{p_{T}^{miss} Yield}")
    elif '2b' in category:
        tobeFitHisto = HistStyle(tobeFitHisto, "#bf{cos#Theta* Yield}")
        mainhisto = HistStyle(mainhisto, "#bf{cos#Theta* Yield}")
    tobeFitHisto.SetNameTitle("QCD Extrapolation","QCD Extrapolation")

    ''''
    ======================
    Fit Histogram Here
    ======================
    '''
    tobeFitHisto.Fit(PrevFitTMP, "IEM", "", 0, fitUptoBin)
    print('chi2/ndf = '+str(PrevFitTMP.GetChisquare())+'/'+str(PrevFitTMP.GetNDF()))
    param = {i:PrevFitTMP.GetParameter(i) for i in range(parameter)}
    param_err = {i:PrevFitTMP.GetParError(i) for i in range(parameter)}

    PrevFitTMP_sigUP = ROOT.TF1("PrevFitTMP_sigUP", myFunc, 0, 1.0)
    PrevFitTMP_sigDown = ROOT.TF1("PrevFitTMP_sigDown", myFunc, 0, 1.0)
    myFuncPost = myFunc
    for key in param:
        PrevFitTMP_sigUP.FixParameter(key, param[key]+param_err[key])
        PrevFitTMP_sigDown.FixParameter(key, param[key]-param_err[key])
        myFuncPost = myFuncPost.replace("["+str(key)+"]",str(param[key]))
    print("Fit Function with parameters: "+str(myFuncPost))
    PostFitTMP = ROOT.TF1("PostFitTMP", myFuncPost, 0, 1.0)

    normfactor = 41
    nominal_qcdReg = PostFitTMP.Integral(0,0.5)*normfactor
    error_qcdReg = ((PrevFitTMP_sigUP.Integral(0,0.5)-PrevFitTMP_sigDown.Integral(0,0.5))*normfactor)/2
    print('Integral(0,0.5)', nominal_qcdReg, error_qcdReg)

    nominal_sigReg = PostFitTMP.Integral(0.5,3.14)*normfactor
    error_sigReg = ((PrevFitTMP_sigUP.Integral(0.5,3.14)-PrevFitTMP_sigDown.Integral(0.5,3.14))*normfactor)/2
    print('Integral(0.5,3.14)', nominal_sigReg,error_sigReg)

    fitparam = 'Fit Parameters:'
    chi2ndf = '\Chi^{2}/ndf = '+str('{0:.3f}'.format(PrevFitTMP.GetChisquare()))+'/'+str(PrevFitTMP.GetNDF())
    param_print = {key:'p'+str(key)+' = '+str('{0:.2f}'.format(param[key]))+'\pm'+str('{0:.2f}'.format(param_err[key])) for key in param}
    ylocation = 0.45
    t2d0 = ExtraText(str(fitparam), 0.58, ylocation)
    t2d0.SetTextSize(0.04)
    t2d0.SetTextAlign(12)
    t2d0.SetNDC(ROOT.kTRUE)
    t2d0.SetTextFont(62)
    ylocation =  ylocation-0.05
    t2d = ExtraText(str(chi2ndf), 0.58, ylocation)
    t2d.SetTextSize(0.04)
    t2d.SetTextAlign(12)
    t2d.SetNDC(ROOT.kTRUE)
    t2d.SetTextFont(42)

    t2dp = {}
    for key in param:
      ylocation -= 0.05
      t2dp.update({key:ExtraText(str(param_print[key]), 0.58, ylocation)})
      t2dp[key].SetTextSize(0.04)
      t2dp[key].SetTextAlign(12)
      t2dp[key].SetNDC(ROOT.kTRUE)
      t2dp[key].SetTextFont(42)
    ''''
    ======================
    Draw Histograms Here
    ======================
    '''
    lgnd = leg()
    lgnd.AddEntry(tobeFitHisto," Used for Fit","PLE")
    lgnd.AddEntry(PrevFitTMP," Fit","l")
    lgnd.AddEntry(mainhisto, " All points", "PLE")
    lgnd.AddEntry(PrevFitTMP_sigUP, " #pm 1 #sigma", "l")
    lgnd.AddEntry(PostFitTMP, " Fit function", "l")

    mainhisto.SetLineColor(6)
    mainhisto.SetMarkerColor(6)
    mainhisto.SetLineWidth(2)
    mainhisto.GetXaxis().SetRangeUser(0,1)
    # mainhisto.GetYaxis().SetRangeUser(-200,6500)
    # mainhisto.GetYaxis().SetNdivisions(510) # Major and minor divisions
    mainhisto.Draw("LE hist")
    PrevFitTMP.Draw("same")
    tobeFitHisto.Draw("PLE same")
    PrevFitTMP_sigUP.SetLineStyle(2)
    PrevFitTMP_sigUP.SetLineColor(8)
    PrevFitTMP_sigUP.Draw('same')
    PrevFitTMP_sigDown.SetLineStyle(2)
    PrevFitTMP_sigDown.SetLineColor(8)
    PrevFitTMP_sigDown.Draw('same')
    PostFitTMP.SetLineStyle(2)
    PostFitTMP.SetLineColor(2)
    PostFitTMP.Draw('same')
    # FitTMP.Draw("same")
    t2d0.Draw("same")
    t2d.Draw("same")
    for key in param:
      t2dp[key].Draw("same")
    lgnd.Draw()
    line = ROOT.TLine(0, 0, 1.0, 0)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kBlack)
    line.Draw('same')
    pt = drawenergy1D(True, text_="  Internal", data=True)
    for ipt in pt:
        ipt.Draw()
    c.SetGrid(1,1)
    # c.SetLogy()
    c.Update()
    c.SaveAs(args.year+"/Overlay_binned_fitted_allBins_"+category+".pdf")
    c.SaveAs(args.year+"/Overlay_binned_fitted_allBins_"+category+".png")
    c.Close()
    c.ResetDrawn()
    return None


fin = ROOT.TFile.Open('rootFiles/step2_qcdDphi_multibins_'+category+'_'+args.year+'.root', "READ")

mainhisto = fin.Get("qcdDphiCTS_tot")

myFunc = "[0]*exp([1]*x)"
# myFunc = "[0]*exp([1]*x)+[2]"
# myFunc = "[0]*(1-x)/([1]+(x^[2])*exp([3]*x))"


# myFunc = "[0]*(1-x)^[1]/(x^([2]+[3]*log(x)))"
# myFunc = "ROOT::Math::Chebyshev9(x,[O],[1],[2],[3],[4],[5],[6],[7],[8],[9])"

# myFunc = "([0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)+[5]*pow(x,5)+[6]*pow(x,6)+[7]*pow(x,7)+[8]*pow(x,8)+[9]*pow(x,9))"

if '1b' in category:
    fitrange = 0.3
elif '2b' in category:
    fitrange = 0.3

fitWorkflow(mainhisto,myFunc,2,fitrange)