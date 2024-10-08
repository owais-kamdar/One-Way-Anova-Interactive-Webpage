import streamlit as st
import pandas as pd
import numpy as np
from anova import myANOVA  # Import the updated ANOVA function with p-value
from scipy.stats import f

# Setting the page title and layout
st.set_page_config(page_title="One-way ANOVA Dashboard", layout="wide")

# App title
st.title("📊 One-way ANOVA Test 📊")

st.write("""
### Welcome to the One-way ANOVA Dashboard! 
This interactive app allows you to:
- Upload a CSV file
- Perform One-way ANOVA to determine if there's a significant difference between groups.
""")

# Sidebar section for explanations
st.sidebar.header("Understanding One-way ANOVA")
st.sidebar.write("""
**One-way ANOVA** (Analysis of Variance) is a statistical method used to compare means of three or more samples. 
It tests the null hypothesis that all groups have the same population mean. The test produces an F-statistic 
and a corresponding p-value to determine statistical significance.
""")

# File upload section
uploaded_file = st.file_uploader("Upload your CSV file for analysis", type=["csv"])

if uploaded_file:
    try:
        # Read the uploaded CSV file and display it
        data = pd.read_csv(uploaded_file)  # <-- Handling file upload

        # Check if the first column is non-numeric and may represent labels (group names)
        if not np.issubdtype(data.iloc[:, 0].dtype, np.number):
            labels = data.iloc[:, 0]  # Save group labels for display
            data_numeric = data.iloc[:, 1:]  # Exclude the first column (non-numeric)
        else:
            labels = None
            data_numeric = data  # If first column is numeric, use all data
        
        st.write("**Uploaded CSV Data:**", data)

        # Select columns instead of rows for ANOVA
        st.write("#### Select the columns representing your groups for the ANOVA test:")
        all_columns = data_numeric.columns.tolist()
        select_all = st.checkbox("Select all columns")

        # If "Select all" is checked, select all columns
        if select_all:
            column_indices = all_columns
        else:
            column_indices = st.multiselect("Choose columns for analysis:", all_columns)

        if column_indices:
            # Query only the selected columns
            selected_columns = data_numeric[column_indices]  # Use selected columns for ANOVA
            st.write("**Selected Data for ANOVA (columns as groups):**", selected_columns)

            # Ensure that we have enough columns for ANOVA
            if len(column_indices) < 2:
                st.error("❌ You need to select at least two columns (groups) for the ANOVA test.")
            else:
                # Allow user to set the significance level (alpha)
                alpha = st.number_input("Set the significance level (alpha)", min_value=0.01, max_value=0.10, value=0.05, step=0.01)

                # Button to run the ANOVA test
                if st.button("Run One-way ANOVA"):
                    try:
                        myGrid = selected_columns.to_numpy().T  # Transpose to treat columns as groups
                        result, myF, Fstat, p_value = myANOVA(myGrid, alpha)

                        # Display results
                        st.write(f"**F-statistic**: {myF}")
                        st.write(f"**Critical F-value**: {Fstat}")
                        st.write(f"**P-value**: {p_value:.10f}")

                        # Provide contextual interpretation
                        if p_value < alpha:
                            st.success(f"Result: There is a statistically significant difference between the groups (p-value = {p_value:.5f}).")
                        else:
                            st.warning(f"Result: There is no evidence for a significant difference between the groups (p-value = {p_value:.5f}).")
                    except Exception as e:
                        st.error(f"❌ Error during ANOVA computation: {e}")

    except Exception as e:
        st.error(f"❌ Error reading CSV: {e}")
else:
    st.info("📂 Please upload a CSV file to begin.")
