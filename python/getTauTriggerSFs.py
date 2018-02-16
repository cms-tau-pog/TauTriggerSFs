

'''
Class to get Tau Trigger SF based on 2017 Rereco data
and MCv2 (non-re-miniaod).

T. Ruggles
5 February, 2018
'''


import ROOT

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
        
        # Load the TH2s containing the eta phi efficiency corrections
        self.diTauEtaPhiData = self.f.Get('diTau_%s_DATA' % self.tauMVAWP )
        self.diTauEtaPhiMC = self.f.Get('diTau_%s_MC' % self.tauMVAWP )
        self.eTauEtaPhiData = self.f.Get('eTau_%s_DATA' % self.tauMVAWP )
        self.eTauEtaPhiMC = self.f.Get('eTau_%s_MC' % self.tauMVAWP )
        self.muTauEtaPhiData = self.f.Get('muTau_%s_DATA' % self.tauMVAWP )
        self.muTauEtaPhiMC = self.f.Get('muTau_%s_MC' % self.tauMVAWP )

        # Eta Phi Avg
        self.diTauEtaPhiAvgData = self.f.Get('diTau_%s_AVG_DATA' % self.tauMVAWP )
        self.diTauEtaPhiAvgMC = self.f.Get('diTau_%s_AVG_MC' % self.tauMVAWP )
        self.eTauEtaPhiAvgData = self.f.Get('eTau_%s_AVG_DATA' % self.tauMVAWP )
        self.eTauEtaPhiAvgMC = self.f.Get('eTau_%s_AVG_MC' % self.tauMVAWP )
        self.muTauEtaPhiAvgData = self.f.Get('muTau_%s_AVG_DATA' % self.tauMVAWP )
        self.muTauEtaPhiAvgMC = self.f.Get('muTau_%s_AVG_MC' % self.tauMVAWP )


    # Make sure we stay on our histograms
    def ptCheck( self, pt ) :
        if pt > 499 : pt = 499
        elif pt < 20 : pt = 21
        return pt

    def getEfficiency( self, pt, eta, phi, effHist, etaPhi, etaPhiAvg ) :
        pt = self.ptCheck( pt )
        eff = effHist.GetBinContent( effHist.FindBin( pt ) )

        # Adjust SF based on (eta, phi) location
        # keep eta barrel boundaries within SF region
        # but, for taus outside eta limits or with unralistic
        # phi values, return zero SF
        if eta == 2.1 : eta = 2.09
        elif eta == -2.1 : eta = -2.09

        etaPhiVal = etaPhi.GetBinContent( etaPhi.FindBin( eta, phi ) )
        etaPhiAvg = etaPhiAvg.GetBinContent( etaPhiAvg.FindBin( eta, phi ) )
        if etaPhiAvg <= 0.0 :
            print "One of the provided tau (eta, phi) values (%3.3f, %3.3f) is outside the boundary of triggering taus" % (eta, phi)
            print "Returning efficiency = 0.0"
            return 0.0
        eff *= etaPhiVal / etaPhiAvg
        if eff > 1. : eff = 1
        return eff


    # This is the efficiency for a single leg of the di-tau trigger
    def getDiTauEfficiencyData( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.diTauData, self.diTauEtaPhiData, self.diTauEtaPhiAvgData )


    # This is the efficiency for a single leg of the di-tau trigger
    def getDiTauEfficiencyMC( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.diTauMC, self.diTauEtaPhiMC, self.diTauEtaPhiAvgMC )


    # This is the SF for a single leg of the di-tau trigger
    def getDiTauScaleFactor( self, pt, eta, phi ) :
        pt = self.ptCheck( pt )
        effData = self.getDiTauEfficiencyData( pt, eta, phi )
        effMC = self.getDiTauEfficiencyMC( pt, eta, phi )
        if effMC < 1e-5 :
            print "Eff MC is suspiciously low. Please contact Tau POG."
            print " - DiTau Trigger SF for Tau MVA: %s   pT: %f   eta: %s   phi: %f" % (self.tauMVAWP, pt, eta, phi)
            print " - MC Efficiency = %f" % effMC
            return 0.0
        sf = effData / effMC
        return sf


    # This is the efficiency for the tau leg of the mu-tau trigger
    def getMuTauEfficiencyData( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.muTauData, self.muTauEtaPhiData, self.muTauEtaPhiAvgData )


    # This is the efficiency for the tau leg of the mu-tau trigger
    def getMuTauEfficiencyMC( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.muTauMC, self.muTauEtaPhiMC, self.muTauEtaPhiAvgMC )


    # This is the SF for the tau leg of the mu-tau trigger
    def getMuTauScaleFactor( self, pt, eta, phi ) :
        pt = self.ptCheck( pt )
        effData = self.getMuTauEfficiencyData( pt, eta, phi )
        effMC = self.getMuTauEfficiencyMC( pt, eta, phi )
        if effMC < 1e-5 :
            print "Eff MC is suspiciously low. Please contact Tau POG."
            print " - MuTau Trigger SF for Tau MVA: %s   pT: %f   eta: %s   phi: %f" % (self.tauMVAWP, pt, eta, phi)
            print " - MC Efficiency = %f" % effMC
            return 0.0
        sf = effData / effMC
        return sf



    # This is the efficiency for the tau leg of the e-tau trigger
    def getETauEfficiencyData( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.eTauData, self.eTauEtaPhiData, self.eTauEtaPhiAvgData )


    # This is the efficiency for the tau leg of the e-tau trigger
    def getETauEfficiencyMC( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.eTauMC, self.eTauEtaPhiMC, self.eTauEtaPhiAvgMC )


    # This is the SF for the tau leg of the e-tau trigger
    def getETauScaleFactor( self, pt, eta, phi ) :
        pt = self.ptCheck( pt )
        effData = self.getETauEfficiencyData( pt, eta, phi )
        effMC = self.getETauEfficiencyMC( pt, eta, phi )
        if effMC < 1e-5 :
            print "Eff MC is suspiciously low. Please contact Tau POG."
            print " - ETau Trigger SF for Tau MVA: %s   pT: %f   eta: %s   phi: %f" % (self.tauMVAWP, pt, eta, phi)
            print " - MC Efficiency = %f" % effMC
            return 0.0
        sf = effData / effMC
        return sf


