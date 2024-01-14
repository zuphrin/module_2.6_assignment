import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def read_rmsd_file(filename):
    """ Read RMSD file and return a DataFrame. """
    try:
        df = pd.read_csv(filename, skiprows=1, header=None, names=['Time', 'RMSD'], sep="\s+")
        df['Time'] = df['Time'] / 1000
        df = df[::5]
    except Exception as e:
        print(f"An unexpected error occurred while reading {filename}: {e}")
    return df

# List of types and replicates
types = ['init', 'MOA', 'MOB']
reps = np.arange(1, 6)  # 5 replicates
colours = ['#7fcdbb', '#2c7fb8', '#edf8b1']

# Dictionary to hold data for each replicate
rep_dict = {}

for rep in reps:
    type_dict = {}
    for type in types:
        filename = f'data/rmsd_{type}_{rep}.out'
        type_dict[type] = read_rmsd_file(filename)
    rep_dict[rep] = type_dict

try:
    # Adjusted subplot grid: 5 rows, 2 columns
    fig = plt.figure(figsize=(8, 10), dpi=200)
    gs = gridspec.GridSpec(5, 2, width_ratios=[6, 1])

    for rep in reps:
        for i, type in enumerate(types):
            data = rep_dict[rep][type] # for better readibility in the loop

            # Plotting the time series in the first column
            ax_ts = plt.subplot(gs[rep-1, 0])
            ax_ts.plot(data['Time'], data['RMSD'], label=type, color=colours[i])

            # Labels
            ax_ts.set_ylabel('RMSD')
            if rep == reps[-1]:
                ax_ts.set_xlabel('Time [ns]')
        
            ax_ts.set_xlim(0,100)
            ax_ts.set_ylim(0,0.7)

            ax_ts.set_title(f'Replicate {rep}')

            # Plotting the histogram in the second column
            ax_hist = plt.subplot(gs[rep-1, 1])

            ax_hist.hist(data['RMSD'], bins=20, orientation='horizontal', alpha=0.5, color=colours[i])#, density=True)

            # Label
            if rep == reps[-1]:
                ax_hist.set_xlabel('Frequency')

            # Turn off y-ticks for the histograms
            ax_hist.set_yticks([])
            
    #plt.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('assignment_plt.png')
    plt.show()
except Exception as e:
    print(f"An unexpected error occurred during plotting: {e}")