# Saliency Unlearning Algorithm for Machine Unlearning

This repository provides an implementation of the Saliency Unlearning algorithm for machine unlearning in Stable Diffusion models. The Saliency Unlearning algorithm allows you to remove specific concepts or styles from a pre-trained model without retraining it from scratch.

### Installation
```
pip install unlearn_diff
```
### Prerequisities
Ensure `conda` is installed on your system. You can install Miniconda or Anaconda:

- **Miniconda** (recommended): [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- **Anaconda**: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)

After installing `conda`, ensure it is available in your PATH by running. You may require to restart the terminal session:

```bash
conda --version
```
### Create environment:
```
create_env <algorithm_name>
```
eg: ```create_env saliency_unlearning```

### Activate environment:
```
conda activate <environment_name>
```
eg: ```conda activate saliency_unlearning```

The <algorithm_name> has to be one of the folders in the `mu/algorithms` folder.

### Downloading data and models.
After you install the package, you can use the following commands to download.

1. **Dataset**:
  - **i2p**:
    - **Sample**:
     ```
     download_data sample i2p
     ```
    - **Full**:
     ```
     download_data full i2p
     ```
  - **quick_canvas**:
    - **Sample**:
     ```
     download_data sample quick_canvas
     ```
    - **Full**:
     ```
     download_data full quick_canvas
     ```

2. **Model**:
  - **compvis**:
    ```
    download_model compvis
    ```
  - **diffuser**:
    ```
    download_model diffuser
    ```

**Verify the Downloaded Files**

After downloading, verify that the datasets have been correctly extracted:
```bash
ls -lh ./data/i2p-dataset/sample/
ls -lh ./data/quick-canvas-dataset/sample/
```
---

## Usage

To train the saliency unlearning algorithm to unlearn a specific concept or style from the Stable Diffusion model, use the `train.py` script located in the `scripts` directory.

**Step 1: Generate mask**

```bash
python -m mu.algorithms.saliency_unlearning.scripts.generate_mask \
--config_path mu/algorithms/saliency_unlearning/configs/mask_config.yaml
```
### Run Train
Create a file, eg, `my_trainer.py` and use examples and modify your configs to run the file.  

**Example Code**
```python
from mu.algorithms.saliency_unlearning.algorithm import (
    SaliencyUnlearningAlgorithm,
)
from mu.algorithms.saliency_unlearning.configs import (
    saliency_unlearning_train_mu,
)

algorithm = SaliencyUnlearningAlgorithm(
    saliency_unlearning_train_mu,
    output_dir="/opt/dlami/nvme/outputs",
)
algorithm.run()
```

**Running the Training Script in Offline Mode**

```bash
WANDB_MODE=offline python my_trainer.py
```

**How It Works** 
* Default Values: The script first loads default values from the train config file as in configs section.

* Parameter Overrides: Any parameters passed directly to the algorithm, overrides these configs.

* Final Configuration: The script merges the configs and convert them into dictionary to proceed with the training. 


**Similarly, you can pass arguments during runtime to generate mask.**

**How It Works** 
* Default Values: The script first loads default values from the YAML file specified by --config_path.

* Command-Line Overrides: Any arguments passed on the command line will override the corresponding keys in the YAML configuration file.

* Final Configuration: The script merges the YAML file and command-line arguments into a single configuration dictionary and uses it for training.


### Directory Structure

- `algorithm.py`: Implementation of the SaliencyUnlearnAlgorithm class.
- `configs/`: Contains configuration files for training and generation.
- `model.py`: Implementation of the SaliencyUnlearnModel class.
- `scripts/train.py`: Script to train the SaliencyUnlearn algorithm.
- `trainer.py`: Implementation of the SaliencyUnlearnTrainer class.
- `utils.py`: Utility functions used in the project.
- `data_handler.py` : Implementation of DataHandler class

---
<br>

**The unlearning has two stages:**

1. Generate the mask 

2. Unlearn the weights.

<br>

### Description of Arguments in mask_config.yaml

The `config/mask_config.yaml` file is a configuration file for generating saliency masks using the `scripts/generate_mask.py` script. It defines various parameters related to the model, dataset, output, and training. Below is a detailed description of each section and parameter:

