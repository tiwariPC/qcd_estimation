import ROOT as ROOT
from array import array
import os, sys
import numpy as np
import argparse
ROOT.gROOT.SetBatch(1)

# Set the default minimizer to Minuit2
ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")

## ----- command line argument
usage = "python step3_fitQCD_total.py -i <input File> -O <output Directory>"
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("-y", "--year", dest="year", default="Year")

args = parser.parse_args()

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
    c.SetBottomMargin(0.12)
    c.SetRightMargin(0.020)
    c.SetLeftMargin(0.15)
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

def leg():
    leg = ROOT.TLegend(0.62, 0.62, 0.88,0.90,'',"brNDC")
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
    # hist.GetXaxis().SetTitle("min(#Delta#phi(Jet,p_{T}^{miss}))")
    hist.GetXaxis().SetTitle("min(#Delta#phi(jet, #it{#vec{p}}_{#font[42]{T}}^{ miss}))")
    # hist.GetXaxis().SetRange(0,1)
    hist.GetXaxis().SetNdivisions(508)
    hist.GetXaxis().SetLabelFont(42)
    hist.GetXaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleSize(0.05)
    hist.GetXaxis().SetTitleOffset(1)
    hist.GetXaxis().SetTitleFont(42)
    hist.GetYaxis().SetTitle(title)
    # hist.GetYaxis().CenterTitle(1)
    hist.GetYaxis().SetNdivisions(508)
    hist.GetYaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetYaxis().SetTitleSize(0.06)
    hist.GetYaxis().SetTitleOffset(1.1)
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
    text = pt.AddText(0.05, 0.57, "#font[42]{ CMS}")

    #pt1 = ROOT.TPaveText(0.0877181,0.9,0.9580537,0.96,"brNDC")
    pt1 = ROOT.TPaveText(0.0877181, 0.95, 0.9580537, 0.96, "brNDC")
    pt1.SetBorderSize(0)
    pt1.SetTextAlign(12)
    pt1.SetFillStyle(0)
    pt1.SetTextFont(52)

    pt1.SetTextSize(preliminarytextfize)
    #text1 = pt1.AddText(0.215,0.4,text_)
    text1 = pt1.AddText(0.18, 0.4, text_)

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
        text3 = pt2.AddText(0.68, 0.5, pavetext)
    if not data:
        text3 = pt2.AddText(0.68, 0.5, pavetext)

    return [pt, pt1, pt2]

