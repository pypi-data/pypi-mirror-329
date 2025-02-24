from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)
import yaml
import os
from naima_lab.models.enums import SaveMethod 

class CallbackConfig(BaseModel):
    use_callbaks: bool = Field(..., description="Whether to use callbacks.")
    early_stopping_patience: int = Field(
        ..., description="Number of patience steps for early stopping."
    )
    early_stopping_threshold: float = Field(
        ..., description="Threshold for early stopping."
    )


class TrainerArgs(BaseModel):
    run_name: str = Field(..., description="Name of the training run.")
    per_device_train_batch_size: int = Field(
        ..., description="Batch size per device during training."
    )
    gradient_accumulation_steps: int = Field(
        ..., description="Number of gradient accumulation steps."
    )
    warmup_steps: int = Field(..., description="Number of warmup steps.")
    num_train_epochs: int = Field(..., description="Total number of training epochs.")
    max_steps: int = Field(..., description="Maximum number of steps.")
    do_eval: bool = Field(..., description="Whether to perform evaluation.")
    eval_steps: int = Field(..., description="Number of steps between evaluations.")
    learning_rate: float = Field(..., description="Learning rate.")
    logging_steps: int = Field(..., description="Number of steps between logging.")
    optim: str = Field(..., description="Optimizer to use.")
    weight_decay: float = Field(..., description="Weight decay for the optimizer.")
    lr_scheduler_type: str = Field(..., description="Type of learning rate scheduler.")
    seed: int = Field(..., description="Random seed.")
    logging_first_step: bool = Field(..., description="Log the first step.")
    eval_strategy: str = Field(..., description="Evaluation strategy.")
    save_strategy: str = Field(..., description="Model save strategy.")
    output_dir: str = Field(..., description="Output directory for the model.")
    report_to: str = Field(..., description="Reporting target.")
    load_best_model_at_end: bool = Field(
        ..., description="Whether to load the best model at the end."
    )


class TrlConfig(BaseModel):
    dataset_text_field: str = Field(
        ..., description="Field in the dataset that contains text."
    )
    dataset_num_proc: int = Field(
        ..., description="Number of processes for dataset loading."
    )
    packing: bool = Field(..., description="Whether to pack the dataset.")
    callbacks: CallbackConfig
    args: TrainerArgs


class FastLanguageModelConfig(BaseModel):
    r: int
    target_modules: list[str]
    lora_alpha: int
    lora_dropout: float
    bias: str
    use_gradient_checkpointing: bool | str
    random_state: int
    use_rslora: bool
    loftq_config: Optional[dict]

class UnslothConfig(BaseModel):
    fast_language_model_config: FastLanguageModelConfig

class InstructionConfig(BaseModel):
    instruction_part: str = Field(..., description="Instruction part.")
    response_part: str = Field(..., description="Response part.")

class Config(BaseModel):
    model_name: str = Field(..., description="Name of the model.")
    chat_template: str = Field(..., description="ChatTemplate name.")
    max_seq_length: int = Field(..., description="Maximum sequence length.")
    load_in_4bit: bool = Field(
        ..., description="Whether to load the model in 4-bit precision."
    )
    test_size: float = Field(..., description="Test size.")
    save_method: SaveMethod = Field(..., description="Method to save the model. ")
    model_save_model: str = Field(..., description="Name of the model to save.")
    unsloth: UnslothConfig = Field(..., description="Unsloth configuration.")
    trl: TrlConfig = Field(..., description="TRL configuration.")
    train_on_responses_only: InstructionConfig = Field(..., description="Whether to train on responses only.")
    @staticmethod
    def get_config(
        config_path: str = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            ),
            "config",
            "config.yml",
        ),
    ) -> "Config":
        with open(config_path, "r", encoding="utf-8") as file:
            config: dict = yaml.safe_load(file)
            config["file_path"] = config_path
        return Config(**config)