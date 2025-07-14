import random
from typing import Tuple

class LikelihoodWeightingSampler:
    def __init__(self, bayes_net):
        self.bn = bayes_net

    def weighted_sample(
        self,
        evidence: dict[str,int],
        topo_order: list[int]
    ) -> Tuple[dict[int,int], float]:
        sample: dict[int,int] = {}
        weight = 1.0

        for node_id in topo_order:
            name = self.bn.get_node_name(node_id)
            definition = self.bn.get_node_definition(node_id)
            parent_ids = self.bn.get_parents(node_id)
            parent_vals = [sample[p] for p in parent_ids]

            if name in evidence:
                obs = evidence[name]
                idx = self.bn.get_cpt_index(node_id, parent_vals, obs)
                p = definition[idx]
                weight *= p
                sample[node_id] = obs
            else:
                num_out = self.bn.get_outcome_count(node_id)
                probs = [
                    definition[self.bn.get_cpt_index(node_id, parent_vals, val)]
                    for val in range(num_out)
                ]
                r = random.random()
                cumulativeSum = 0.0
                chosen = num_out - 1
                for i, pr in enumerate(probs):
                    cumulativeSum += pr
                    if r < cumulativeSum:
                        chosen = i
                        break
                sample[node_id] = chosen

        return sample, weight

    def likelihood_weighting(
        self,
        evidence: dict[str,int],
        num_samples: int
    ) -> Tuple[list[dict[int,int]], list[float]]:
        topo_order = self.bn.get_topological_order()
        samples: list[dict[int,int]] = []
        weights: list[float] = []
        for _ in range(num_samples):
            s, w = self.weighted_sample(evidence, topo_order)
            samples.append(s)
            weights.append(w)
        return samples, weights