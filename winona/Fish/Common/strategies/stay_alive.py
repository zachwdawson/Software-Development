from game_tree import GameStateTree


class StayAlive(object):

    def __init__(self, tree: GameStateTree):
        self.decision_tree = tree
        self.current_player = self.decision_tree.state.current_player

    def traverse(self, node, value, policy_map=None) -> int:
        if policy_map is None:
            policy_map = {}

        if node.state.current_player == self.current_player:
            value += 1

            for next_node in node.get_children():
                new_node_value = self.traverse(next_node, value, policy_map)
                if new_node_value > value:
                    value = new_node_value
                    policy_map[node.state] = next_node

        else:
            for next_node in node.get_children():
                value = max(self.traverse(next_node, value, policy_map), value)

        return value

    def build_policy(self):
        policy_map = {}
        self.traverse(node=self.decision_tree, value=0, policy_map=policy_map)
        return lambda state: policy_map[state]
