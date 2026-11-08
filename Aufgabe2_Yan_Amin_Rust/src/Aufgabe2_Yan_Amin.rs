use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader},
    time::Instant,
};

use colored::*;

type Choreography = Vec<usize>;

#[derive(Debug)]
struct Figure {
    name: String,
    takte: usize,
    data: [u8; 16],
    dist: usize,
}

impl Figure {
    /// # Example
    /// input line: "Cast_Up 4 BCDEFGHIJKLMNOPA"
    /// output: Figure {
    ///     name: "Cast_Up",
    ///     takte: 4,
    ///     data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0],
    ///     dist: 30,
    /// }
    pub fn from_line(line: &str) -> Self {
        let slice: Vec<&str> = line.split(' ').collect();
        let [name, takte, data] = slice[..] else {
            panic!()
        };
        let data: [u8; 16] = data
            .bytes()
            .map(|c| c - b'A')
            .collect::<Vec<u8>>()
            .try_into()
            .unwrap();

        Self {
            name: name.to_string(),
            takte: takte.parse().unwrap(),
            data,
            dist: data
                .iter()
                .enumerate()
                .map(|(i, &v)| i.abs_diff(v as usize))
                .sum(),
        }
    }

    // inline is probably not necessary, but you never know
    // constant space because [u8; 16] is always 16 bytes
    // constant time because map is called on a constant sized array
    #[inline]
    pub fn apply_transformation(&self, config: [u8; 16]) -> [u8; 16] {
        config.map(|i| self.data[i as usize])
    }
}

// path: resources/choreo0X.txt
fn calculate_file(path: &str) {     
    // --- read the file ---
    let f = File::open(path).unwrap();
    let br = BufReader::new(f);
    let mut lines = br.lines();

    let takte_total: usize = lines.next().unwrap().unwrap().parse().unwrap();
    // figure count, not important
    _ = lines.next().unwrap().unwrap();
    // read figures
    let figures: Vec<Figure> = lines.map(|l| Figure::from_line(&l.unwrap())).collect();

    // --- set up backtracking ---
    let mut choreographies: Vec<Choreography> = Vec::new();

    // call the backtracking function to collect all the valid choreograhies
    backtrack_recursively(
        &mut Vec::new(),
        takte_total,
        ORDER_CONFIG,
        &figures,
        &mut choreographies,
        figures.iter().map(|f| f.takte).min().unwrap(),
    );

    if choreographies.is_empty() {
        println!("{}", "No choreographies can be constructed".bold().yellow());
        return;
    }

    println!(
        "{}",
        format!(
            "{} choreographies can be constructed in total",
            choreographies.len()
        )
        .bold()
        .green()
    );

    let first = &choreographies[0];
    let first_dist = first.iter().map(|&i| figures[i].dist).sum();
    let first_count = first.len();
    let first_unique_count = first.iter().collect::<HashSet<&usize>>().len();

    let mut max_count = first_count;
    let mut max_count_path = first.clone();
    let mut min_count = first_count;
    let mut min_count_path = first.clone();
    let mut max_uniques = first_unique_count;
    let mut max_uniques_path = first.clone();
    let mut min_dist = first_dist;
    let mut min_dist_path = first.clone();
    let mut max_dist = first_dist;
    let mut max_dist_path = first.clone();

    for seq in &choreographies[1..] {
        let dist: usize = seq.iter().map(|i| figures[*i].dist).sum();
        let total_count = seq.len();
        let unique_count = seq.iter().collect::<HashSet<&usize>>().len();

        if total_count < min_count {
            min_count = total_count;
            min_count_path = seq.clone();
        }
        if total_count > max_count {
            max_count = total_count;
            max_count_path = seq.clone();
        }
        if unique_count > max_uniques {
            max_uniques = unique_count;
            max_uniques_path = seq.clone();
        }
        if dist < min_dist {
            min_dist = dist;
            min_dist_path = seq.clone();
        }
        if dist > max_dist {
            max_dist = dist;
            max_dist_path = seq.clone();
        }
    }

    print_category(&figures, "most figures", max_count, max_count_path);
    print_category(&figures, "least figures", min_count, min_count_path);
    print_category(&figures, "most different", max_uniques, max_uniques_path);
    print_category(&figures, "most distance", max_dist, max_dist_path);
    print_category(&figures, "least distance", min_dist, min_dist_path);
}

const ORDER_CONFIG: [u8; 16] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];

fn backtrack_recursively(
    unfinished_choreo: &mut Choreography,
    takte_left: usize,
    config: [u8; 16],
    figures: &[Figure],
    choreographies: &mut Vec<Choreography>,
    min_choreo_takte: usize,
) {
    // base case
    if takte_left < min_choreo_takte {
        if takte_left == 0 && config == ORDER_CONFIG {
            // this sequence is a valid choreography
            choreographies.push(unfinished_choreo.clone());
        }
        return;
    }

    figures
        .iter()
        .enumerate()
        .filter(|(_, f)| f.takte <= takte_left)
        .for_each(|(i, f)| {
            unfinished_choreo.push(i);
            backtrack_recursively(
                unfinished_choreo,
                takte_left - f.takte,
                f.apply_transformation(config),
                figures,
                choreographies,
                min_choreo_takte,
            );
            unfinished_choreo.pop();
        });
}

// ---------- Not important, mostly IO ----------

const TEST_INPUT_FOLDER: &str = "resources";
fn main() {
    let total_timer = Instant::now();

    let file_names = (1..=6)
        .map(|i| format!("choreo{:02}", i))
        .chain(std::iter::once("choreoA".to_string()));

    for file_name in file_names {
        let timer = Instant::now();
        println!("Datei: {}", file_name);
        calculate_file(&format!("{TEST_INPUT_FOLDER}/{file_name}.txt"));
        println!("Took {:?}", timer.elapsed());
        println!();
    }

    println!("Total time: {:?}", total_timer.elapsed());
}

fn print_category(figures: &[Figure], name: &str, count: usize, path: Choreography) {
    let path: Vec<&String> = path.into_iter().map(|i| &figures[i].name).collect();
    println!("{} ({}): {:#?}", name, count.to_string().bold(), path);
    // println!("{:<14} ({:^5}): {:?}", name, count.to_string().bold(), path);
}
