import ROOT

class SFProvider:
    supported_decay_modes = [ 0, 1, 10, 11 ]

    def __init__(self, input_file, channel, wp):
        root_file = ROOT.TFile(input_file, "READ")
        if root_file.IsZombie():
            raise RuntimeError('tau_trigger::SFProvider: unable to open "{}".'.format(input_file))

        self.eff_data = {}
        self.eff_mc = {}
        self.sf = {}

        histograms = { "data": self.eff_data , "mc": self.eff_mc, "sf": self.sf }
        for dm in SFProvider.supported_decay_modes:
            for type_name, hist_dict in histograms.iteritems():
                hist_name = '{}_{}_{}_dm{}_fitted'.format(type_name, channel, wp, dm)
                hist_dict[dm] = SFProvider._LoadHistogram(root_file, hist_name)
        root_file.Close()

    def getEfficiencyData(self, tau_pt, tau_dm, unc_scale = 0):
        tau_dm = SFProvider._CheckDM(tau_dm)
        return self._FindBinValue(self.eff_data[tau_dm], tau_pt, unc_scale)

    def getEfficiencyMC(self, tau_pt, tau_dm, unc_scale = 0):
        tau_dm = SFProvider._CheckDM(tau_dm)
        return self._FindBinValue(self.eff_mc[tau_dm], tau_pt, unc_scale)

    def getSF(self, tau_pt, tau_dm, unc_scale = 0):
        tau_dm = SFProvider._CheckDM(tau_dm)
        return self._FindBinValue(self.sf[tau_dm], tau_pt, unc_scale)

    @staticmethod
    def _LoadHistogram(file, name):
        hist = file.Get(name)
        if hist is None or type(hist) != ROOT.TH1F:
            raise RuntimeError('tau_trigger::SFProvider: unable to load "{}" from the root file "{}".' \
                               .format(name, file.GetName()))
        cloned_hist = hist.Clone()
        cloned_hist.SetDirectory(0)
        return cloned_hist

    @staticmethod
    def _FindBinValue(hist, x, unc_scale):
        bin = hist.FindFixBin(x)
        bin = min(hist.GetNbinsX(), max(1, bin))
        return hist.GetBinContent(bin) + unc_scale * hist.GetBinError(bin)

    @staticmethod
    def _CheckDM(tau_dm):
        if tau_dm == 2:
            tau_dm = 1
        if tau_dm not in SFProvider.supported_decay_modes:
            raise RuntimeError('tau_trigger::SFProvider: decay mode = {} is not supported.'.format(tau_dm))
        return tau_dm
