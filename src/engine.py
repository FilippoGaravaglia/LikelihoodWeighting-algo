from typing import Dict
class InferenceEngine:
    def __init__(self, bayes_net, sampler):
        self.bn = bayes_net
        self.sampler = sampler

    def estimate_posterior(
        self,
        evidence: dict[str,int],
        query_node_name: str,
        num_samples: int
    ) -> Dict[str, float]:
        query_id = self.bn.get_node(query_node_name)
        outcome_count = self.bn.get_outcome_count(query_id)

        samples, weights = self.sampler.likelihood_weighting(evidence, num_samples)
        total_weight = sum(weights)

        weighted_counts = [0.0] * outcome_count
        for sample, w in zip(samples, weights):
            qv = sample[query_id]
            weighted_counts[qv] += w

        posterior = [wc / total_weight for wc in weighted_counts]
        outcome_names = [
            self.bn.get_outcome_id(query_id, i)
            for i in range(outcome_count)
        ]
        return dict(zip(outcome_names, posterior))