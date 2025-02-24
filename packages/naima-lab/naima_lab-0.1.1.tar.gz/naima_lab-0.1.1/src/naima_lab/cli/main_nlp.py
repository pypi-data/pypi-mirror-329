import typer
import logging
from typing_extensions import Annotated
import os
import json

from naima_lab.models.config import Config

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def llm_sft_instruct(
    config_file: Annotated[
        str, typer.Option(help="This is the path to the config file")
    ] = os.path.join("config", "config_llama3.2_1B_fast.yml"),
    dataset_path: Annotated[
        str, typer.Option(help="This is the path to the dataset.")
    ] = os.path.join("data", "raw", "FineTome-100k.json"),
):
    """Fine-tune the LLM with the given dataset.
The dataset should be in the following format:
1[
[{
    "from": "human",
    "value": "Can you help me make pasta carbonara?"
},
{
    "from": "assistant",
    "value": "Would you like the traditional Roman recipe, or a simpler version?"
},..],
[{
    "from": "human",
    "value": "The traditional version please"
},
{
    "from": "assistant",
    "value": "The authentic Roman carbonara uses just a few ingredients: pasta, guanciale, eggs, Pecorino Romano, and black pepper. Would you like the detailed recipe?"
}]
]
}
    
    """
    from naima_lab.nlp.llm.train import ClassificatorTrainLLM
    
    try:
        dataset = json.load(open(dataset_path, "r"))
    except FileNotFoundError:
        raise ValueError("Dataset not found")
    config = Config.get_config(config_file)
    trainer = ClassificatorTrainLLM(config=config)
    trainer.fine_tune_instruct(dataset=dataset)
