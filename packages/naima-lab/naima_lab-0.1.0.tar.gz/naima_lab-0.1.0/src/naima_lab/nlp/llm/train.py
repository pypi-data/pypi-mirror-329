from trl import SFTTrainer
from transformers import TrainingArguments, DataCollatorForSeq2Seq
from unsloth import is_bfloat16_supported
from transformers import EarlyStoppingCallback
from naima_lab.models.config import Config
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template
from unsloth.chat_templates import standardize_sharegpt
from functools import partial
from unsloth.chat_templates import train_on_responses_only
from naima_lab.models.enums import SaveMethod
from datasets import Dataset
from typing import Any

class ClassificatorTrainLLM:
    def __init__(self, config: Config):
        self.config = config

    @staticmethod
    def formatting_prompts_func_instruct(tokenizer, examples):
        convos = examples["conversations"]
        texts = [
            tokenizer.apply_chat_template(
                convo, tokenize=False, add_generation_prompt=False
            )
            for convo in convos
        ]
        return {
            "text": texts,
        }

    def _get_dataset(self, dataset: list[dict], tokenizer: Any) -> Dataset:
        dataset = Dataset.from_dict({"conversations": dataset})
        
        tokenizer = get_chat_template(
            tokenizer,
            chat_template=self.config.chat_template,
        )
        dataset: Dataset = standardize_sharegpt(dataset)
        dataset = dataset.map(
            partial(self.formatting_prompts_func_instruct, tokenizer),
            batched=True,
        )

        dataset = dataset.shuffle(seed=42)
        return dataset


    def fine_tune_instruct(self, dataset: list[dict]) -> None:
                        
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=self.config.model_name,
            max_seq_length=self.config.max_seq_length,
            dtype=(None),
            load_in_4bit=self.config.load_in_4bit,
        )
        model = FastLanguageModel.get_peft_model(
            model,
            r=self.config.unsloth.fast_language_model_config.r,  # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
            target_modules=self.config.unsloth.fast_language_model_config.target_modules,
            lora_alpha=self.config.unsloth.fast_language_model_config.lora_alpha,
            lora_dropout=self.config.unsloth.fast_language_model_config.lora_dropout,  # Supports any, but = 0 is optimized
            bias=self.config.unsloth.fast_language_model_config.bias,  # Supports any, but = "none" is optimized
            use_gradient_checkpointing=self.config.unsloth.fast_language_model_config.use_gradient_checkpointing,  # True or "unsloth" for very long context
            random_state=self.config.unsloth.fast_language_model_config.random_state,
            use_rslora=self.config.unsloth.fast_language_model_config.use_rslora,  # We support rank stabilized LoRA
            loftq_config=self.config.unsloth.fast_language_model_config.loftq_config,  # And LoftQ
        )
        tokenizer = get_chat_template(
            tokenizer,
            chat_template=self.config.chat_template,
        )
        dataset = self._get_dataset(dataset, tokenizer).select(range(10))
        if self.config.test_size == 0:
            train_dataset = dataset
            eval_dataset = None
        else:
            train_val_split = dataset.train_test_split(test_size=self.config.test_size)
            train_dataset = train_val_split["train"]
            eval_dataset = train_val_split["test"]
        if self.config.trl.callbacks.use_callbaks:
            callbacks = [
                    EarlyStoppingCallback(
                        early_stopping_patience=self.config.trl.callbacks.early_stopping_patience,
                        early_stopping_threshold=self.config.trl.callbacks.early_stopping_threshold,
                    )
                ]
        else:
            callbacks = []
        trainer = SFTTrainer(
            model=model,
            tokenizer=tokenizer,
            train_dataset=train_dataset,  # I changed this
            eval_dataset=eval_dataset,  # I added this
            dataset_text_field=self.config.trl.dataset_text_field,
            max_seq_length=self.config.max_seq_length,
            data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer),
            dataset_num_proc=self.config.trl.dataset_num_proc,
            packing=self.config.trl.packing,  # Can make training 5x faster for short sequences.
            callbacks=callbacks,
            args=TrainingArguments(
                run_name=self.config.trl.args.run_name,
                per_device_train_batch_size=self.config.trl.args.per_device_train_batch_size,
                gradient_accumulation_steps=self.config.trl.args.gradient_accumulation_steps,
                warmup_steps=self.config.trl.args.warmup_steps,
                num_train_epochs=self.config.trl.args.num_train_epochs,
                do_eval=self.config.trl.args.do_eval,
                eval_steps=self.config.trl.args.eval_steps,
                max_steps=self.config.trl.args.max_steps,
                learning_rate=self.config.trl.args.learning_rate,
                fp16=not is_bfloat16_supported(),
                bf16=is_bfloat16_supported(),
                logging_steps=self.config.trl.args.logging_steps,
                optim=self.config.trl.args.optim,
                weight_decay=self.config.trl.args.weight_decay,
                lr_scheduler_type=self.config.trl.args.lr_scheduler_type,
                seed=self.config.trl.args.seed,
                logging_first_step=self.config.trl.args.logging_first_step,
                eval_strategy=self.config.trl.args.eval_strategy,
                save_strategy=self.config.trl.args.save_strategy,
                output_dir=self.config.trl.args.output_dir,
                report_to=self.config.trl.args.report_to,  # Use this for WandB etc
                load_best_model_at_end=self.config.trl.args.load_best_model_at_end,
            ),
        )
        trainer = train_on_responses_only(
            trainer,
            instruction_part=self.config.train_on_responses_only.instruction_part,
            response_part=self.config.train_on_responses_only.response_part,
        )

        trainer.train()
        if self.config.save_method == SaveMethod.ADAPTERS:
            model.save_pretrained(self.config.model_save_model)  # Local saving
            tokenizer.save_pretrained(self.config.model_save_model)  # Local saving            
        elif self.config.save_method == SaveMethod.FULL:
            model.save_pretrained(self.config.model_save_model,tokenizer, save_method = "merged_16bit",)
        else:
            raise ValueError(f"Save method {self.config.save_method} not supported.")