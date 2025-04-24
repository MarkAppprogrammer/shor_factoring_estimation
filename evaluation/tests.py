import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from clean import extract_data, extract_dataEx

data = {
    'RSA_size': [2048, 3072, 4096, 8192, 12288, 16384],
    'Old_time': [4.1, 19, 48, 480, 1700, 3900],
    'New_time': [1.15, 4.15, 10.54, 102.31, 389.49, 1011.21]
}
df = pd.DataFrame(data)

fileName = 'C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\circuits\\Shor1991\\Agib25\\openingdata1e3wrunway(1).csv'
mydata = extract_data(fileName)
fileNameEx = 'C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\circuits\\Shor1991\\Agib25\\gid+ekera(more).csv'
mydataEx = extract_dataEx(fileNameEx)

fileNameEx2 = 'C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\circuits\\Shor1991\\Agib25\\gou.csv'
mydataEx2 = extract_dataEx(fileNameEx2)

dataExtended = {
    'RSA_size': [row[0] for row in mydata],
    'GE_time': [row[1] for row in mydataEx],
    'GS_time': [row[1] for row in mydataEx2],
    'New_time': [row[1] for row in mydata]
}
dataExtended = pd.DataFrame(dataExtended)


# glm_ge = smf.glm(formula='GE_time ~ RSA_size', data=dataExtended,
#                   family=sm.families.Gamma(link=sm.families.links.log())).fit()
# glm_gs = smf.glm(formula='GS_time ~ RSA_size', data=dataExtended,
#                   family=sm.families.Gamma(link=sm.families.links.log())).fit()
# glm_new = smf.glm(formula='New_time ~ RSA_size', data=dataExtended,
#                   family=sm.families.Gamma(link=sm.families.links.log())).fit()

# print(glm_ge.summary())
# print(glm_gs.summary())
# print(glm_new.summary())

rsa_range = np.linspace(1000, 70000, 500)
# df_pred = pd.DataFrame({'RSA_size': rsa_range})
# ge_pred = glm_ge.predict(df_pred)
# gs_pred = glm_gs.predict(df_pred)
# new_pred = glm_new.predict(df_pred)


# #Plot 1 (GLM w/ predicted values)

# plt.figure(figsize=(10, 6))
# plt.plot(rsa_range, ge_pred, label='GE_time (Predicted)', color='red', linestyle='--')
# plt.plot(rsa_range, gs_pred, label='GS_time (Predicted)', color='purple', linestyle='--')
# plt.plot(rsa_range, new_pred, label='New_time (Predicted)', color='blue', linestyle='--')
# plt.scatter(dataExtended['RSA_size'], dataExtended['GE_time'], color='red', label='GE_time (Actual)', marker='o')
# plt.scatter(dataExtended['RSA_size'], dataExtended['GS_time'], color='purple', label='GS_time (Actual)', marker='o')
# plt.scatter(dataExtended['RSA_size'], dataExtended['New_time'], color='blue', label='New_time (Actual)', marker='x')

# plt.xlabel('RSA Key Size (bits)')
# plt.ylabel('Execution Time (seconds)')
# plt.title('Gamma GLM: RSA Key Size vs Execution Time')
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.yscale('log')  # Log scale for better visibility
# plt.show()

