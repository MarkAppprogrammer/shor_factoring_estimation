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

"""Used for origonal spacetime volume graphs"""
# fileName = 'openingdata1e3wrunway(1).csv'
# mydata = extract_data(fileName)

# fileNameEx = 'gid+ekera(more).csv'
# mydataEx = extract_dataEx(fileNameEx)

# fileNameEx2 = 'gou.csv'
# mydataEx2 = extract_dataEx(fileNameEx2)

# dataExtended = {
#     'RSA_size': [row[0] for row in mydata],
#     'GE_time': [row[1] for row in mydataEx],
#     'GS_time': [row[1] for row in mydataEx2],
#     'New_time': [row[1] for row in mydata]
# }
# dataExtended = pd.DataFrame(dataExtended)

fileName = 'openingdata1e3wrunway(1).csv'
mydata = extract_data(fileName, onevar=False)

fileNameEx = 'gid+ekera(more).csv'
mydataEx = extract_dataEx(fileNameEx, onevar=False)

fileNameEx2 = 'gou.csv'
mydataEx2 = extract_dataEx(fileNameEx2, onevar=False)

"""Note GE_time and others refer to spacetimevolume but we kept as time to make it easier"""

dataExtraExtended = {
    'RSA_size': [row[0] for row in mydata],
    'GE_time': [row[1] for row in mydataEx],
    'GS_time': [row[1] for row in mydataEx2],
    'New_time': [row[1] for row in mydata],
    'GE_qubits': [row[2] for row in mydataEx],
    'GS_qubits': [row[2] for row in mydataEx2],
    'New_qubits': [row[2] for row in mydata],
    'GE_days': [row[3] for row in mydataEx],
    'GS_days': [row[3] for row in mydataEx2],
    'New_days': [row[3] for row in mydata]
}
dataExtraExtended = pd.DataFrame(dataExtraExtended)

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
dataExtraExtended['log_RSA_size'] = np.log(dataExtraExtended['RSA_size'])
dataExtraExtended['log_GE_time'] = np.log(dataExtraExtended['GE_time'])
dataExtraExtended['log_GS_time'] = np.log(dataExtraExtended['GS_time'])
dataExtraExtended['log_New_time'] = np.log(dataExtraExtended['New_time'])

# Add log-transformed qubit and day columns
dataExtraExtended['log_GE_qubits'] = np.log(dataExtraExtended['GE_qubits'])
dataExtraExtended['log_GS_qubits'] = np.log(dataExtraExtended['GS_qubits'])
dataExtraExtended['log_New_qubits'] = np.log(dataExtraExtended['New_qubits'])

dataExtraExtended['log_GE_days'] = np.log(dataExtraExtended['GE_days'])
dataExtraExtended['log_GS_days'] = np.log(dataExtraExtended['GS_days'])
dataExtraExtended['log_New_days'] = np.log(dataExtraExtended['New_days'])

# Fit linear models on log-log data
lm_ge_loglog = smf.ols(formula='log_GE_time ~ log_RSA_size', data=dataExtraExtended).fit()
lm_gs_loglog = smf.ols(formula='log_GS_time ~ log_RSA_size', data=dataExtraExtended).fit()
lm_new_loglog = smf.ols(formula='log_New_time ~ log_RSA_size', data=dataExtraExtended).fit()

# Linear models for qubits
lm_ge_qubits_loglog = smf.ols(formula='log_GE_qubits ~ log_RSA_size', data=dataExtraExtended).fit()
lm_gs_qubits_loglog = smf.ols(formula='log_GS_qubits ~ log_RSA_size', data=dataExtraExtended).fit()
lm_new_qubits_loglog = smf.ols(formula='log_New_qubits ~ log_RSA_size', data=dataExtraExtended).fit()

# Linear models for days
lm_ge_days_loglog = smf.ols(formula='log_GE_days ~ log_RSA_size', data=dataExtraExtended).fit()
lm_gs_days_loglog = smf.ols(formula='log_GS_days ~ log_RSA_size', data=dataExtraExtended).fit()
lm_new_days_loglog = smf.ols(formula='log_New_days ~ log_RSA_size', data=dataExtraExtended).fit()

# Predict over same range
log_rsa_range = np.log(rsa_range)
df_log_pred = pd.DataFrame({'log_RSA_size': log_rsa_range})

