



import ROOT
import json
from array import array

# "Average" : 0.5485,
# "NonPixelProblemBarrel" : 0.5570,
# "EndCap" : 0.5205,
# "PixelProblemBarrel" : 0.3589

def fillH2( trigger, wp, info_map, h2 ) :
    print "Filling: ",h2
    for x in range( 1, h2.GetXaxis().GetNbins()+1 ) :
        for y in range( 1, h2.GetYaxis().GetNbins()+1 ) :
            #print x,y
            if x == 1 or x == 6 : # beyond eta range, abs(eta)>2.1
                h2.SetBinContent( x, y, 0.0 )
            elif x == 2 or x == 5 : # end cap, 1.5<abs(eta)<2.1
                h2.SetBinContent( x, y, info_map[ trigger ][ wp ][ "EndCap" ] )
            elif x == 3 or (x == 4 and y != 2) : # barrel and not pixel probel region
                h2.SetBinContent( x, y, info_map[ trigger ][ wp ][ "NonPixelProblemBarrel" ] )
            elif x == 4 and y == 2 : # barrel pixel probel region
                h2.SetBinContent( x, y, info_map[ trigger ][ wp ][ "PixelProblemBarrel" ] )
            else :
                print "Didn't we cover all the values?",x,y
        
def fillAvgH2( trigger, wp, info_map, h2 ) :
    print "Filling: ",h2
    for x in range( 1, h2.GetXaxis().GetNbins()+1 ) :
        for y in range( 1, h2.GetYaxis().GetNbins()+1 ) :
            #print x,y
            if x == 1 or x == 3 : # beyond eta range, abs(eta)>2.1
                h2.SetBinContent( x, y, 0.0 )
            elif x == 2 : # abs(eta)<2.1
                h2.SetBinContent( x, y, info_map[ trigger ][ wp ][ "Average" ] )
            else :
                print "Didn't we cover all the values?",x,y



with open('data/tauTriggerEfficienciesEtaPhiMap2017_DATA.json') as etaPhiDATA :
    data_map = json.load( etaPhiDATA )

with open('data/tauTriggerEfficienciesEtaPhiMap2017_MC.json') as etaPhiMC :
    mc_map = json.load( etaPhiMC )

print "Making Eta Phi Map"

oFile = ROOT.TFile( 'data/tauTriggerEfficienciesEtaPhi2017.root', 'RECREATE' )
oFile.cd()

xBinning = array('f', [-2.5, -2.1, -1.5, 0, 1.5, 2.1, 2.5] )
yBinning = array('f', [-3.2, 2.8, 3.2] )
xBinningAvg = array('f', [-2.5, -2.1, 2.1, 2.5] )
yBinningAvg = array('f', [-3.2, 3.2] )

for wp in ['medium', 'tight', 'vtight' ] :
    for trigger in ['diTau', 'eTau', 'muTau'] :
        print trigger, wp
        h_data = ROOT.TH2F( '%s_%s_DATA' % (trigger, wp), '%s_%s_DATA;#tau #eta;#tau #phi;Efficiency' % (trigger, wp), len(xBinning)-1, xBinning, len(yBinning)-1, yBinning) 
        h_mc = ROOT.TH2F( '%s_%s_MC' % (trigger, wp), '%s_%s_MC;#tau #eta;#tau #phi;Efficiency' % (trigger, wp), len(xBinning)-1, xBinning, len(yBinning)-1, yBinning) 
        h_sf = ROOT.TH2F( '%s_%s_SF' % (trigger, wp), '%s_%s_SF;#tau #eta;#tau #phi;Efficiency' % (trigger, wp), len(xBinning)-1, xBinning, len(yBinning)-1, yBinning) 

        h_data_avg = ROOT.TH2F( '%s_%s_AVG_DATA' % (trigger, wp), '%s_%s_AVG_DATA;#tau #eta;#tau #phi;Efficiency' % (trigger, wp), len(xBinningAvg)-1, xBinningAvg, len(yBinningAvg)-1, yBinningAvg) 
        h_mc_avg = ROOT.TH2F( '%s_%s_AVG_MC' % (trigger, wp), '%s_%s_AVG_MC;#tau #eta;#tau #phi;Efficiency' % (trigger, wp), len(xBinningAvg)-1, xBinningAvg, len(yBinningAvg)-1, yBinningAvg) 
        h_sf_avg = ROOT.TH2F( '%s_%s_AVG_SF' % (trigger, wp), '%s_%s_AVG_SF;#tau #eta;#tau #phi;Efficiency' % (trigger, wp), len(xBinningAvg)-1, xBinningAvg, len(yBinningAvg)-1, yBinningAvg) 

        fillH2( trigger, wp, data_map, h_data )
        fillH2( trigger, wp, mc_map, h_mc )
        h_sf.Add( h_data )
        h_sf.Divide( h_mc )

        fillAvgH2( trigger, wp, data_map, h_data_avg )
        fillAvgH2( trigger, wp, mc_map, h_mc_avg )
        h_sf_avg.Add( h_data_avg )
        h_sf_avg.Divide( h_mc_avg )


        oFile.cd()
        h_data.Write()
        h_mc.Write()
        h_sf.Write()
        h_data_avg.Write()
        h_mc_avg.Write()
        h_sf_avg.Write()


