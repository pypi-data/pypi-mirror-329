from effconnpy import CausalityAnalyzer
import numpy as np
# Generate sample time series
data = np.random.rand(100, 3)
analyzer = CausalityAnalyzer(data)
results = analyzer.causality_test(method='transfer_entropy')
print(results)
binary_matrix = create_connectivity_matrix_GC(results, threshold=0.05, metric='p_value')
