import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io  # For handling uploaded files

# Function to categorize (expand with your rules; supports Spanish keywords)
def categorize_transactions(df):
    def get_category(description):
        desc = description.lower()
        if any(word in desc for word in ['supermercado', 'comida', 'groceries', 'mercado']):
            return 'Groceries / Comestibles'
        elif any(word in desc for word in ['restaurante', 'dining', 'comida fuera', 'restaurant']):
            return 'Dining Out / Comida Fuera'
        elif any(word in desc for word in ['alquiler', 'hipoteca', 'housing', 'renta']):
            return 'Housing / Vivienda'
        elif any(word in desc for word in ['transporte', 'gasolina', 'transport', 'transito']):
            return 'Transportation / Transporte'
        else:
            return 'Other / Otro'
    
    df['Category'] = df['Description'].apply(get_category)
    return df

# Function to analyze
def analyze_data(df):
    category_sums = df.groupby('Category')['Amount'].sum().reset_index()
    total = df['Amount'].sum()
    insights = f"Total Expenses: ${total:.2f}\nLargest category: {category_sums.loc[category_sums['Amount'].idxmax()]['Category']}"
    return category_sums, total, insights

# Streamlit UI
st.title("Personal Finance Agent App")
st.write("Upload your bank statement (CSV format) and analyze your finances privately.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file, encoding='utf-8')  # Assume columns: Date, Description, Amount
    st.write("Preview of your data:")
    st.dataframe(df.head())
    
    if st.button("Categorize & Analyze"):
        categorized_df = categorize_transactions(df)
        category_sums, total, insights = analyze_data(categorized_df)
        
        # Display table
        st.subheader("Categorized Expenses")
        st.dataframe(category_sums)
        
        # Pie chart
        fig, ax = plt.subplots()
        ax.pie(category_sums['Amount'], labels=category_sums['Category'], autopct='%1.1f%%')
        st.pyplot(fig)
        
        # Insights
        st.subheader("Insights")
        st.write(insights)
        
        # Export option
        csv = category_sums.to_csv(index=False).encode('utf-8')
        st.download_button("Download Report", data=csv, file_name="finance_report.csv", mime="text/csv")