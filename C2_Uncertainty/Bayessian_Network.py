from pomegranate import *
# from pomegranate import DiscreteDistribution as pome_DiscreteDistribution 
# d2 = Exp([0.8, 1.4, 4.1])


# # Define nodes representing random variables
# weather = pomegranate.DiscreteDistribution({'sunny': 0.7, 'rainy': 0.3})
# traffic = ConditionalProbabilityTable(
#     [['sunny', 'low', 0.9],
#      ['sunny', 'high', 0.1],
#      ['rainy', 'low', 0.2],
#      ['rainy', 'high', 0.8]],
#     [weather]
# )

# late_to_work = ConditionalProbabilityTable(
#     [['sunny', 'low', 'no', 0.95],
#      ['sunny', 'low', 'yes', 0.05],
#      ['sunny', 'high', 'no', 0.7],
#      ['sunny', 'high', 'yes', 0.3],
#      ['rainy', 'low', 'no', 0.8],
#      ['rainy', 'low', 'yes', 0.2],
#      ['rainy', 'high', 'no', 0.1],
#      ['rainy', 'high', 'yes', 0.9]],
#     [weather, traffic]
# )

# # Create state objects for each random variable
# s1 = State(weather, name='weather')
# s2 = State(traffic, name='traffic')
# s3 = State(late_to_work, name='late_to_work')

# # Create a Bayesian network and add the states
# network = BayesianNetwork()
# network.add_states(s1, s2, s3)

# # Add edges to represent dependencies
# network.add_edge(s1, s2)
# network.add_edge(s1, s3)
# network.add_edge(s2, s3)

# # Finalize the network
# network.bake()

# # Query the network for probabilities
# result = network.predict_proba({'weather': 'sunny', 'traffic': 'low'})
# print(result)