"""
                 Generalized Linear Model Regression Results (GE)
==============================================================================
Dep. Variable:                GE_time   No. Observations:                   20
Model:                            GLM   Df Residuals:                       18
Model Family:                   Gamma   Df Model:                            1
Link Function:                    log   Scale:                         0.70006
Method:                          IRLS   Log-Likelihood:                -187.04
Date:                Sun, 06 Apr 2025   Deviance:                       29.012
Time:                        20:31:56   Pearson chi2:                     12.6
No. Iterations:                    44   Pseudo R-squ. (CS):             0.9999
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      4.6899      0.276     17.005      0.000       4.149       5.230
RSA_size       0.0002   9.89e-06     17.536      0.000       0.000       0.000
==============================================================================
                 Generalized Linear Model Regression Results (GS)
==============================================================================
Dep. Variable:                GS_time   No. Observations:                   20
Model:                            GLM   Df Residuals:                       18
Model Family:                   Gamma   Df Model:                            1
Link Function:                    log   Scale:                         0.86739
Method:                          IRLS   Log-Likelihood:                -175.53
Date:                Sun, 06 Apr 2025   Deviance:                       34.484
Time:                        20:31:56   Pearson chi2:                     15.6
No. Iterations:                    48   Pseudo R-squ. (CS):             0.9973
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      4.4079      0.307     14.358      0.000       3.806       5.010
RSA_size       0.0002    1.1e-05     14.712      0.000       0.000       0.000
==============================================================================
                 Generalized Linear Model Regression Results (New)
==============================================================================
Dep. Variable:               New_time   No. Observations:                   20
Model:                            GLM   Df Residuals:                       18
Model Family:                   Gamma   Df Model:                            1
Link Function:                    log   Scale:                         0.83654
Method:                          IRLS   Log-Likelihood:                -155.99
Date:                Sun, 06 Apr 2025   Deviance:                       31.939
Time:                        20:31:56   Pearson chi2:                     15.1
No. Iterations:                    46   Pseudo R-squ. (CS):             0.9981
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      3.4355      0.301     11.395      0.000       2.845       4.026
RSA_size       0.0002   1.08e-05     14.941      0.000       0.000       0.000
==============================================================================

Diffrence = e^(Intercept + coef2*RSA_size)
"""

# Add log-transformed columns
dataExtended['log_RSA_size'] = np.log(dataExtended['RSA_size'])
dataExtended['log_GE_time'] = np.log(dataExtended['GE_time'])
dataExtended['log_GS_time'] = np.log(dataExtended['GS_time'])
dataExtended['log_New_time'] = np.log(dataExtended['New_time'])

# Fit linear models on log-log data
lm_ge_loglog = smf.ols(formula='log_GE_time ~ log_RSA_size', data=dataExtended).fit()
lm_gs_loglog = smf.ols(formula='log_GS_time ~ log_RSA_size', data=dataExtended).fit()
lm_new_loglog = smf.ols(formula='log_New_time ~ log_RSA_size', data=dataExtended).fit()

# Predict over same range
log_rsa_range = np.log(rsa_range)
df_log_pred = pd.DataFrame({'log_RSA_size': log_rsa_range})
ge_loglog_pred = np.exp(lm_ge_loglog.predict(df_log_pred))
gs_loglog_pred = np.exp(lm_gs_loglog.predict(df_log_pred))
new_loglog_pred = np.exp(lm_new_loglog.predict(df_log_pred))

# intercept_ge = lm_ge_loglog.params['Intercept']
# intercept_gs = lm_gs_loglog.params['Intercept']
# intercept_new = lm_new_loglog.params['Intercept']
# slope_ge = lm_ge_loglog.params['log_RSA_size']
# slope_gs = lm_gs_loglog.params['log_RSA_size']
# slope_new = lm_new_loglog.params['log_RSA_size']

# a_ge = np.exp(intercept_ge)
# a_gs = np.exp(intercept_gs)
# a_new = np.exp(intercept_new)

# print(f"Intercept for GE_time model (log(a)): {intercept_ge}, a: {a_ge}, b: {slope_ge}")
# print(f"Intercept for GS_time model (log(a)): {intercept_gs}, a: {a_gs}, b: {slope_gs}")
# print(f"Intercept for New_time model (log(a)): {intercept_new}, a: {a_new}, b: {slope_new}")

# Plot log-log regression predictions
plt.figure(figsize=(10, 6))
# plt.plot(rsa_range, ge_loglog_pred, label='GE Volume Prediction', color='red', linestyle='-.')
plt.plot(rsa_range, gs_loglog_pred, label='GS Volume Prediction', color='purple', linestyle='-.')
plt.plot(rsa_range, new_loglog_pred, label='New Volume Prediction', color='green', linestyle='-.')
# plt.scatter(dataExtended['RSA_size'], dataExtended['GE_time'], color='red', label='GE Volume (Actual)', marker='o')
plt.scatter(dataExtended['RSA_size'], dataExtended['GS_time'], color='purple', label='GS Volume (Actual)', marker='^')
plt.scatter(dataExtended['RSA_size'], dataExtended['New_time'], color='green', label='New Volume (Actual)', marker='x')

