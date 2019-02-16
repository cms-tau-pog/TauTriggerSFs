import ROOT
ROOT.gROOT.SetBatch(True)
from getTauTriggerSFs import getTauTriggerSFs
from array import array



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
        min_ = 40
        name = 'Di-Tau'
    if target_type == 'etau' :
        min_ = 35
        name = 'E-Tau'
    if target_type == 'mutau' :
        min_ = 32
        name = 'Mu-Tau'

    pts = array('d', [])
    sfs = array('d', [])
    sfs2 = array('d', [])
    sfs3 = array('d', [])

    for pt in range( min_, 200 ) :
        pts.append( pt )
        if target_type == 'ditau' :
            sfs.append( tauSFs.getTriggerScaleFactor( pt, 0.0, 0.0, dm ) )
            sfs2.append( tauSFs.getTriggerScaleFactor( pt, 2.0, 0.0, dm ) )
            sfs3.append( tauSFs.getTriggerScaleFactor( pt, 1.0, 2.9, dm ) )
        if target_type == 'etau' :
            sfs.append( tauSFs.getTriggerScaleFactor( pt, 0.0, 0.0, dm ) )
            sfs2.append( tauSFs.getTriggerScaleFactor( pt, 2.0, 0.0, dm ) )
            sfs3.append( tauSFs.getTriggerScaleFactor( pt, 1.0, 2.9, dm ) )
        if target_type == 'mutau' :
            sfs.append( tauSFs.getTriggerScaleFactor( pt, 0.0, 0.0, dm ) )
            sfs2.append( tauSFs.getTriggerScaleFactor( pt, 2.0, 0.0, dm ) )
            sfs3.append( tauSFs.getTriggerScaleFactor( pt, 1.0, 2.9, dm ) )

    g = ROOT.TGraph( len(pts), pts, sfs )
    g2 = ROOT.TGraph( len(pts), pts, sfs2 )
    g3 = ROOT.TGraph( len(pts), pts, sfs3 )
    g.SetLineWidth( 2 )
    g.SetTitle( 'Barrel' )
    g2.SetTitle( 'End Cap' )
    g3.SetTitle( 'Barrel, Pixel Region' )
    g2.SetLineColor(ROOT.kRed)
    g3.SetLineColor(ROOT.kBlue)
    mg = ROOT.TMultiGraph()
    mg.Add( g )
    mg.Add( g2 )
    mg.Add( g3 )
    mg.SetMaximum( 1.2 )
    mg.Draw( 'alp' )
    mg.GetXaxis().SetTitle( 'Offline Tau p_{T} (GeV)' )
    mg.GetYaxis().SetTitle( 'Trigger SF' )
    leg = build_legend( [g, g2, g3] )
    leg.Draw('same')
    g.SetTitle( '%s, type: %s, WP: %s' % (name, wp, tauWP) )
    p.Update()
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/tauSFs/Feb16_new_SFs/'+name+'_'+wp+'_'+tauWP+'_DM'+str(dm)+'.png')

    del sfs, sfs2, sfs3, g, g2, g3, mg


c = ROOT.TCanvas('c','c',600,400)
p = ROOT.TPad('p','p',0,0,1,1)
p.Draw()
p.cd()

for trigger in ['ditau',]:# 'mutau', 'etau'] :
    #for tauWP in ['vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'] :
    for tauWP in ['vloose', 'medium', 'vvtight'] :
        tauSFs = getTauTriggerSFs('ditau', 2017, tauWP, 'MVAv2')
        make_plots( tauSFs, 'ditau', 0 )
        make_plots( tauSFs, 'ditau', 1 )
        make_plots( tauSFs, 'ditau', 10 )
        del tauSFs
        tauSFs = getTauTriggerSFs('etau', 2017, tauWP, 'MVAv2')
        make_plots( tauSFs, 'etau', 0 )
        make_plots( tauSFs, 'etau', 1 )
        make_plots( tauSFs, 'etau', 10 )
        del tauSFs
        tauSFs = getTauTriggerSFs('mutau', 2017, tauWP, 'MVAv2')
        make_plots( tauSFs, 'mutau', 0 )
        make_plots( tauSFs, 'mutau', 1 )
        make_plots( tauSFs, 'mutau', 10 )
        del tauSFs


