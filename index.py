import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import datetime
import warnings
import base64

warnings.filterwarnings("ignore")

# _______________________________________________________________________________________________________________
# importing raw data
raw_data = pd.read_csv(r"./cpi Group data.csv")

# _______________________________________________________________________________________________________________
# preprocessing data
# print(raw_data)
# print(raw_data.info())

# observing all the unique values of every column (before cleaning)
# print(f"{raw_data['BaseYear'].value_counts()} \n\n {raw_data['Year'].value_counts()} \n\n {raw_data['Month'].value_counts()} \n\n {raw_data['State'].value_counts()}")
# print(f"\n\n {raw_data['Sector'].value_counts()} \n\n {raw_data['Group'].value_counts()} \n\n {raw_data['SubGroup'].value_counts()} \n\n {raw_data['Index'].value_counts()}\n\n {raw_data['Inflation (%)'].value_counts()}")

# we have noticed that the data is right skewed in terms of "Inflation %" and "Index" so replacing them with index
# Replace '*' with NaN
data = raw_data
data.replace("*", np.nan, inplace=True)

# Convert columns to numeric (to handle NaN correctly)
data["Inflation (%)"] = pd.to_numeric(raw_data["Inflation (%)"], errors='coerce')
data["Index"] = pd.to_numeric(raw_data["Index"], errors='coerce')

# Replace NaN with median of respective columns
data["Inflation (%)"].fillna(raw_data["Inflation (%)"].median(), inplace=True)
data["Index"].fillna(raw_data["Index"].median(), inplace=True)

data['BaseYear'] = [str(i) for i in data["BaseYear"]]
data['Year'] = [str(i) for i in data["Year"]]

# _______________________________________________________________________________________________________________
# applying the css
# Encode image to base64

# with open("cpi1.png", "rb") as image_file:
#     encoded_image = base64.b64encode(image_file.read()).decode()

# Optional background image
with open("bg1.png", "rb") as bg_file:
    bg_image = base64.b64encode(bg_file.read()).decode()



    #    /* Full screen overlay */
    #     .intro-sheet 
    #     {{
    #         position: fixed;
    #         top: 0;
    #         left: 0;
    #         height: 100%;
    #         width: 100%;
    #         background-color: rgba(0, 0, 0, 0.85); /* optional: dim background */
    #         z-index: 9999;
    #         display: flex;
    #         align-items: center;
    #         justify-content: center;
    #         transition: transform 0.5s ease-in-out;
    #     }}

    #     .intro-sheet img 
    #     {{
    #         max-width: 100%;
    #         max-height: 100%;
    #         transition: transform 0.3s ease-in-out;
    #         border-radius: 20px;
    #         box-shadow: 0 0 40px rgba(255,255,255,0.2);
    #     }}

    #     .intro-sheet img:hover 
    #     {{
    #         transform: scale(1.05);
    #     }}
        
    #     .image {{
    #         position: relative;
    #         transition: transform 0.3s ease-in-out;
    #         display: block;
    #         margin: auto;
    #         width: 100%; /* optional */
    #     }}

    #     .image:hover {{
    #         transform: translateY(-50px);
    #     }}
    # 
    #   YE WAALA <style></style> ke baad likhna hai
    #   <img src="data:image/png;base64,{encoded_image}" alt="Your Image" class="image">



# CSS and image rendering
st.markdown(
    f"""
    <style>
 
        .stApp {{
           background-image: url("data:image/png;base64,{bg_image}");
           background-size: cover;
           background-position: center;
           height: 100%;
           background-attachment: property;
        }}
    </style>


    """,
    unsafe_allow_html=True
)

# _______________________________________________________________________________________________________________
# making the UI

st.metric(label="hi", value="Consumer Price Index - 2013 to 2025", label_visibility="hidden")
tabs = st.tabs(["Introduction","Static data","Data Insights","Comparision"])

