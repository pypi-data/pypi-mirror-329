from hierarchical_mechanism_LDP import Private_Tree
import numpy as np

# test Quantile
B = 4000
b = 4
eps = 1
q = 0.4
protocol = 'unary_encoding'
tree = Private_Tree(B, b)
data = np.random.randint(0, B, 100000)
# get quantile of the data
true_quantile = np.quantile(data, q)
# get private quantile
tree.update_tree(data, eps, protocol)
tree.compute_cdf()
private_quantile = tree.get_quantile(q)
print(f"Closest item to {q}: {private_quantile}")
print(f"True quantile: {true_quantile}")

# test range query
left = 1000
right = 2000
true_range_query = np.sum(data >= left) - np.sum(data >= right)
private_range_query = tree.get_range_query(left, right, normalized=False)
print(f"True range query: {true_range_query}")
print(f"Private range query: {private_range_query}")