

'''
Class to get Tau Trigger SF based on 2017 Rereco data
and MCv2 (non-re-miniaod).

T. Ruggles
5 February, 2018
'''


import ROOT
import json

class getTauTriggerSFs :
    

    def __init__( self, tauMVAWP='medium' ):

        # Default to loading the Tau MVA Medium ID based WPs
        self.tauMVAWP = tauMVAWP
        assert( self.tauMVAWP in ['medium', 'tight', 'vtight'] ), "You must choose a WP from: medium, tight, or vtight (vloose and loose possibly coming with re-miniaod)"
        print "Loading Efficiencies for Tau MVA ID WP ", self.tauMVAWP

        # Load the TH1s containing the bin by bin values
        self.f = ROOT.TFile( 'data/tauTriggerEfficiencies2017.root', 'r' )
        self.diTauData = self.f.Get('hist_diTauTriggerEfficiency_%sTauMVA_DATA' % self.tauMVAWP )
        self.diTauMC = self.f.Get('hist_diTauTriggerEfficiency_%sTauMVA_MC' % self.tauMVAWP )
        self.eTauData = self.f.Get('hist_ETauTriggerEfficiency_%sTauMVA_DATA' % self.tauMVAWP )
        self.eTauMC = self.f.Get('hist_ETauTriggerEfficiency_%sTauMVA_MC' % self.tauMVAWP )
        self.muTauData = self.f.Get('hist_MuTauTriggerEfficiency_%sTauMVA_DATA' % self.tauMVAWP )
        self.muTauMC = self.f.Get('hist_MuTauTriggerEfficiency_%sTauMVA_MC' % self.tauMVAWP )
        
        with open('data/tauTriggerEfficienciesEtaPhiMap2017.json') as etaPhiSFs :
            self.etaPhiMap = json.load( etaPhiSFs )


    # This is the SF for a single leg of the di-tau trigger
    def getDiTauScaleFactor( self, pt, eta, phi ) :
        # Make sure we stay on our histograms
        if pt > 499 : pt = 499
        elif pt < 20 : pt = 21
        effData = self.diTauData.GetBinContent( self.diTauData.FindBin( pt ) )
        effMC = self.diTauMC.GetBinContent( self.diTauMC.FindBin( pt ) )
        if effMC <= 0.0 : print "Eff MC too low. Value is ",effMC," this is a problem"
        sf = effData / max(effMC, 1e-5)

        # Adjust SF based on (eta, phi) location
        sf *= self.getEtaPhiSF( eta, phi, 'diTau' )
        return sf

    # This is the SF for the tau leg of the e-tau trigger
    def getETauScaleFactor( self, pt, eta, phi ) :
        # Make sure we stay on our histograms
        if pt > 499 : pt = 499
        elif pt < 20 : pt = 21
        effData = self.eTauData.GetBinContent( self.eTauData.FindBin( pt ) )
        effMC = self.eTauMC.GetBinContent( self.eTauMC.FindBin( pt ) )
        if effMC <= 0.0 : print "Eff MC too low. Value is ",effMC," this is a problem"
        sf = effData / max(effMC, 1e-5)

        # Adjust SF based on (eta, phi) location
        sf *= self.getEtaPhiSF( eta, phi, 'eTau' )
        return sf

    # This is the SF for the tau leg of the mu-tau trigger
    def getMuTauScaleFactor( self, pt, eta, phi ) :
        # Make sure we stay on our histograms
        if pt > 499 : pt = 499
        elif pt < 20 : pt = 21
        effData = self.muTauData.GetBinContent( self.muTauData.FindBin( pt ) )
        effMC = self.muTauMC.GetBinContent( self.muTauMC.FindBin( pt ) )
        if effMC <= 0.0 : print "Eff MC too low. Value is ",effMC," this is a problem"
        sf = effData / max(effMC, 1e-5)

        # Adjust SF based on (eta, phi) location
        sf *= self.getEtaPhiSF( eta, phi, 'muTau' )
        return sf

    def getEtaPhiSF( self, eta, phi, trigger ) :
        avg = self.etaPhiMap[ trigger ][ self.tauMVAWP ][ "Average" ]
        if abs(eta) > 1.479 : # End cap
            return self.etaPhiMap[ trigger ][ self.tauMVAWP ][ "EndCap" ] / avg
        if eta > 0 and phi > 2.8 : # Dead pixel module region
            return self.etaPhiMap[ trigger ][ self.tauMVAWP ][ "PixelProblemBarrel" ] / avg
        else : # Rest of Barrel
            return self.etaPhiMap[ trigger ][ self.tauMVAWP ][ "NonPixelProblemBarrel" ] / avg
        
        
