# /*---------------------------------------------------------------------------------------------
#  * Copyright (c) 2022 STMicroelectronics.
#  * All rights reserved.
#  *
#  * This software is licensed under terms that can be found in the LICENSE file in
#  * the root directory of this software component.
#  * If no LICENSE file comes with this software, it is provided AS-IS.
#  *--------------------------------------------------------------------------------------------*/
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from hydra.core.hydra_config import HydraConfig

def vis_training_curves(history=None, output_dir: str = None) -> None:
    """
    Visualizes the training curves of the model.

    Args:
        history: The history object returned by the model.fit() method.
        output_dir (Optional[str]): The output directory to save the training curves plot.

    Returns:
        None
    """
    # Extract the accuracy and loss values for training and validation data
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(len(acc))

    # Create dataframes for the training and validation data
    df_val = pd.DataFrame(
        {'run': 'validation', 'step': epochs_range, 'epoch_accuracy': val_acc, 'epoch_loss': val_loss})
    df_train = pd.DataFrame({'run': 'train', 'step': epochs_range, 'epoch_accuracy': acc, 'epoch_loss': loss})

    # Concatenate the dataframes
    frames = [df_val, df_train]
    df = pd.concat(frames)
    df = df.reset_index()

    # Plot the training curves
    plt.figure(figsize=(16, 6))
    plt.subplot(1, 2, 1)
    sns.lineplot(data=df, x="step", y="epoch_accuracy", hue="run").set_title("accuracy")
    plt.grid()
    plt.subplot(1, 2, 2)
    sns.lineplot(data=df, x="step", y="epoch_loss", hue="run").set_title("loss")
    plt.grid()
    plt.savefig(os.path.join(output_dir, 'Training_curves.png'))
    plt.plot()
    plt.pause(0.01)