# Introduction slide
with tabs[0]:
    st.write("""The Consumer Price Index (CPI) dataset provides a comprehensive record of price changes over time, measuring 
inflation trends across different regions, sectors, and consumption categories. It consists of 304,871 rows and includes 
the following key attributes:""")
    
    st.write(
'''BaseYear: The reference year against which price changes are measured.

Year: The specific year of the recorded CPI data.

Month: The month corresponding to the recorded CPI data.

State: The geographic region where the data was collected.

Sector: Classification into urban or rural areas.

Group: Broad expenditure category, such as Food, Housing, Transport, etc.

SubGroup: A more detailed breakdown of specific goods or services within a group.

Index: The CPI value, representing the cost of a basket of goods and services relative to the base year.

Inflation (%): The percentage change in CPI over a specified period, indicating the rate of inflation.''')

    st.divider()
    st.dataframe(data, height=1000, width=7000)

# static data
with tabs[1]:
    st.header("Year")
    a = st.radio(label= "Year", options = sorted(data['Year'].unique()), horizontal = True, key="static[0]", label_visibility='collapsed')    
        
    # Group recorded for inflation
    st.header("Category Ratio per Year")
    col1, = st.columns(1)

    with col1:
        a2 = data[data["Year"]==a]["Group"].value_counts()
        a3, a4 = plt.subplots()
        a4.pie(a2, autopct='%1.1f%%', startangle=90, pctdistance=0.78)
        a4.set_title("Category Ratio per Year", fontsize=18, fontweight='bold')
        plt.legend(a2.index, loc="lower left", bbox_to_anchor=(-0.5, 0))
        st.pyplot(a3)

    st.header("Sector Ratio per Year")
    col2, = st.columns(1)
    # sector recorded for inflation
    with col2:
        a2 = data[data["Year"]==a]["Sector"].value_counts()
        a3, a4 = plt.subplots(figsize=(5,5))
        a4.pie(a2, labels=a2.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 20})
        a4.set_title("Sector Ratio per Year", fontsize=14, fontweight='bold')
        st.pyplot(a3)

    # inflation with respect to year
    st.header("Inflation per Year")
    col3, = st.columns(1)
    with col3:
        a1 = data[data['State']=="All India"][['Year','Inflation (%)']].groupby('Year').median()
        # a2 = data[data['State'] !="All India"][['Year','Inflation (%)']].groupby('Year').median()
        a1.index = pd.to_datetime(a1.index, format='%Y')
        st.line_chart(a1, x_label="Year", y_label="Inflation (%)")
        # st.line_chart(a2, x_label="year", y_label="Inflation (%)")
    
    st.divider()
    # graphs with respect to graph (Category)
    st.header("Category")
    a6 = st.radio(options = data["Group"].unique(), label="Category", horizontal=True, label_visibility='collapsed')
    
    col8, = st.columns(1)

    # inflation of {group} w.r.t. year
    with col8:
        a1 = data[data['Group']== a6][['Year','Inflation (%)']].groupby('Year').median()
        a1.index = pd.to_datetime(a1.index, format='%Y')
        
        st.header(f"Inflation of {a6} item with respect to year")
        st.line_chart(a1, x_label="Year", y_label="Inflation (%)")


    # inflation of {sub-group} w.r.t. year
    col5,  = st.columns(1)   
    with col5:
        b2 = list(data[data["Group"]==a6]['SubGroup'].unique())
        b2.remove(np.nan)
        if (b2 == []):
            st.info("Sub-category not available")
        else:
            # sub-group ratio of each group 
            st.header(f"Sub-group Ratio of {a6}")
            a7 = data[data['Group']==a6]["SubGroup"].value_counts()
            col6,  = st.columns(1)    
            with col6:
                a3, a4 = plt.subplots(figsize=(10,10))
                a4.pie(a7, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 20}, labels = a7.index)
                st.pyplot(a3)

            # Inflation of subgroup w.r.t year
            col7, = st.columns(1)
            with col7:
                st.header("Category")
                a8 = st.radio(options = data[data['Group']==a6]["SubGroup"].unique(), label="Category", horizontal=True, label_visibility="collapsed")
                a9 = data[data['SubGroup']== a8][['Year','Inflation (%)']].groupby('Year').median()
                a9.index = pd.to_datetime(a9.index, format='%Y')
                st.line_chart(a9, x_label="Year", y_label="Inflation (%)")

    
        
    
