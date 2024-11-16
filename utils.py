import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 20)


def square_plot(X, Y, log_errorbands=True, folds=(2, 3), axis_labels = ('Predicted', 'Measured')):
    """
    Plots a square X-Y graph with unity line and fold error bands.
    
    Parameters:
    - X, Y: Lists or arrays of data to be plotted.
    - log_errorbands: Boolean, if True, the error bands will be in log scale.
    - folds: Tuple of fold errors to display (e.g., (2, 3)).
    """
    X = np.array(X)
    Y = np.array(Y)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Add the unity line
    limits = [min(X.min(), Y.min())-1, max(X.max(), Y.max())+1]
    ax.plot(limits, limits, 'k--', label='Unity line', linewidth=1.5)

    # Add fold error bands based on log_errorbands
    for fold, color in zip(folds, ['blue', 'lightblue']):
        if not log_errorbands:
            lower_band = limits[0] / fold, limits[1] / fold
            upper_band = limits[0] * fold, limits[1] * fold
        else:
            lower_band = limits[0] - np.log10(fold), limits[1] - np.log10(fold)
            upper_band = limits[0] + np.log10(fold), limits[1] + np.log10(fold)

        ax.fill_between(
            limits,
            lower_band,
            upper_band,
            color=color,
            alpha=0.3,
            label=f'{fold}-fold error'
        )
    # Plot the data points
    ax.scatter(X, Y, c='white', alpha=0.7, edgecolors='k', s=100)

    # Configure plot appearance
    ax.set_xlim(limits)
    ax.set_ylim(limits)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel(axis_labels[0])
    ax.set_ylabel(axis_labels[1])
    ax.legend()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Show plot
    plt.show()
  

def process_numeric_list(lst, remove_lower_than = True):
    result = []
    for val in lst:
        if type(val)==float:
            result.append(val)
        elif ("<" in val) & remove_lower_than:
            result.append(np.nan)
        else:
            # Use regex to extract the number and convert to float
            number = re.findall(r"[-+]?\d*\.\d+|\d+", val)
            if number:
                result.append(float(number[0]))
            else:
                result.append(np.nan)  # In case no valid number is found
    return result
