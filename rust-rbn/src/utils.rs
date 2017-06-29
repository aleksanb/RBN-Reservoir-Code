use rand;

pub fn polyval(arr: &[u8]) -> u8 {
    arr.iter()
        .rev()
        .enumerate()
        .map(|(idx, item)| item * (1 << idx))
        .sum()
}

pub fn rand_bits(num_bits: usize) -> Vec<u8> {
    let mut bits = vec![0; num_bits];

    for bit in bits.iter_mut() {
        *bit = rand::random::<u8>() % 2;
    }

    bits
}

#[macro_export]
macro_rules! l {
    ($body:expr, $i:ident <- $iter:expr) => {
        l!($body, $i <- $iter, true);
    };
    ($body:expr, $i:ident <- $iter:expr, $pred:expr) => {{
        let mut temp_vec = Vec::with_capacity($iter.len());
        for $i in $iter {
            if $pred {
                temp_vec.push($body);
            }
        }
        temp_vec
    }};
}

#[macro_export]
macro_rules! p {
    ($e:expr) => (println!("{:?}", $e));
}