month_order = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

# dynamic data
with tabs[2]:
    # option of ratio
    st.header("Year")
    a = st.radio(label= "Year", options = sorted(data['Year'].unique()), horizontal = True, key="dynamic[0]", label_visibility="collapsed")
    
    st.header(f"Inflation Rate of Each State in {a}")
    col1, = st.columns(1)
    # inflation of each state of chosen year
    with col1:
        a1 = data[data['Year']==a][['State', 'Inflation (%)']].groupby('State').median()
        st.bar_chart(a1, x_label="States", y_label="Inflations (%)")
        
    # inflation of each month of chosen year
    st.header(f"Inflation Rate Each Month in {a}")
    col2,  = st.columns(1)
    with col2:
        a2 = data[data["Year"] == a][['Month','Inflation (%)']].groupby('Month').median().sort_values("Month")
        a2.index = pd.Categorical(a2.index, categories=month_order, ordered=True,)
        a2.sort_index()
        st.line_chart(a2, x_label="Month", y_label="Inflation (%)")

    # option of {state} to be chosen
    st.divider()
    st.header("States")            
    col3, col4 = st.columns(2)

    with col3:
        a4 = st.selectbox(options = data['State'].unique(), label = "States",  label_visibility='collapsed')

    with col4:
        a = st.radio(label= "Year", options = sorted(data['Year'].unique()), horizontal = True, key="dynamic[2]", label_visibility="collapsed")
    
    col5, col6= st.columns(2)
    
    # inflation of chosen {state} w.r.t. year
    with col5:
        st.header(f"Inflation Rate of {a4} in {a}")
        a1 = data[data['State'] == a4][['Year', 'Inflation (%)']].groupby("Year").median()
        a1.index = pd.to_datetime(a1.index, format='%Y')
        st.line_chart(a1, x_label="Year", y_label="Inflation (%)")   
        
    # index of chosen {state} w.r.t. year
    with col6:
        st.header(f"Index Rate of {a4} in {a}")
        a1 = data[data['State'] == a4][['Year', 'Index']].groupby("Year").median()
        a1.index = pd.to_datetime(a1.index, format='%Y')
        st.line_chart(a1, x_label="Year", y_label="Index")   
        
    
    col5,  = st.columns(1)
    with col5:
        st.header(f"Inflation Rate Per Month of {a4} in {a}")
        a9 = data[(data['Year']==a) & (data['State']==a4)][['Month','Inflation (%)']].groupby('Month').median()
        st.line_chart(a9)
        
        
with tabs[3]:  
    a4 = data['State'].unique()
    st.header("Comparision of Inflation Rate of Indian States")
    a5 = st.multiselect(label="Select States", options=a4, max_selections=3, default="All India")


    if a5:
        combined_df = pd.DataFrame()  # Empty DataFrame to store merged data

        for state in a5:
            a6 = data[data['State'] == state][['Year', 'Inflation (%)']].groupby('Year').median()
            a6.rename(columns={"Inflation (%)": state}, inplace=True)  # Rename column to state name
            
            if combined_df.empty:
                combined_df = a6
            else:
                combined_df = combined_df.join(a6, how='outer')  # Merge states' data

        combined_df.index = pd.to_datetime(combined_df.index, format='%Y')  # Convert index to datetime
        st.line_chart(combined_df)  # Single chart with multiple lines

