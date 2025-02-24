use pyo3::prelude::*;
use rand::seq::IndexedRandom;

// return p value tstats for the amount of permutations given
#[pyfunction]
fn test(perm: usize, group_0: Vec<f64>, group_1: Vec<f64> ) -> PyResult<(f64, Vec<f64>)> {
    // calculate the initial tstat
    let init_tstat = calc_tstat(group_0.clone(), group_1.clone());

    // assign labels to the different groups
    let mut labels : Vec<bool> = Vec::new();
    for _i in 0..group_0.len(){
        labels.push(false);
    }
    for _i in 0..group_1.len(){
        labels.push(true);
    }
    
    // make a data variable from the different groups
    let data = [group_0, group_1].concat();

    // create a varable to put the randomised t-stats in
    let mut rand_tstat : Vec<f64> = Vec::new();

    // make a loop for the length of permutations
    for _i in 0..perm{

        // create randomised labels
        let mut rng = &mut rand::rng();
        let rand_labels: Vec<bool> = labels.choose_multiple(&mut rng, labels.len()).cloned().collect();
        
        // use these labels to assign data to a group
        let mut group_0 : Vec<f64>= Vec::new();
        let mut group_1 : Vec<f64>= Vec::new();
        for j in 0..rand_labels.len(){
            if rand_labels[j] == true {
                group_1.push(data[j]);
            }
            else {
                group_0.push(data[j]);
            }
        }

        // calculate the tstat for these groups and add it to the randomised tstats
        rand_tstat.push(calc_tstat(group_0,group_1));

    }
    // use calculated and initial tstats to calculate a p value

    let p_value = calc_p_value(init_tstat, rand_tstat.clone());


    Ok((p_value, rand_tstat))
}

// calculate the tstat of the difference of two groups
#[pyfunction]
fn calc_tstat (group_0: Vec<f64>, group_1: Vec<f64>) -> f64 {

    // calculate the amount of data in each group
    let n_0 = group_0.len() as f64;
    let n_1 = group_1.len() as f64;

    // use this to calculate the mean in each group
    let mean_0 = calc_mean(&group_0, n_0);
    let mean_1 = calc_mean(&group_1, n_1);

    // use this to calculate the standard deviation^2 of both groups
    let sigma_0_sqrd = calc_sigma_squared(group_0, mean_0, n_0);
    let sigma_1_sqrd = calc_sigma_squared(group_1, mean_1, n_1);

    // use these to calculate the standard deviation of the difference in means
    let s = (((n_0 - 1.0) * sigma_0_sqrd + (n_1 - 1.0) * sigma_1_sqrd) * (1.0 / n_0 + 1.0 / n_1) / (n_0 + n_1 - 2.0)).sqrt();

    // calculate t-test
    (mean_0 - mean_1) / s
        
}

fn calc_p_value(initial:f64, permutations: Vec<f64>) -> f64 {
    // use the amount and tstats of the permutations and initial tstat to calculate the p value
    let perms = permutations.len() as f64;
    let mut p_value : f64 = 0.0;
    for i in permutations{
        if i <= initial {
            p_value = p_value + 1.0 / perms ;
        }
    }
    p_value
}



fn calc_mean(group:&Vec<f64>, n: f64) -> f64 {
    // calculate the mean as the sum of the data divided by its length
    let mut mean : f64 = 0.0;
    for i in group {
        mean = mean + i/n;
    }
    mean
}
fn calc_sigma_squared(group: Vec<f64>,mean:f64, n :f64) -> f64{
    // calculate the sigma^2 as the sum of (x-mean)^2 / (N-1)
    let mut sigma_squared : f64 = 0.0;
    for i in group {
        sigma_squared = sigma_squared + (i - mean) * (i-mean) / (n-1.0);
    }
    sigma_squared
}



/// A Python module implemented in Rust.
#[pymodule]
fn perm_test(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(test, m)?)?;
    m.add_function(wrap_pyfunction!(calc_tstat, m)?)?;
    Ok(())
}
