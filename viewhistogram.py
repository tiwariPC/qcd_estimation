import ROOT
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Open the ROOT files
file_paths_1b = ["rootFiles/step3_qcdDphi_fitted_1b_2016.root", "rootFiles/step3_qcdDphi_fitted_1b_2017.root", "rootFiles/step3_qcdDphi_fitted_1b_2018.root"]
file_paths_2b = ["rootFiles/step3_qcdDphi_fitted_2b_2016.root", "rootFiles/step3_qcdDphi_fitted_2b_2017.root", "rootFiles/step3_qcdDphi_fitted_2018.root"]

# Function to plot data from a list of files with overlay
def plot_data(files, title):
    plt.figure(figsize=(8, 6))  # Create a new figure

    for file_path in files:
        # Open the ROOT file
        file = ROOT.TFile.Open(file_path, "READ")

        # Get the 'qcd_sigReg' histogram
        histogram = file.Get("qcd_sigReg")

        # Convert ROOT histogram to NumPy arrays
        n_bins = histogram.GetNbinsX()
        bin_contents = np.array([histogram.GetBinContent(i) for i in range(1, n_bins + 1)])
        bin_errors = np.array([histogram.GetBinError(i) for i in range(1, n_bins + 1)])

        # Get bin edges
        bin_edges = np.array([histogram.GetXaxis().GetBinLowEdge(i) for i in range(1, n_bins + 2)])

        # Plot the data with error bars
        plt.errorbar(bin_edges[:-1], bin_contents, yerr=bin_errors, fmt='o-', label=file_path.split('/')[-1].split('.')[0])

    # Set the title and labels
    plt.title(title)
    plt.xlabel('Variable')
    plt.ylabel('Count')

    # Add a legend
    plt.legend()

    # Save the plot as a PNG file
    plt.savefig(title + '.png')

# Plot the 1b data with overlay
plot_data(file_paths_1b, 'Overlay Plot for 1b')

# Plot the 2b data with overlay
plot_data(file_paths_2b, 'Overlay Plot for 2b')