def fitWorkflow(mainhisto,myFunc,parameter,fitUptoBin,cr, file_out):
    total_bins = array('d',np.append(np.linspace(0.0, 3.10, num = 125), 3.14))
    binsInUse = [i for i in total_bins if i <= fitUptoBin]

    tobeFitHisto = ROOT.TH1F('tobeFitHisto', 'tobeFitHisto', len(binsInUse)-1, array('d', binsInUse))
    for i in range(1,len(binsInUse)+1):
        tobeFitHisto.SetBinContent(i, mainhisto.GetBinContent(i))

    PrevFitTMP = ROOT.TF1("PrevFitTMP", myFunc, 0, fitUptoBin)
    PrevFitTMP.SetParLimits(0, 0.0, 2E4) # Set a lower limit of 0 for parameter [0]
    # PrevFitTMP.SetParLimits(1, -1E6,0.0) # Set a lower limit of 0 for parameter [1]
    PrevFitTMP.SetParLimits(2, 0.0, 0.5) # Set a lower limit of 0 for parameter [2]
    if ('1b' in cr) or ('2j' in cr):
        tobeFitHisto = HistStyle(tobeFitHisto, "p_{T}^{miss} yield")
        mainhisto = HistStyle(mainhisto, "p_{T}^{miss} yield}")
    elif ('2b' in cr) or ('3j' in cr):
        tobeFitHisto = HistStyle(tobeFitHisto, "cos#Theta* yield")
        mainhisto = HistStyle(mainhisto, "cos#Theta* yield")
    tobeFitHisto.SetNameTitle("QCD Extrapolation","QCD Extrapolation")

    ''''x`
    ======================
    Fit Histogram Here
    ======================
    '''
    # tobeFitHisto.Fit(PrevFitTMP, "IEM", "", 0, fitUptoBin)
    tobeFitHisto.Fit(PrevFitTMP, "LFRS", "", 0, fitUptoBin)

    # Create a histogram to hold the confidence intervals
    bin_edges = array('d',np.append(np.linspace(0.0, 3.10, num = 125), 3.14))
    hint = ROOT.TH1D("hint", "Fitted Gaussian with .95 conf.band", len(bin_edges) - 1, bin_edges)
    ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint)

    print('chi2/ndf = '+str(PrevFitTMP.GetChisquare())+'/'+str(PrevFitTMP.GetNDF()))
    param = {i:PrevFitTMP.GetParameter(i) for i in range(parameter)}
    param_err = {i:PrevFitTMP.GetParError(i) for i in range(parameter)}

    PrevFitTMP_sigUP = ROOT.TF1("PrevFitTMP_sigUP", myFunc, 0, 1.0)
    PrevFitTMP_sigDown = ROOT.TF1("PrevFitTMP_sigDown", myFunc, 0, 1.0)
    #  PrevFitTMP_sigDown.SetParLimits(2, 0, 1.E7)
    myFuncPost = myFunc
    for key in param:
        PrevFitTMP_sigUP.FixParameter(key, param[key]+param_err[key])
        PrevFitTMP_sigDown.FixParameter(key, param[key]-param_err[key])
        myFuncPost = myFuncPost.replace("["+str(key)+"]",str(param[key]))
    print("Fit Function with parameters: "+str(myFuncPost))
    PostFitTMP = ROOT.TF1("PostFitTMP", myFuncPost, 0, 3.14)

    error_cls = array('d', [0.0])
    integral = hint.IntegralAndError(hint.FindBin(0.5), hint.FindBin(3.14), error_cls)
    print("The integral is", integral, "+/-", error_cls)

    fitparam = 'Fit Parameters:'
    chi2ndf = '\chi^{2}/ndf = '+str('{0:.3f}'.format(PrevFitTMP.GetChisquare()))+'/'+str(PrevFitTMP.GetNDF())
    param_print = {key:'p'+str(key)+' = '+str('{0:.2f}'.format(param[key]))+'\pm'+str('{0:.2f}'.format(param_err[key])) for key in param}

    # t2d1 = ExtraText(str(cr).replace('QCDCR_',' '), 0.15, 0.880)
    # t2d1.SetTextSize(0.05)
    # t2d1.SetTextAlign(12)
    # t2d1.SetNDC(ROOT.kTRUE)
    # t2d1.SetTextFont(62)

    t2d1tl = ExtraText("#splitline{QCD CR}{(#Delta#phi<0.5)}", 0.42, 0.50)
    t2d1tl.SetTextSize(0.04)
    t2d1tl.SetTextAlign(12)
    t2d1tl.SetNDC(ROOT.kTRUE)
    t2d1tl.SetTextFont(42)
    t2d1tl.SetTextColor(ROOT.kBlue)

    t2d1tr = ExtraText('#splitline{    SR}{(#Delta#phi > 0.5)}', 0.6, 0.50)
    t2d1tr.SetTextSize(0.04)
    t2d1tr.SetTextAlign(12)
    t2d1tr.SetNDC(ROOT.kTRUE)
    t2d1tr.SetTextFont(42)
    t2d1tr.SetTextColor(ROOT.kBlue)

    ylocation = 0.420
    t2d0 = ExtraText(str(fitparam), 0.63, ylocation)
    t2d0.SetTextSize(0.04)
    t2d0.SetTextAlign(12)
    t2d0.SetNDC(ROOT.kTRUE)
    t2d0.SetTextFont(62)
    # ylocation =  ylocation-0.05
    t2d = ExtraText(str(chi2ndf), 0.64, 0.59)
    t2d.SetTextSize(0.05)
    t2d.SetTextAlign(12)
    t2d.SetNDC(ROOT.kTRUE)
    t2d.SetTextFont(42)

    t2dp = {}
    for key in param:
        ylocation -= 0.05
        t2dp.update({key:ExtraText(str(param_print[key]), 0.64, ylocation)})
        t2dp[key].SetTextSize(0.04)
        t2dp[key].SetTextAlign(12)
        t2dp[key].SetNDC(ROOT.kTRUE)
        t2dp[key].SetTextFont(42)
    ''''
    ======================
    Draw Histograms Here
    ======================
    '''
    maxXaxis = 1.0
    lgnd = leg()
    lgnd.AddEntry(tobeFitHisto," Used for fit","PLE")
    lgnd.AddEntry(PrevFitTMP," Fit","l")
    lgnd.AddEntry(mainhisto, " All points", "PLE")
    # lgnd.AddEntry(PrevFitTMP_sigUP, " #pm 1 #sigma", "l")
    lgnd.AddEntry(hint, " #pm 1 #sigma", "f")
    lgnd.AddEntry(PostFitTMP, " Fit function", "l")
    mainhisto.Draw("LE hist")
    file_out.WriteObject(mainhisto,"all_points")
    PrevFitTMP.Draw("same")
    # PrevFitTMP_nPoints = mainhisto.GetNbinsX()  # Number of points to sample
    # PrevFitTMP_x_values = [PrevFitTMP.GetXmin() + i * (PrevFitTMP.GetXmax() - PrevFitTMP.GetXmin()) / PrevFitTMP_nPoints for i in range(PrevFitTMP_nPoints)]
    # PrevFitTMP_y_values = [PrevFitTMP.Eval(x) for x in PrevFitTMP_x_values]
    # PrevFitTMP_graph = ROOT.TGraph(PrevFitTMP_nPoints)
    # for i in range(PrevFitTMP_nPoints):
    #     PrevFitTMP_graph.SetPoint(i, PrevFitTMP_x_values[i], PrevFitTMP_y_values[i])
    # file_out.WriteObject(PrevFitTMP_graph, "fit")

    lastbinofPrevFitTMP = mainhisto.FindBin(fitUptoBin)
    PrevFitTMP_samebinning = mainhisto.Clone("PrevFitTMP_samebinning")
    PrevFitTMP_samebinning.Reset()
    for i in range(1,PrevFitTMP_samebinning.GetNbinsX()-1):
        if i <= lastbinofPrevFitTMP:
            x = PrevFitTMP_samebinning.GetBinCenter(i)
            y = PrevFitTMP.Eval(x)
            PrevFitTMP_samebinning.SetBinContent(i,y)
        else:
            PrevFitTMP_samebinning.SetBinContent(i,0)
    file_out.WriteObject(PrevFitTMP_samebinning, "fit")
    tobeFitHisto.Draw("PLE same")
    lastbinoftobeFitHisto = tobeFitHisto.GetNbinsX()
    tobeFitHisto_samebinning = mainhisto.Clone("tobeFitHisto_samebinning")
    tobeFitHisto_samebinning.Reset()
    for i in range(1,tobeFitHisto_samebinning.GetNbinsX()-1):
        if i <= lastbinoftobeFitHisto:
            tobeFitHisto_samebinning.SetBinContent(i,tobeFitHisto.GetBinContent(i))
        else:
            tobeFitHisto_samebinning.SetBinContent(i,0)
    file_out.WriteObject(tobeFitHisto_samebinning, "used_for_fit")
    hint.SetStats(False)
    hint.SetFillColor(8)
    hint_combined_error = hint.Clone("hint_combined_error")
    for i in range(1, hint_combined_error.GetNbinsX() + 1):
        default_error = hint.GetBinError(i)
        flat_error = hint.GetBinContent(i) * 0.2
        combined_error = (default_error**2 + flat_error**2)**0.5
        hint_combined_error.SetBinError(i, combined_error)
        # hint_combined_error.SetBinContent(i, combined_error)
    hint_combined_error.Sumw2()
    error_combined_error = array('d', [0.0])
    integral_combined_error = hint_combined_error.IntegralAndError(hint_combined_error.FindBin(0.5), hint_combined_error.FindBin(3.14), error_combined_error)
    print("The combined integral is", integral_combined_error, "+/-", error_combined_error)    # Set fill color for the combined error bars

    # hint_combined_error.Draw("same e3")
    hint.SetFillColorAlpha(ROOT.kGreen, 0.4)
    hint.Draw("e3 same")
    file_out.WriteObject(hint, "pm1_sigma")
    PrevFitTMP_sigUP.SetLineStyle(2)
    PrevFitTMP_sigUP.SetLineColor(8)
