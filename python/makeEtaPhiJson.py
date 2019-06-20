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
#ROOT.gStyle.SetOptStat(0)
from array import array
#ROOT.gROOT.SetBatch(True)
import json

# choose which year's eta-phi JSON files to make!
year2017 = False
year2018 = False
year2016 = True

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
	if(year2017):
            with open('data/tauTriggerEfficienciesEtaPhiMap2017_FINAL.json', 'w') as outFile :
                json.dump( to_dump, outFile, indent=2 )
                outFile.close()
        elif(year2018):
            with open('data/tauTriggerEfficienciesEtaPhiMap2018_pre.json', 'w') as outFile :
                json.dump( to_dump, outFile, indent=2 )
                outFile.close()
        elif(year2016):
            with open('data/tauTriggerEfficienciesEtaPhiMap2016_pre.json', 'w') as outFile :
                json.dump( to_dump, outFile, indent=2 )
                outFile.close()

def get_2017trigger_map() :

    # It turns out all triggers are measured from the same 2 files
    trigger_map = {
        'etau' : {
            'data' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_Data_Run2017BCDEF_31Mar2018_SSsubtraction_VVLooseWP2017v2.root",
            'mc' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_DYJetsToLL_12Apr2018_v1Andext1v1_12062018_puWeightsANDtauEScorrectionIncluded_OStauGenMatched_VVLooseWP2017v2.root",
            'ptThreshold' : 35,
            'accept' : 'hasHLTetau_Path_13',
        },
        'mutau' : {
            'data' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_Data_Run2017BCDEF_31Mar2018_SSsubtraction_VVLooseWP2017v2.root",
            'mc' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_DYJetsToLL_12Apr2018_v1Andext1v1_12062018_puWeightsANDtauEScorrectionIncluded_OStauGenMatched_VVLooseWP2017v2.root",
            'ptThreshold' : 32,
            'accept' : 'hasHLTmutauPath_13',
        },
        'ditau' : {
            'data' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_Data_Run2017BCDEF_31Mar2018_SSsubtraction_VVLooseWP2017v2.root",
            'mc' : "/afs/cern.ch/user/h/hsert/public/Fall17Samples_31MarData_12AprMC/NTuple_DYJetsToLL_12Apr2018_v1Andext1v1_12062018_puWeightsANDtauEScorrectionIncluded_OStauGenMatched_VVLooseWP2017v2.root",
            'ptThreshold' : 40,
            'accept' : 'hasHLTditauPath_9or10or11',
        },
    }

    return trigger_map

def get_2018trigger_map() :

    # It turns out all triggers are measured from the same 2 files
    trigger_map = {
        'etau' : {
            'data' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_SingleMuon_Run2018ABCDReReco17SepPromptRecoD_190121_SSsubtraction_VVLooseWP2017v2_forFit_260419.root",
            'mc' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_DYJetsToLL_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_190121_PUreweight1000MCbin_OStauGenMatched_VVLooseWP2017v2_forFit_260419.root",
            'ptThreshold' : 35,
            'accept' : 'hasHLTetauPath_8and14',
        },
        'mutau' : {
             'data' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_SingleMuon_Run2018ABCDReReco17SepPromptRecoD_190121_SSsubtraction_VVLooseWP2017v2_forFit_260419.root",
            'mc' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_DYJetsToLL_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_190121_PUreweight1000MCbin_OStauGenMatched_VVLooseWP2017v2_forFit_260419.root",
            'ptThreshold' : 32,
            'accept' : 'hasHLTmutauPath_8and14',
        },
        'ditau' : {
            'data' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_SingleMuon_Run2018ABCDReReco17SepPromptRecoD_190121_SSsubtraction_VVLooseWP2017v2_forFit_260419.root",
            'mc' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_DYJetsToLL_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_190121_PUreweight1000MCbin_OStauGenMatched_VVLooseWP2017v2_forFit_260419.root",
            'ptThreshold' : 40,
            'accept' : 'hasHLTditauPath_4or5or6and15or20',
        },
    }

    return trigger_map

def get_2016trigger_map() :

    trigger_map = {
        'etau' : {
            'data' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_SingleMuon_Run2016BtoH-17Jul2018_190228_SSsubtraction_VVLooseWP2017v2_forFit_270519.root",
            'mc' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_DYJets_RunIISummer16MiniAODv3_94X_mcRun2_ext1ANDext2-v2_190306_PUreweight_OStauGenMatched_VVLooseWP2017v2_forFit_270519.root",
            'ptThreshold' : 25,
            'accept' : 'hasHLTetauPath_0and1',
        },
        'mutau' : {
             'data' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_SingleMuon_Run2016BtoH-17Jul2018_190228_SSsubtraction_VVLooseWP2017v2_forFit_270519.root",
            'mc' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_DYJets_RunIISummer16MiniAODv3_94X_mcRun2_ext1ANDext2-v2_190306_PUreweight_OStauGenMatched_VVLooseWP2017v2_forFit_270519.root",
            'ptThreshold' : 25,
            'accept' : 'hasHLTmutauPath_0',
        },
        'ditau' : {
            'data' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_SingleMuon_Run2016BtoH-17Jul2018_190228_SSsubtraction_VVLooseWP2017v2_forFit_270519.root",
            'mc' : "/afs/cern.ch/user/h/hsert/public/Run2SamplesTrigger/Ntuple_DYJets_RunIISummer16MiniAODv3_94X_mcRun2_ext1ANDext2-v2_190306_PUreweight_OStauGenMatched_VVLooseWP2017v2_forFit_270519.root",
            'ptThreshold' : 40,
            'accept' : 'hasHLTditauPath_3or4',
        },
    }

    return trigger_map

