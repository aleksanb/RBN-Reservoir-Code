use ndarray::{Array2};
use rand::{self, thread_rng, Rng};
use utils;

type NodeState = u8;

#[derive(Debug)]
pub struct RBN {
    n_nodes: usize,
    connectivity: usize,
    output_connectivity: usize,
    initial_state: Vec<NodeState>,
    neighbors: Array2<usize>,
    rules: Array2<NodeState>,
    input_nodes: Vec<usize>,
}

impl RBN {
    pub fn new(n_nodes: usize, connectivity: usize, input_connectivity: usize) -> Self {
        let mut state = vec![0; n_nodes];
        for item in state.iter_mut() {
            *item = rand::random::<NodeState>() % 2;
        }

        let neighbors = Array2::<usize>::from_shape_fn(
            (n_nodes, connectivity), |_| rand::random::<usize>() % n_nodes);

        let rules = Array2::<NodeState>::from_shape_fn(
            (n_nodes, 2usize.pow(connectivity as u32)),
            |_| rand::random::<NodeState>() % 2);

        let mut input_nodes: Vec<_> = (0..n_nodes).collect();
        thread_rng().shuffle(&mut input_nodes);
        input_nodes.truncate(input_connectivity);

        RBN {
            n_nodes: n_nodes,
            connectivity: connectivity,
            output_connectivity: n_nodes,
            initial_state: state,
            neighbors: neighbors,
            rules: rules,
            input_nodes: input_nodes,
        }
    }

    fn advance_from(&self, current_state: Vec<u8>) -> Vec<u8> {
        self.neighbors.inner_iter()
            .enumerate()
            .map(|(node_id, node_neighbors)| {
                let states: Vec<_> = node_neighbors.iter()
                    .map(|item| current_state[*item])
                    .collect();
                let rule = utils::polyval(&states);
                self.rules[[node_id, rule as usize]]
            })
            .collect()
    }

    pub fn execute(&self, inputs: &[NodeState]) -> Vec<NodeState> {
        let mut intermediate_states = Vec::with_capacity(inputs.len() * self.n_nodes);
        let mut current_state = self.initial_state.clone();

        for input in inputs {
            for input_node in &self.input_nodes {
                current_state[*input_node] = input.clone();
            }

            current_state = self.advance_from(current_state);
            intermediate_states.extend(current_state.clone());
        }

        intermediate_states
    }
}
