# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: Treacher
"""

# %% 0. Notes

'''
Function to calculate the slope of a series of n datapoints

Basic idea:
    Give the function n datapoints of e.g. price, MACD or whatever
    Use SciKit Learn linear regression to work out a straight line fit
    Use trigonometry to calculate what the angle is from the straight line
'''

# %% 1. Function definition


def Slope(dataPoints, n=40):
    """
    Parameters
    ----------
    dataPoints : 1-dimensional DataFrame
        These are the datapoints you're trying to extract a slope from
    n : int
        The number of points to include in the calculation
            The lower the n value, the more unstable the angle.
            Higher n values smooth the slope calculation

    Returns
    -------
    intercept : float
        y - axis value of the intercept at x = 0
    angle : float
        Slope of the line incoporating n points

    Package requirements
    -------
    pandas as pd\n
    numpy as np\n
    from sklearn.linear_model import LinearRegression
    """

    lr = LinearRegression()  # Instantiate a linear regression object
    angles = []  # Each time you add a datapoint, you'll need new slope

    # Loop over the data
    for i in range(n, len(dataPoints)-1):
        # x and y data
        x = np.arange(n)
        y = dataPoints[i-n:i]

        # Scale the axes so they're not all squished up at x=0
        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())

        lr.fit(x_scaled[:, None], y_scaled[:, None])
        angles.append(lr.coef_[0][0])
    slope_angle = (np.rad2deg(np.arctan(np.array(angles))))

    return slope_angle
