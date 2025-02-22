# evopt
### User Friendly Data-Driven Numerical Optimisation
`evopt` is a package for efficient parameter optimization using the CMA-ES (Covariance Matrix Adaptation Evolution Strategy) algorithm. It provides a user-friendly way to find the best set of parameters for a given problem, especially when the problem is complex, non-linear, and doesn't have easily calculable derivatives.

## What it Does

The `evopt` package provides a simple and efficient way to perform parameter optimization using the CMA-ES (Covariance Matrix Adaptation Evolution Strategy) algorithm. It's designed to be a user-friendly tool for finding the best set of parameters for a given problem, especially when the problem is complex, non-linear, and doesn't have easily calculable derivatives.

## Scope

*   **Focus**: The primary focus is on providing a CMA-ES-based optimization routine that is easy to set up and use.
*   **Parameter Optimization**: The package is designed for problems where you need to find the optimal values for a set of parameters.
*   **Function-Value-Free Optimization**: It is designed to work without needing derivative information.
*   **Directory Management**: The package includes robust directory management to organize results, checkpoints, and logs.
*   **Logging**: It provides logging capabilities to track the optimization process.
*   **Checkpointing**: It supports saving and loading checkpoints to resume interrupted optimization runs.
*   **CSV Output**: It writes results and epoch data to CSV files for easy analysis.

## Potential Use Cases

1.  **Calibration of Simulation Models**:
    *   **Scenario**: You have a complex simulation model (e.g., in engineering, physics, or finance) with several adjustable parameters. You want to find the parameter values that make the simulation output match real-world data as closely as possible.
    *   **`evopt` Use**: You can define the parameters and their bounds in `evopt`, write an evaluator function that compares the simulation output to the real data, and then use `evopt` to automatically find the best parameter values.

2.  **Fine-Tuning Machine Learning Models**:
    *   **Scenario**: You have a machine learning model with hyperparameters that need to be tuned for optimal performance.
    *   **`evopt` Use**: You can define the hyperparameters and their ranges, use a validation set to evaluate the model's performance with different hyperparameter settings, and then use `evopt` to find the best hyperparameter configuration.

3.  **Optimizing Engineering Designs**:
    *   **Scenario**: You're designing an engineering component (e.g., an airfoil, a bridge, or a circuit) and want to find the dimensions or material properties that maximize performance (e.g., lift, strength, or efficiency).
    *   **`evopt` Use**: You can create a simulation or model of the component's performance, define the design parameters and their constraints, and then use `evopt` to find the optimal design.

4.  **Parameter Estimation in Scientific Models**:
    *   **Scenario**: You have a scientific model (e.g., in biology, chemistry, or climate science) and want to estimate the values of certain parameters based on experimental data.
    *   **`evopt` Use**: You can define the parameters and their plausible ranges, write an evaluator function that compares the model's predictions to the experimental data, and then use `evopt` to find the parameter values that best fit the data.

5.  **Automated Experiment Design**:
    *   **Scenario**: You want to design a series of experiments to efficiently explore a parameter space and gather data for a model.
    *   **`evopt` Use**: You can use `evopt` to suggest the next set of experiments to run, based on the results of previous experiments. The evaluator function would then be the process of running the experiment and collecting the data.

## Key Advantages

*   **Ease of Use**: Simple API for defining parameters, evaluator, and optimization settings.
*   **Derivative-Free**: Works well for problems where derivatives are unavailable or difficult to compute.
*   **Robustness**: CMA-ES is a powerful optimization algorithm that can handle non-convex and noisy problems.
*   **Organization**: Automatic directory management and logging for easy tracking and analysis.

## Installation

You can install the package using `pip`:

```
pip install evopt
```

## Usage

Here is an example of how to use the `evopt` package to optimise the Rosenbrock function:

```python
import evopt

# Define your parameters, their bounds, and evaluator function
params = {
    'param1': (-5, 5),
    'param2': (-5, 5),
}
def evaluator(param_dict):
    # Your evaluation logic here, in this case the Rosenbrock function
    p1 = param_dict['param1']
    p2 = param_dict['param2']
    return (1-p1)**2 + 100*(p2-p1**2)**2

# Run the optimisation using .optimise method
evopt.optimise(params, evaluator)
```

Here is the corresponding output:

```terminal
Starting new CMAES run in directory path\to\base\dir\evolve_1
Epoch 0 | (1/16) | Params: [1.477, -2.369] | Error: 2069.985
Epoch 0 | (2/16) | Params: [-2.644, -1.651] | Error: 7481.172
Epoch 0 | (3/16) | Params: [0.763, -4.475] | Error: 2557.411
Epoch 0 | (4/16) | Params: [4.269, -0.929] | Error: 36687.174
Epoch 0 | (5/16) | Params: [-1.879, -4.211] | Error: 5999.711
Epoch 0 | (6/16) | Params: [4.665, -2.186] | Error: 57374.982
Epoch 0 | (7/16) | Params: [-1.969, -2.326] | Error: 3856.201
Epoch 0 | (8/16) | Params: [-1.588, -3.167] | Error: 3244.840
Epoch 0 | (9/16) | Params: [-2.191, -2.107] | Error: 4780.562
Epoch 0 | (10/16) | Params: [2.632, -0.398] | Error: 5369.439
Epoch 0 | (11/16) | Params: [-2.525, -1.427] | Error: 6099.094
Epoch 0 | (12/16) | Params: [4.161, -2.418] | Error: 38955.920
Epoch 0 | (13/16) | Params: [-0.435, -1.422] | Error: 261.646
Epoch 0 | (14/16) | Params: [-0.008, -3.759] | Error: 1414.379
Epoch 0 | (15/16) | Params: [-4.243, -0.564] | Error: 34496.083
Epoch 0 | (16/16) | Params: [0.499, -3.170] | Error: 1169.217
Epoch 0 | Mean Error: 13238.614 | Sigma Error: 17251.295
Epoch 0 | Mean Parameters: [0.062, -2.286] | Sigma parameters: [2.663, 1.187]
Epoch 0 | Normalised Sigma parameters: [1.065, 0.475]
...
Epoch 21 | Mean Error: 2.315 | Sigma Error: 0.454
Epoch 21 | Mean Parameters: [-0.391, 0.192] | Sigma parameters: [0.140, 0.154]
Epoch 21 | Normalised Sigma parameters: [0.056, 0.062]
Terminating after meeting termination criteria at epoch 22.
```

## Directory Structure

When you run an optimization with `evopt`, it creates the following directory structure to organize the results:

```
base_directory/
└── evolve_{dir_id}/
    ├── epochs/
    │   └── epoch0000/
    │       └── solution0000/
    │       └── solution0001/
    │       └── ...
    │   └── epoch0001/
    │       └── ...
    │   └── ...
    ├── checkpoints/
    │   └── checkpoint_epoch0000.pkl
    │   └── checkpoint_epoch0001.pkl
    │   └── ...
    ├── logs/
    │   └── logfile.log
    ├── epochs.csv
    └── results.csv
```

*   `base_directory`: This is the base directory where the optimization runs are stored. If not specified, it defaults to the current working directory.
*   `evolve_{dir_id}`: Each optimization run gets its own directory named `evolve_{dir_id}`, where `dir_id` is a unique integer.
*   `epochs`: This directory contains subdirectories for each epoch of the optimization.
*   `epoch####`: Each epoch directory contains subdirectories for each solution evaluated in that epoch.
*   `solution####`: Each solution directory can contain files generated by the evaluator function for that specific solution.
*   `checkpoints`: This directory stores checkpoint files, allowing you to resume interrupted optimization runs.
*   `logs`: This directory contains the log file (`logfile.log`) which captures the output of the optimization process.
*   `epochs.csv`: This file contains summary statistics for each epoch, such as mean error, parameter values, and sigma values.
*   `results.csv`: This file contains the results for each solution evaluated during the optimization, including parameter values and the corresponding error.

## Citing
If you publish research making use of this library, we encourage you to cite this repository:
> Hart-Villamil, R. (2024). Evopt, simple but powerful gradient-free numerical optimisation.

This library makes fundamental use of the `pycma` implementation of the state-of-the-art CMA-ES algorithm.
Hence we kindly ask that research using this library cites:
> Nikolaus Hansen, Youhei Akimoto, and Petr Baudis. CMA-ES/pycma on Github. Zenodo, DOI:10.5281/zenodo.2559634, February 2019.


## License

This project is licensed under the GNU General Public License v3.0 License.
