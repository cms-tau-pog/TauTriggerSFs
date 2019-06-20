



import ROOT
ROOT.gROOT.SetBatch(True)
import json
from array import array

# choose which year's eta-phi ROOT files to make!
year2017 = False
year2018 = False
year2016 = True
# "Average" : 0.5485,
# "NonPixelProblemBarrel" : 0.5570,
# "EndCap" : 0.5205,
# "PixelProblemBarrel" : 0.3589

def fillH2( trigger, wp, dm, sample, info_map, h2 ) :
    print "Filling: ",h2
    for x in range( 1, h2.GetXaxis().GetNbins()+1 ) :
        for y in range( 1, h2.GetYaxis().GetNbins()+1 ) :
            #print x,y
            if x == 1 or x == 6 : # beyond eta range, abs(eta)>2.1
                h2.SetBinContent( x, y, 0.0 )
            elif x == 2 or x == 5 : # end cap, 1.5<abs(eta)<2.1
                h2.SetBinContent( x, y, info_map[ trigger ][ sample ][ wp ][ dm ][ "EndCap" ] )
            elif x == 3 or (x == 4 and y != 2) : # barrel and not pixel probel region
                h2.SetBinContent( x, y, info_map[ trigger ][ sample ][ wp ][ dm ][ "NonPixelProblemBarrel" ] )
            elif x == 4 and y == 2 : # barrel pixel probel region
                h2.SetBinContent( x, y, info_map[ trigger ][ sample ][ wp ][ dm ][ "PixelProblemBarrel" ] )
            else :
                print "Didn't we cover all the values?",x,y

def fillH2_2018( trigger, wp, dm, sample, info_map, h2 ) :
    print "Filling: ",h2
    for x in range( 1, h2.GetXaxis().GetNbins()+1 ) :
        for y in range( 1, h2.GetYaxis().GetNbins()+1 ) :
            #print x,y
            if x == 1 or x == 6 : # beyond eta range, abs(eta)>2.1
                h2.SetBinContent( x, y, 0.0 )
            elif x == 2  and y == 2 : # end cap, broken HCAL modules region, 1.5< eta <2.1 and -1.6 < phi< -0.8
                h2.SetBinContent( x, y, info_map[ trigger ][ sample ][ wp ][ dm ][ "HCALProblemEndCap" ] )
            elif((x == 2  and y !=2) or x == 5) : # end cap rest
                h2.SetBinContent( x, y, info_map[ trigger ][ sample ][ wp ][ dm ][ "NonHCALProblemEndCap" ] )
            elif x == 3 or x == 4 : # barrel
                h2.SetBinContent( x, y, info_map[ trigger ][ sample ][ wp ][ dm ][ "Barrel" ] )
            else :
                print "Didn't we cover all the values?",x,y

def fillH2_2016( trigger, wp, dm, sample, info_map, h2 ) :
    print "Filling: ",h2
    for x in range( 1, h2.GetXaxis().GetNbins()+1 ) :
        for y in range( 1, h2.GetYaxis().GetNbins()+1 ) :
            if x == 1 or x == 3 : # beyond eta range, abs(eta)>2.1
                h2.SetBinContent( x, y, 0.0 )
            elif x == 2 : # the rest of the eta phi region, no eta phi separation applied for 2016
                h2.SetBinContent( x, y, info_map[ trigger ][ sample ][ wp ][ dm ][ "Average" ] )
            else :
                print "Didn't we cover all the values?",x,y

        
def fillAvgH2( trigger, wp, dm, sample, info_map, h2 ) :
    print "Filling: ",h2
    for x in range( 1, h2.GetXaxis().GetNbins()+1 ) :
        for y in range( 1, h2.GetYaxis().GetNbins()+1 ) :
            #print x,y
            if x == 1 or x == 3 : # beyond eta range, abs(eta)>2.1
                h2.SetBinContent( x, y, 0.0 )
            elif x == 2 : # abs(eta)<2.1
                h2.SetBinContent( x, y, info_map[ trigger ][ sample ][ wp ][ dm ][ "Average" ] )
            else :
                print "Didn't we cover all the values?",x,y


if(year2017):
	with open('data/tauTriggerEfficienciesEtaPhiMap2017_FINAL.json') as etaPhiInfo :
		info_map = json.load( etaPhiInfo )
elif(year2018):
	with open('data/tauTriggerEfficienciesEtaPhiMap2018_pre.json') as etaPhiInfo :
		info_map = json.load( etaPhiInfo )
elif(year2016):
        with open('data/tauTriggerEfficienciesEtaPhiMap2016_pre.json') as etaPhiInfo :
                info_map = json.load( etaPhiInfo )


