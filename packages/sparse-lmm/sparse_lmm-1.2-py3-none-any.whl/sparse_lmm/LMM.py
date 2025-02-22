import scipy.optimize as opt
import numpy.linalg as linalg
import numpy as np

import time

from .helpingMethods import *
from sklearn.linear_model import Lasso

class LMM:
    def __init__(self, modified=True, lamda=0.1, numintervals=100, ldeltamin=-5, ldeltamax=5, scale=0, alpha=0.05, fdr=False,
                 acceleration=True,
                 quiet=True):
        self.numintervals = numintervals
        self.ldeltamin = ldeltamin
        self.ldeltamax = ldeltamax
        self.scale = scale
        self.alpha = alpha
        self.modified = modified  # Only rotate X, and apply Lasso instead of hypothesis test
        self.lamda = lamda  # Regularization coeffecient for Lasso.
        self.fdr = fdr
        self.ldelta0 = None
        self.quiet = quiet
        self.acceleration = acceleration
        self.K = None

    def estimateDelta(self, y):
        if y.ndim == 1:
            y = y.reshape((y.shape[0], 1))
        self.y = y
        self.S, self.U, self.ldelta0= self.train_nullmodel(y, self.K)
        print(self.ldelta0)

    def setK(self, K):
        self.K = K

    def setLDelta(self, delta0):
        self.ldelta0=delta0

    def setCovarianceThreshold(self, covT):
        self.covT = covT


    def fit(self, X, y):
        if self.acceleration:
            self.fit_fast(X, y)
        else:
            self.fit_detail(X, y)

    def fit_fast(self, X, y):
        [n_s, n_f] = X.shape
        if self.K is None:
            self.K = np.dot(X, X.T)

        if y.ndim == 1:
            y = np.reshape(y, (n_s, 1))

        self.y = y
        self.S, self.U, ldelta0= self.train_nullmodel(self.y, self.K)

        self.ldelta0 = ldelta0

        if not self.modified:
            X0 = np.ones(len(self.y)).reshape(len(self.y), 1)

        delta0 = np.exp(self.ldelta0)
        Sdi = 1. / (self.S + delta0)
        Sdi_sqrt = np.sqrt(Sdi)
        SUX = np.dot(self.U.T, X)
        SUX = SUX * np.tile(Sdi_sqrt, (n_f, 1)).T
        if not self.modified:
            SUy = np.dot(self.U.T, self.y)
            SUy = SUy * Sdi_sqrt.reshape((n_s, 1))

        self.SUX = SUX
        if not self.modified:
            self.SUy = SUy
            SUX0 = np.dot(self.U.T, X0)
            self.SUX0 = SUX0 * np.tile(Sdi_sqrt, (1, 1)).T
            self.X0 = X0
            self.neg_log_p, self.beta = self.hypothesisTest(self.SUX, self.SUy, X, self.SUX0, self.X0)
        else:
            self.lasso = Lasso(alpha=self.lamda)
            self.lasso.fit(self.SUX, self.y)
            self.beta = self.lasso.coef_
            self.neg_log_p = None


    def fit_detail(self, X, y):
        [n_s, n_f] = X.shape
        if self.K is None:
            self.K = np.dot(X, X.T)

        self.neg_log_p = np.zeros(n_f)
        self.beta = np.zeros(n_f)

        stepSize = n_f*0.05
        count = 0
        countStep = 1

        start = time.time()

        for i in range(n_f):

            if not self.quiet:
                count += 1
                if count > countStep*stepSize:
                    print ('Finished ', countStep*5, '% of the progress, ', end = '')
                    print ('with', time.time() - start, 'seconds')
                    countStep += 1

            try:
                self.neg_log_p[i], self.beta[i] = self.fit_helper(X[:, i].reshape([n_s, 1]), y)
            except:
                self.neg_log_p[i] = 0
                self.beta[i] = 0

    def fit_helper(self, X, y):
        [n_s, n_f] = X.shape
        if y.ndim == 1:
            y = y.reshape((y.shape[0], 1))
        self.y = y
        self.S, self.U, ldelta0= self.train_nullmodel(y, self.K)

        # if self.ldelta0 is None:
        #     self.ldelta0 = ldelta0
        self.ldelta0 = ldelta0

        X0 = np.ones(len(self.y)).reshape(len(self.y), 1)

        delta0 = np.exp(self.ldelta0)
        Sdi = 1. / (self.S + delta0)
        Sdi_sqrt = np.sqrt(Sdi)
        SUX = np.dot(self.U.T, X)
        SUX = SUX * np.tile(Sdi_sqrt, (n_f, 1)).T
        SUy = np.dot(self.U.T, self.y)
        SUy = SUy * Sdi_sqrt.reshape((n_s, 1))

        self.SUX = SUX
        self.SUy = SUy
        SUX0 = np.dot(self.U.T, X0)
        self.SUX0 = SUX0 * np.tile(Sdi_sqrt, (1, 1)).T
        self.X0 = X0
        neg_log_p, beta = self.hypothesisTest(self.SUX, self.SUy, X, self.SUX0, self.X0)
        return neg_log_p, beta

    def fdrControl(self):
        tmp = np.exp(-self.neg_log_p)
        tmp = sorted(tmp)
        threshold = 1e-8
        n = len(tmp)
        for i in range(n):
            if tmp[i] < (i+1)*self.alpha/n:
                threshold = tmp[i]
        self.neg_log_p[self.neg_log_p<-np.log(threshold)] = 0

    def getNegLogP(self):
        if self.neg_log_p is None:
            return None
        if not self.fdr:
            return self.neg_log_p.copy()
        else:
            self.fdrControl()
            return self.neg_log_p.copy()

    def hypothesisTest(self, UX, Uy, X, UX0, X0):
        [m, n] = X.shape
        p = []
        betas = []
        for i in range(n):
            if UX0 is not None:
                UXi = np.hstack([UX0, UX[:, i].reshape(m, 1)])
                XX = matrixMult(UXi.T, UXi)
                XX_i = linalg.pinv(XX)
                beta = matrixMult(matrixMult(XX_i, UXi.T), Uy)
                Uyr = Uy - matrixMult(UXi, beta)
                Q = np.dot(Uyr.T, Uyr)
                sigma = Q * 1.0 / m
                betas.append(beta[1])
            else:
                Xi = np.hstack([X0, UX[:, i].reshape(m, 1)])
                XX = matrixMult(Xi.T, Xi)
                XX_i = linalg.pinv(XX)
                beta = matrixMult(matrixMult(XX_i, Xi.T), Uy)
                Uyr = Uy - matrixMult(Xi, beta)
                Q = np.dot(Uyr.T, Uyr)
                sigma = Q * 1.0 / m
                betas.append(beta[1])
            ts, ps = tstat(beta[1], XX_i[1, 1], sigma, 1, m)
            if -1e100 < ts < 1e100:
                p.append(ps)
            else:
                p.append(1)
        p = np.array(p)
        return -np.log(p), np.array(betas)

    def train_nullmodel(self, y, K, S=None, U=None, numintervals=500):
        self.ldeltamin += self.scale
        self.ldeltamax += self.scale

        if S is None or U is None:
            S, U = linalg.eigh(K)

        Uy = np.dot(U.T, y)

        # grid search
        nllgrid = np.ones(numintervals + 1) * np.inf
        ldeltagrid = np.arange(numintervals + 1) / (numintervals * 1.0) * (self.ldeltamax - self.ldeltamin) + self.ldeltamin
        for i in np.arange(numintervals + 1):
            nllgrid[i] = nLLeval(ldeltagrid[i], Uy, S) # the method is in helpingMethods

        nllmin = nllgrid.min()
        ldeltaopt_glob = ldeltagrid[nllgrid.argmin()]

        for i in np.arange(numintervals - 1) + 1:
            if (nllgrid[i] < nllgrid[i - 1] and nllgrid[i] < nllgrid[i + 1]):
                ldeltaopt, nllopt, iter, funcalls = opt.brent(nLLeval, (Uy, S),
                                                              (ldeltagrid[i - 1], ldeltagrid[i], ldeltagrid[i + 1]),
                                                              full_output=True)
                if nllopt < nllmin:
                    nllmin = nllopt
                    ldeltaopt_glob = ldeltaopt
        return S, U, ldeltaopt_glob

    def predict(self, X_new):
        if X_new.ndim == 1:
            X_new = X_new.reshape(1, -1)

        # Check if necessary parameters are initialized
        if self.K is None or self.U is None or self.S is None:
            raise ValueError("Model has not been properly initialized with training data.")

        # Multiply the transformed data by beta coefficients to get predictions
        # Ensure beta is reshaped appropriately for matrix multiplication
        beta = self.beta.copy()
        if beta.ndim == 1:
            beta = beta.reshape(-1, 1)
        
        if self.modified:  # LASSO mode
            y_pred = np.dot(X_new, beta) + self.lasso.intercept_
        else:  # Standard LMM mode
            y_pred = np.dot(X_new, beta)

        return y_pred.flatten()  # Flatten in case the output is a single sample

    def getBeta(self):
        if not hasattr(self, 'beta') or self.beta is None:
            raise ValueError("Model has not been fit yet. Call fit() first.")
        
        if not isinstance(self.beta, np.ndarray):
            raise TypeError("beta must be a numpy array")
        
        return self.beta.copy()

