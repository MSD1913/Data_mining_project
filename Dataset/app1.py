import streamlit as st
import pandas as pd
import numpy as np

# Streamlit App Title
st.title("Interactive Data Exploration and Cleaning")

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Select Section",
    ["Upload Dataset", "Data Overview", "Data Cleaning", "Visualizations"]
)

# Initialize session state for data
if "df" not in st.session_state:
    st.session_state["df"] = None

# Section 1: File Upload
if section == "Upload Dataset":
    st.header("Upload Your Dataset")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        st.session_state["df"] = pd.read_csv(uploaded_file)
        st.success("Dataset Uploaded Successfully!")
        st.write("Preview of the Dataset:")
        st.dataframe(st.session_state["df"].head())

# Section 2: Data Overview
if section == "Data Overview":
    if st.session_state["df"] is not None:
        st.header("Data Overview")
        df = st.session_state["df"]
        st.write("Shape of the dataset:", df.shape)
        st.write("Column Names:")
        st.write(df.columns.tolist())
        st.write("Data Types:")
        st.write(df.dtypes)
        st.write("Missing Values Count:")
        st.write(df.isnull().sum())
        st.write("Preview of the Dataset:")
        st.dataframe(df.head())
    else:
        st.warning("Please upload a dataset first!")

# Section 3: Data Cleaning
if section == "Data Cleaning":
    if st.session_state["df"] is not None:
        st.header("Data Cleaning")
        df = st.session_state["df"].copy()

        # Remove duplicates
        if st.button("Remove Duplicates"):
            before = len(df)
            df = df.drop_duplicates()
            after = len(df)
            st.session_state["df"] = df
            st.success(f"Removed {before - after} duplicate rows!")

        # Handle missing values
        if st.checkbox("Handle Missing Values"):
            method = st.selectbox("Select Method", ["Drop Rows", "Fill with Mean", "Fill with Median", "Fill with Mode"])
            for col in df.select_dtypes(include=[np.number]).columns:
                if df[col].isnull().sum() > 0:
                    if method == "Drop Rows":
                        df = df.dropna()
                    elif method == "Fill with Mean":
                        df[col] = df[col].fillna(df[col].mean())
                    elif method == "Fill with Median":
                        df[col] = df[col].fillna(df[col].median())
                    elif method == "Fill with Mode":
                        df[col] = df[col].fillna(df[col].mode()[0])
            st.session_state["df"] = df
            st.success("Missing values handled!")

        # Drop specific columns
        if st.checkbox("Drop Columns"):
            columns_to_drop = st.multiselect("Select Columns to Drop", df.columns.tolist())
            if st.button("Drop Selected Columns"):
                df = df.drop(columns=columns_to_drop)
                st.session_state["df"] = df
                st.success(f"Dropped columns: {columns_to_drop}")

        st.write("Preview of the Cleaned Dataset:")
        st.dataframe(df.head())
    else:
        st.warning("Please upload a dataset first!")

# Section 4: Visualizations
if section == "Visualizations":
    if st.session_state["df"] is not None:
        st.header("Data Visualizations")
        df = st.session_state["df"]

        # Correlation Heatmap (placeholder)
        if st.checkbox("Show Correlation Heatmap"):
            st.write("This feature is under development!")

        # Histogram
        if st.checkbox("Show Histogram"):
            column = st.selectbox("Select Column for Histogram", df.columns)
            if column:
                st.bar_chart(df[column].value_counts())
    else:
        st.warning("Please upload a dataset first!")
