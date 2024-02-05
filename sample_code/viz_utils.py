# https://matplotlib.org/3.2.0/api/_as_gen/matplotlib.colors.TwoSlopeNorm.html?highlight=twoslopenorm#matplotlib.colors.TwoSlopeNorm
# Useful when mapping data with an unequal rates of change around a conceptual center, e.g., data that range from -2 to 4, with 0 as the midpoint.

# create rank scatter plots for different buffer sizes/backcasts for each WRZ

from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'monospace'

def rank(x):
    if x.std() == 0:
        ranked = np.array([len(x) / 2 + 0.5] * len(x))
    else:
        temp = x.argsort()
        ranks = np.empty_like(temp)
        ranks[temp] = np.arange(len(x))
        ranked = ranks + 1
    return ranked


def scatter_density(x, y, ax, title='', cmap='cividis'):
    """Sometimes first doesn't work -- need to resolve why later."""
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]
    ax.scatter(x, y, c=z, s=10, cmap=cmap)
    ax.set_title(title)
    return ax


def polar_contour_plot_example():
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import gridspec

    gs=gridspec.GridSpec(1,1)
    gs.update(wspace=0.205, hspace=0.105) 
    fig=plt.figure(figsize=(500/72.27,450/72.27))

    X = np.arange(0, 70, 10)
    Y = np.radians(np.linspace(0, 360, 20))
    r, theta = np.meshgrid(X,Y)
    Z1 = np.random.random((Y.size, X.size))


    ax=fig.add_subplot(gs[0,0], projection='polar')
    cax=ax.contourf(theta, r, Z1, 10)

    ax.set_rticks([0,20,40,60])
    ax.tick_params(colors='white', axis="y", which='both') 
    plt.show()