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
        #yErrors.append( sqrt(yEPlus**2 + yEMin**2) )
        yErrors.append(max(yEPlus, yEMin))
    # Don't forget to add the high end of last bin
    xSpacing.append( x+xEPlus )

    outH = ROOT.TH1F( name, name, len(xSpacing)-1, xSpacing )
    for bin in range( 1, outH.GetNbinsX()+1 ) :
        outH.SetBinContent( bin, yVals[bin-1] )
        outH.SetBinError( bin, yErrors[bin-1] )
    return outH


def getHistFromGraph( f, hName, saveName ) :
   # f = ROOT.TFile( 'data/'+fName, 'r' )
    graph = f.Get( hName )
    h = getTH1FfromTGraphAsymmErrors( graph, saveName )
    h.SetDirectory( 0 )
    return h


def getGraph( f, gName, saveName ) :
    graph = f.Get( gName )
    graph.SetName( saveName )
    graph.SetTitle( saveName )
    return graph


def getHist( f, hName, saveName ) :
    hist = f.Get( hName )
    hist.SetName( saveName )
    hist.SetTitle( saveName )
    hist.SetDirectory( 0 )
    return hist


def getFit( f, fName, saveName ) :
    fit = f.Get( fName )
    fit.SetName( saveName )
    fit.SetTitle( saveName )
    return fit


