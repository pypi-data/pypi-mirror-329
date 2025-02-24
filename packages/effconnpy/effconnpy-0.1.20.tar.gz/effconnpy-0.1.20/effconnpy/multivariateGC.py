import numpy as np
import pandas as pd
from typing import Union, List, Optional, Dict
import statsmodels.api as sm
from statsmodels.tsa.api import VAR
import scipy.stats as stats
from .utils import validate_input

class MultivariateGrangerCausality:
    def __init__(self, data: Union[np.ndarray, pd.DataFrame, List[np.ndarray]]):
        """Same as before"""
        self.data = validate_input(data)
        
        if len(self.data.shape) == 1:
            self.num_series = 1
            self.data = self.data.reshape(-1, 1)
        else:
            self.num_series = self.data.shape[1]
        
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
        residuals = var_results.resid
        sigma = np.dot(residuals.T, residuals) / len(residuals)
        
        # Compute residuals for restricted model
        y = var_results.model.endog
        x = var_results.model.exog
        restricted_resid = y - np.dot(x, restricted_params)
        
        # Compute covariance matrix for restricted model
        restricted_sigma = np.dot(restricted_resid.T, restricted_resid) / len(restricted_resid)
        
        # Compute log-likelihood
        nobs = len(residuals)
        restricted_llf = -0.5 * (nobs * (self.num_series * np.log(2 * np.pi) + 
                                np.log(np.linalg.det(restricted_sigma))))
        
        return restricted_llf

    def multivariate_granger_causality(self, max_lag: int = 1, verbose: bool = False) -> Dict:
        """Same as before but with modified test statistic calculation"""
        if self.num_series == 1:
            return {"error": "Granger Causality requires multiple time series"}
        
        causality_results = {}
        
        # Fit VAR model
        var_model = VAR(self.df)
        var_results = var_model.fit(maxlags=max_lag)
        
        for target in range(self.num_series):
            causality_results[f"Series_{target}"] = {}
            
            for predictor in range(self.num_series):
                if target != predictor:
                    # Create restricted model
                    restricted_params = var_results.params.copy()
                    mask = [f'L{i+1}.{predictor}' for i in range(max_lag)]
                    for param in mask:
                        if param in restricted_params.index:
                            restricted_params.loc[param] = 0
                    
                    # Calculate test statistic
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
