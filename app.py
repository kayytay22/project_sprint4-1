import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from matplotlib import pyplot as plt

cars = pd.read_csv('vehicles_us.csv')

cars.rename(columns={'model_year': 'year'}, inplace=True)
cars['year'] = cars['year'].astype('Int64')
cars['date_posted'] = pd.to_datetime(cars['date_posted'], format='%Y-%m-%d')
cars['is_4wd'] = cars['is_4wd'].fillna(0).astype(bool)
cars['paint_color'] = cars['paint_color'].fillna('unknown')

filtered_cars = cars[(cars['price'] >= 100) & (cars['price'] <= 110000)].copy()
# filtered the cars dataframe to include only cars with price between 100 and 110000
# No one would sell a real car for less than 100 dollars
# The cars above 110000 are old cars that are not even close to that price on the market
# the highest price for a car in 109999, being an old chevy corvette which may actally be worth that much.

def categorize_brand(row):
    """ This function categorizes car brands based on the model name."""

    model = row['model'].lower()
    if 'ford' in model:
        return 'Ford'
    elif 'chevrolet' in model or 'chevy' in model:
        return 'Chevrolet'
    elif 'toyota' in model:
        return 'Toyota'
    elif 'honda' in model:
        return 'Honda'
    elif 'nissan' in model:
        return 'Nissan'
    elif 'jeep' in model:
        return 'Jeep'
    elif 'bmw' in model:
        return 'BMW'
    elif 'mercedes' in model or 'benz' in model:
        return 'Mercedes-Benz'
    elif 'acura' in model:
        return 'Acura'
    elif 'volkswagen' in model:
        return 'Volkswagen'
    elif 'hyundai' in model:
        return 'Hyundai'
    elif 'chrysler' in model:
        return 'Chrysler'
    elif 'kia' in model:
        return 'Kia'
    elif 'dodge' in model or 'ram' in model:
        return 'Dodge'
    elif 'gmc' in model:
        return 'GMC'
    elif 'subaru' in model:
        return 'Subaru'
    elif 'cadillac' in model:
        return 'Cadillac'
    elif 'buick' in model:
        return 'Buick'
    else:
        return 'Other'
filtered_cars['brand'] = filtered_cars.apply(categorize_brand, axis=1)

# now we will start building the streamlit app

st.header('Cars for Sale')
st.markdown('---')
st.write(""" #### **This App analyzes the dataset of vehicles for sale** """)

st.sidebar.header('Filter Options')
years_in_data = sorted(filtered_cars['year'].dropna().unique(), reverse=True)
year_options = ['All Years'] + [str(year) for year in years_in_data if year >= 1960] + ['Cars older than 1960']
selected_year = st.sidebar.selectbox('Select Year:', year_options)
if selected_year == 'All Years':
    selected_cars = filtered_cars
elif selected_year == 'Cars older than 1960':
    selected_cars = filtered_cars[filtered_cars['year'] < 1960]
else:
    year_value = int(selected_year)
    selected_cars = filtered_cars[filtered_cars['year'] == year_value]

# Adding a price slider
min_price = int(filtered_cars['price'].min())
max_price = int(filtered_cars['price'].max())
price_range = st.sidebar.slider(
    'Select price range:',
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

selected_cars = selected_cars[
    (selected_cars['price'] >= price_range[0]) & (selected_cars['price'] <= price_range[1])
]
# Adding a checkbox for 4wd
is_4wd = st.sidebar.checkbox('Show only 4WD cars')

if is_4wd:
    selected_cars = selected_cars[selected_cars['is_4wd'] == True]

# Adding a Brand muliselect
brands = sorted(filtered_cars['brand'].unique())
selected_brands = st.sidebar.multiselect(
    'Select brand(s):',
    options=brands,
    default=brands
)
# Adding a Fuel Type Multiselect
fuel_types = sorted(filtered_cars['fuel'].dropna().unique())
selected_fuel_types = st.sidebar.multiselect(
    'Select fuel type(s):',
    options=fuel_types,
    default=fuel_types
)
# Adding a condition Multiselect
conditions = sorted(filtered_cars['condition'].dropna().unique())
selected_conditions = st.sidebar.multiselect(
    'Select condition(s):',
    options=conditions,
    default=conditions
)
selected_cars = selected_cars[(selected_cars['brand'].isin(selected_brands)) & (selected_cars['fuel'].isin(selected_fuel_types)) & (selected_cars['condition'].isin(selected_conditions))]

st.write(""" ##### Displaying cars matching selected criteria: """)

# Displaying the filtered DataFrame
st.dataframe(selected_cars)

st.markdown('---')
st.header('Histogram of Odometer Distribution by Condition of Vehicles')

# Streamlit multiselect for conditions
conditions = filtered_cars['condition'].unique()
selected_conditions = st.multiselect(
    'Select car condition(s) to display odometer distribution:',
    options=conditions,
    default=list(conditions)
)

filtered_by_condition = filtered_cars[filtered_cars['condition'].isin(selected_conditions)]

# Plotting the histogram for odometer distribtution, sorted by condition
fig, ax = plt.subplots(figsize=(10, 6))
for condition in selected_conditions:
    subset = filtered_by_condition[filtered_by_condition['condition'] == condition]
    ax.hist(subset['odometer'], bins=30, alpha=0.5, label=condition)

ax.set_title('Odometer Distribution by Condition')
ax.set_xlabel('Odometer Reading')
ax.set_ylabel('Number of Cars')
ax.set_xlim(0, 400000)  
ax.set_xticks(range(0, 400001, 50000))
ax.legend(title='Condition')
st.pyplot(fig)

st.markdown('---')
st.header('Scatter Plot: Price vs Year by Brand')
st.write("""###### Please go to fullscreen mode to see full list of brands in the legend\nDouble click on a brand to see only that brand displayed""")
# Creating a Scatter plot using Plotly Express
fig = px.scatter(
    filtered_cars,
    x='year',
    y='price',
    color='brand',
    title='Car Price vs Model Year by Brand',
    labels={'year': 'Year', 'price': 'Price'},
    opacity=0.7,
    template='plotly',
)

fig.update_layout(
    legend_title_text='Brand',
    legend=dict(
        itemsizing='constant',
        itemclick='toggle',  
        itemdoubleclick='toggleothers' 
    )
)

st.plotly_chart(fig, use_container_width=True)

