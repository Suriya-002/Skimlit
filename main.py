import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

st.set_page_config(
    page_title="SkimLit",
    page_icon="data.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Skimlit 🌌")

st.write("""
### Welcome to Skimlit!

Harness the power of AI and data visualization in just a few clicks. Skimlit turns raw CSV data into insightful visualizations and cleans any inconsistencies.

🔍 **Explore** - Dive deep into hidden patterns.
✨ **Transform** - Let Skimlit enhance your datasets.
📊 **Visualize** - Bring your data to life in vivid charts.

#### 🚀 How to Use Skimlit:

1. **Upload Your CSV**: Use the uploader below.
2. **Wait for Magic**: Skimlit processes and visualizes your data.
3. **Download**: Get your cleaned data with the 'Download' button.

Ready? Let's start!
""")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    val = to_excel(df)
    b64 = base64.b64encode(val).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="cleaned_data.xlsx" style="background-color:#f63366;color:white;padding:8px 16px;border-radius:4px;text-decoration:none">Download cleaned data</a>'

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Original Data")
    st.write(data)

    # Handle missing data
    if data.isnull().sum().sum() > 0:
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            if data[col].isnull().sum() > 0:
                data[col].fillna(data[col].mean(), inplace=True)
        non_numeric_cols = data.select_dtypes(exclude=['float64', 'int64']).columns
        for col in non_numeric_cols:
            if data[col].isnull().sum() > 0:
                mode_val = data[col].mode()[0]
                data[col].fillna(mode_val, inplace=True)

    st.write("Feature Distributions and Insights")
    for column in data.columns:
        try:
            if data[column].dtype in ['float64', 'int64']:
                fig, ax = plt.subplots()
                data[column].hist(ax=ax)
                ax.set_title(f'Histogram for {column}')
                ax.set_xlabel(column)
                ax.set_ylabel('Frequency')
                st.pyplot(fig)

                fig, ax = plt.subplots()
                sns.boxplot(y=data[column], ax=ax)
                ax.set_title(f'Box Plot for {column}')
                st.pyplot(fig)

            else:
                if data[column].nunique() <= 10:
                    fig, ax = plt.subplots()
                    data[column].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
                    ax.set_title(f'Pie Chart for {column}')
                    st.pyplot(fig)
                else:
                    fig, ax = plt.subplots()
                    data[column].value_counts().plot.bar(ax=ax)
                    ax.set_title(f'Bar Chart for {column}')
                    st.pyplot(fig)

        except Exception as e:
            st.write(f"An error occurred when trying to plot {column}. Error: {e}")

    st.markdown(get_table_download_link(data), unsafe_allow_html=True)

footer = """
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #111;
    color: #fff;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
</style>
<div class="footer">
    Developed with ❤️ and care by <a href="https://github.com/Suriya-002" target="_blank">Suriya</a>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
