fileLoc_2016="/eos/cms/store/group/phys_susy/sus-23-008/2016_AnalysedFiles/analyser_v16_12-02-02_Merged"
fileLoc_2017="/eos/cms/store/group/phys_susy/sus-23-008/2017_AnalysedFiles/analyser_v17_12-02-02_Merged"
fileLoc_2018="/eos/cms/store/group/phys_susy/sus-23-008/2018_AnalysedFiles/analyser_v18_12-02-02_Merged"


for year in 2016 2017 2018
do
    # fileVar="fileLoc_${year}"
    # eval "fileLoc=\$$fileVar"
    # echo python step1_qcdDphi_allCRs.py -i ${fileLoc} -y ${year}
    # python step1_qcdDphi_allCRs.py -i ${fileLoc} -y ${year}
    # wait
    # echo python step2_qcdDphi_allCRs.py -y ${year}
    # python step2_qcdDphi_allCRs.py -y ${year}
    # wait
    echo python step3_fitQCD_total_allCRs.py  -y ${year}
    python step3_fitQCD_total_allCRs.py  -y ${year}
    wait
    echo python step3_fitQCD_binwise_allCRs.py  -y ${year}
    python step3_fitQCD_binwise_allCRs.py  -y ${year}
done
