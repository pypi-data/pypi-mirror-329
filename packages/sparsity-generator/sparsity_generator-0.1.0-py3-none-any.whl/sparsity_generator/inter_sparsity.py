import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt
import mpl_toolkits
from matplotlib import rc
rc('text', usetex=False)
rc('mathtext', fontset='stix')
rc('font', family='STIXGeneral')
plt.rc('xtick', direction='out')  # Set x-ticks outside
plt.rc('ytick', direction='out')  # Set y-ticks outside

# Configure matplotlib to use LaTeX font


# Data preparation
layer = [1, 2, 3, 4, 5, 6]

# Define the data arrays
sparsity = [0.12164215543376866, 0.03983128485988029, 0.019092313092739427,
            0.000607314987562189, 0.00031458916355721393, 0.00026463750583022387]
sparsitywp = [0.03203480279267724, 0.020937411939326803, 0.013313027756724192,
              0.0026627725629664177, 0.00031458916355721393, 0.00025674241099191543]
sparsitywm = [0.193704785399176, 0.042374188627176616, 0.0075685871181203354,
              0.0002815664111085199, 0.00027890940803793534, 0.0002688887107431592]
sparsityp = [0.03915951856926306, 0.012070689035292289, 0.007759056281094527,
             0.00028627310226212686, 0.0002495305455146144, 0.0002593234996890547]

err2 = [0.06383673777307743, 0.025220224709370662, 0.01110511186261588,
        0.0004625301665290363, 0.0003684823839465349, 0.0003489083419345094]
err3 = [0.027466940991390132, 0.019394709459833296, 0.013415298433453243,
        0.0035009000015010904, 0.0012488120889678248, 0.00033721389675248797]
err4 = [0.09040569858831936, 0.02122363304308078, 0.004444572911185212,
        0.0003389921249963215, 0.0003534417753805783, 0.0003626286834240015]
err1 = [0.03171812624683867, 0.009579580193887372, 0.006431935097925539,
        0.0002978641814416524, 0.0011409171185090175, 0.0003580503303498942]

# Define the methods and their corresponding data
methods = ['RPCANet', 'RPCANet$^{++}$ wo DCPM', 'RPCANet$^{++}$ wo MAM', 'RPCANet$^{++}$']
sparsity_values = [sparsity, sparsitywp, sparsitywm, sparsityp]
error_values = [err2, err3, err4, err1]

# Define the aesthetics mappings
colors = {
    'RPCANet': '#FFCCFF',
    'RPCANet$^{++}$ wo DCPM': '#B7B7B7',
    'RPCANet$^{++}$ wo MAM': '#2F64FF',
    'RPCANet$^{++}$': '#00FFFF'
}
shapes = {
    'RPCANet': 's',
    'RPCANet$^{++}$ wo DCPM': 'o',
    'RPCANet$^{++}$ wo MAM': '^',
    'RPCANet$^{++}$': 'd'
}
line_styles = {
    'RPCANet': '--',
    'RPCANet$^{++}$ wo DCPM': '-.',
    'RPCANet$^{++}$ wo MAM': ':',
    'RPCANet$^{++}$': '-'
}

# Create a list to hold individual DataFrames
data_list = []

for method, sparsity_vals, error_vals in zip(methods, sparsity_values, error_values):
    df = pd.DataFrame({
        'Layer': layer,
        'Sparsity': sparsity_vals,
        'Error': error_vals,
        'Method': method,
    })
    data_list.append(df)

# Combine all data into a single DataFrame
data = pd.concat(data_list, ignore_index=True)



# Set axis limits and ticks (unchanged)
x_limits = (0.8, 6.2)
y_limits = (-0.01, 0.3)
x_ticks = [1, 2, 3, 4, 5, 6]

# Define line width variable
line_width = 2 # You can adjust this value as needed

# Create the plot
plot = (
    ggplot(data, aes('Layer', 'Sparsity', color='Method', shape='Method', linetype='Method')) +
    geom_line(size=line_width) +
    geom_point(size=4, stroke=0.7) +
    geom_errorbar(aes(ymin='Sparsity - Error', ymax='Sparsity + Error'), width=0.2, size=line_width) +
    scale_x_continuous(breaks=x_ticks, limits=x_limits) +
    scale_y_continuous(limits=y_limits) +
    scale_color_manual(values=colors) +
    scale_shape_manual(values=shapes) +
    scale_linetype_manual(values=line_styles) +
    # [Your scales for color, shape, linetype]
    theme_minimal() +
    theme(
        axis_text=element_text(size=22, family='Palatino Linotype'),
        axis_title=element_text(size=24, family='Palatino Linotype'),
        plot_title=element_text(size=24, family='Palatino Linotype', ha='center'),
        legend_title=element_blank(),
        legend_position=(0.68, 0.75),
        legend_direction='vertical',
        legend_background=element_rect(fill='white',  color='grey', alpha = 0.7, size=0.7),
        # legend_key=element_rect(size=0),
        # legend_box_margin=element_rect(margin={'t': 100, 'b':100, 'l': 100, 'r': 100}),
        legend_key_height=12,  # Adjust the height of the legend key boxes
        legend_key_width=30,  # Adjust the width of the legend key boxes
        # legend_spacing_y=0.5,  # Adjust vertical spacing between legend entries
        legend_box_spacing=100,  # Adjust spacing around the legend box
        legend_box_margin=5,


        # legend_entry_spacing_x=12,  # Horizontal spacing between legend entries
        # legend_entry_spacing_y=6,
        legend_text=element_text(size=22, family='Palatino Linotype'),
        panel_background=element_rect(fill='gray', alpha=0.1, color='white'),
        panel_grid_major=element_line(color='white', linetype='--', size=1.5, alpha=0.9),
        panel_border=element_blank(),
        axis_ticks_length=0,
        axis_ticks_length_major=5,
        axis_ticks=element_line(size=1.5),
        axis_ticks_major=element_line(color='gray'),
        axis_ticks_major_x=element_line(size=1.5),  # override size=2
        axis_ticks_major_y=element_line(color='gray') # override color=purple
        # tick_params=dict(which='both', direction='out')       # axis_line=element_line(color="black", size=0.5)
    ) +
    guides(
        color=guide_legend(nrow=4),  # Adjust spacing in the legend
        shape=guide_legend(nrow=4),
        linetype=guide_legend(nrow=4)
    )+

    labs(
        x='Stage - $k$',
        y=r'Sparsity   ($\|\mathbf{T}^k\|_0 / {H \times W}$)',
        title='Sparsity Measurement Across Stages'
    )
)

plot.save("sparsity_measurement.png", dpi=500, width=8, height=7)

print(plot)
