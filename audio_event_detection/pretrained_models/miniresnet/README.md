# Quantized miniresnet

## **Use case** : [AED](../../src/README.md)

# Model description

ResNets are well known image classification models, that use skip-connections between blocks of convolutional layers to address gradient vanishing and explosion problems.

However, they are also widely used in AED and Audio classification, by converting the audio to a mel-spectrogram, and passing that as input to the model.


MiniResNet is based on the ResNet implementation found in tensorflow, and is a resized version of a ResNet18 with a custom block function. These blocks are then assembled in stacks, and the user can specify the number of stacks desired, with more stacks resulting in a larger network.

A note on pooling : In some of our pretrained models, we do not use a pooling function at the end of the convolutional backbone, as is traditionally done. Because of the small number of convolutional blocks, the number of filters is low even for larger model sizes, leading to a low embedding size after pooling.
We found that in many cases we obtain a better performance / model size / inference time tradeoff by not performing any pooling. This makes the linear classification layer larger, but in cases with a relatively low number of classes, this remains cheaper than adding more convolutional blocks.

Naturally, you are able to set the type of pooling you wish to use when training a model, whether from scratch or using transfer learning.

The MiniResNet backbones provided in the model zoo are pretrained on [FSD50K](https://zenodo.org/records/4060432)


Source implementation : https://keras.io/api/applications/resnet/

Papers : [ResNet](https://arxiv.org/abs/1512.03385)

## Network information


| Network Information     |  Value          |
|-------------------------|-----------------|
|  Framework              | TensorFlow Lite |
|  Params 1stack          | 135K            |
|  Params 2stacks         | 450K            |
|  Quantization           | int8            |
|  Provenance             | https://keras.io/api/applications/resnet/ |

## Network inputs / outputs
The pre-trained networks expects patches of shape (64, 50, 1), with 64 mels and 50 frames per patch.

When training from scratch, you can specify whichever input shape you desire.

It outputs embedding vectors of size 2048 for the 2 stacks version, and 3548 for the 1 stack version. If you use the model zoo scripts to perform transfer learning or training from scratch, a classification head with the specified number of classes will automatically be added to the network.

## Recommended platforms

| Platform | Supported | Recommended |
|----------|-----------|-----------|
| STM32U5  |[x]|[x]|


# Performances

## Training 

To train a MiniResNet model with pretrained weights you need to configure the [user_config.yaml](../../src/README.md) file following the [documentation](../../src/README.md).
Additionally, a shorter tutorial focused on model training is available [here](../../src/training/README.md)

As an example, the [miniresnet_1stacks_64x50_tl_config.yaml](ST_pretrainedmodel_public_dataset/esc10/miniresnet_1stacks_64x50_tl/miniresnet_1stacks_64x50_tl_config.yaml) file is used to train a 1-stack MiniResNet on the ESC10 dataset. You can copy its content in the [user_config.yaml](../../src/README.md) file to reproduce the results presented below.


## Metrics


Measures are done with default STM32Cube.AI configuration with enabled input / output allocated option.


### Reference MCU memory footprint based on ESC-10 dataset


| Model             | Format | Resolution | Series  | Activation RAM (kB) | Runtime RAM (kB) | Weights Flash (kB) | Code Flash (kB) | Total RAM (kB)  | Total Flash (kB) | STM32Cube.AI version  |
|-------------------|--------|------------|---------|----------------|-------------|---------------|------------|-------------|-------------|-----------------------|
| [MiniResNet 1stack ](ST_pretrainedmodel_public_dataset/esc10/miniresnet_1stacks_64x50_tl/miniresnet_1stacks_64x50_tl_int8.tflite) | int8 | 64x50x1 | B-U585I-IOT02A    | 59.89 | 5.38               |   123.6       |   58.35            | 65.27 | 181.95 | 8.1.0                 |
| [MiniResNet 2stacks ](ST_pretrainedmodel_public_dataset/esc10/miniresnet_2stacks_64x50_tl/miniresnet_2stacks_64x50_tl_int8.tflite) | int8 | 64x50x1 | B-U585I-IOT02A    | 59.89 |   8.37      |   431.1           |   65.11      | 68.26 | 496.21 | 8.1.0                | 


### Reference inference time based on ESC-10 dataset


| Model             | Format | Resolution | Board            | Execution Engine | Frequency   | Inference time  | STM32Cube.AI version  |
|-------------------|--------|------------|------------------|------------------|-------------|-----------------|-----------------------|
| [MiniResNet 1stacks ](ST_pretrainedmodel_public_dataset/esc10/miniresnet_1stacks_64x50_tl/miniresnet_1stacks_64x50_tl_int8.tflite) | int8 | 64x50x1 | B-U585I-IOT02A | 1 CPU | 160 MHz | 106.43 ms | 8.1.0                 |
| [MiniResNet 2stacks ](ST_pretrainedmodel_public_dataset/esc10/miniresnet_2stacks_64x50_tl/miniresnet_2stacks_64x50_tl_int8.tflite) | int8 | 64x50x1 | B-U585I-IOT02A | 1 CPU | 160 MHz | 163.25 ms | 8.1.0               |


### Accuracy with ESC-10 dataset

A note on clip-level accuracy : In a traditional AED data processing pipeline, audio is converted to a spectral representation (in this model zoo, mel-spectrograms), which is then cut into patches. Each patch is fed to the inference network, and a label vector is output for each patch. The labels on these patches are then aggregated based on which clip the patch belongs to, to form a single aggregate label vector for each clip. Accuracy is then computed on these aggregate label vectors.

The reason this metric is used instead of patch-level accuracy is because patch-level accuracy varies immensely depending on the specific manner used to cut spectrogram into patches, and also because clip-level accuracy is the metric most often reported in research papers.

| Model | Format | Resolution | Clip-level Accuracy |
|-------|--------|------------|----------------|
| [MiniResNet 1stack ](ST_pretrainedmodel_public_dataset/esc10/miniresnet_1stacks_64x50_tl/miniresnet_1stacks_64x50_tl.h5) | float32 | 64x50x1 | 89.9% |
| [MiniResNet 1stack ](ST_pretrainedmodel_public_dataset/esc10/miniresnet_1stacks_64x50_tl/miniresnet_1stacks_64x50_tl_int8.tflite) | int8 | 64x50x1 | 89.9% |
| [MiniResNet 2stacks ](ST_pretrainedmodel_public_dataset/esc10/miniresnet_2stacks_64x50_tl/miniresnet_2stacks_64x50_tl.h5) | float32 | 64x50x1 | 92.4% |
| [MiniResNet 2stacks ](ST_pretrainedmodel_public_dataset/esc10/miniresnet_2stacks_64x50_tl/miniresnet_2stacks_64x50_tl_int8.tflite) | int8 | 64x50x1 | 93.6% |

## Retraining and code generation


Please refer to the configuration file documentation: [here](../../src/README.md)


## Demos
### Integration in a simple example


Please refer to the deployment tutorial [here](../../deployment/README.md)
