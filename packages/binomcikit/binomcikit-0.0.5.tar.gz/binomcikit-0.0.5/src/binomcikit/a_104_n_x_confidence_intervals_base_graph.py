from plotnine import *
from .a_111_n_adj_confidence_intervals import *
def plotciawd(n, alp, h):
    # Input validation
    if n < 1 or n > 1000:
        raise ValueError("n must be between 1 and 1000")
    if not (0.5 <= alp <= 1) or not (0 < h < 1):
        raise ValueError("alp must be between 0.5 and 1, and h must be between 0 and 1")

    # Compute the confidence intervals
    WaldCI_df = ciawd(n, alp, h)

    # Create DataFrame with necessary columns
    ss1 = pd.DataFrame({
        'x': WaldCI_df['x'],
        'LowerLimit': WaldCI_df['LAWD'],
        'UpperLimit': WaldCI_df['UAWD'],
        'LowerAbb': WaldCI_df['LABB'],
        'UpperAbb': WaldCI_df['UABB'],
        'ZWI': WaldCI_df['ZWI']
    })

    # Add ID column
    ss1['ID'] = range(1, len(ss1) + 1)

    # Get the subsets for different aberrations
    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    # Combine the aberration data
    ldf = pd.concat([
        ll[['ID', 'LowerLimit']].assign(Abberation='Lower').rename(columns={'LowerLimit': 'Value'}),
        ul[['ID', 'UpperLimit']].assign(Abberation='Upper').rename(columns={'UpperLimit': 'Value'}),
        zl[['ID', 'LowerLimit']].assign(Abberation='ZWI').rename(columns={'LowerLimit': 'Value'})
    ], ignore_index=True)

    # Plot
    plot = ggplot(ss1, aes(x='UpperLimit', y='ID'))
    plot += geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5, color='black')

    if not ldf.empty:
        plot += geom_point(data=ldf, mapping=aes(x='Value', y='ID'),

                           aes(color='Abberation', legend=False),
                           stroke='indigo', fill='indigo')

    # Assign colors
    plot + scale_colour_manual(name='Abberation', type='line',
                               values={'Lower': 'green', 'Upper': 'blue', 'ZWI': 'red'})

    return plot


# Example usage:
if __name__ == "__main__":
    n = 1000
    alp = 0.95
    h = 0.5
    plot = plotciawd(n, alp, h)
    plot.show()
x=5; n=5; alp=0.05;e=0.5
plotciawd(x,n,alp,e)