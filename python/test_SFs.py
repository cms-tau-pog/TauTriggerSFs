import ROOT
ROOT.gROOT.SetBatch(True)
from TauAnalysisTools.TauTriggerSFs.getTauTriggerSFs import getTauTriggerSFs
from array import array


# choose which year's eta-phi files to make!
year2017 = False
year2018 = False
year2016 = True

def build_legend( graphs ) :
    legend = ROOT.TLegend(0.50, 0.7, 0.90, 0.9)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for g in graphs :
        legend.AddEntry( g, g.GetTitle(), 'l')
    return legend
    

def make_plots( tauSFs, target_type = 'ditau', dm=0 ) :

    wp = 'MVAv2'

    if target_type == 'ditau' :
        min_ = 20
        name = 'Di-Tau'
    if target_type == 'etau' :
        min_ = 20
        name = 'E-Tau'
    if target_type == 'mutau' :
        min_ = 20
        name = 'Mu-Tau'

    pts = array('d', [])
    sfs = array('d', [])
    sfsA = array('d', [])
    sfsB = array('d', [])
    sfs2 = array('d', [])
    sfs2A = array('d', [])
    sfs2B = array('d', [])
    sfs3 = array('d', [])
    sfs3A = array('d', [])
    sfs3B = array('d', [])

    for pt in range( min_, 200 ) :
        if(year2017):
            pts.append( pt )
            sfs.append( tauSFs.getTriggerScaleFactor( pt, 0.0, 0.0, dm ) )
            sfsA.append( tauSFs.getTriggerScaleFactorUncert( pt, 0.0, 0.0, dm, 'Up' ) )
            sfsB.append( tauSFs.getTriggerScaleFactorUncert( pt, 0.0, 0.0, dm, 'Down' ) )
            sfs2.append( tauSFs.getTriggerScaleFactor( pt, 2.0, 0.0, dm ) )
            sfs2A.append( tauSFs.getTriggerScaleFactorUncert( pt, 2.0, 0.0, dm, 'Up' ) )
            sfs2B.append( tauSFs.getTriggerScaleFactorUncert( pt, 2.0, 0.0, dm, 'Down' ) )
            sfs3.append( tauSFs.getTriggerScaleFactor( pt, 1.0, 2.9, dm ) )
            sfs3A.append( tauSFs.getTriggerScaleFactorUncert( pt, 1.0, 2.9, dm, 'Up' ) )
            sfs3B.append( tauSFs.getTriggerScaleFactorUncert( pt, 1.0, 2.9, dm, 'Down' ) )
        elif(year2018 or year2016):
            pts.append( pt )
            sfs.append( tauSFs.getTriggerScaleFactor( pt, 0.0, 0.0, dm ) )
            sfsA.append( tauSFs.getTriggerScaleFactorUncert( pt, 0.0, 0.0, dm, 'Up' ) )
            sfsB.append( tauSFs.getTriggerScaleFactorUncert( pt, 0.0, 0.0, dm, 'Down' ) )
            sfs2.append( tauSFs.getTriggerScaleFactor( pt, 2.0, 0.0, dm ) )
            sfs2A.append( tauSFs.getTriggerScaleFactorUncert( pt, 2.0, 0.0, dm, 'Up' ) )
            sfs2B.append( tauSFs.getTriggerScaleFactorUncert( pt, 2.0, 0.0, dm, 'Down' ) )
            sfs3.append( tauSFs.getTriggerScaleFactor( pt, -2.0, -1.5, dm ) )
            sfs3A.append( tauSFs.getTriggerScaleFactorUncert( pt, -2.0, -1.5, dm, 'Up' ) )
            sfs3B.append( tauSFs.getTriggerScaleFactorUncert( pt, -2.0, -1.5, dm, 'Down' ) )

    g = ROOT.TGraph( len(pts), pts, sfs )
    gA = ROOT.TGraph( len(pts), pts, sfsA )
    gB = ROOT.TGraph( len(pts), pts, sfsB )
    g2 = ROOT.TGraph( len(pts), pts, sfs2 )
    g2A = ROOT.TGraph( len(pts), pts, sfs2A )
    g2B = ROOT.TGraph( len(pts), pts, sfs2B )
    g3 = ROOT.TGraph( len(pts), pts, sfs3 )
    g3A = ROOT.TGraph( len(pts), pts, sfs3A )
    g3B = ROOT.TGraph( len(pts), pts, sfs3B )
    g.SetLineWidth( 2 )
    g2.SetLineWidth( 2 )
    g3.SetLineWidth( 2 )
    if(year2017):
        g.SetTitle( 'Barrel' )
        g2.SetTitle( 'End Cap' )
        g3.SetTitle( 'Barrel, Pixel Region' )
    elif(year2018):
        g.SetTitle( 'Barrel' )
        g2.SetTitle( 'End Cap' )
        g3.SetTitle( 'End Cap, HCAL Region' )
    elif(year2016):
        g3.SetTitle( 'Scale Factor' )
        g3A.SetTitle( '+1 #sigma unc.' )
        g3B.SetTitle( '-1 #sigma unc.' )
    g2.SetLineColor(ROOT.kRed)
    g2A.SetLineColor(ROOT.kRed)
    g2B.SetLineColor(ROOT.kRed)
    g3.SetLineColor(ROOT.kBlue)
    g3A.SetLineColor(ROOT.kBlue)
    g3B.SetLineColor(ROOT.kBlue)
    g2.SetMarkerColor(ROOT.kRed)
    g2A.SetMarkerColor(ROOT.kRed)
    g2B.SetMarkerColor(ROOT.kRed)
    g3.SetMarkerColor(ROOT.kBlue)
    g3A.SetMarkerColor(ROOT.kBlue)
    g3B.SetMarkerColor(ROOT.kBlue)
    mg = ROOT.TMultiGraph()
    mg.Add( g )
    mg.Add( gA )
    mg.Add( gB )
    mg.Add( g2 )
    mg.Add( g2A )
    mg.Add( g2B )
    mg.Add( g3 )
    mg.Add( g3A )
    mg.Add( g3B )
    mg.SetMaximum( 1.3 )
    mg.SetMaximum( 0.1 )
    mg.Draw( 'alp' )
    mg.GetXaxis().SetTitle( 'Offline Tau p_{T} (GeV)' )
    mg.GetYaxis().SetTitle( 'Trigger SF' )
    leg = build_legend( [g, g2, g3] )
    if(year2016): leg = build_legend( [g3, g3A, g3B] )
    leg.Draw('same')
    g.SetTitle( '%s, type: %s, WP: %s' % (name, wp, tauWP) )
    p.Update()
    c.SaveAs('testPlots_18June2019_dfit/'+name+'_'+wp+'_'+tauWP+'_DM'+str(dm)+'.png')

    del sfs, sfs2, sfs3, g, g2, g3, mg


c = ROOT.TCanvas('c','c',600,400)
p = ROOT.TPad('p','p',0,0,1,1)
p.Draw()
p.cd()

for trigger in ['ditau', 'mutau', 'etau'] :
    for tauWP in ['vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'] :
    #for tauWP in ['vvtight',] :
    #for tauWP in ['vloose', 'medium', 'vvtight'] :
        if(year2017): tauSFs = getTauTriggerSFs(trigger, 2017, tauWP, 'MVAv2')
        elif(year2018): tauSFs = getTauTriggerSFs(trigger, 2018, tauWP, 'MVAv2')
        elif(year2016): tauSFs = getTauTriggerSFs(trigger, 2016, tauWP, 'MVAv2')
        make_plots( tauSFs, trigger, 0 )
        make_plots( tauSFs, trigger, 1 )
        make_plots( tauSFs, trigger, 10 )
        del tauSFs


