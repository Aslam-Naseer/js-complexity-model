# JavaScript Function Complexity Analyzer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-Acorn-green?logo=node.js&logoColor=white)
![Modal](https://img.shields.io/badge/Modal-Serverless-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

A hybrid machine learning system that analyzes JavaScript code to predict function complexity. It uses an **ensemble approach** combining a fine-tuned LLM (Qwen-4B) and a custom Neural Network to evaluate both semantic and structural code complexity.

---

## 🚀 Project Overview

This project moves beyond traditional static analysis rules by integrating AI to understand code readability and maintainability. It parses JavaScript code to extract structural features and feeds them into two complementary models:

1.  **🧠 Neural Networks (NN):** A regression model trained on structural metrics (nesting depth, parameter count, etc.).
2.  **🤖 Large Language Models (LLM):** A fine-tuned **Qwen/Qwen3-4B-Instruct** model running on Modal.com to capture semantic nuance.

The system isolates individual functions (and sub-functions) and provides a comprehensive complexity report via a CLI or an interactive **Gradio web interface**.

---

## 📂 Project Structure

```bash
├── agents/             # Logic for LLM, NN, and Orchestrator agents
├── code_analyzer/      # Python wrapper + JS Acorn parser
├── llm_model/          # Qwen-3 4B fine-tuning & Modal deployment logic
├── nn_model/           # Neural Network training artifacts & scalers
├── notebooks/          # Experiments: Dataset generation, training & evaluation
├── utils/              # Helper functions
├── app.py              # Gradio Web Interface
└── main.py             # CLI Demo script
```

---

## ✨ Key Features

### 🔍 Deep Code Analysis

- **AST Parsing:** Uses **Acorn** to parse raw JS strings.
- **Hierarchy Detection:** Identifies global functions and recursively maps nested sub-functions.
- **Feature Extraction:** Computes _Parameter Count, Statement Count, Variable Count, and Max Nesting Depth._

### ⚖️ Dual-Model Ensemble

- **LLM Agent:** Qwen3-4B-Instruct (4-bit quantized) analyzes code semantics.
- **NN Agent:** Custom neural network analyzes structural features.
- **Ensemble Evaluator:** Computes a weighted average of both predictions for a robust final score.

### 📊 Interactive Dashboard

- **Gradio UI:** Real-time analysis with visualization.
- **Detailed Logs:** View the decision-making process of the orchestrator.
- **Structured Output:** JSON-formatted reports for easy integration, displayed in table.

---

## 💻 Installation & Setup

### Prerequisites

- **Python 3.10+** (Managed via \`uv\`)
- **Node.js** (Required for the Acorn parser)
- **Modal.com** account (For LLM inference)

### 1. Clone the repository

```bash
git clone https://github.com/Aslam-Naseer/js-complexity-model.git
cd js-complexity-analyzer
```

### 2. Install Python Dependencies (using uv)

This project uses `uv` for fast package management.

```bash
# Install dependencies from pyproject.toml
uv sync
```

### 3. Install JavaScript Dependencies

The code analyzer requires the Acorn parser packages.

```bash
cd code_analyzer
npm install
cd ..
```

### 4. Configure Environment

Create a `.env` file in the root directory:

```env
MODAL_TOKEN_ID=your_modal_id
MODAL_TOKEN_SECRET=your_modal_secret
HF_TOKEN=your_huggingface_token
```

---

## 🖥️ Usage

### 🌐 Web Interface (Gradio)

Launch the interactive dashboard to visualize function trees and complexity scores.

```bash
uv run app.py
```

- Opens local server at \`http://127.0.0.1:7860\`

### ⚡ Command Line Demo

Run a quick analysis on the default code snippet.

```bash
uv run main.py
```

---

## 🧠 Model Architecture

### The LLM Model

- **Base:** Qwen/Qwen3-4B-Instruct-2507
- **Training:** Fine-tuned on a custom JavaScript complexity dataset.
- **Deployment:** 4-bit quantization on Modal.com serverless GPU.
- _See [llm_model/README.md](llm_model/README.md) for fine-tuning details._

### The Neural Network

- **Input:** Normalized structural features (Cyclomatic metrics).
- **Architecture:** Dense layers with ReLU activation.
- **Comparison:** Outperformed Linear Regression and Random Forest benchmarks.
- _See [nn_model/README.md](nn_model/README.md) for architecture details._

---

## 📚 Dataset & Methodology

The models were trained on a subset of the **Semeru/code-text-javascript** dataset.

1.  **Labeling:** Complexity scores generated using **Lizard** (Cyclomatic Complexity).
2.  **Preprocessing:** Reduced to 5k (Train) / 500 (Val) / 500 (Test) samples.
3.  **Experimentation:** The `notebooks/` folder contains experiments on:
    - Ensemble weight optimization.
    - Feature importance analysis.
    - Comparison of ML algorithms (XGBoost, RF, Linear).

---

## 📝 Example Usage (Python)

```python
from agents.orchestrator import ComplexityOrchestrator

orchestrator = ComplexityOrchestrator()
code = """
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
"""

result = orchestrator.process_file(code)
print(result)
```

---

> **Note:** This project serves as a portfolio demonstration of full-stack ML engineering, from dataset creation and model fine-tuning to deployment and application integration.
