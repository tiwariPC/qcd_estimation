fileLoc_2016="/eos/cms/store/group/phys_exotica/bbMET/analysis_files/2016_AnalysedFiles/analyser_v16_12-02-02_Merged"
fileLoc_2017="/eos/cms/store/group/phys_exotica/bbMET/analysis_files/2017_AnalysedFiles/analyser_v17_12-02-02_Merged"
fileLoc_2018="/eos/cms/store/group/phys_exotica/bbMET/analysis_files/2018_AnalysedFiles/analyser_v18_12-02-02_Merged"

for year in 2016 2017 2018
do
    for cat in "1b" #"2b"
    do
        fileVar="fileLoc_${year}"
        eval "fileLoc=\$$fileVar"
        echo python step1_qcdDphi.py -i ${fileLoc} -y ${year} -c ${cat}
        python step1_qcdDphi.py -i ${fileLoc} -y ${year} -c ${cat}
        wait

        echo python step2_qcd_dphi_multibins_bbDM.py -y ${year} -c ${cat}
        python step2_qcd_dphi_multibins_bbDM.py -y ${year} -c ${cat}
        wait

        echo python step3_fitQCD_total.py  -y ${year} -c ${cat}
        python step3_fitQCD_total.py  -y ${year} -c ${cat}
        wait

        echo python step3_fitQCD_binwise.py  -y ${year} -c ${cat}
        python step3_fitQCD_binwise.py  -y ${year} -c ${cat}
    done
done
