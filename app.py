import streamlit as st
from expr import parseExpression, simplifyExpression, beautifyExpression, evaluateExpression
from equation import solveEquation

st.title("Algebruh")

mode = st.selectbox("Mode", ["Simplify", "Solve Equation", "Evaluate"])
user_input = st.text_input("Expression or Equation", placeholder="e.g., 4 + 3x^2 - 1 or x^2 - 4 = 0")

x_val = 0.0
if mode == "Evaluate":
    x_val = st.number_input("Value for x", value=0.0)

if st.button("Run"):
    try:
        if not user_input.strip():
            raise ValueError("Type an expression or equation first.")

        if mode == "Simplify":
            tree = parseExpression(user_input)
            simplified = simplifyExpression(tree)
            st.success(beautifyExpression(simplified))

        elif mode == "Solve Equation":
            st.success(solveEquation(user_input))

        elif mode == "Evaluate":
            tree = parseExpression(user_input)
            result = evaluateExpression(tree, {"x": x_val})
            st.success(f"{result}")

    except (ValueError, ZeroDivisionError, KeyError) as e:
        st.error(str(e))