#     PrevFitTMP_sigUP.Draw('same')
    PrevFitTMP_sigDown.SetLineStyle(2)
    PrevFitTMP_sigDown.SetLineColor(8)
#     PrevFitTMP_sigDown.Draw('same')
    PostFitTMP.SetLineStyle(2)
    PostFitTMP.SetLineColor(2)
    PostFitTMP.Draw('same')
    PostFitTMP_nPoints = mainhisto.GetNbinsX()  # Number of points to sample
    PostFitTMP_x_values = [PostFitTMP.GetXmin() + i * (PostFitTMP.GetXmax() - PostFitTMP.GetXmin()) / PostFitTMP_nPoints for i in range(PostFitTMP_nPoints)]
    PostFitTMP_y_values = [PostFitTMP.Eval(x) for x in PostFitTMP_x_values]
    PostFitTMP_graph = ROOT.TGraph(PostFitTMP_nPoints)
    for i in range(PostFitTMP_nPoints):
        PostFitTMP_graph.SetPoint(i, PostFitTMP_x_values[i], PostFitTMP_y_values[i])
    file_out.WriteObject(PostFitTMP_graph, "fit_function")
    # FitTMP.Draw("same")
    # t2d1.Draw("same")
    t2d1tl.Draw("same")
    t2d1tr.Draw("same")
    # t2d0.Draw("same")
    t2d.Draw("same")
    # for key in param:
    #     t2dp[key].Draw("same")
    lgnd.Draw()
    linex = ROOT.TLine(0, 0, maxXaxis, 0)
    linex.SetLineStyle(2)
    linex.SetLineColor(ROOT.kBlack)
    linex.Draw('same')
    liney = ROOT.TLine(0.5, mainhisto.GetMinimum(), 0.5, mainhisto.GetMaximum())
    liney.SetLineStyle(2)
    liney.SetLineWidth(2)
    liney.SetLineColor(ROOT.kBlue)
    liney.Draw('same')
    pt = drawenergy1D(True, text_=" ", data=True)
    for ipt in pt:
        ipt.Draw()
    # c.SetGrid(1,1)
    c.SetLogy()
    c.Update()
    if not os.path.exists(args.year+'/'+cr):
        os.makedirs(args.year+'/'+cr)
    c.SaveAs(args.year+"/"+cr+"/Overlay_binned_fitted_allBins_"+cr+".pdf")
    c.SaveAs(args.year+"/"+cr+"/Overlay_binned_fitted_allBins_"+cr+".png")
    c.Close()
    c.ResetDrawn()
    if hint: hint.Delete()
    if PrevFitTMP: PrevFitTMP.Delete()
    if tobeFitHisto: tobeFitHisto.Delete()
    if PostFitTMP: PostFitTMP.Delete()

    # Get the total number of bins
    n_bins = mainhisto.GetNbinsX()

    # Initialize a variable to store the sum of errors
    sum_errors = []

    # Loop through each bin and sum the errors
    for i in range(1, n_bins + 1):
        error = mainhisto.GetBinError(i)
        sum_errors.append(error)
    # error_diff = max(sum_errors)-error_cls[0]
    error_diff = np.mean(sum_errors)-error_cls[0]
    # Print the  error
    print("***"*15)
    print("***"*15)
    print("==="*5+"0*0"*5+"==="*5)
    print("ERROR Difference: "+str(error_diff))
    print("==="*5+"0*0"*5+"==="*5)
    print("***"*15)
    print("***"*15)
    return None


