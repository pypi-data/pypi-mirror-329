# Reasoning Symbolic Regressor

**LLM-enhanced symbolic regression:** A reasoning-driven AI that refines equations using structured feedback and adaptive learning.

## 🚀 Overview
`ReasoningSymbolicRegressor` integrates symbolic regression with LLM-powered reasoning, allowing AI to not only search for equations but also **self-correct and refine them** through structured feedback.

## 📦 Installation
You can install this package via PyPI:
```bash
pip install reasoning-symbolic-regressor
```

## 🔧 Usage
Note: Make sure your `OPENAI_API_KEY` is set.
```python
from reasoning_symbolic_regressor import ReasoningSymbolicRegressor

# Initialize the AI reasoning-driven symbolic regressor
regressor = ReasoningSymbolicRegressor(debug=True)

# Fit the model to data
regressor.fit(X, y)
```

## ✨ Features
✅ **LLM-Guided Exploration**: Dynamically adjusts search parameters using AI reasoning.  
✅ **Self-Repairing Feedback**: Detects errors in PySR configurations and prompts LLM to correct them.  
✅ **Iterative Refinement**: Improves equations over multiple guided cycles.  
✅ **Early Stopping**: Terminates when the LLM determines the correct equation has been found.  

## 🛠️ Development
To contribute or modify the project, clone the repository and install dependencies:
```bash
git clone https://github.com/sidu/ReasoningSymbolicRegressor.git
cd ReasoningSymbolicRegressor
pip install -r requirements.txt
```
## 🧪 Testing
To run the tests, use the following command:
```bash
pip install -e .
python tests/test_gravitation.py
```

## 📜 License
This project is licensed under the **MIT License**.

## 🌟 Acknowledgments
Inspired by **symbolic regression**, **LLM reasoning**, and **adaptive AI systems**.