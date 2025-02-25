"""
=====================================================
Exporting a fitted Earth models as a sympy expression
=====================================================

A simple example returning a sympy expression describing the fit of a sine function computed by Earth.

"""

from __future__ import annotations

import numpy

from pyearth import Earth, export

# Create some fake data
numpy.random.seed(2)
m = 1000
n = 10
X = 10 * numpy.random.uniform(size=(m, n)) - 40
y = 100 * (numpy.sin((X[:, 6])) - 4.0) + 10 * numpy.random.normal(size=m)

# Fit an Earth model
model = Earth(max_degree=2, minspan_alpha=0.5, verbose=False)
model.fit(X, y)

print(model.summary())

# return sympy expression
print("Resulting sympy expression:")
print(export.export_sympy(model))
