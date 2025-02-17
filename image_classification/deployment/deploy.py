# /*---------------------------------------------------------------------------------------------
#  * Copyright (c) 2022 STMicroelectronics.
#  * All rights reserved.
#  *
#  * This software is licensed under terms that can be found in the LICENSE file in
#  * the root directory of this software component.
#  * If no LICENSE file comes with this software, it is provided AS-IS.
#  *--------------------------------------------------------------------------------------------*/


import os
import sys
import warnings

from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig
from typing import Optional

warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

sys.path.append(os.path.abspath('../src/utils'))
sys.path.append(os.path.abspath('../common'))

from common_deploy import stm32ai_deploy
from gen_h_file import gen_h_user_file
from models_mgt import get_model_name_and_its_input_shape
from common_benchmark import get_model_name


def deploy(cfg: DictConfig = None, model_path_to_deploy: Optional[str] = None,
           credentials: list[str] = None) -> None:
    """
    Deploy the AI model to a target device.

    Args:
        cfg (DictConfig): The configuration dictionary. Defaults to None.
        model_path_to_deploy (str, optional): Model path to deploy. Defaults to None
        credentials list[str]: User credentials used before to connect.

    Returns:
        None
    """
    # Build and flash Getting Started
    board = cfg.deployment.hardware_setup.board
    c_project_path = cfg.deployment.c_project_path
    output_dir = HydraConfig.get().runtime.output_dir
    stm32ai_output = output_dir + "/generated"
    stm32ai_version = cfg.tools.stm32ai.version
    optimization = cfg.tools.stm32ai.optimization
    path_to_stm32ai = cfg.tools.stm32ai.path_to_stm32ai
    path_to_cube_ide = cfg.tools.path_to_cubeIDE
    verbosity = cfg.deployment.verbosity
    stm32ai_ide = cfg.deployment.IDE
    stm32ai_serie = cfg.deployment.hardware_setup.serie
    check_large_model=False
    # Get model name for STM32Cube.AI STATS
    model_path = model_path_to_deploy if model_path_to_deploy else cfg.general.model_path
    model_name, input_shape = get_model_name_and_its_input_shape(model_path=model_path)

    get_model_name_output = get_model_name(model_type=str(model_name),
                                           input_shape=str(input_shape[0]),
                                           project_name=cfg.general.project_name)
    # Get model name
    # Generate ai_model_config.h for C embedded application
    print("[INFO] : Generating C header file for Getting Started...")
    gen_h_user_file(config=cfg, quantized_model_path=model_path,board=board)

    if stm32ai_serie.upper() == "STM32H7" and stm32ai_ide.lower() == "gcc":
        if board == "STM32H747I-DISCO":
            stmaic_conf_filename = "stmaic_STM32H747I-DISCO.conf"
        elif board == "NUCLEO-H743ZI2":
            stmaic_conf_filename = "stmaic_NUCLEO-H743ZI2.conf"
        else:
            raise TypeError("The hardware selected in cfg.deployment.hardware_setup.board is not supported yet!\n"
                            "Please choose one of the following boards : `STM32H747I-DISCO` or `NUCLEO-H743ZI2`.")

        # Run the deployment
        stm32ai_deploy(target=board, stm32ai_version=stm32ai_version, c_project_path=c_project_path,
                       output_dir=output_dir,
                       stm32ai_output=stm32ai_output, optimization=optimization, path_to_stm32ai=path_to_stm32ai,
                       path_to_cube_ide=path_to_cube_ide, stmaic_conf_filename=stmaic_conf_filename,
                       verbosity=verbosity,
                       debug=False, model_path=model_path, get_model_name_output=get_model_name_output,
                       stm32ai_ide=stm32ai_ide, stm32ai_serie=stm32ai_serie, credentials=credentials, on_cloud=cfg.tools.stm32ai.on_cloud, 
                       check_large_model=True, cfg=cfg)
    else:
        raise TypeError("Options for cfg.deployment.hardware_setup.serie and cfg.deployment.IDE not supported yet!\n"
                        "Only options are respectively `STM32H7` and `GCC`.")