ge_loglog_pred = np.exp(lm_ge_loglog.predict(df_log_pred))
gs_loglog_pred = np.exp(lm_gs_loglog.predict(df_log_pred))
new_loglog_pred = np.exp(lm_new_loglog.predict(df_log_pred))

# Predict for qubits
ge_qubits_loglog_pred = np.exp(lm_ge_qubits_loglog.predict(df_log_pred))
gs_qubits_loglog_pred = np.exp(lm_gs_qubits_loglog.predict(df_log_pred))
new_qubits_loglog_pred = np.exp(lm_new_qubits_loglog.predict(df_log_pred))

# Predict for days
ge_days_loglog_pred = np.exp(lm_ge_days_loglog.predict(df_log_pred))
gs_days_loglog_pred = np.exp(lm_gs_days_loglog.predict(df_log_pred))
new_days_loglog_pred = np.exp(lm_new_days_loglog.predict(df_log_pred))


intercept_ge = lm_ge_days_loglog.params['Intercept']
intercept_gs = lm_gs_days_loglog.params['Intercept']
intercept_new = lm_new_days_loglog.params['Intercept']
slope_ge = lm_ge_days_loglog.params['log_RSA_size']
slope_gs = lm_gs_days_loglog.params['log_RSA_size']
slope_new = lm_new_days_loglog.params['log_RSA_size']

a_ge = np.exp(intercept_ge)
a_gs = np.exp(intercept_gs)
a_new = np.exp(intercept_new)

print(f"Intercept for GE_qubits model (log(a)): {intercept_ge}, a: {a_ge}, b: {slope_ge}")
print(f"Intercept for GS_qubits model (log(a)): {intercept_gs}, a: {a_gs}, b: {slope_gs}")
print(f"Intercept for New_qubits model (log(a)): {intercept_new}, a: {a_new}, b: {slope_new}")

print(lm_ge_days_loglog.summary())
print(lm_gs_days_loglog.summary())
print(lm_new_days_loglog.summary())

# Plot log-log regression predictions
"""
Plotting for spacetime volume

plt.figure(figsize=(10, 6))
plt.plot(rsa_range, ge_loglog_pred, label='GE Volume Prediction', color='red', linestyle='-.')
plt.plot(rsa_range, gs_loglog_pred, label='GS Volume Prediction', color='purple', linestyle='-.')
plt.plot(rsa_range, new_loglog_pred, label='New Volume Prediction', color='green', linestyle='-.')
plt.scatter(dataExtraExtended['RSA_size'], dataExtraExtended['GE_time'], color='red', label='GE Volume (Actual)', marker='o')
plt.scatter(dataExtraExtended['RSA_size'], dataExtraExtended['GS_time'], color='purple', label='GS Volume (Actual)', marker='^')
plt.scatter(dataExtraExtended['RSA_size'], dataExtraExtended['New_time'], color='green', label='New Volume (Actual)', marker='x')

plt.xlabel('RSA Key Size (bits)')
plt.ylabel('Expected Volume (Megaqubitdays)')
plt.title('RSA Key Size vs Expected Volume')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.yscale('log')  # Log scale
plt.xscale('log')  # Log scale for RSA size
plt.show()
"""

# Plot log-log regression predictions for qubits
"""
plt.figure(figsize=(10, 6))
plt.plot(rsa_range, ge_qubits_loglog_pred, label='GE Qubits Prediction', color='red', linestyle='-.')
plt.plot(rsa_range, gs_qubits_loglog_pred, label='GS Qubits Prediction', color='purple', linestyle='-.')
plt.plot(rsa_range, new_qubits_loglog_pred, label='New Qubits Prediction', color='green', linestyle='-.')

plt.scatter(dataExtraExtended['RSA_size'], dataExtraExtended['GE_qubits'], color='red', label='GE Qubits (Actual)', marker='o')
plt.scatter(dataExtraExtended['RSA_size'], dataExtraExtended['GS_qubits'], color='purple', label='GS Qubits (Actual)', marker='^')
plt.scatter(dataExtraExtended['RSA_size'], dataExtraExtended['New_qubits'], color='green', label='New Qubits (Actual)', marker='x')

plt.xlabel('RSA Key Size (bits)')
plt.ylabel('Expected Number of Qubits (Millions)')
plt.title('RSA Key Size vs Expected Qubits')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.yscale('log')
plt.xscale('log')
#plt.show()
"""

