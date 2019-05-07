"""
Grab the efficiency files from Hale's output root file
to make a consolidated single file with all needed
efficiency ingredients:
    TGraph used for the fit (not used for applying trigger efficiencies/SFs)
    TF1 from resulting fit to TGraph
    TH1 containing error band from fit
"""

import ROOT
from TauAnalysisTools.TauTriggerSFs.helpers import getHist, getGraph, getFit

# choose which year's SF to calculate!
year2017 = False
year2018 = True


print "Making initial SF file"

if(year2017):
	iFile = ROOT.TFile( '/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/tauTriggerEfficiencies2017_final_perDM_v3.root', 'r' )

	oFile = ROOT.TFile( 'data/tauTriggerEfficiencies2017_FINAL.root', 'RECREATE' )
	oFile.cd()
elif(year2018):
	iFile = ROOT.TFile( '/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/tauTriggerFitResults2018_pre.root', 'r' )

	oFile = ROOT.TFile( 'data/tauTriggerEfficiencies2018_pre.root', 'RECREATE' )
	oFile.cd()


# Supporting 2017 MVAv2 only
for trigger in ['ditau', 'mutau', 'etau'] :
    for wp in ['vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'] : # No VVLoose
        for dm in ['dm0', 'dm1', 'dm10'] :
            for sample in ['DATA', 'MC'] :
                iName2017 = trigger+'_XXX_'+dm+'_'+wp+'TauMVA_'+sample
                iName2018 = trigger+'_XXX_'+wp+'TauMVA_'+dm+'_'+sample
                print iName2018
                if(year2017): iName = iName2017
                elif(year2018): iName = iName2018
                saveName = trigger+'_'+wp+'MVAv2_'+dm+'_'+sample
                print saveName
                g = getGraph( iFile, iName.replace('XXX','gEffi'), saveName+'_graph' )
                f = getFit( iFile, iName.replace('XXX','fit'), saveName+'_fit' )
                h = getHist( iFile, iName.replace('XXX','herrband'), saveName+'_errorBand' )
                oFile.cd()
                g.Write()
                f.Write()
                h.Write()

oFile.Close() 

