from pysr import PySRRegressor
import numpy as np
import openai
import json
import os
import shutil
from pydantic import BaseModel
from typing import Dict, List, Optional
from collections import deque 
from typing import Deque

class PySRConfig(BaseModel):
    reasoning: str
    niterations: int
    binary_operators: List[str]
    unary_operators: List[str]
    constraints: Optional[Dict[str, List[float]]] = None
    parsimony: Optional[float]
    maxsize: Optional[int]

class EquationFeedback(BaseModel):
    reasoning: str
    validity: bool
    issue: Optional[str] = None  # Allows nuanced responses like "missing G"
    suggested_constraints: Optional[Dict[str, List[float]]] = None
    suggested_constants: Optional[Dict[str, float]] = None 
    adjustments: Optional[Dict[str, float]] = None
    new_binary_operators: Optional[List[str]] = None
    new_unary_operators: Optional[List[str]] = None
    terminate: bool

class ReasoningSymbolicRegressor:
    def __init__(self, base_iterations=500, cycles=5, llm_model="gpt-4o",
                 context="Scientific Equation Discovery and Symbolic Regression", debug=False):
        """
        AI-Driven Symbolic Regression with LLM-Driven Initial PySR Config.
        - Runs PySR in cycles
        - Uses LLM to analyze equations and return structured JSON feedback
        - Dynamically adjusts PySR settings based on AI feedback
        - Tracks last 5 LLM responses for context steering
        """
        self.base_iterations = base_iterations
        self.cycles = cycles
        self.llm_model = llm_model
        self.context = context
        self.debug = debug
        self.history: Deque[str] = deque(maxlen=5)

        # Ensure OpenAI API Key is Set
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("❌ ERROR: OpenAI API key is missing. Set OPENAI_API_KEY before running.")

        # Ask LLM for the best starting PySR parameters
        self.pysr_config = self.get_initial_pysr_config()

        # Initialize the PySR model using LLM-recommended settings
        self.model = self.create_pysr_model(self.pysr_config)

    def get_initial_pysr_config(self):
        """Uses the LLM to determine the best initial settings for PySR, with automatic error repair."""
        history_text = "\n".join(self.history) if self.history else "No previous responses yet."

        prompt = f"""
        You are an AI scientist assisting with symbolic regression in the field of **{self.context}**.

        **Scientific Context:**
        We are using PySR, a symbolic regression framework, to discover equations that best describe {self.context}.
        Your task is to recommend **optimal initial PySR settings** for this problem.

        **Recent LLM Responses for Reference:**
        {history_text}

        **What You Should Provide:**
        - `"reasoning"`: Explain why you selected these settings.
        - `"niterations"`: The number of iterations for PySR to run in the first evolution cycle.
        - `"binary_operators"`: The set of binary operators to use (`+`, `-`, `*`, `/`, `^`, etc.).
        - `"unary_operators"`: The set of unary operators to use (`sqrt`, `log`, `exp`, etc.).
        - `"constraints"`: If applicable, specify any numerical constraints (e.g., restrict `^` to `[-2, -2]` for inverse-square laws).
        - `"parsimony"`: Suggested parsimony coefficient (to balance simplicity vs accuracy).
        - `"maxsize"`: The maximum size of the symbolic equation.

        Respond **strictly** using structured JSON format based on the `PySRConfig` schema.
        """

        if self.debug:
            print("\n🔍 Prompt Sent to LLM for Initial PySR Config:\n", prompt)

        for attempt in range(3):  # Allow up to 3 attempts
            try:
                client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                response = client.beta.chat.completions.parse(
                    model=self.llm_model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format=PySRConfig
                )

                structured_response = response.choices[0].message.parsed
                self.history.append(structured_response.reasoning)  
                if self.debug:
                    print("✅ LLM Initial PySR Config (Parsed JSON):", structured_response.model_dump_json(indent=2))

                return structured_response

            except Exception as e:
                if self.debug:
                    print(f"❌ OpenAI API Call Failed (Attempt {attempt+1}/3): {e}")
                    if attempt < 2:
                        print("🔄 Retrying with improved error handling...")

        if self.debug:
            print("⚠️ Using default PySR configuration due to repeated failures.")
        return PySRConfig(
            reasoning="Fallback to default settings due to LLM failure",
            niterations=self.base_iterations,  
            binary_operators=["+", "-", "*", "/", "^"],
            unary_operators=["sqrt", "log", "exp"],
            constraints={"^": [-2, -2]},
            parsimony=0.1,
            maxsize=20
        )


    def create_pysr_model(self, config: PySRConfig):
        """Creates a new PySRRegressor instance using LLM-recommended settings, with error repair support."""
        parallelism_mode = "multithreading"

        # Ensure iterations do not exceed the LLM's recommendation
        capped_iterations = min(config.niterations, 1000)  

        if self.debug:
            print(f"⏳ PySR will run for {capped_iterations} iterations.")

        try:
            return PySRRegressor(
                niterations=capped_iterations,
                binary_operators=config.binary_operators,
                unary_operators=config.unary_operators,
                constraints=config.constraints if config.constraints else {"^": [-2, -2]},  
                extra_sympy_mappings={},
                verbosity=2 if self.debug else 0,
                parallelism=parallelism_mode,
                procs=4,
                warm_start=False,  
                precision=64,
                maxsize=config.maxsize if config.maxsize else 20,  
                update=False,
                parsimony=config.parsimony if config.parsimony else 0.0001,  
            )

        except Exception as e:
            print(f"❌ PySR Initialization Failed: {e}")

            # Send error message to LLM for repair
            repair_prompt = f"""
            The symbolic regression framework PySR encountered an error while initializing:

            **Error Message:**
            {e}

            **Recent LLM Responses for Reference:**
            {history_text}

            **What You Should Do:**
            - Identify what might have gone wrong in the previous response.
            - Suggest corrected parameters that will allow PySR to run properly.

            Respond **strictly** using structured JSON format based on the `PySRConfig` schema.
            """

            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.beta.chat.completions.parse(
                model=self.llm_model,
                messages=[{"role": "user", "content": repair_prompt}],
                response_format=PySRConfig
            )

            structured_response = response.choices[0].message.parsed
            self.history.append(structured_response.reasoning)  

            print("\n✅ LLM has repaired the PySR settings. Retrying...")

            return PySRRegressor(
                niterations=structured_response.niterations,
                binary_operators=structured_response.binary_operators,
                unary_operators=structured_response.unary_operators,
                constraints=structured_response.constraints if structured_response.constraints else {"^": [-2, -2]},
                extra_sympy_mappings={},
                verbosity=2 if self.debug else 0,
                parallelism=parallelism_mode,
                procs=4,
                warm_start=False,  
                precision=64,
                maxsize=structured_response.maxsize if structured_response.maxsize else 20,  
                update=False,
                parsimony=structured_response.parsimony if structured_response.parsimony else 0.0001,  
            )


    def fit(self, X, y, context=None):
        """Runs PySR and refines it using AI guidance over multiple cycles."""
        if context:
            self.context = context  # Allow dynamic updates to the scientific context
        if self.debug:
            print(f"\n🔬 AI is now working on: {self.context}")

        for cycle in range(self.cycles):
            if self.debug:
                print(f"\n🚀 **AI-Guided Evolution Cycle {cycle + 1}** 🚀")

            try:
                # Train the model on the current iteration
                self.model.fit(X, y)

                # Get the best discovered equation
                best_equation = str(self.model.sympy())
                if self.debug:
                    print(f"Best Equation So Far: {best_equation}")

                # Ask LLM to Analyze and Guide the Next Evolution
                feedback_json = self.evaluate_equation(best_equation)
                if feedback_json:
                    self.history.append(feedback_json.reasoning)
                    if self.debug:
                        print(f"🧠 LLM Feedback: {feedback_json.model_dump_json(indent=2)}")

                    # Stop if LLM confirms the equation is correct
                    if feedback_json.terminate:
                        if self.debug:
                            print("\n🎉 ✅ LLM confirms that the correct equation has been found. Stopping further iterations.")
                        break

                    # Only recreate model if we're continuing to next cycle
                    if cycle < self.cycles - 1:
                        self.update_model_based_on_feedback(feedback_json)

            except Exception as e:
                if self.debug:
                    print(f"⚠️ Error during cycle {cycle + 1}: {str(e)}")
                continue

        if self.debug:
            print("\n✅ AI-Guided Symbolic Regression Complete!")
        return self.model

    def evaluate_equation(self, equation):
        """Uses an LLM to analyze an equation and return structured JSON feedback with termination support."""
        history_text = "\n".join(self.history) if self.history else "No previous responses yet."

        prompt = f"""
        You are an AI scientist assisting with mathematical equation discovery in the field of **{self.context}**.

        **Scientific Context:**
        This equation is generated by an AI system that searches for fundamental relationships between variables.
        The goal is to determine whether this equation correctly describes the physical principles governing {self.context}.

        **Recent LLM Responses for Reference:**
        {history_text}

        **Equation to Analyze:**
        {equation}

        **Your Task:**
        - Provide a **scientific reasoning** field explaining your evaluation of this equation.
        - Assess **whether the equation follows known physical relationships**.
        - If the equation is valid but missing a fundamental constant (e.g., G for gravity), return `"validity": true, "issue": "missing G"`.
        - If modifications are needed, provide **specific numerical constraints** (e.g., `"^": [-2, -2]`).
        - If a missing constant is detected, provide its expected value in `"suggested_constants"`.
        - Suggest **only meaningful binary operators** (avoid `mod`, `max`, `min`).
        - Suggest **only relevant unary operators** (e.g., `sqrt`, `log`).
        - **If the equation is fully correct, set `"terminate": true"` to indicate that no further improvements are needed. Otherwise, return `"terminate": false"`.**

        Respond **strictly** using structured JSON format based on the `EquationFeedback` schema.
        """

        if self.debug:
            print("\n🔍 Prompt Sent to LLM for Equation Evaluation:\n", prompt)

        for attempt in range(3):  # Allow up to 3 attempts
            try:
                client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                response = client.beta.chat.completions.parse(
                    model=self.llm_model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format=EquationFeedback
                )

                structured_response = response.choices[0].message.parsed
                self.history.append(structured_response.reasoning)

                if self.debug:
                    print("\n✅ LLM Response (Parsed JSON):", structured_response.model_dump_json(indent=2))
                    print("\n📜 Updated History:", list(self.history))

                return structured_response

            except Exception as e:
                if self.debug:
                    print(f"❌ OpenAI API Call Failed (Attempt {attempt+1}/3): {e}")
                    if attempt < 2:
                        print("🔄 Retrying...")

        if self.debug:
            print("⚠️ Using fallback feedback due to repeated failures.")
        return EquationFeedback(
            reasoning="Fallback response due to LLM failure",
            validity=False,
            issue="LLM evaluation failed",
            terminate=False
        )

    def update_model_based_on_feedback(self, feedback: EquationFeedback):
        """Parses LLM JSON feedback and updates PySR model properties."""
        # Convert Pydantic model to dict for easier access
        feedback_dict = feedback.model_dump()
        
        suggested_constraints = feedback_dict.get("suggested_constraints", {})
        adjustments = feedback_dict.get("adjustments", {}) or {}  # Default to empty dict if None
        suggested_constants = feedback_dict.get("suggested_constants", {})

        if self.debug:
            print(f"🔧 Applying LLM-Suggested Adjustments: {adjustments}")
            print(f"🔒 Setting Constraints: {suggested_constraints}")
            print(f"🌍 Suggested Constants: {suggested_constants}")

        # Recreate PySR with updated settings
        self.model = self.create_pysr_model(PySRConfig(
            reasoning="Updated configuration based on LLM feedback",
            niterations=adjustments.get("niterations", self.base_iterations),
            binary_operators=feedback_dict.get("new_binary_operators") or ["+", "-", "*", "/", "^"],
            unary_operators=feedback_dict.get("new_unary_operators") or ["sqrt", "log", "exp"],
            constraints=suggested_constraints,
            parsimony=adjustments.get("parsimony", 0.0001),
            maxsize=adjustments.get("maxsize", 20)
        ))