"""
Script to graph the eta / phi SFs from the standard Tau POG
efficiency ntuples. The current eta-phi mapping is based on
the region of noticed pixel problems where there were
Data / MC discrepancies in 2017.

The mapping will need to be updated for 2018.

Author: Tyler Ruggles
Date: 13 February 2019
"""

import ROOT
ROOT.gStyle.SetOptStat(0)
from array import array
ROOT.gROOT.SetBatch(True)
import json



def get_hist( name, tree, cut, weight, x_var, binning ) :
    h = ROOT.TH1D( name, "%s;%s" % (name, x_var), len(binning)-1, binning )
    t.Draw( "%s >> %s" % (x_var, name), "%s * %s" % (cut, weight) )
    h.SetDirectory(0)
    return h

def get_hist_2d( name, tree, cut, weight, x_var, y_var, xBinning, yBinning ) :
    h = ROOT.TH2D( name, "%s;%s;%s" % (name, x_var, y_var), \
        len(xBinning)-1, xBinning, len(yBinning)-1, yBinning )
    t.Draw( "%s:%s >> %s" % (y_var, x_var, name), "%s * %s" % (cut, weight) )
    h.SetDirectory(0)
    return h

def printJson( to_dump ) :
    with open('efficiencies.json', 'w') as outFile :
        json.dump( to_dump, outFile, indent=2 )
        outFile.close()

def get_trigger_map( wp ) :

    trigger_map = {
        'eTau' : {
            'data' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_Data_Run2017BCDEF_31Mar2018_SSsubtraction_%sWP2017v2.root" % wp,
            'mc' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_DYJetsToLL_12Apr2018_v1Andext1v1_12062018_puWeightsANDtauEScorrectionIncluded_OStauGenMatched_%sWP2017v2.root" % wp,
            'ptThreshold' : 35,
            'accept' : 'hasHLTetau_Path_13',
        },
        #'muTau' : {
        #    'data' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_Data_Run2017BCDEF_31Mar2018_SSsubtraction_%sWP2017v2.root" % wp,
        #    'mc' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_DYJetsToLL_12Apr2018_v1Andext1v1_12062018_puWeightsANDtauEScorrectionIncluded_OStauGenMatched_%sWP2017v2.root" % wp,
        #    #'data' : "...%sWP2017v2.root" % wp,
        #    #'mc' : "..._%sWP2017v2.root" % wp,
        #    'ptThreshold' : 32,
        #    'accept' : 'hasHLTmutau_Path_13',
        #},
        'diTau' : {
            'data' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_Data_Run2017BCDEF_31Mar2018_SSsubtraction_%sWP2017v2.root" % wp,
            'mc' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_DYJetsToLL_12Apr2018_v1Andext1v1_12062018_puWeightsANDtauEScorrectionIncluded_OStauGenMatched_%sWP2017v2.root" % wp,
            'ptThreshold' : 40,
            'accept' : 'hasHLTditauPath_9or10or11',
        },
    }

    return trigger_map

saveDir = '/afs/cern.ch/user/t/truggles/www/tau_fits_Feb13v1/'

x_var = "tauPt"
x_var = "tauEta"
y_var = "tauPhi"
weight = "bkgSubW"
wp = "VVLoose"
trigger_map = get_trigger_map( wp )


# For visualization
xBinning = array('f', [-2.3, -2.1, -1.5, 0, 1.5, 2.1, 2.3] )
yBinning = array('f', [-3.2, 2.8, 3.2] )

# For computing json file
xBinning = array('f', [-2.3, 2.3] )
yBinning = array('f', [-3.2, 3.2] )

eta_phi_regions = {
    'Average' : '(1.)',
    'EndCap' : '(abs(tauEta) > 1.5)',
    'NonPixelProblemBarrel' : '(abs(tauEta) < 1.5 && (tauPhi < 2.8 || tauEta <= 0))',
    'PixelProblemBarrel' : '(tauEta > 0 && tauEta < 1.5 && tauPhi > 2.8)',
}

all_info = {}

for trigger in trigger_map.keys() :

    accept = trigger_map[ trigger ]['accept']
    
    all_info[ trigger ] = {}
        
    c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()
    p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
    p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
    p.Draw()
    p.cd()

    # FIXME once we have more files or now how to access this
    # we need a loop here. Are multiple WPs stored in the same file?
    # Or do we need to open a new file for each?
    #for wp in wpList :
    
    for sample in ['data', 'mc'] :

        all_info[ trigger ][ sample ] = {}

        f = ROOT.TFile( trigger_map[ trigger ][ sample ], 'r' )
        print trigger, sample, f
        t = f.Get("TagAndProbe")


        for region, etaPhiCut in eta_phi_regions.iteritems() :
    

            h_sample_pass = get_hist_2d( 'h_%s_%s_pass' % (trigger, sample), t, \
                    "(%s==1 && tauPt > %i && %s)" % (accept, trigger_map[ trigger ]['ptThreshold'], etaPhiCut), \
                    "(%s)" % weight, x_var, y_var, xBinning, yBinning )

            h_sample_total = get_hist_2d( 'h_%s_%s_total' % (trigger, sample), t, \
                    "(tauPt > %i && %s)" % (trigger_map[ trigger ]['ptThreshold'], etaPhiCut), \
                    "(%s)" % weight, x_var, y_var, xBinning, yBinning )
            
            h_efficiency = h_sample_pass.Clone()
            h_efficiency.Divide( h_sample_total )
            #h_efficiency.Draw('COLZ TEXT')
            h_efficiency.Draw('COLZ')
            h_efficiency.GetZaxis().SetRangeUser(0, 1.1)

            # Add to info_map
            all_info[ trigger ][ sample ][ region ] = round( h_efficiency.GetBinContent( h_efficiency.FindBin( 0., 0. ) ), 3 )

            #c.SaveAs( saveDir+'%s_%s_%s_%s.png' % (trigger, wp, sample, region) )
        
            del h_sample_pass, h_sample_total, h_efficiency
        
printJson( all_info )



