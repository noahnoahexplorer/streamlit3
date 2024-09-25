import streamlit as st
import pandas as pd
import ast
from itertools import combinations
import plotly.express as px
import plotly.graph_objects as go

# Title of the app
st.title("CSV File Uploader with Total Cost Calculation and Group Analysis")

# Create a file uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Sidebar for filters
avg_cost_threshold = st.sidebar.slider("Minimum Average Cost Threshold", min_value=0, max_value=200, value=50)
unique_count_threshold = st.sidebar.slider("Minimum Unique Number Count Threshold", min_value=0, max_value=100,
                                           value=10)
group_unique_number_threshold = st.sidebar.slider("Combinations of rows with more than how many unique numbers",
                                                  min_value=0, max_value=100, value=70)
group_profit_rate_range = st.sidebar.slider("Group Profit Rate (%)", min_value=-200, max_value=100, value=(-10, 10))
group_max_overlapping_number_threshold = st.sidebar.slider("Group Maximum Overlapping Number Count", min_value=0,
                                                           max_value=100, value=5)
avg_cost_diff_threshold = st.sidebar.slider("Max Average Cost Difference", min_value=0, max_value=100, value=50)

# Apply filter button
apply_filter = st.sidebar.button("Apply Filter")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file and ensure 'username' column is read as a string
    df = pd.read_csv(uploaded_file, dtype={'username': str})

    # Display the raw data with total number of rows
    st.write(f"Raw Data (Total number of rows: {df.shape[0]}):")
    st.dataframe(df)

    # Clean column names by stripping any leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Check if the 'number_cost_dict' column exists
    if 'number_cost_dict' in df.columns:
        # Convert the 'number_cost_dict' column from string to dictionary
        df['number_cost_dict'] = df['number_cost_dict'].apply(ast.literal_eval)

        # Ensure all keys in the dictionaries are strings (fix for Arrow compatibility)
        df['number_cost_dict'] = df['number_cost_dict'].apply(
            lambda d: {str(k): v for k, v in d.items()} if isinstance(d, dict) else d
        )

        # Calculate the total cost for each row in 'number_cost_dict'
        df['total_cost'] = df['number_cost_dict'].apply(lambda x: sum(x.values()))

        # Check if the 'rewards' column exists in the data
        if 'rewards' not in df.columns:
            st.write("The 'rewards' column is not found in the dataset. Please check your data.")
        else:
            # Calculate the average cost for each row
            df['avg_cost'] = df['number_cost_dict'].apply(lambda x: sum(x.values()) / len(x))

            # Calculate the unique count of numbers in 'number_cost_dict'
            df['unique_count'] = df['number_cost_dict'].apply(lambda x: len(set(x.keys())))

            # Apply the filters when the button is clicked
            if apply_filter:
                # Filter rows where avg_cost > threshold and unique_count > threshold
                filtered_df = df[(df['avg_cost'] > avg_cost_threshold) & (df['unique_count'] > unique_count_threshold)]

                # Display the filtered dataframe and total number of rows in the filtered data
                st.write(
                    f"Rows with average cost greater than {avg_cost_threshold} and unique count greater than {unique_count_threshold} (Total number of rows: {filtered_df.shape[0]}):")
                st.dataframe(filtered_df)

                # Profit Rate calculation and distribution visualization
                filtered_df['profit_rate'] = (filtered_df['rewards'] - filtered_df['total_cost']) / filtered_df[
                    'total_cost'] * 100

                # Total cost distribution (with Plotly)
                st.subheader("Total Cost Distribution")
                fig_total_cost = px.bar(filtered_df, x=filtered_df.index, y='total_cost', title="Total Cost per Bet")
                st.plotly_chart(fig_total_cost)

                # Profit Rate distribution (with Plotly)
                st.subheader("Profit Rate Distribution (%)")
                fig_profit_rate = px.histogram(filtered_df, x='profit_rate', nbins=20, title="Profit Rate Distribution")
                st.plotly_chart(fig_profit_rate)

                # Average cost and unique number count scatter plot (with Plotly)
                st.subheader("Average Cost vs Unique Number Count")
                fig_avg_vs_unique = px.scatter(filtered_df, x='avg_cost', y='unique_count',
                                               title="Average Cost vs Unique Number Count",
                                               labels={'avg_cost': 'Average Cost', 'unique_count': 'Unique Numbers'})
                st.plotly_chart(fig_avg_vs_unique)

                # Heatmap for overlapping numbers
                st.subheader("Number Overlap Heatmap")
                numbers_list = [set(d.keys()) for d in filtered_df['number_cost_dict']]
                overlap_matrix = [[len(a & b) for b in numbers_list] for a in numbers_list]
                fig_heatmap = go.Figure(data=go.Heatmap(z=overlap_matrix,
                                                        x=filtered_df.index,
                                                        y=filtered_df.index,
                                                        colorscale='Viridis'))
                st.plotly_chart(fig_heatmap)

                # You can add more advanced visualizations as needed