if __name__ == '__main__':

    from matplotlib import pyplot as plt

    X = np.random.randn(500, 900)
    beta = np.random.randn(900, 1)
    beta[np.array(np.random.choice(range(900), 850))] = 0
    y = np.dot(X, beta).reshape([500])
    # y = np.random.randn(500, 1).reshape([500])

    model = LMM(fdr=False, acceleration=True)

    model.fit(X, y)
    neg_log_p = model.getNegLogP() # negative log of p-value
    pvalue = np.exp(-neg_log_p)
    beta_ = model.getBeta()

    print(neg_log_p)
    print(beta_.T)
    print(beta.T)

    # Create a figure to hold the subplots
    fig = plt.figure(figsize=(12, 4))

    # 1st subplot: negative log p-values
    ax1 = fig.add_subplot(131)  # 131 means 1 row, 3 columns, and this is the 1st plot
    im1 = ax1.imshow(neg_log_p.reshape([30, 30]))
    fig.colorbar(im1, ax=ax1)
    ax1.set_title('Negative Log P-values')

    # 2nd subplot: estimated coefficients
    ax2 = fig.add_subplot(132)  # This is the 2nd plot
    im2 = ax2.imshow(beta_.reshape([30, 30]))
    fig.colorbar(im2, ax=ax2)
    ax2.set_title('Estimated Coefficients')

    # 3rd subplot: true coefficients
    ax3 = fig.add_subplot(133)  # This is the 3rd plot
    im3 = ax3.imshow(beta.reshape([30, 30]))
    fig.colorbar(im3, ax=ax3)
    ax3.set_title('True Coefficients')

    # Save the figure with subplots
    plt.tight_layout()
    plt.savefig('combined_plots.png')
    plt.close()