exit()

# Plot log-log regression predictions for days
plt.figure(figsize=(10, 6))
plt.plot(rsa_range, ge_days_loglog_pred, label='GE Days Prediction', color='red', linestyle='-.')
plt.plot(rsa_range, gs_days_loglog_pred, label='GS Days Prediction', color='purple', linestyle='-.')
plt.plot(rsa_range, new_days_loglog_pred, label='New Days Prediction', color='green', linestyle='-.')

plt.scatter(dataExtraExtended['RSA_size'], dataExtraExtended['GE_days'], color='red', label='GE Days (Actual)', marker='o')
plt.scatter(dataExtraExtended['RSA_size'], dataExtraExtended['GS_days'], color='purple', label='GS Days (Actual)', marker='^')
plt.scatter(dataExtraExtended['RSA_size'], dataExtraExtended['New_days'], color='green', label='New Days (Actual)', marker='x')

plt.xlabel('RSA Key Size (bits)')
plt.ylabel('Expected Runtime (Days)')
plt.title('RSA Key Size vs Expected Runtime (Days)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.yscale('log')  # Log scale for y-axis
plt.xscale('log')  # Log scale for x-axis
#plt.show()


# plt.savefig("C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\graphs\\rsadaysloglogstage3.png", bbox_inches='tight', dpi=300)
# plt.close()

"""
Plot 1 spacetime volume

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

"""
Plot 2 qubits

Intercept for GE_qubits model (log(a)): -6.659076682931891, a: 0.0012823298209607154, b: 1.27565437779418
Intercept for GS_qubits model (log(a)): -6.135593336464388, a: 0.0021644405952855345, b: 0.24613266049657326
Intercept for New_qubits model (log(a)): -6.304152110848795, a: 0.0018286960431270272, b: 0.2564397027210583

graph: "C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\graphs\\rsaqubitsloglogstage3.png"

                            OLS Regression Results
==============================================================================
Dep. Variable:          log_GE_qubits   R-squared:                       0.988
Model:                            OLS   Adj. R-squared:                  0.987
Method:                 Least Squares   F-statistic:                     1502.
Date:                Sat, 26 Apr 2025   Prob (F-statistic):           8.56e-19
Time:                        23:54:54   Log-Likelihood:                 8.6333
No. Observations:                  20   AIC:                            -13.27
Df Residuals:                      18   BIC:                            -11.28
Df Model:                           1
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept       -6.6591      0.312    -21.350      0.000      -7.314      -6.004
log_RSA_size     1.2757      0.033     38.751      0.000       1.206       1.345
==============================================================================
Omnibus:                        0.323   Durbin-Watson:                   1.038
Prob(Omnibus):                  0.851   Jarque-Bera (JB):                0.387
Skew:                          -0.254   Prob(JB):                        0.824
Kurtosis:                       2.547   Cond. No.                         80.7
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
                            OLS Regression Results
==============================================================================
Dep. Variable:          log_GS_qubits   R-squared:                       0.983
Model:                            OLS   Adj. R-squared:                  0.982
Method:                 Least Squares   F-statistic:                     1051.
Date:                Sat, 26 Apr 2025   Prob (F-statistic):           2.03e-17
Time:                        23:54:54   Log-Likelihood:                 37.977
No. Observations:                  20   AIC:                            -71.95
Df Residuals:                      18   BIC:                            -69.96
Df Model:                           1
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept       -6.1356      0.072    -85.316      0.000      -6.287      -5.985
log_RSA_size     0.2461      0.008     32.427      0.000       0.230       0.262
==============================================================================
Omnibus:                        2.345   Durbin-Watson:                   0.834
Prob(Omnibus):                  0.310   Jarque-Bera (JB):                1.862
Skew:                          -0.714   Prob(JB):                        0.394
Kurtosis:                       2.555   Cond. No.                         80.7
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
                            OLS Regression Results
==============================================================================
Dep. Variable:         log_New_qubits   R-squared:                       0.988
Model:                            OLS   Adj. R-squared:                  0.988
Method:                 Least Squares   F-statistic:                     1544.
Date:                Sat, 26 Apr 2025   Prob (F-statistic):           6.67e-19
Time:                        23:54:54   Log-Likelihood:                 41.000
No. Observations:                  20   AIC:                            -78.00
Df Residuals:                      18   BIC:                            -76.01
Df Model:                           1
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept       -6.3042      0.062   -101.962      0.000      -6.434      -6.174
log_RSA_size     0.2564      0.007     39.297      0.000       0.243       0.270
==============================================================================
Omnibus:                        2.296   Durbin-Watson:                   1.456
Prob(Omnibus):                  0.317   Jarque-Bera (JB):                1.828
Skew:                          -0.705   Prob(JB):                        0.401
Kurtosis:                       2.549   Cond. No.                         80.7
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
"""

"""
Plot 3 days

Intercept for GE_qubits model (log(a)): -18.020484970390264, a: 1.4921167860670216e-08, b: 2.1491301253028405
Intercept for GS_qubits model (log(a)): -18.381219438162592, a: 1.0402502464444704e-08, b: 3.0895972507192075
Intercept for New_qubits model (log(a)): -18.405659613109883, a: 1.0151345150366214e-08, b: 3.002284801719819

graph: "C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\graphs\\rsadaysloglogstage3.png"

                            OLS Regression Results
Dep. Variable:            log_GE_days   R-squared:                       0.997
==============================================================================
Model:                            OLS   Adj. R-squared:                  0.997
Method:                 Least Squares   F-statistic:                     6477.
Date:                Sat, 26 Apr 2025   Prob (F-statistic):           1.79e-24
Time:                        23:57:30   Log-Likelihood:                 12.818
No. Observations:                  20   AIC:                            -21.64
Df Residuals:                      18   BIC:                            -19.64
Df Model:                           1
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept      -18.0205      0.253    -71.224      0.000     -18.552     -17.489
log_RSA_size     2.1491      0.027     80.479      0.000       2.093       2.205
==============================================================================
Omnibus:                        4.490   Durbin-Watson:                   1.185
Prob(Omnibus):                  0.106   Jarque-Bera (JB):                1.468
Skew:                          -0.029   Prob(JB):                        0.480
Kurtosis:                       1.674   Cond. No.                         80.7
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
                            OLS Regression Results
==============================================================================
Dep. Variable:            log_GS_days   R-squared:                       1.000
Model:                            OLS   Adj. R-squared:                  1.000
Method:                 Least Squares   F-statistic:                 1.312e+05
Date:                Sat, 26 Apr 2025   Prob (F-statistic):           3.20e-36
Time:                        23:57:30   Log-Likelihood:                 35.641
No. Observations:                  20   AIC:                            -67.28
Df Residuals:                      18   BIC:                            -65.29
Df Model:                           1
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept      -18.3812      0.081   -227.417      0.000     -18.551     -18.211
log_RSA_size     3.0896      0.009    362.168      0.000       3.072       3.108
==============================================================================
Omnibus:                        2.036   Durbin-Watson:                   0.707
Prob(Omnibus):                  0.361   Jarque-Bera (JB):                1.697
Skew:                          -0.650   Prob(JB):                        0.428
Kurtosis:                       2.410   Cond. No.                         80.7
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
                            OLS Regression Results
==============================================================================
Dep. Variable:           log_New_days   R-squared:                       1.000
Model:                            OLS   Adj. R-squared:                  1.000
Method:                 Least Squares   F-statistic:                 6.171e+04
Date:                Sat, 26 Apr 2025   Prob (F-statistic):           2.83e-33
Time:                        23:57:30   Log-Likelihood:                 28.674
No. Observations:                  20   AIC:                            -53.35
Df Residuals:                      18   BIC:                            -51.36
Df Model:                           1
Covariance Type:            nonrobust
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept      -18.4057      0.115   -160.734      0.000     -18.646     -18.165
log_RSA_size     3.0023      0.012    248.410      0.000       2.977       3.028
==============================================================================
Omnibus:                        8.633   Durbin-Watson:                   0.829
Prob(Omnibus):                  0.013   Jarque-Bera (JB):                5.961
Skew:                           1.187   Prob(JB):                       0.0508
Kurtosis:                       4.231   Cond. No.                         80.7
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

"""