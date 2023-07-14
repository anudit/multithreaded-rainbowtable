use indicatif::{ProgressBar, ProgressStyle};
use sha2::{Digest, Sha256};
use std::fs::File;
use std::io::{prelude::*, BufWriter};

fn main() {
    let chunk_size = 50_000_000;
    let total_numbers = 499_999_999;
    let progress_bar = ProgressBar::new(total_numbers);
    progress_bar.set_style(
        ProgressStyle::default_bar()
            .template("{pos}/{len} [{elapsed_precise}] {bar:40.cyan/blue} {percent}%")
            .unwrap(),
    );

    let file = File::create("rainbow_table.csv").expect("Failed to create file");
    let mut writer = BufWriter::new(file);

    for chunk_start in (9_000_000_000..=9_499_999_999).step_by(chunk_size) {
        let chunk_end = chunk_start + chunk_size - 1;
        let chunk_end = chunk_end.min(9_499_999_999);
        let chunk_range = chunk_start..=chunk_end;

        for number in chunk_range {
            let phone_number = format!("{:010}", number);
            let hash = calculate_hash(&phone_number);

            writeln!(writer, "{},{}", phone_number, hash).expect("Failed to write to file");
            progress_bar.inc(1);
        }
    }

    progress_bar.finish();
}

fn calculate_hash(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input);
    let hash = hasher.finalize();
    format!("{:x}", hash)
}
