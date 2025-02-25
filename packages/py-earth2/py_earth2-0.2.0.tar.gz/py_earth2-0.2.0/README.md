# py-earth2

This project is copied from [py-earth](https://github.com/scikit-learn-contrib/py-earth), which has been archived since December 2023 and is licensed under BSD-3-Clause Copyright (c) 2013, Jason Rudy.

The original README can be found in [`README-original.md`](README-original.md)

A Python implementation of Jerome Friedman's Multivariate Adaptive Regression Splines algorithm,
in the style of scikit-learn. The py-earth package implements Multivariate Adaptive Regression Splines using Cython and provides an interface that is compatible with scikit-learn's Estimator, Predictor, Transformer, and Model interfaces.  For more information about
Multivariate Adaptive Regression Splines, see the references below.

---

## Usage

```python
import numpy
from pyearth import Earth
from matplotlib import pyplot

#Create some fake data
numpy.random.seed(0)
m = 1000
n = 10
X = 80*numpy.random.uniform(size=(m,n)) - 40
y = numpy.abs(X[:,6] - 4.0) + 1*numpy.random.normal(size=m)

#Fit an Earth model
model = Earth()
model.fit(X,y)

#Print the model
print(model.trace())
print(model.summary())

#Plot the model
y_hat = model.predict(X)
pyplot.figure()
pyplot.plot(X[:,6],y,'r.')
pyplot.plot(X[:,6],y_hat,'b.')
pyplot.xlabel('x_6')
pyplot.ylabel('y')
pyplot.title('Simple Earth Example')
pyplot.show()
```
