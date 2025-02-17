# Image Classification STM32 Model Deployment

This tutorial demonstrates how to deploy a pre-trained image classification model built with TensorFlow Lite (.tflite), Keras (.h5), or (.ONNX) on an STM32 board using STM32Cube.AI.

## <a id="">Table of contents</a>
### <a href="#1">1. Before You Start</a>
#### <a href="#1-1">1.1 Hardware Setup</a>
#### <a href="#1-2">1.2 Software Requirements</a>
#### <a href="#1-3">1.3 Specifications</a>
### <a href="#2">2. Configure the yaml file</a>
#### <a href="#2-1">2.1 Setting the model and the operation mode</a>
#### <a href="#2-2">2.2 Dataset Configuration</a>
#### <a href="#2-3">2.3 Deployment Parameters</a>
#### <a href="#2-4">2.4 Hydra and MLflow settings</a>
### <a href="#3">3. Deploy pretrained model on STM32 board</a>


__________________________________________

## <a id="1">1. Before You Start</a>
### <a id="1-1">1.1 Hardware Setup</a>

The [stm32ai application code](../../stm32ai_application_code/image_classification/README.md) runs on a hardware setup consisting of an STM32 microcontroller board connected to a camera module board. This version supports the following boards only:

- [STM32H747I-DISCO](https://www.st.com/en/product/stm32h747i-disco)
- [B-CAMS-OMV](https://www.st.com/en/product/b-cams-omv)

### <a id="1-2">1.2 Software Requirements</a>

You need to download and install the following software:

- [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html)
- If using [STM32Cube.AI](https://www.st.com/en/embedded-software/x-cube-ai.html) locally, open the link and download the package, then extract both `.zip` and `.pack` files.

### <a id="1-3"> 1.3 Specifications</a>

- `serie`: STM32H7
- `IDE`: GCC
- `resizing`: nearest
- Supports only 8-bits quantized TFlite model, i.e. `quantize`: True if model not quantized
- `quantization_input_type`: int8 or uint8
- `quantization_output_type`: float

## <a id="2"> 2. Configure the YAML File</a>

You can use the deployment service by using a model zoo pre-trained model from the [STM32 model zoo](../pretrained_models/README.md) or your own image classification model. Please refer to the YAML file [deployment_config.yaml](../src/config_file_examples/deployment_config.yaml), which is a ready YAML file with all the necessary sections ready to be filled, or you can update the [user_config.yaml](../src/user_config.yaml) to use it.

As an example, we will show how to deploy the model [mobilenet_v2_0.35_128_fft_int8.tflite](../pretrained_models/mobilenetv2/ST_pretrainedmodel_public_dataset/flowers/mobilenet_v2_0.35_128_fft) pre-trained on the Flowers dataset using the necessary parameters provided in [mobilenet_v2_0.35_128_fft_config.yaml](../pretrained_models/mobilenetv2/ST_pretrainedmodel_public_dataset/flowers/mobilenet_v2_0.35_128_fft/mobilenet_v2_0.35_128_fft_config.yaml).

### <a id="2-1"> 2.1 Setting the Model and the Operation Mode

The first section of the configuration file is the `general` section that provides information about your project and the path to the model you want to deploy. The `operation_mode` attribute should be set to `deployment` as follows:

```yaml
general:
   model_path: ../pretrained_models/mobilenetv2/ST_pretrainedmodel_public_dataset/flowers/mobilenet_v2_0.35_128_fft/mobilenet_v2_0.35_128_fft_int8.tflite

operation_mode: deployment
```

In the `general` section, users must provide the path to their model file using the `model_path` attribute. This can be either a Keras model file with a `.h5` filename extension (float model), a TensorFlow Lite model file with a `.tflite` filename extension (quantized model), or an ONNX model with a `.onnx` filename extension.
In this example, the path to the MobileNet V2 model is provided in the `model_path` parameter. Please check out the [STM32 model zoo](../pretrained_models/README.md) for more image classification models.

You must copy the `preprocessing` section to your own configuration file, to ensure you have the correct preprocessing parameters.

### <a id="2-2"> 2.2 Dataset Configuration

Configure the **dataset** section in the YAML file as follows:

```yaml
dataset:
  class_names: [daisy, dandelion, roses, sunflowers, tulips]
```
The `class_names` attribute specifies the classes that the model is trained on. This information must be provided in the YAML file, as there is no dataset from which the classes can be inferred.

### <a id="2-3"> 2.3 Deployment parameters</a>

To deploy the model in **STM32H747I-DISCO** board, we will use *STM32Cube.AI* to convert the model into optimized C code and *STM32CubeIDE* to build the C application and flash the board.

These steps will be done automatically by configuring the **tools** and **deployment** sections in the YAML file as the following:

```yaml
tools:
   stm32ai:
      version: 8.1.0
      optimization: balanced
      on_cloud: True
      path_to_stm32ai: C:/Users/<XXXXX>/STM32Cube/Repository/Packs/STMicroelectronics/X-CUBE-AI/<*.*.*>/Utilities/windows/stm32ai.exe
   path_to_cubeIDE: C:/ST/STM32CubeIDE_1.10.1/STM32CubeIDE/stm32cubeide.exe

deployment:
   c_project_path: ../../stm32ai_application_code/image_classification/
   IDE: GCC
   verbosity: 1
   hardware_setup:
      serie: STM32H7
      board: STM32H747I-DISCO
      input: CAMERA_INTERFACE_DCMI
      output: DISPLAY_INTERFACE_USB
```

where:
- `version` - Specify the **STM32Cube.AI** version used to benchmark the model, e.g. **8.1.0**.
- `optimization` - *String*, define the optimization used to generate the C model, options: "*balanced*", "*time*", "*ram*".
- `path_to_stm32ai` - *Path* to stm32ai executable file to use local download, else **False**.
- `path_to_cubeIDE` - *Path* to stm32cubeide executable file.
- `c_project_path` - *Path* to [stm32ai application code](../../stm32ai_application_code/image_classification/README.md) project.
- `IDE` -**GCC**, only supported option for *stm32ai application code*.
- `verbosity` - *0* or *1*. Mode 0 is silent, and mode 1 displays messages when building and flashing C application on STM32 target.
- `serie` - **STM32H7**, only supported option for *stm32ai application code*.
- `board` - **STM32H747I-DISCO** or **NUCLEO-H743ZI2**, see the [README](../../stm32ai_application_code/image_classification/README.md) for more details. 
- `input` - **CAMERA_INTERFACE_DCMI**, **CAMERA_INTERFACE_USB** or **CAMERA_INTERFACE_SPI**.
- `output`- **DISPLAY_INTERFACE_USB** or **DISPLAY_INTERFACE_SPI**.

#### <a id="2-4">2.4 Hydra and MLflow settings</a>

The `mlflow` and `hydra` sections must always be present in the YAML configuration file. The `hydra` section can be used to specify the name of the directory where experiment directories are saved and/or the pattern used to name experiment directories. With the YAML code below, every time you run the Model Zoo, an experiment directory is created that contains all the directories and files created during the run. The names of experiment directories are all unique as they are based on the date and time of the run.

```yaml
hydra:
   run:
      dir: ./experiments_outputs/${now:%Y_%m_%d_%H_%M_%S}
```

The `mlflow` section is used to specify the location and name of the directory where MLflow files are saved, as shown below:

```yaml
mlflow:
   uri: ./experiments_outputs/mlruns
```

## <a id="3">3. Deploy pretrained model on STM32 board</a>

First you need to connect the camera board to the *STM32H747I-DISCO* discovery board, then connect the discovery board to your computer using an usb cable.

The picture below shows how to connect the camera board to the *STM32H747I-DISCO* board using a flat flex cable:

![plot](./doc/img/hardware_setup.JPG)

If you chose to modify the [user_config.yaml](../src/user_config.yaml) you can deploy the model by running the following command from the **src/** folder to build and flash the application on your board::

```bash
python stm32ai_main.py 
```
If you chose to update the [deployment_config.yaml](../src/config_file_examples/deployment_config.yaml) and use it then run the following command from the **src/** folder to build and flash the application on your board:: 

```bash
python stm32ai_main.py --config-path ./config_file_examples/ --config-name deployment_config.yaml
```

If you have a Keras model that has not been quantized and you want to quantize it before deploying it, you can use the `chain_qd` tool to quantize and deploy the model sequentially. To do this, update the [chain_qd_config.yaml](../src/config_file_examples/chain_qd_config.yaml) file and then run the following command from the `src/` folder to build and flash the application on your board:

```bash
python stm32ai_main.py --config-path ./config_file_examples/ --config-name chain_qd_config.yaml
```

When the application is running on the *STM32H747I-DISCO* discovery board, the LCD displays the following information:
- Data stream from camera board
- Class name with confidence score in % concerning the output class with the highest
probability (Top1)
- The model inference time (in milliseconds)
- The number of frames processed per second (FPS) by the model

![plot](./doc/img/output_application.JPG)
