
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# 1. Page Configuration
# -----------------------------

st.set_page_config(
    page_title="DataLens Analytics",
    page_icon="📊",
    layout="wide"
)


# -----------------------------
# 2. Application Header
# -----------------------------

st.title("📊 DataLens Analytics")

st.write(
    "Upload a CSV dataset and explore it using "
    "statistical analysis and visualizations."
)

st.divider()


# -----------------------------
# 3. Upload CSV File
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)


if uploaded_file is not None:

    try:

        # Read uploaded CSV
        df = pd.read_csv(uploaded_file)

        st.success("Dataset uploaded successfully!")

        # -----------------------------
        # 4. Dataset Overview
        # -----------------------------

        st.subheader("Dataset Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rows", df.shape[0])

        col2.metric("Total Columns", df.shape[1])

        col3.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

        # -----------------------------
        # 5. Dataset Preview
        # -----------------------------

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(100),
            use_container_width=True
        )

        # -----------------------------
        # 6. Statistical Summary
        # -----------------------------

        st.subheader("Statistical Summary")

        st.dataframe(
            df.describe(),
            use_container_width=True
        )

        # -----------------------------
        # 7. Missing Value Analysis
        # -----------------------------

        st.subheader("Missing Value Analysis")

        missing = df.isnull().sum()

        missing = missing[missing > 0]

        if not missing.empty:

            st.bar_chart(missing)

        else:

            st.success("No missing values found!")

        # -----------------------------
        # 8. Data Visualization
        # -----------------------------

        st.subheader("Data Visualization")

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns.tolist()

        if numeric_columns:

            selected_column = st.selectbox(
                "Select a numerical column",
                numeric_columns
            )

            fig, ax = plt.subplots(figsize=(8, 4))

            ax.hist(
                df[selected_column].dropna(),
                bins=20
            )

            ax.set_title(
                f"Distribution of {selected_column}"
            )

            ax.set_xlabel(selected_column)

            ax.set_ylabel("Frequency")

            st.pyplot(fig)

            plt.close(fig)

        else:

            st.warning(
                "This dataset has no numerical columns."
            )

        # -----------------------------
        # 9. Correlation Analysis
        # -----------------------------

        if len(numeric_columns) >= 2:

            st.subheader("Correlation Analysis")

            correlation = df[
                numeric_columns
            ].corr()

            st.dataframe(
                correlation,
                use_container_width=True
            )

            fig, ax = plt.subplots(figsize=(8, 5))

            image = ax.imshow(
                correlation,
                cmap="coolwarm",
                vmin=-1,
                vmax=1
            )

            ax.set_xticks(
                range(len(numeric_columns))
            )

            ax.set_yticks(
                range(len(numeric_columns))
            )

            ax.set_xticklabels(
                numeric_columns,
                rotation=45,
                ha="right"
            )

            ax.set_yticklabels(numeric_columns)

            ax.set_title("Correlation Heatmap")

            fig.colorbar(image)

            st.pyplot(fig)

            plt.close(fig)

        # -----------------------------
        # 10. Download Dataset
        # -----------------------------

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Dataset",
            data=csv_data,
            file_name="analyzed_data.csv",
            mime="text/csv"
        )

    except Exception as error:

        st.error(
            f"An error occurred while reading the file: {error}"
        )

else:

    st.info(
        "Upload a CSV file to start analyzing your data."
    )

    st.subheader("What DataLens can do")

    st.write(
        """
        - Explore datasets
        - Calculate statistical summaries
        - Identify missing values
        - Generate histograms
        - Analyze correlations
        - Download datasets
        """
    )