fin = ROOT.TFile.Open('rootFiles/step2/step2_qcdDphi_'+args.year+'.root', "READ")
crs = ['QCDbCR_1b', 'QCDbCR_2b','ZeeQCDCR_2j', 'ZeeQCDCR_3j', 'ZmumuQCDCR_2j', 'ZmumuQCDCR_3j', 'WenuQCDCR_1b', 'WmunuQCDCR_1b', 'TopenuQCDCR_2b', 'TopmunuQCDCR_2b']
# crs=[ 'QCDbCR_2b']

for cr in crs:
    file_out = ROOT.TFile('rootFiles/step3/step3_qcdDphi_fitted_'+cr+'_'+args.year+'.root', 'RECREATE')
    c = myCanvas1D()
    c.SetTicky(1)
    c.SetTickx(1)
    mainhisto = fin.Get("qcdDphiCTS_"+cr+"_tot")
    myFunc = "[0]*exp([1]*x)+[2]"
    #  myFunc = "[0]/(exp([1]*x)"z
    #  myFunc = "[0]*(exp([1]*x)/(x^[2]))"
    # myFunc = "[0]*exp([1]*x)+[2]"
    # myFunc = "[0]*(1-x)/([1]+(x^[2])*exp([3]*x))"
    # myFunc = "[0]*(1-x)^[1]/(x^([2]+[3]*log(x)))"
    # myFunc = "ROOT::Math::Chebyshev9(x,[O],[1],[2],[3],[4],[5],[6],[7],[8],[9])"
    # myFunc = "([0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)+[5]*pow(x,5)+[6]*pow(x,6)+[7]*pow(x,7)+[8]*pow(x,8)+[9]*pow(x,9))"
    if mainhisto.GetMaximum() < 40: fitrange = 0.4
    else: fitrange = 0.3
    fitWorkflow(mainhisto,myFunc,3,fitrange,cr,file_out)
    file_out.Close()
