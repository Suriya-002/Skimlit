# imports
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Ensure the theme is dark
st.set_page_config(layout="wide")

st.title("Skimlit 🌌")

st.write("""
### Welcome to Skimlit!

Harness the power of AI and data visualization in just a few clicks. Skimlit is designed to turn raw CSV data into insightful visualizations while also cleaning up any inconsistencies.

🔍 **Explore** - Dive deep into your data's hidden patterns.
✨ **Transform** - Let Skimlit work its magic on your raw datasets.
📊 **Visualize** - Watch as your data comes to life in vivid charts.

---

#### 🚀 How to Use Skimlit:

1. **Upload Your CSV**: Use the uploader below to provide your dataset.
2. **Wait for Magic**: Skimlit will preprocess your data, handling missing values and more.
3. **Enjoy the Visuals**: Scroll down to discover histograms, bar charts, pie charts, and more insightful representations of your data columns.
4. **Download**: Want your cleaned data? Hit the 'Download cleaned data' button at the end.

Ready to embark on your data journey? Let's get started!
""")


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df, filename='data.xlsx', text='Download cleaned data'):
    val = to_excel(df)
    b64 = base64.b64encode(val)
    button_html = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}" style="display:inline-block;background-color:#f63366;color:white;padding:8px 16px;border-radius:4px;text-decoration:none">{text}</a>'
    return button_html

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    # Show the original data
    st.write("Original Data")
    st.write(data)

    # Data Preprocessing
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
    non_numeric_cols = data.select_dtypes(exclude=['float64', 'int64']).columns
    for col in non_numeric_cols:
        mode_val = data[col].mode()[0]
        data[col] = data[col].fillna(mode_val)

    # Visualization
    st.write("Feature Distributions and Insights")
    for column in data.columns:
        # Numeric columns
        if data[column].dtype in ['float64', 'int64']:
            # Histogram
            fig, ax = plt.subplots()
            sns.histplot(data[column], ax=ax)
            ax.set_title(f'Histogram for {column}', fontsize=15)
            st.pyplot(fig)
            # Box Plot
            fig, ax = plt.subplots()
            sns.boxplot(data[column], ax=ax)
            ax.set_title(f'Box Plot for {column}', fontsize=15)
            st.pyplot(fig)
        # Categorical columns
        else:
            if data[column].nunique() <= 10:
                fig, ax = plt.subplots()
                data[column].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax, legend=True, fontsize=10)
                ax.set_title(f'Pie Chart for {column}', fontsize=15)
                st.pyplot(fig)
            else:
                fig, ax = plt.subplots()
                data[column].value_counts().plot.bar(ax=ax, legend=True, fontsize=10)
                ax.set_title(f'Bar Chart for {column}', fontsize=15)
                st.pyplot(fig)
    # Correlation heatmap for numeric columns
    corr = data[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(10,8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title('Correlation Heatmap', fontsize=15)
    st.pyplot(fig)

    # Download link for cleaned data in Excel format styled as a button
    st.markdown(get_table_download_link(data), unsafe_allow_html=True)

# Footer
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
