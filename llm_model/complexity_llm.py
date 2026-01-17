import modal
from modal import Volume, Image

app = modal.App("complexity-service")
image = Image.debian_slim().pip_install(
    "huggingface", "transformers", "torch", "bitsandbytes", "accelerate", "peft"
)

secrets = [modal.Secret.from_name("huggingface-secret")]

GPU = "T4"
BASE_MODEL = "Qwen/Qwen3-4B-Instruct-2507"
PROJECT_NAME = "complexity"
HF_USER = "aslam-naseer"
RUN_NAME = "2026-01-08_05.47.09"
PROJECT_RUN_NAME = f"{PROJECT_NAME}-{RUN_NAME}"
FINETUNED_MODEL = f"{HF_USER}/{PROJECT_RUN_NAME}"
CACHE_DIR = "/cache"

MIN_CONTAINERS = 0
hf_cache_volume = Volume.from_name("hf-hub-cache", create_if_missing=True)


@app.cls(
    image=image.env({"HF_HUB_CACHE": CACHE_DIR}),
    secrets=secrets,
    gpu=GPU,
    timeout=1800,
    scaledown_window=450,
    min_containers=MIN_CONTAINERS,
    volumes={CACHE_DIR: hf_cache_volume},
)
class ComplexityLLM:
    @modal.enter()
    def setup(self):
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        from peft import PeftModel

        # Quant Config
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
        )

        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"
        self.base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL, quantization_config=quant_config, device_map="auto"
        )
        self.fine_tuned_model = PeftModel.from_pretrained(
            self.base_model, FINETUNED_MODEL
        )

    @modal.method()
    def complexity(self, messages: list) -> float:
        import re
        import torch
        from transformers import set_seed

        set_seed(42)
        prompt_str = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        inputs = self.tokenizer(prompt_str, return_tensors="pt").to("cuda")

        with torch.no_grad():
            output_ids = self.fine_tuned_model.generate(
                **inputs, max_new_tokens=128, pad_token_id=self.tokenizer.eos_token_id
            )

        prompt_len = inputs["input_ids"].shape[1]
        generated_ids = output_ids[0, prompt_len:]
        full_response = self.tokenizer.decode(
            generated_ids, skip_special_tokens=True)

        match = re.search(
            r"Complexity Score:\s*(\d+(?:\.\d+)?)", full_response)

        if match:
            try:
                return float(match.group(1))
            except ValueError:
                print(f"Error converting '{match.group(1)}' to float")
                return 0.0
        else:
            print("Score pattern not found in response")
            return 0.0