plt.xlabel('RSA Key Size (bits)')
plt.ylabel('Expected Volume (Megaqubitdays)')
plt.title('RSA Key Size vs Expected Volume')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.yscale('log')  # Log scale
plt.xscale('log')  # Log scale for RSA size
plt.savefig("C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\graphs\\rsavolumeloglogstage2.png", bbox_inches='tight', dpi=300)
plt.close()

"""
Plot 2 (Log-Log Regression)

Results: 

Intercept for GE_time model (log(a)): -24.709261701965794, a: 1.857393797425398e-11, b: 3.4256799999206162
Intercept for GS_time model (log(a)): -24.516812774626985, a: 2.2515598626601837e-11, b: 3.335729911215781
Intercept for New_time model (log(a)): -24.70981172395868, a: 1.85637247088914e-11, b: 3.258724504440877

graph: "C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\graphs\\rsavolumeloglogsstage3.png"

                            OLS Regression Results
==============================================================================
Dep. Variable:            log_GE_time   R-squared:                       0.997
Model:                            OLS   Adj. R-squared:                  0.997
Method:                 Least Squares   F-statistic:                     5435.
Date:                Sun, 06 Apr 2025   Prob (F-statistic):           8.65e-24
Time:                        20:56:07   Log-Likelihood:                 1.7388
No. Observations:                  20   AIC:                            0.5225
Df Residuals:                      18   BIC:                             2.514
Df Model:                           1
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept      -24.7093      0.440    -56.122      0.000     -25.634     -23.784
log_RSA_size     3.4257      0.046     73.720      0.000       3.328       3.523
==============================================================================
Omnibus:                        1.493   Durbin-Watson:                   0.821
Prob(Omnibus):                  0.474   Jarque-Bera (JB):                1.070
Skew:                           0.301   Prob(JB):                        0.586
Kurtosis:                       2.039   Cond. No.                         80.7
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
                            OLS Regression Results
==============================================================================
Dep. Variable:            log_GS_time   R-squared:                       1.000
Model:                            OLS   Adj. R-squared:                  1.000
Method:                 Least Squares   F-statistic:                 5.740e+04
Date:                Sun, 06 Apr 2025   Prob (F-statistic):           5.43e-33
Time:                        20:56:07   Log-Likelihood:                 25.843
No. Observations:                  20   AIC:                            -47.69
Df Residuals:                      18   BIC:                            -45.69
Df Model:                           1
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept      -24.5168      0.132   -185.845      0.000     -24.794     -24.240
log_RSA_size     3.3357      0.014    239.573      0.000       3.306       3.365
==============================================================================
Omnibus:                        6.754   Durbin-Watson:                   0.239
Prob(Omnibus):                  0.034   Jarque-Bera (JB):                5.056
Skew:                          -1.226   Prob(JB):                       0.0798
Kurtosis:                       3.225   Cond. No.                         80.7
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
                            OLS Regression Results
==============================================================================
Dep. Variable:           log_New_time   R-squared:                       1.000
Model:                            OLS   Adj. R-squared:                  1.000
Method:                 Least Squares   F-statistic:                 1.960e+05
Date:                Sun, 06 Apr 2025   Prob (F-statistic):           8.62e-38
Time:                        20:56:07   Log-Likelihood:                 38.590
No. Observations:                  20   AIC:                            -73.18
Df Residuals:                      18   BIC:                            -71.19
Df Model:                           1
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept      -24.7098      0.070   -354.294      0.000     -24.856     -24.563
log_RSA_size     3.2587      0.007    442.693      0.000       3.243       3.274
==============================================================================
Omnibus:                       10.947   Durbin-Watson:                   0.649
Prob(Omnibus):                  0.004   Jarque-Bera (JB):                8.561
Skew:                           1.258   Prob(JB):                       0.0138
Kurtosis:                       4.986   Cond. No.                         80.7
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

"""