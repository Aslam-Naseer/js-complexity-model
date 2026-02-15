# LLM Agent: Qwen-3 4B Fine-Tune

![Modal](https://img.shields.io/badge/Deployed_on-Modal-orange?logo=modal&logoColor=white)
![Model](https://img.shields.io/badge/Qwen-4B_Instruct-blue)
![PEFT](https://img.shields.io/badge/PEFT-LoRA-green)
![Quantization](https://img.shields.io/badge/Quantization-4--bit_NF4-yellow)

This directory contains the deployment logic and training configuration for the **semantic analysis agent** of the complexity ensemble. We utilize a fine-tuned **Qwen/Qwen3-4B-Instruct** model to evaluate code readability and logic flow.

---

## 🏗️ Deployment Architecture (Modal.com)

The model is deployed as a serverless microservice using **Modal**. This allows the LLM to scale to zero when not in use, optimizing costs while providing on-demand GPU inference.

### Infrastructure Specs

- **GPU:** NVIDIA T4 (chosen for cost-efficiency with 4-bit quantization).
- **Container:** Debian Slim + PyTorch 2.0.
- **Cold Start Handling:**
  - `keep_warm`: 0 (Scale to zero enabled).
  - `scaledown_window`: 450s (Keeps container alive for burst requests).
  - `timeout`: 1800s.

### Inference Pipeline

1.  **Input:** Receives a chat-formatted message containing the JavaScript function.
2.  **Processing:**
    - Loads the Base Model (Qwen-4B) + LoRA Adapters.
    - Merges on-the-fly using `PeftModel`.
    - Generates a response (Max 128 new tokens).
3.  **Output Extraction:** Uses Regex to extract the specific float value from the model's textual response:
    > "Complexity Score: 12.5" -> `12.5`

---

## 🔧 Fine-Tuning Details

The model was fine-tuned to act as a **Complexity Scorer**, learning to map code snippets to numerical complexity values based on a custom dataset.

### Dataset

- **Source:** Subset of `semeru/code-text-javascript`.
- **Format:** Chat-completion messages (User: Code -> Assistant: Score).
- **HuggingFace Repo:** `aslam-naseer/js-function-complexity-messages`

### Training Configuration (QLoRA)

We used **QLoRA** (Quantized Low-Rank Adaptation) to fine-tune the model on a T4 GPU (Google Colab).

| Parameter           | Value                         |
| :------------------ | :---------------------------- |
| **Base Model**      | `Qwen/Qwen3-4B-Instruct-2507` |
| **Quantization**    | 4-bit NF4 (Double Quant)      |
| **LoRA Rank (r)**   | 32                            |
| **LoRA Alpha**      | 16                            |
| **Target Modules**  | `all-linear`                  |
| **Optimizer**       | `paged_adamw_32bit`           |
| **Learning Rate**   | `1e-4` (Cosine Schedule)      |
| **Sequence Length** | 3072                          |

### 📝 Training Run Notes

- **Effective Epochs:** ~1.7
- **Constraint:** Training was halted early due to compute resource limits (Colab T4 timeout). However, validation loss at the 1.7 epoch mark showed sufficient convergence for the ensemble task, preventing significant overfitting.
- **Artifacts:** The final adapter weights are hosted on HuggingFace at `aslam-naseer/complexity-2026-01-08_05.47.09`.
