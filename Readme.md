# CSVC-PSO Project

Welcome to our code repository for the CSVC-PSO project, which implements a clustering-based support vector classifier for dynamic time-linkage optimization.

## Features
- **Supports solving various optimization problems**: The project is designed to solve a range of complex optimization problems in dynamic environments.
- **Flexible parameter configuration**: Easily adjust algorithm parameters through the `configs.py` file to fit different experimental needs.
- **Efficient algorithm implementation**: The project leverages parallel computing and efficient data handling methods to enhance performance.

## Project Structure

The project directory is organized as follows:

```
CSVC-PSO/
├── csvc_component/
│   ├── buffer.py                
│   ├── CSVC_Model.py
│   ├── demo.py
│   ├── MPB.py
│   ├── Pearsonr.py
│   ├── PSO.py
├── data_save/
│   ├── fig_data/
│   ├── run_data/
├── draw_tool/
│   ├── draw.py
│   ├── test_all.py
│   ├── utils.py
├── configs.py                  
├── main.py                    
```

### Key Files Description

- **`csvc_component/`**: Contains the core components for the CSVC and PSO algorithms.
  - `buffer.py`: Manages data buffering during the optimization process.
  - `CSVC_Model.py`: Defines the CSVC model and its functionalities.
  - `demo.py`: Demonstrates the usage of the CSVC and PSO components.
  - `MPB.py`: Implements the Moving Peaks Benchmark (MPB) for dynamic optimization.
  - `Pearsonr.py`: Computes Pearson correlation coefficients.
  - `PSO.py`: Contains the implementation of the Particle Swarm Optimization (PSO) algorithm.

- **`data_save/`**: Stores generated data and figures.
  - `fig_data/`: Stores the generated figures from the optimization process.
  - `run_data/`: Contains the raw data generated during the optimization runs.

- **`draw_tool/`**: Contains utilities for visualizing the optimization results.
  - `draw.py`: Functions for plotting and visualizing data.
  - `test_all.py`: A script to test all drawing functionalities.
  - `utils.py`: Utility functions to support drawing operations.

- **`configs.py`**: Contains configuration settings for the optimization and drawing processes.

- **`main.py`**: The main execution script for running the entire dynamic time-linkage optimization workflow.

### Detailed Description of `main.py`

The `main.py` script is the central entry point for this project, orchestrating the dynamic time-linkage optimization process. It handles data generation, execution of optimization algorithms, and visualization of results. Below is a brief description of the key functions in `main.py`:

- **`run_data()`**: Initializes the data generation process, manages parallel computation using multiprocessing, and handles the iteration over different time factors (`b_list`).

- **`run_one(sample_id, save_path, rand_seed, b)`**: Runs the core algorithms (CSVC_PSO, Optimal, PSO_only) for a specific sample and time factor, recording execution time and saving the results.

- **`draw_fit(filename)`**: Reads the generated data and produces visualizations of the optimization results, saving the figures to the appropriate directory.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/GaomMeng/CSVC-PSO.git
   ```

2. Navigate into the project directory:

   ```bash
   cd CSVC-PSO
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage Example

To run the project, you will need to adjust the configuration parameters as needed and then execute the `main.py` script from the terminal. Below is a guide to the main parameters in `configs.py` and a simple usage example.

### Key Configuration Parameters in `configs.py`

- **`rand_seed`**: A random seed for reproducibility. Default is `10086`.
- **`MPB_seed`**: Seed for the Moving Peaks Benchmark. Default is `123`.
- **`filename`**: The directory path where the run data will be saved. Default is `'data_save/run_data'`.
- **`sample_num`**: The number of samples to be generated for each time factor. Default is `20`.
- **`b_list`**: A list of time factors to iterate over, which influences the dynamics of the optimization process. Default is `[10, 50, 100]`.
- **`using_multiprocessing`**: Boolean flag to enable multiprocessing for faster computations. Default is `True`.

### Other Parameters

- **MPB Parameters**: Control the dimensionality, peak number, and other aspects of the Moving Peaks Benchmark.
- **PSO Parameters**: Configure the Particle Swarm Optimization, such as population size and iteration number.
- **Model Parameters**: Define the mode of operation (e.g., `csvc`), and parameters related to the Support Vector Classifier (SVC).

### Running the Project

1. Modify the configuration in `configs.py` as necessary for your experiment.
2. Open your terminal and run:

   ```bash
   python main.py
   ```

This will:
- Initialize and execute the data generation and optimization algorithms.
- Use multiprocessing to speed up the process if enabled.
- Automatically generate visualizations of the results.

## Bibliography

We welcome you to use our code for your research and projects. If you use this codebase or the methodologies in your work, please consider citing us using the following formats:

### BibTeX Entry:
```bibtex
@INPROCEEDINGS{10371998,
  author={Gao, Meng and Liu, Xiao-Fang and Zhan, Zhi-Hui and Zhang, Jun},
  booktitle={2023 IEEE Symposium Series on Computational Intelligence (SSCI)}, 
  title={A Clustering-Based Support Vector Classifier for Dynamic Time-Linkage Optimization}, 
  year={2023},
  pages={953-958},
  doi={10.1109/SSCI52147.2023.10371998}
}
```

### IEEE Citation:
```
M. Gao, X. -F. Liu, Z. -H. Zhan and J. Zhang, "A Clustering-Based Support Vector Classifier for Dynamic Time-Linkage Optimization," 2023 IEEE Symposium Series on Computational Intelligence (SSCI), Mexico City, Mexico, 2023, pp. 953-958, doi: 10.1109/SSCI52147.2023.10371998.
```

We hope this documentation helps you understand and utilize the CSVC-PSO project effectively. If you use this code, please cite our work using the provided BibTeX and IEEE citation formats.

