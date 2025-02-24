import numpy as np
from reasoning_symbolic_regressor import ReasoningSymbolicRegressor

def test_gravitational_regression():
    """Test if the AI regressor correctly finds Newton's Law of Gravitation."""

    # Generate synthetic gravitational data
    num_samples = 1000
    G = 6.6743e-11  # Gravitational constant
    m1 = np.random.uniform(1, 100, num_samples)  # Mass 1
    m2 = np.random.uniform(1, 100, num_samples)  # Mass 2
    r = np.random.uniform(0.1, 10, num_samples)  # Distance (avoid zero)
    F = (G * m1 * m2) / (r ** 2)  # Newton's Law

    # Prepare inputs
    X = np.vstack([m1, m2, r]).T
    y = F

    # Run the AI-guided regressor
    regressor = ReasoningSymbolicRegressor(
        base_iterations=500,  # Start small for quick validation
        cycles=10,  # Let LLM refine equations
        context="Gravitational Physics",
        debug=True
    )

    model = regressor.fit(X, y)

    # Get the best equation found
    best_equation = str(model.sympy())
    print(f"\n🌟 Best Equation Found: {best_equation}")

    # Validate if the equation matches F = (m1 * m2) / r^2
    assert "x0" in best_equation and "x1" in best_equation and ("/ x2**2" in best_equation or "/(x2*x2)" in best_equation), \
        f"❌ The regressor did not find the correct gravitational equation: {best_equation}"

    print("✅ Gravitational Regression Test Passed!")

# Run the test when executed directly
if __name__ == "__main__":
    test_gravitational_regression()