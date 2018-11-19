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
    

def make_plots( tauSFs, target_type = 'di-tau' ) :

    if target_type == 'di-tau' :
        min_ = 35
        name = 'Di-Tau'
    if target_type == 'e-tau' :
        min_ = 30
        name = 'E-Tau'
    if target_type == 'mu-tau' :
        min_ = 25
        name = 'Mu-Tau'

    pts = array('d', [])
    sfs = array('d', [])
    sfs2 = array('d', [])
    sfs3 = array('d', [])

    for pt in range( min_, 200 ) :
        pts.append( pt )
        if target_type == 'di-tau' :
            sfs.append( tauSFs.getDiTauScaleFactor( pt, 0.0, 0.0 ) )
            sfs2.append( tauSFs.getDiTauScaleFactor( pt, 2.0, 0.0 ) )
            sfs3.append( tauSFs.getDiTauScaleFactor( pt, 1.0, 2.9 ) )
        if target_type == 'e-tau' :
            sfs.append( tauSFs.getETauScaleFactor( pt, 0.0, 0.0 ) )
            sfs2.append( tauSFs.getETauScaleFactor( pt, 2.0, 0.0 ) )
            sfs3.append( tauSFs.getETauScaleFactor( pt, 1.0, 2.9 ) )
        if target_type == 'mu-tau' :
            sfs.append( tauSFs.getMuTauScaleFactor( pt, 0.0, 0.0 ) )
            sfs2.append( tauSFs.getMuTauScaleFactor( pt, 2.0, 0.0 ) )
            sfs3.append( tauSFs.getMuTauScaleFactor( pt, 1.0, 2.9 ) )

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
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/tauSFs/Aug12_new_SFs/old_'+name+'_'+wp+'_'+tauWP+'.png')

    del sfs, sfs2, sfs3, g, g2, g3, mg


c = ROOT.TCanvas('c','c',600,400)
p = ROOT.TPad('p','p',0,0,1,1)
p.Draw()
p.cd()

for wp in ['MVA',]:# 'dR0p3'] :
    #for tauWP in ['vvloose', 'vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'] :
    for tauWP in ['medium', 'tight', 'vtight'] :
        #tauSFs = getTauTriggerSFs(tauWP, wp)
        tauSFs = getTauTriggerSFs(tauWP)

        make_plots( tauSFs, 'di-tau' )
        make_plots( tauSFs, 'e-tau' )
        make_plots( tauSFs, 'mu-tau' )

