#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
=============================================================
Compare the effect of different scalers on data with outliers
=============================================================

Feature 0 (median income in a block) and feature 5 (number of households) of
the `California housing dataset
<https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html>`_ have very
different scales and contain some very large outliers. These two
characteristics lead to difficulties to visualize the data and, more
importantly, they can degrade the predictive performance of many machine
learning algorithms. Unscaled data can also slow down or even prevent the
convergence of many gradient-based estimators.

Indeed many estimators are designed with the assumption that each feature takes
values close to zero or more importantly that all features vary on comparable
scales. In particular, metric-based and gradient-based estimators often assume
approximately standardized data (centered features with unit variances). A
notable exception are decision tree-based estimators that are robust to
arbitrary scaling of the data.

This example uses different scalers, transformers, and normalizers to bring the
data within a pre-defined range.

Scalers are linear (or more precisely affine) transformers and differ from each
other in the way to estimate the parameters used to shift and scale each
feature.

``QuantileTransformer`` provides non-linear transformations in which distances
between marginal outliers and inliers are shrunk. ``PowerTransformer`` provides
non-linear transformations in which data is mapped to a normal distribution to
stabilize variance and minimize skewness.

Unlike the previous transformations, normalization refers to a per sample
transformation instead of a per feature transformation.

The following code is a bit verbose, feel free to jump directly to the analysis
of the results_.

"""
import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import PowerTransformer


def HandleData(file_in):
    pd_data = pd.read_csv(file_in, sep='\t', header=0, index_col=0)
    return pd_data

def SelectMethod(X, method, outfile):
    if method == 'standard':
        data = StandardScaler().fit_transform(X)
    elif method == 'min-max':
        data = MinMaxScaler().fit_transform(X)
    elif method == 'max-abs':
        data = MaxAbsScaler().fit_transform(X)
    elif method == 'robust':
        data = RobustScaler(quantile_range=(25, 75)).fit_transform(X)
    elif method == 'power':
        data = PowerTransformer(method='yeo-johnson').fit_transform(X)
    elif method == 'quantile':
        data = QuantileTransformer(output_distribution='normal').fit_transform(X)
    elif method == 'normalize':
        data = Normalizer().fit_transform(X)
    df = pd.DataFrame(data, index=X.index, columns=X.columns).round(4)
    df.to_csv(outfile, sep='\t')

def main():
    pd_data = HandleData(sys.argv[1])
    if len(sys.argv) == 3:
        SelectMethod(pd_data, 'standard', sys.argv[2])
    else:
        SelectMethod(pd_data, sys.argv[3], sys.argv[2])


if __name__ == '__main__':
    main()
