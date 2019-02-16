"""
Grab the efficiency files from Hale's output root file
to make a consolidated single file with all needed
efficiency ingredients:
    TGraph used for the fit (not used for applying trigger efficiencies/SFs)
    TF1 from resulting fit to TGraph
    TH1 containing error band from fit
"""

import ROOT
from helpers import getHist, getGraph, getFit



print "Making initial SF file"

iFile = ROOT.TFile( '/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/tauTriggerEfficiencies2017_final_perDM.root', 'r' )

oFile = ROOT.TFile( 'data/tauTriggerEfficiencies2017_FINAL.root', 'RECREATE' )
oFile.cd()

# Supporting 2017 MVAv2 only
for trigger in ['ditau', 'mutau', 'etau'] :
    for wp in ['vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'] : # No VVLoose
        for dm in ['dm0', 'dm1', 'dm10'] :
            for sample in ['DATA', 'MC'] :
                iName = trigger+'_XXX_'+dm+'_'+wp+'TauMVA_'+sample
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

