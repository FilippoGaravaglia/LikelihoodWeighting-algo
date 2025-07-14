from network import BayesianNetwork
from sampler import LikelihoodWeightingSampler
from engine import InferenceEngine

if __name__ == "__main__":
    # 1) Carico la rete
    bn = BayesianNetwork("complex_network.xdsl")

    # 2) Imposto evidenza e parametri
    evidence = {"E": 0}     # E=True
    query = "D"
    num_samples = 1000

    # 3) Istanzio sampler ed engine
    sampler = LikelihoodWeightingSampler(bn)
    engine = InferenceEngine(bn, sampler)

    # 4) Calcolo posterior
    posterior = engine.estimate_posterior(evidence, query, num_samples)

    # 5) Stampo
    print(f"Distribuzione a posteriori di '{query}' dato E=True:")
    for outcome, prob in posterior.items():
        print(f"  {outcome}: {prob:.4f}")