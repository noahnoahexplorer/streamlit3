import streamlit as st
import pandas as pd
import ast
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Title of the app
st.title("CSV File Uploader with Betting Heatmap Visualization")

# Create a file uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file, dtype={'username': str})

    # Display the raw data with the total number of rows
    st.write(f"Raw Data (Total number of rows: {df.shape[0]}):")
    st.dataframe(df)

    # Clean column names by stripping any leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Check if the 'number_cost_dict' column exists
    if 'number_cost_dict' in df.columns:
        # Convert the 'number_cost_dict' column from string to dictionary
        df['number_cost_dict'] = df['number_cost_dict'].apply(ast.literal_eval)

        # Initialize an array to store the total bets on each number (from 1 to 100)
        total_bets = np.zeros(100)

        # Loop through each row and aggregate the betting amounts by number
        for _, row in df.iterrows():
            bet_dict = row['number_cost_dict']
            for number, bet_amount in bet_dict.items():
                # Add the bet amount to the corresponding number in total_bets array
                total_bets[int(number) - 1] += bet_amount

        # Create a DataFrame for heatmap visualization
        heatmap_data = pd.DataFrame(total_bets.reshape(10, 10))  # Reshape into 10x10 grid for the heatmap
        heatmap_data.columns = [f'{i+1}' for i in range(10)]     # Label columns as 1-10, 11-20, etc.
        heatmap_data.index = [f'{i*10+1}-{(i+1)*10}' for i in range(10)]  # Label rows based on range 1-10, 11-20, etc.

        # Visualize the heatmap
        st.subheader("Heatmap of Total Bets by Number (1 to 100)")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlGnBu', ax=ax)
        st.pyplot(fig)
    else:
        st.write("The 'number_cost_dict' column is not found in the dataset. Please check your data.")
