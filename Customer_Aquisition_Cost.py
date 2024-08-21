import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
data = pd.read_csv("customer_acquisition_cost_dataset.csv")
data['CAC'] = data['Marketing_Spend'] / data['New_Customers']
data['Conversion_Rate'] = data['New_Customers'] / data['Marketing_Spend'] * 100
data['Break_Even_Customers'] = data['Marketing_Spend'] / data['CAC']

# Streamlit app
st.title("📊 Customer Acquisition Cost Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
channels = st.sidebar.multiselect("Select Marketing Channels:", options=data['Marketing_Channel'].unique(), 
                                  default=data['Marketing_Channel'].unique())

min_customers = st.sidebar.slider("Minimum Number of New Customers:", 
                                  min_value=int(data['New_Customers'].min()), 
                                  max_value=int(data['New_Customers'].max()), 
                                  value=(int(data['New_Customers'].min()), int(data['New_Customers'].max())))

# Apply Filters
filtered_data = data[(data['Marketing_Channel'].isin(channels)) & 
                     (data['New_Customers'].between(min_customers[0], min_customers[1]))]

# Add a sidebar toggle for switching between visualizations
toggle = st.sidebar.radio("Choose a Visualization", ["CAC by Marketing Channel", "New Customers vs. CAC", 
                                                     "Conversion Rates", "Break-Even Customers",
                                                     "Actual vs. Break-Even Customers", 
                                                     "Spend per New Customer"])

if toggle == "CAC by Marketing Channel":
    fig1 = px.bar(filtered_data, x='Marketing_Channel', y='CAC', title='CAC by Marketing Channel')
    st.plotly_chart(fig1)

elif toggle == "New Customers vs. CAC":
    fig2 = px.scatter(filtered_data, x='New_Customers', y='CAC', color='Marketing_Channel', 
                      title='New Customers vs. CAC', trendline='ols')
    st.plotly_chart(fig2)

elif toggle == "Conversion Rates":
    fig3 = px.bar(filtered_data, x='Marketing_Channel', y='Conversion_Rate', 
                  title='Conversion Rates by Marketing Channel')
    st.plotly_chart(fig3)

elif toggle == "Break-Even Customers":
    fig4 = px.bar(filtered_data, x='Marketing_Channel', y='Break_Even_Customers', 
                  title='Break-Even Customers by Marketing Channel')
    st.plotly_chart(fig4)

elif toggle == "Actual vs. Break-Even Customers":
    fig5 = go.Figure()

    # Actual Customers Acquired
    fig5.add_trace(go.Bar(x=filtered_data['Marketing_Channel'], y=filtered_data['New_Customers'],
                         name='Actual Customers Acquired', marker_color='royalblue'))

    # Break-Even Customers
    fig5.add_trace(go.Bar(x=filtered_data['Marketing_Channel'], y=filtered_data['Break_Even_Customers'],
                         name='Break-Even Customers', marker_color='lightcoral'))

    # Update the layout
    fig5.update_layout(barmode='group', title='Actual vs. Break-Even Customers by Marketing Channel',
                      xaxis_title='Marketing Channel', yaxis_title='Number of Customers')

    st.plotly_chart(fig5)

elif toggle == "Spend per New Customer":
    fig6 = px.scatter(filtered_data, x='New_Customers', y='Marketing_Spend', 
                      color='Marketing_Channel', title='Spend per New Customer')
    st.plotly_chart(fig6)

# Display summary statistics
st.subheader("Summary Statistics")
summary_stats = filtered_data.groupby('Marketing_Channel')['CAC'].describe()
st.write(summary_stats)

# Display the filtered dataframe with download option
st.subheader("Filtered Data Table")
st.dataframe(filtered_data)

# Download button for filtered data
st.download_button(label="Download Filtered Data", 
                   data=filtered_data.to_csv(index=False), 
                   file_name='filtered_data.csv',
                   mime='text/csv')