print "Making Eta Phi Map"
#saveDir = '/afs/cern.ch/user/t/truggles/www/tau_fits_Feb13v2/'
#c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
#p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
#p.Draw()
#p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
#p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
#p.Draw()
if(year2017):
	oFile = ROOT.TFile( 'data/tauTriggerEfficienciesEtaPhi2017_FINAL.root', 'RECREATE' )
	oFile.cd()
elif(year2018):
	oFile = ROOT.TFile( 'data/tauTriggerEfficienciesEtaPhi2018_pre.root', 'RECREATE' )
	oFile.cd()
elif(year2016):
        oFile = ROOT.TFile( 'data/tauTriggerEfficienciesEtaPhi2016_pre.root', 'RECREATE' )
        oFile.cd()

xBinning = array('f', [-2.5, -2.1, -1.5, 0, 1.5, 2.1, 2.5] )
if(year2017):
	yBinning = array('f', [-3.2, 2.8, 3.2] )
elif(year2018):
	yBinning = array('f', [-3.2, -1.6, -0.8, 3.2] )
elif(year2016):
        yBinning = array('f', [-3.2, 3.2] )
        xBinning = array('f', [-2.5, -2.1, 2.1, 2.5] )

xBinningAvg = array('f', [-2.5, -2.1, 2.1, 2.5] )
yBinningAvg = array('f', [-3.2, 3.2] )

for trigger in ['ditau', 'etau', 'mutau'] :
    for wp in ['vvloose', 'vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight' ] :
        for dm in ['dm0', 'dm1', 'dm10', 'dmCmb'] :
            print trigger, wp, dm
            h_data = ROOT.TH2F( '%s_%sMVAv2_%s_DATA' % (trigger, wp, dm), '%s_%sMVAv2_%s_DATA;#tau #eta;#tau #phi;Efficiency' % (trigger, wp, dm), len(xBinning)-1, xBinning, len(yBinning)-1, yBinning) 
            h_mc = ROOT.TH2F( '%s_%sMVAv2_%s_MC' % (trigger, wp, dm), '%s_%sMVAv2_%s_MC;#tau #eta;#tau #phi;Efficiency' % (trigger, wp, dm), len(xBinning)-1, xBinning, len(yBinning)-1, yBinning) 

            h_data_avg = ROOT.TH2F( '%s_%sMVAv2_%s_DATA_AVG' % (trigger, wp, dm), '%s_%sMVAv2_%s_AVG_DATA;#tau #eta;#tau #phi;Efficiency' % (trigger, wp, dm), len(xBinningAvg)-1, xBinningAvg, len(yBinningAvg)-1, yBinningAvg) 
            h_mc_avg = ROOT.TH2F( '%s_%sMVAv2_%s_MC_AVG' % (trigger, wp, dm), '%s_%sMVAv2_%s_AVG_MC;#tau #eta;#tau #phi;Efficiency' % (trigger, wp, dm), len(xBinningAvg)-1, xBinningAvg, len(yBinningAvg)-1, yBinningAvg)

            if(year2017):
                fillH2( trigger, wp, dm, 'data', info_map, h_data )
                fillH2( trigger, wp, dm, 'mc', info_map, h_mc )
            elif(year2018):
                fillH2_2018( trigger, wp, dm, 'data', info_map, h_data )
                fillH2_2018( trigger, wp, dm, 'mc', info_map, h_mc )
            elif(year2016):
                fillH2_2016( trigger, wp, dm, 'data', info_map, h_data )
                fillH2_2016( trigger, wp, dm, 'mc', info_map, h_mc )
            fillAvgH2( trigger, wp, dm, 'data', info_map, h_data_avg )
            fillAvgH2( trigger, wp, dm, 'mc', info_map, h_mc_avg )


            oFile.cd()
            h_data.Write()
            h_mc.Write()
            h_data_avg.Write()
            h_mc_avg.Write()

            #p.cd()
            #h_data.Draw('COLZ TEXT')
            #c.SaveAs( saveDir+'%s_%s_%s_DM%s.png' % (trigger, wp, 'DATA', dm) )
            #h_mc.Draw('COLZ TEXT')
            #c.SaveAs( saveDir+'%s_%s_%s_DM%s.png' % (trigger, wp, 'MC', dm) )
            #h_data_avg.Draw('COLZ TEXT')
            #c.SaveAs( saveDir+'%s_%s_%s_DM%s_AVG.png' % (trigger, wp, 'DATA', dm) )
            #h_mc_avg.Draw('COLZ TEXT')
            #c.SaveAs( saveDir+'%s_%s_%s_DM%s_AVG.png' % (trigger, wp, 'MC', dm) )

