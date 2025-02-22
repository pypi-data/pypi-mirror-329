import numpy as np
from LMM import VariableSelection
from matplotlib import pyplot as plt

def main():
    # Generating synthetic dataset
    n_samples, n_features = 500, 900

    # Features matrix
    X = np.random.randn(n_samples, n_features)

    # True coefficient vector with many zero coefficients
    beta = np.random.randn(n_features, 1)
    beta[np.array(np.random.choice(range(n_features), 850))] = 0

    # Outcome variable
    y = np.dot(X, beta).reshape([n_samples])

    # Initialize the VariableSelection model
    model = VariableSelection(fdr=False, acceleration=True)

    # Fit the model to data
    model.fit(X, y)

    neg_log_p = model.getNegLogP()  # negative log of p-value
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
    plt.savefig('combined_plots_test.png')
    plt.close()


if __name__ == "__main__":
    main()