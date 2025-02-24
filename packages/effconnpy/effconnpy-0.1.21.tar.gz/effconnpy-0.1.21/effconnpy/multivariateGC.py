import numpy as np
import pandas as pd
from typing import Union, List, Optional, Dict
import statsmodels.api as sm
from statsmodels.tsa.api import VAR
import scipy.stats as stats
from .utils import validate_input

class MultivariateGrangerCausality:
    def __init__(self, data: Union[np.ndarray, pd.DataFrame, List[np.ndarray]]):
        """
        Initialize Multivariate Granger Causality analyzer
        
        Args:
            data: Input time series data
        """
        self.data = validate_input(data)
        
        # Detect number of time series
        if len(self.data.shape) == 1:
            self.num_series = 1
            self.data = self.data.reshape(-1, 1)
        else:
            self.num_series = self.data.shape[1]
        
        # Convert to DataFrame for VAR analysis
        self.df = pd.DataFrame(self.data)
    
    def _compute_likelihood(self, var_results, restricted_params):
        """
        Compute log-likelihood for restricted model
        
        Args:
            var_results: Original VAR model results
            restricted_params: Restricted parameter matrix
        
        Returns:
            Log-likelihood of restricted model
        """
        T = var_results.nobs
        k = self.num_series
        
        # Get residuals using restricted parameters
        y = var_results.model.endog[var_results.k_ar:]
        x = var_results.model.exog
        
        # Compute residuals using restricted parameters
        beta = restricted_params.values.reshape(-1, k)
        resid = y - np.dot(x, beta)
        
        # Compute covariance matrix
        sigma = np.dot(resid.T, resid) / T
        
        # Compute log-likelihood
        llf = -(T * k / 2) * (1 + np.log(2 * np.pi)) - (T / 2) * np.log(np.linalg.det(sigma))
        
        return llf

    def multivariate_granger_causality(self, max_lag: int = 1, verbose: bool = False) -> Dict:
        """
        Perform Multivariate Granger Causality test using VAR model
        
        Args:
            max_lag: Maximum number of lags to test
            verbose: Whether to print detailed results
        
        Returns:
            Dictionary of Granger Causality test results
        """
        # Univariate case
        if self.num_series == 1:
            return {"error": "Granger Causality requires multiple time series"}
        
        # Prepare results dictionary
        causality_results = {}
        
        # Fit VAR model
        var_model = VAR(self.df)
        var_results = var_model.fit(maxlags=max_lag)
        
        # Perform Granger causality test for each variable
        for target in range(self.num_series):
            causality_results[f"Series_{target}"] = {}
            
            for predictor in range(self.num_series):
                if target != predictor:
                    # Get original parameters
                    params = var_results.params.copy()
                    
                    # Create restricted parameters by setting coefficients to zero
                    restricted_params = params.copy()
                    for lag in range(1, max_lag + 1):
                        col_name = f"L{lag}.{predictor}"
                        if col_name in restricted_params.index:
                            restricted_params.loc[col_name] = 0
                    
                    # Calculate log-likelihood ratio
                    llf_unrestricted = var_results.llf
                    llf_restricted = self._compute_likelihood(var_results, restricted_params)
                    llr = 2 * (llf_unrestricted - llf_restricted)
                    
                    # Degrees of freedom (number of restrictions)
                    df = max_lag
                    
                    # Chi-square test
                    p_value = 1 - stats.chi2.cdf(llr, df)
                    
                    result = {
                        "log_likelihood_ratio": llr,
                        "p_value": p_value,
                        "significant": p_value < 0.05
                    }
                    
                    causality_results[f"Series_{target}"][f"Series_{predictor}_cause"] = result
                    
                    if verbose:
                        print(f"Granger Causality from Series {predictor} to Series {target}:")
                        print(f"Log-Likelihood Ratio: {llr}")
                        print(f"p-value: {p_value}")
                        print(f"Significant: {p_value < 0.05}\n")
        
        return causality_results
