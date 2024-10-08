
# CSVC-PSO 项目

欢迎来到我们CSVC-PSO项目的代码库，该项目实现了基于聚类的支持向量分类器，用于黑盒动态时链优化问题。

## 功能特性
- **支持多种优化问题的求解**：该项目旨在解决动态环境下的多种复杂优化问题。
- **灵活的参数配置**：通过 `configs.py` 文件可以轻松调整算法参数，以适应不同的实验需求。
- **高效的算法实现**：该项目利用并行计算和高效的数据处理方法来提高性能。

## 项目结构

项目目录组织如下：

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

### 关键文件描述

- **`csvc_component/`**: 包含CSVC和PSO算法的核心组件。
  - `buffer.py`: 在优化过程中管理数据缓冲。
  - `CSVC_Model.py`: 定义CSVC模型及其功能。
  - `demo.py`: 演示CSVC和PSO组件的使用。
  - `MPB.py`: 实现用于动态优化的移动峰基准（MPB）。
  - `Pearsonr.py`: 计算皮尔逊相关系数。
  - `PSO.py`: 包含粒子群优化（PSO）算法的实现。

- **`data_save/`**: 存储生成的数据和图像。
  - `fig_data/`: 存储优化过程中生成的图像。
  - `run_data/`: 包含在优化运行过程中生成的原始数据。

- **`draw_tool/`**: 包含可视化优化结果的工具。
  - `draw.py`: 用于绘制和可视化数据的函数。
  - `test_all.py`: 测试所有绘图功能的脚本。
  - `utils.py`: 支持绘图操作的实用函数。

- **`configs.py`**: 包含优化和绘图过程中的配置设置。

- **`main.py`**: 用于运行整个动态时间关联优化工作流的主要执行脚本。

### `main.py` 的详细描述

`main.py` 脚本是该项目的核心入口，负责协调动态时间关联优化过程。它处理数据生成、优化算法的执行以及结果的可视化。以下是 `main.py` 中关键函数的简要描述：

- **`run_data()`**: 初始化数据生成过程，使用多进程管理并行计算，并处理不同时间因子 (`b_list`) 的迭代。

- **`run_one(sample_id, save_path, rand_seed, b)`**: 针对特定的样本和时间因子运行核心算法（CSVC_PSO、Optimal、PSO_only），记录执行时间并保存结果。

- **`draw_fit(filename)`**: 读取生成的数据并生成优化结果的可视化图像，将图像保存到相应的目录中。

## 安装

1. 将仓库克隆到本地：

   ```bash
   git clone https://github.com/GaomMeng/CSVC-PSO.git
   ```

2. 进入项目目录：

   ```bash
   cd CSVC-PSO
   ```

3. 安装所需依赖：

   ```bash
   pip install -r requirements.txt
   ```

## 使用示例

要运行该项目，您需要根据需要调整配置参数，然后在终端中执行 `main.py` 脚本。以下是 `configs.py` 中主要参数的说明以及一个简单的使用示例。

### `configs.py` 中的关键配置参数

- **`rand_seed`**: 随机种子，用于结果的可重复性。默认值为 `10086`。
- **`MPB_seed`**: 用于移动峰基准（MPB）的种子。默认值为 `123`。
- **`filename`**: 运行数据将保存的目录路径。默认值为 `'data_save/run_data'`。
- **`sample_num`**: 为每个时间因子生成的样本数量。默认值为 `20`。
- **`b_list`**: 一个时间因子列表，影响优化过程的动态性。默认值为 `[10, 50, 100]`。
- **`using_multiprocessing`**: 启用多进程以加快计算的布尔标志。默认值为 `True`。

### 其他参数

- **MPB 参数**: 控制移动峰基准的维度、峰值数量及其他相关设置。
- **PSO 参数**: 配置粒子群优化的参数，如种群大小和迭代次数。
- **模型参数**: 定义操作模式（例如 `csvc`），以及与支持向量分类器（SVC）相关的参数。

### 运行项目

1. 根据实验需要修改 `configs.py` 中的配置。
2. 打开终端并运行：

   ```bash
   python main.py
   ```

这将：
- 初始化并执行数据生成和优化算法。
- 如果启用了多进程，将加快处理速度。
- 自动生成结果的可视化图像。

## 参考文献

我们欢迎您在研究和项目中使用我们的代码。如果您在工作中使用了该代码库或方法，请考虑使用以下格式引用我们：

### BibTeX 条目:
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

### IEEE 引用:
```
M. Gao, X. -F. Liu, Z. -H. Zhan and J. Zhang, "A Clustering-Based Support Vector Classifier for Dynamic Time-Linkage Optimization," 2023 IEEE Symposium Series on Computational Intelligence (SSCI), Mexico City, Mexico, 2023, pp. 953-958, doi: 10.1109/SSCI52147.2023.10371998.
```

我们希望这份文档能够帮助您有效地理解和使用 CSVC-PSO 项目。如果您使用了此代码，请按照提供的 BibTeX 和 IEEE 引用格式引用我们的工作。
