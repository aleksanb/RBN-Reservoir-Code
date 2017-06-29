extern crate ndarray;
extern crate rand;
extern crate rusty_machine;
use rusty_machine::prelude::*;
use rusty_machine::learning::logistic_reg::LogisticRegressor;

use rand;

#[macro_use]
mod utils;
mod tasks;
mod rbn;

use tasks::{Task, TaskType};

fn main() {
    /*let n_samples = 4000;
    let n_nodes = 400;
    let rbn = rbn::RBN::new(n_nodes, 3, n_nodes / 2);

    let training_set = Task::new(TaskType::TemporalParity,
                                        n_samples,
                                        3);
    let matrix = Matrix::new(
        n_samples, n_nodes,
        l![i as f64, i <- rbn.execute(&training_set.input)]);
    let training_output = Vector::new(l![i as f64, i <- training_set.output]);

    let mut lin_mod = LogisticRegressor::default();
    lin_mod.train(&matrix, &training_output).expect("Training failed");


    let testing_samples = 200;
    let testing_set = Task::new(TaskType::TemporalParity,
                                testing_samples,
                                3);
    let test_result = Matrix::new(
        testing_samples, n_nodes,
        l![i as f64, i <- rbn.execute(&testing_set.input)]);
    let predictions = lin_mod.predict(&test_result).expect("Couldn't predict dataset");


    let mut n_errors = 0;
    for (est, corr) in predictions.iter().zip(testing_set.output) {
        if (est > &0.5) as u8 != corr {
            n_errors += 1;
        }
    }

    let accuracy = 1.0 - ((n_errors as f64) / (predictions.size() as f64));
    p!(n_errors);
    p!(accuracy);*/

    struct Node {
        node_id: u8,
        neighbors: Vec<u8>,
        rule: u64,
    }

    let n_nodes = 64;
    let nodes = Vec::with_capacity(n_nodes);
    for node_id in 0..n_nodes {
        nodes.push(Node {
            node_id: node_id,
            neighbors: vec![
                rand::random::<u8>() % n_nodes,
                rand::random::<u8>() % n_nodes,
                rand::random::<u8>() % n_nodes,
            ],
            rule: rand::random::<u8>()
        });
    }

    // Reversed, node 0 is far right, node 1 next to far right
    let prev_state = 0u64;
    let next_state = 0u64;

    for Node { node_id, neighbors, rule } in nodes {
        let rule_idx = 0u8;
        for neighbor in neighbors {

            let neighbor_state = ((prev_state >> i) & 1) << i;
        }

        let n1 = rbn_state >> idx1 & 1;
        let n2 = rbn_state >> idx2 & 1;
        let n3 = rbn_state >> idx3 & 1;

        let rule_idx = n1 << 2 + n2 << 1 + n3 << 0;

        let state = (rules[node_id] >> rule_idx & 1) << node_id;
    }

    let rules = 2 3
}