wp_map = {
    'vvtight' : 'byVVTightIsolationMVArun2017v2DBoldDMwLT2017',
    'vtight' : 'byVTightIsolationMVArun2017v2DBoldDMwLT2017',
    'tight' : 'byTightIsolationMVArun2017v2DBoldDMwLT2017',
    'medium' : 'byMediumIsolationMVArun2017v2DBoldDMwLT2017',
    'loose' : 'byLooseIsolationMVArun2017v2DBoldDMwLT2017',
    'vloose' : 'byVLooseIsolationMVArun2017v2DBoldDMwLT2017',
    'vvloose' : 'byVVLooseIsolationMVArun2017v2DBoldDMwLT2017', # Not supporting the VVLoose WP
}


saveDir = '../../../tau_fits2016_18June19/'

x_var = "tauPt"
x_var = "tauEta"
y_var = "tauPhi"
weight = "bkgSubW"

if(year2017):
	trigger_map = get_2017trigger_map()
elif(year2018):
	trigger_map = get_2018trigger_map()
elif(year2016):
        trigger_map = get_2016trigger_map()

# For visualization
#xBinning = array('f', [] )
#yBinning = array('f', [] )
#for i in range( -23, 24 ) :
#    xBinning.append( i/10. )
#for i in range( -32, 33 ) :
#    yBinning.append( i/10. )
    

# For computing json file
xBinning = array('f', [-2.3, 2.3] )
yBinning = array('f', [-3.2, 3.2] )

eta_phi_regions_2017 = {
    'Average' : '(1.)',
    'EndCap' : '(abs(tauEta) > 1.5)',
    'NonPixelProblemBarrel' : '(abs(tauEta) < 1.5 && (tauPhi < 2.8 || tauEta <= 0))',
    'PixelProblemBarrel' : '(tauEta > 0 && tauEta < 1.5 && tauPhi > 2.8)',
}

eta_phi_regions_2018 = {
    'Average' : '(1.)',
    'Barrel' : '(tauEta > -1.5  && tauEta < 1.5)',
    'NonHCALProblemEndCap' : '(((tauEta > -2.1 && tauEta < -1.5) && (tauPhi > -3.2  && tauPhi < -1.6)) || ((tauEta > -2.1 && tauEta < -1.5) &&  (tauPhi > -0.8  && tauPhi < 3.2)) || ( tauEta > 1.5 && tauEta < 2.1))',
    'HCALProblemEndCap' : '( (tauEta > -2.1 && tauEta < -1.5) &&  (tauPhi >-1.6 && tauPhi < -0.8) )',
}

eta_phi_regions_2016 = {
    'Average' : '(1.)',
    'Barrel' : '(1.)',
    'EndCap' : '(1.)',
}

if(year2017):
	eta_phi_regions = eta_phi_regions_2017
elif(year2018):
	eta_phi_regions = eta_phi_regions_2018
elif(year2016):
        eta_phi_regions = eta_phi_regions_2016
dm_map = {
    'dm0' : 'tauDM == 0',
    'dm1' : 'tauDM == 1',
    'dm10' : 'tauDM == 10',
    'dmCmb' : 'tauDM > -1',
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

    for sample in ['data', 'mc'] :

        all_info[ trigger ][ sample ] = {}

        f = ROOT.TFile( trigger_map[ trigger ][ sample ], 'r' )
        print trigger, sample, f
        t = f.Get("TagAndProbe")

        for wp, wp_long in wp_map.iteritems() :
    
            all_info[ trigger ][ sample ][ wp ] = {}

            for dm, dm_cut in dm_map.iteritems() :

                all_info[ trigger ][ sample ][ wp ][ dm ] = {}

                for region, etaPhiCut in eta_phi_regions.iteritems() :
    

                    h_sample_pass = get_hist_2d( 'h_%s_%s_pass' % (trigger, sample), t, \
                            "(%s==1 && tauPt > %i && %s && %s > 0.5 && %s)" % (accept, \
                            trigger_map[ trigger ]['ptThreshold'], etaPhiCut, wp_long, dm_cut), \
                            "(%s)" % weight, x_var, y_var, xBinning, yBinning )

                    h_sample_total = get_hist_2d( 'h_%s_%s_total' % (trigger, sample), t, \
                            "(tauPt > %i && %s && %s > 0.5 && %s)" % \
                            (trigger_map[ trigger ]['ptThreshold'], etaPhiCut, wp_long, dm_cut), \
                            "(%s)" % weight, x_var, y_var, xBinning, yBinning )
                    
                    h_efficiency = h_sample_pass.Clone()
                    h_efficiency.Divide( h_sample_total )
                    #h_efficiency.Draw('COLZ TEXT')
                    h_efficiency.Draw('COLZ')
                    h_efficiency.GetZaxis().SetRangeUser(-1.1, 1.1)

                    # Add to info_map
                    all_info[ trigger ][ sample ][ wp ][ dm ][ region ] = \
                        round( h_efficiency.GetBinContent( h_efficiency.FindBin( 0., 0. ) ), 3 )

                    #c.SaveAs( saveDir+'%s_%s_%s_DM%s_%s.png' % (trigger, wp, sample, dm, region) )
                
                    del h_sample_pass, h_sample_total, h_efficiency
        
printJson( all_info )



