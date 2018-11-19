import ROOT
from array import array
from math import sqrt

# Function to create TH1Fs from TGraphAsymmErrors
# This does not preserve the asymmetric errors, only
# bin width and value and does a rough approximation
# on symmetric errors.
def getTH1FfromTGraphAsymmErrors( asym, name ) :

    # Holding vals for TH1F binning and y-vals
    xSpacing = array( 'd', [] )
    yVals = array( 'd', [] )
    yErrors = array( 'd', [] )

    nVals = asym.GetN()
    x, y = ROOT.Double(0.), ROOT.Double(0.)
    xEPlus, xEMin = 0., 0.
    yEPlus, yEMin = 0., 0.

    for n in range( nVals ) :
        asym.GetPoint( n, x, y )
        xEPlus = asym.GetErrorXhigh( n )
        xEMin = asym.GetErrorXlow( n )
        yEPlus = asym.GetErrorYhigh( n )
        yEMin = asym.GetErrorYlow( n )
        xSpacing.append( x-xEMin )
        yVals.append( y )
        # To simplify, take asymm errors and go to approximation
        # of symmetric for TH1
        yErrors.append( sqrt(yEPlus**2 + yEMin**2) )

    # Don't forget to add the high end of last bin
    xSpacing.append( x+xEPlus )

    outH = ROOT.TH1F( name, name, len(xSpacing)-1, xSpacing )
    for bin in range( 1, outH.GetNbinsX()+1 ) :
        outH.SetBinContent( bin, yVals[bin-1] )
        outH.SetBinError( bin, yErrors[bin-1] )
    return outH


def getHist( fName, hName, saveName ) :
    f = ROOT.TFile( 'data/'+fName, 'r' )
    graph = f.Get( hName )
    h = getTH1FfromTGraphAsymmErrors( graph, saveName )
    h.SetDirectory( 0 )
    return h

def getGraph( fName, hName, saveName ) :
    f = ROOT.TFile( 'data/'+fName, 'r' )
    graph = f.Get( hName )
    graph.SetName( saveName )
    graph.SetTitle( saveName )
    return graph


if '__main__' in __name__ :
    print "Making initial SF file"

    oFile = ROOT.TFile( 'data/tauTriggerEfficiencies2017_New.root', 'RECREATE' )
    oFile.cd()
    
    histMap = {
        'histo_ETauTriggerPath_IsoMu20_LooseChargedIsoPFTau27_plusL1Tau26andHLTTau30' : 'ETauTriggerEfficiency',
        'histo_MuTauTriggerPath_IsoMu20_LooseChargedIsoPFTau27' : 'MuTauTriggerEfficiency',
        'histo_DiTauTriggerPath_TightTau35TightIDorMediumTau35TightIDplusHLTTau40orTightTau35plusHLTTau40_plusL1Tau32' : 'diTauTriggerEfficiency',
    }

    wpMap = {
        '2017v2' : 'MVA',
        'dR0p32017v2' : 'dR0p3',
    }

    # Supporting 2017 MVA and cut-based 2017 dR0p3
    for wp in wpMap.keys() :

        for tauWP in ['vvloose', 'vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'] :
            #dataFileName = 'fitOutput_Data_MuTau2017BCDEF_SFpaths_SSsubtraction_%sTauMVAWP.root' % tauWP
            #mcFileName = 'fitOutput_MC_MuTau2017_DYJetsFall17_nomPlusExt_SFpaths_OStaugenmatchPositive_%sTauMVAWP.root' % tauWP
            dataFileName = 'hales/fitOutput_Data_MuTau2017BCDEF_newFunction_%sWP%s_realTau.root' % (tauWP, wp)
            mcFileName = 'hales/fitOutput_MC_MuTau2017_DYJetsFall17_newFunction_%sWP%s_realTau.root' % (tauWP, wp)
            for hName, saveName in histMap.iteritems() :
                hData = getHist( dataFileName, hName, 'hist_'+saveName+'_'+tauWP+'Tau'+wpMap[wp]+'_DATA' )
                gData = getGraph( dataFileName, hName, 'graph_'+saveName+'_'+tauWP+'Tau'+wpMap[wp]+'_DATA' )
                print hData
                hMC = getHist( mcFileName, hName, 'hist_'+saveName+'_'+tauWP+'Tau'+wpMap[wp]+'_MC' )
                gMC = getGraph( mcFileName, hName, 'graph_'+saveName+'_'+tauWP+'Tau'+wpMap[wp]+'_MC' )
                print hMC
                oFile.cd()
                hData.Write()
                gData.Write()
                hMC.Write()
                gMC.Write()
        

