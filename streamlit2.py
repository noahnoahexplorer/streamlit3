import streamlit as st
import pandas as pd
import ast
import numpy as np
import plotly.express as px

# Title of the app
st.title("Lottery Betting Heatmap Visualization")

# File uploader for CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file and ensure 'number_cost_dict' column is read correctly
    df = pd.read_csv(uploaded_file, dtype={'username': str})

    # Clean column names by stripping any leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Check if the 'number_cost_dict' column exists
    if 'number_cost_dict' in df.columns:
        # Convert the 'number_cost_dict' column from string to dictionary
        df['number_cost_dict'] = df['number_cost_dict'].apply(ast.literal_eval)

        # Initialize an array to store the total bet amount for each number (1 to 100)
        bet_totals = np.zeros(100)

        # Loop through each row in the dataframe
        for _, row in df.iterrows():
            for number, bet in row['number_cost_dict'].items():
                number = int(number)  # Ensure the number is an integer
                bet_totals[number - 1] += bet  # Add the bet amount to the corresponding number

        # Create a DataFrame for the heatmap
        heatmap_df = pd.DataFrame({
            'Number': np.arange(1, 101),
            'Total Bet Amount': bet_totals
        })

        # Reshape the data for a 10x10 heatmap grid
        heatmap_data = heatmap_df.pivot_table(values='Total Bet Amount', 
                                              index=pd.cut(heatmap_df['Number'], bins=np.arange(1, 102, 10), labels=range(1, 11)),
                                              columns=pd.cut(heatmap_df['Number'], bins=np.arange(1, 102, 10), labels=range(1, 11))))

        # Plot the heatmap
        fig = px.imshow(heatmap_data, 
                        labels=dict(x="Numbers", y="Bet Amounts", color="Total Bet Amount"),
                        x=heatmap_data.columns,
                        y=heatmap_data.index,
                        title="Heatmap of Bets on Numbers")

        # Display the heatmap
        st.plotly_chart(fig)
    else:
        st.write("The 'number_cost_dict' column is not found in the dataset.")
