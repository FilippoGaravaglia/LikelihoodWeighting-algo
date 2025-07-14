import pysmile_license     # deve essere importato PRIMA di pysmile.Network()
import pysmile

class BayesianNetwork:
    def __init__(self, xdsl_path: str):
        self.network = pysmile.Network()
        self.network.read_file(xdsl_path)

    def get_parents(self, node_id: int) -> list[int]:
        return self.network.get_parents(node_id)

    def get_outcome_count(self, node_id: int) -> int:
        return self.network.get_outcome_count(node_id)

    def get_node_definition(self, node_id: int) -> list[float]:
        return self.network.get_node_definition(node_id)

    def get_node_name(self, node_id: int) -> str:
        return self.network.get_node_name(node_id)

    def get_node(self, node_name: str) -> int:
        return self.network.get_node(node_name)

    def get_outcome_id(self, node_id: int, idx: int) -> str:
        return self.network.get_outcome_id(node_id, idx)

    def get_cpt_index(
        self,
        node_id: int,
        parent_vals: list[int],
        child_val: int
    ) -> int:
        parents = self.get_parents(node_id)
        parent_sizes = [self.get_outcome_count(p) for p in parents]
        offset = 0
        for i, v in enumerate(parent_vals):
            stride = 1
            for size in parent_sizes[i+1:]:
                stride *= size
            offset += v * stride
        num_child = self.get_outcome_count(node_id)
        return offset * num_child + child_val

    def get_topological_order(self) -> list[int]:
        nodes = list(self.network.get_all_nodes())
        parent_map = {n: set(self.get_parents(n)) for n in nodes}
        order = []
        no_parents = [n for n, prs in parent_map.items() if not prs]
        while no_parents:
            n = no_parents.pop(0)
            order.append(n)
            for m, prs in parent_map.items():
                if n in prs:
                    prs.remove(n)
                    if not prs:
                        no_parents.append(m)
        return order