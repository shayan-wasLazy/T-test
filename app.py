import streamlit as st
import numpy as np
from scipy.stats import t

# ---- Function ----
def one_sample_t(data, mu0, alpha=0.05, alternative='two-sided'):
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    df = n - 1

    t_stat = (mean - mu0) / (std / np.sqrt(n))

    if alternative == 'two-sided':
        p_value = 2 * (1 - t.cdf(abs(t_stat), df))
    elif alternative == 'greater':
        p_value = 1 - t.cdf(t_stat, df)
    elif alternative == 'less':
        p_value = t.cdf(t_stat, df)
    else:
        raise ValueError("Choose 'two-sided', 'greater', or 'less'")

    decision = "Reject H0" if p_value < alpha else "Fail to Reject H0"
    return t_stat, p_value, decision


# ---- Streamlit UI ----
st.title("One Sample t-Test Calculator")

st.write("Enter sample data separated by commas:")

data_input = st.text_area("Sample Data", "12, 15, 14, 10, 13")

mu0 = st.number_input("Hypothesized Mean (μ₀)", value=12.0)
alpha = st.slider("Significance Level (α)", 0.01, 0.10, 0.05)

alternative = st.selectbox(
    "Alternative Hypothesis",
    ['two-sided', 'greater', 'less']
)

if st.button("Run Test"):
    try:
        data = np.array([float(x.strip()) for x in data_input.split(",")])
        t_stat, p_value, decision = one_sample_t(data, mu0, alpha, alternative)

        st.subheader("Results")
        st.write(f"t-statistic: {t_stat:.4f}")
        st.write(f"p-value: {p_value:.4f}")
        st.write(f"Decision: {decision}")

    except:
        st.error("Invalid input. Please enter numeric values separated by commas.")