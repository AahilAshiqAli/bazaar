import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.write("# Daily Sales Revenue  for the Month in Thousands")

df = pd.read_csv("Analytics Case Study - Launchpad 2024 (Dataset).csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='%d/%m/%Y')

df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date'], format='%d/%m/%Y')
df = df.iloc[:, :-16]

# Daily Revenue
daily_revenue = df[df['order_status'] == 'CLOSED'].groupby('order_date').apply(
    lambda x: (x['amount_per_unit'] * x['ordered_quantity'] - x['item_discount']).sum()
).reset_index(name='daily_revenue')

plt.figure(figsize=(20, 10))
plt.plot(daily_revenue['order_date'], daily_revenue['daily_revenue'], marker='o')
plt.title('Daily Sales Revenue Over Time')
plt.xlabel('Date')
plt.ylabel('Sales Revenue')
plt.grid(True)
plt.savefig('daily_revenue.png')

st.image("daily_revenue.png",use_column_width=True)


# Assuming you have loaded your DataFrame 'df'

# Group by warehouse ID and store ID and count unique order numbers
orders_by_warehouse_store = df.groupby(['order_warehouse_id', 'store_id'])['order_number'].nunique().reset_index(name='order_count')

# Calculate the total orders for each store
total_orders_by_store = orders_by_warehouse_store.groupby('store_id')['order_count'].sum()

# If you also want to know the total orders for each warehouse, you can do:
total_orders_by_warehouse = orders_by_warehouse_store.groupby('order_warehouse_id')['order_count'].sum()

# Streamlit app
st.title('Comparison of Single and Repeated Orders per Warehouse')

# Create a list of warehouses
warehouses = orders_by_warehouse_store['order_warehouse_id'].unique()

# Initialize lists to store counts for each warehouse
count_greater_than_1_list = []
count_equal_to_1_list = []

# Loop through each warehouse
for warehouse_id in warehouses:
    # Filter the data for the selected warehouse
    warehouse_data = orders_by_warehouse_store[orders_by_warehouse_store['order_warehouse_id'] == warehouse_id]
    
    # Calculate the count of orders where the count is greater than 1 and where it's equal to 1
    count_greater_than_1 = len(warehouse_data[warehouse_data['order_count'] > 1])
    count_equal_to_1 = len(warehouse_data[warehouse_data['order_count'] == 1])
    
    # Append counts to the respective lists
    count_greater_than_1_list.append(count_greater_than_1 / len(warehouse_data))
    count_equal_to_1_list.append(count_equal_to_1 / len(warehouse_data))
# Plotting the bar graph
plt.figure(figsize=(10, 6))
plt.bar(warehouses, count_greater_than_1_list, label='Count > 1', color='skyblue')
plt.bar(warehouses, count_equal_to_1_list, bottom=count_greater_than_1_list, label='Count = 1', color='salmon')
plt.xlabel('Warehouse ID')
plt.ylabel('Number of Orders')
plt.title('Comparison of Orders (Count > 1 vs Count = 1) for Each Warehouse')
plt.legend()
plt.xticks(rotation=45)
plt.grid(axis='y')

# Save the bar graph
plt.savefig('warehouse_order_comparison_bargraph.png')

# Display the bar graph in Streamlit
st.image('warehouse_order_comparison_bargraph.png', use_column_width=True)


orders_by_warehouse = df.groupby('order_warehouse_id').size().reset_index(name='order_count')
st.title("Distribution of Orders by Warehouse")
# Plot the pie chart
plt.figure(figsize=(10, 10))
plt.pie(orders_by_warehouse['order_count'], labels=orders_by_warehouse['order_warehouse_id'], autopct='%1.1f%%')
plt.title('Distribution of Orders by Warehouse')
plt.savefig('warehouse_distribution.png')

# Display the bar graph in Streamlit
st.image('warehouse_distribution.png', use_column_width=True)

st.title("Distribution of Orders by Stores ")
# Calculate total revenue by store
revenue_by_store = df[df['order_status'] == 'CLOSED'].groupby('store_id').apply(
    lambda x: (x['amount_per_unit'] * x['ordered_quantity'] - x['item_discount']).sum()
).reset_index(name='total_revenue')

# Plot the bar chart
plt.figure(figsize=(14, 7))
sns.barplot(data=revenue_by_store, x='store_id', y='total_revenue')
plt.title('Total Revenue by Store')
plt.xlabel('Store ID')
plt.ylabel('Total Revenue')
plt.xticks(rotation=90)
plt.savefig("store_distribution.png")
st.image("store_distribution.png",use_column_width = True)


warehouse_order_status_counts = df.groupby('order_warehouse_id')['order_status'].value_counts().unstack().fillna(0)

# Calculate the total counts for each warehouse
warehouse_order_status_counts['total_orders'] = warehouse_order_status_counts.sum(axis=1)

# Calculate the normalized scores for each warehouse
for status in ['CANCELLED', 'CLOSED']:
    warehouse_order_status_counts[f'{status}_normalized'] = warehouse_order_status_counts[status] / warehouse_order_status_counts['total_orders']

# Plotting the bar graph
plt.figure(figsize=(10, 6))
warehouse_order_status_counts[['CANCELLED_normalized', 'CLOSED_normalized']].plot(kind='bar', stacked=True)
plt.xlabel('Warehouse ID')
plt.ylabel('Normalized Count')
plt.title('Normalized Counts of Cancelled and Closed Orders per Warehouse')
plt.xticks(rotation=45)
plt.legend(title='Order Status')
plt.grid(axis='y')

# Save the bar graph
plt.savefig('warehouse_order_status_bargraph.png')

# Display the bar graph in Streamlit
st.image('warehouse_order_status_bargraph.png', use_column_width=True)
