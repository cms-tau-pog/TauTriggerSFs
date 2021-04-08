from TauAnalysisTools.TauTriggerSFs.SFProvider import SFProvider as TauTriggerSFProvider

for year in [ "2016ULpreVFP","2016ULpostVFP", "2017UL", "2018UL" ]:
    print("Testing tau trigger SF for {}".format(year))
    file_name = '../data/{}_tauTriggerEff_DeepTau2017v2p1.root'.format(year)

    channel_list = [ 'ditau', 'mutau', 'etau'] 
    for channel in channel_list:
        for wp in [ 'VVVLoose', 'VVLoose', 'VLoose', 'Loose', 'Medium', 'Tight', 'VTight', 'VVTight' ]:
            sf_provider = TauTriggerSFProvider(file_name, channel, wp)

            for pt in [ 45, 80, 120, 400 ]:
                for dm in [ 0, 1, 10, 11,1011 ]:
                    for unc_scale in [ -1, 0, 1 ]:
                        eff_data = sf_provider.getEfficiencyData(pt, dm, unc_scale)
                        eff_mc = sf_provider.getEfficiencyMC(pt, dm, unc_scale)
                        sf = sf_provider.getSF(pt, dm, unc_scale)
                        print("year={}, channel={}, wp={}, pt={}, dm={}, unc_scale={}, eff_data={}, eff_mc={}, sf={}" \
                              .format(year, channel, wp, pt, dm, unc_scale, eff_data, eff_mc, sf))

print("Tau trigger SF tests successfully finished.")
