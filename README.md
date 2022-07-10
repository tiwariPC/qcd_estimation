# QCD Estimation
## Step 1
Run ``step1_qcdDphi.py`` file using following command:

```python step1_qcdDphi.py -i <input Directory> -o <step1_qcdDphi_output.root>```

This will give file output containing 2D histogram with ``min(Dphi)`` in x-axis and ``MET`` or ``costheta*`` in y-axis and histogram containing ``h_total_mcweight``

## Step 2
Run ``step2_qcd_dphi_multibins_bbDM.py`` or ``step2_qcd_dphi_multibins_monoH.py``  file using following command:

```python fitQCD_binwise.py -i <step1_qcdDphi_output.root> -o <step2_qcd_dphi_multibins_output.root>```

This will give ``min(Dphi)`` vs ``MET`` or ``(costheta*)`` plots for each bin and for all bin together.

## Step 3

### For individual bins
Run ``step3_fitQCD_binwise.py`` file using following command:

```python step3_fitQCD_binwise.py -i <step2_qcd_dphi_multibins_output.root> -O <output Directory>```

This will plot the histogram as well as the fit for each bin
### For all bins 
Run ``step3_fitQCD_total.py`` file using following command:

```python step3_fitQCD_total.py -i <step2_qcd_dphi_multibins_output.root> -O <output Directory>```

This will plot the histogram as well as the fit for all bins together.
