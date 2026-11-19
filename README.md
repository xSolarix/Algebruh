# Algebruh

> *A symbolic algebra math engine with an even more symbolic name.*

**Algebruh** is a lightweight, zero-dependency symbolic math parser, simplifier, and equation solver written in Python with a Streamlit web interface.

🔗 **Try it live:** [algebruh.streamlit.app](https://streamlit.app)

---

## Features

* **Custom Tokenizer & Parser (`expr.py`):** Converts raw math strings into nested Python tuple Abstract Syntax Trees (ASTs)—because *aren't tuples beautiful enough already?* Supports unary signs, operator precedence, and implicit multiplication (`2x` and `(x + 2)(x + 3)`, for example).
* **Recursive Simplification:**
  * Constant folding and identity reductions (`x - x = 0`, `0 / x = 0`, `x^0 = 1`).
  * Flattened addition and multiplication (`flatten_add` & `flatten_multiply`) to collect like terms and combine exponents (`x * x` -> `x^2`).
  * Full distributive property expansion across nested brackets.
* **Expression Evaluation:** Evaluates symbolic ASTs using custom variable dictionaries.
* **Equation Solver (`equation.py`):**
  * **Linear Equations:** Rearranges expressions into *LHS - RHS = 0* form and isolates x (including edge cases for infinite or no solutions).
  * **Quadratic Equations:** Solves degree-2 polynomials using the quadratic formula, complete with complex conjugate root formatting (`0.0 + 2.0i, 0.0 - 2.0i`) when the discriminant goes negative.
* **Interactive Web UI (`app.py`):** Built with Streamlit to simplify expressions, evaluate variables, and solve equations directly in the browser.
* **Helpful™ Error Messages:** Very gently and softly reminds you when you divide by zero, give it anything it can't handle, or do something stupid.

---

## Examples

| Mode | Input | Output |
| :--- | :--- | :--- |
| **Simplify** | `(x + 2)(x + 3)` | `((6 + 5x) + x^2)` |
| **Simplify** | `bruh` | `(((b * r) * u) * h)` |
| **Solve Equation** | `4 * x = 10x + 5` | `x = -0.8333333333333334` |
| **Solve Equation** | `x^2 = -4` | `x = 0.0 + 2.0i, 0.0 - 2.0i` |
| **Solve Equation** | `3x^3 = 12` | `ValueError: Sir, I don't know how to handle this. Degree-3s are such a pain...` |

---

## Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd Algebruh
   ```

2. **Install Streamlit:**
   ```bash
   pip install streamlit
   ```

3. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

---

## Roadmap

* [x] Tokenizer, recursive AST parser, and pretty-printer
* [x] Linear & quadratic equation solvers (with complex root support)
* [x] Flattened multiplication, exponent grouping, and distributive expansion
* [x] Streamlit web deployment
* [ ] Polynomial factoring & Binomial Theorem expansion
* [ ] Rational Root Theorem & higher-degree root finding
* [ ] LaTeX rendering in Streamlit
* [ ] Trigonometry support
* [ ] Symbolic differentiation and integration support