**Model Configuration**

These parameters specify settings for the Stable Diffusion model and guidance configurations.

* c_guidance: Guidance scale used during loss computation in the model. Higher values may emphasize certain features in mask generation.
    
    * Type: float
    * Example: 7.5

* batch_size: Number of images processed in a single batch.

    * Type: int
    * Example: 4

* ckpt_path: Path to the model checkpoint file for Stable Diffusion.

    * Type: str
    * Example: /path/to/compvis.ckpt

* model_config_path: Path to the model configuration YAML file for Stable Diffusion.

    * Type: str
    * Example: /path/to/model_config.yaml

* num_timesteps: Number of timesteps used in the diffusion process.

    * Type: int
    * Example: 1000

* image_size: Size of the input images used for training and mask generation (in pixels).

    * Type: int
    * Example: 512


**Dataset Configuration**

These parameters define the dataset paths and settings for mask generation.

* raw_dataset_dir: Path to the directory containing the original dataset, organized by themes and classes.

    * Type: str
    * Example: /path/to/raw/dataset

* processed_dataset_dir: Path to the directory where processed datasets will be saved after mask generation.

    * Type: str
    * Example: /path/to/processed/dataset

* dataset_type: Type of dataset being used.

    * Choices: unlearncanvas, i2p
    * Type: str
    * Example: i2p

* template: Type of template for mask generation.

    * Choices: object, style, i2p
    * Type: str
    * Example: style

* template_name: Specific template name for the mask generation process.

    * Example Choices: self-harm, Abstractionism
    * Type: str
    * Example: Abstractionism

* threshold: Threshold value for mask generation to filter salient regions.

    * Type: float
    * Example: 0.5

**Output Configuration**

These parameters specify the directory where the results are saved.

* output_dir: Directory where the generated masks will be saved.

    * Type: str
    * Example: outputs/saliency_unlearning/masks


**Training Configuration**

These parameters control the training process for mask generation.

* lr: Learning rate used for training the masking algorithm.

    * Type: float
    * Example: 0.00001

* devices: CUDA devices used for training, specified as a comma-separated list.

    * Type: str
    * Example: 0

* use_sample: Flag indicating whether to use a sample dataset for training and mask generation.

    * Type: bool
    * Example: True


### Description of Arguments train_config.yaml

The `scripts/train.py` script is used to fine-tune the Stable Diffusion model to perform saliency-based unlearning. This script relies on a configuration file (`config/train_config.yaml`) and supports additional runtime arguments for further customization. Below is a detailed description of each argument:

**General Arguments**

* alpha: Guidance scale used to balance the loss components during training.
    
    * Type: float
    * Example: 0.1

* epochs: Number of epochs to train the model.
    
    * Type: int
    * Example: 5

* train_method: Specifies the training method or strategy to be used.

    * Choices: noxattn, selfattn, xattn, full, notime, xlayer, selflayer
    * Type: str
    * Example: noxattn

* model_config_path: Path to the model configuration YAML file for Stable Diffusion.
    
    * Type: str
    * Example: 'mu/algorithms/saliency_unlearning/configs/model_config.yaml'


**Dataset Arguments**

* raw_dataset_dir: Path to the directory containing the raw dataset, organized by themes and classes.

    * Type: str
    * Example: 'path/raw_dataset/'

* processed_dataset_dir: Path to the directory where the processed dataset will be saved.

    * Type: str
    * Example: 'path/processed_dataset_dir'

* dataset_type: Specifies the type of dataset to use for training.

    * Choices: unlearncanvas, i2p
    * Type: str
    * Example: i2p

* template: Specifies the template type for training.

    * Choices: object, style, i2p
    * Type: str
    * Example: style

* template_name: Name of the specific template used for training.

    * Example Choices: self-harm, Abstractionism
    * Type: str
    * Example: Abstractionism


**Output Arguments**

* output_dir: Directory where the fine-tuned model and training outputs will be saved.

    * Type: str
    * Example: 'output/folder_name'

* mask_path: Path to the saliency mask file used during training.

    * Type: str
    * Example: 



