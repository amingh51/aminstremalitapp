import streamlit as st
import pandas as pd 
import numpy as np
import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly_express as px
import plotly.graph_objects as go
import streamlit_card as st_card
import pandas as pd
from plotly.offline import init_notebook_mode,iplot

df= pd.read_csv("/Users/aminghobar/Desktop/Assignment 3/marketingcampaign.csv")



#dropping null values
df.dropna()

#Dropping rare marital status
df.drop(df.loc[df['Marital_Status']== 'YOLO'].index, inplace=True)
df.drop(df.loc[df['Marital_Status']== 'Alone'].index, inplace=True)
df.drop(df.loc[df['Marital_Status']== 'Absurd'].index, inplace=True)

#Adding Mnt (total amounts spent) column per customer
column_names = ['MntWines','MntFruits','MntMeatProducts','MntFishProducts','MntSweetProducts','MntGoldProds']
df['Total Amount Spent']= df[column_names].sum(axis=1)


#Adding Total number of children column 
column_names = ['Kidhome','Teenhome']

df['Number of Children']= df[column_names].sum(axis=1)


#Adding total number of purchases per customer 
column_names = ['NumDealsPurchases','NumWebPurchases','NumCatalogPurchases','NumStorePurchases','NumWebVisitsMonth']

df['Total Purchases']= df[column_names].sum(axis=1)



# Changing Education categories to PG and UG
df['Education'] = df['Education'].replace(['PhD','2n Cycle','Graduation', 'Master'],'Post Graduate')  
df['Education'] = df['Education'].replace(['Basic'], 'Under Graduate')


# dropping columns 
df.drop(columns= ['Response','Z_Revenue','Z_CostContact','Kidhome','Teenhome','Complain','AcceptedCmp1','AcceptedCmp2','AcceptedCmp3','AcceptedCmp4','AcceptedCmp5'],inplace=True)

df['Dt_Customer'] = df['Dt_Customer'].str[-4:]

df.Dt_Customer.value_counts()

# adding column age 
df['Age']= 2014- df.Year_Birth

df.drop(columns= ['Year_Birth','Dt_Customer'],inplace=True)

#relationship and single
df['Marital_Status'] = df['Marital_Status'].replace(['Married', 'Together'],'Relationship')
df['Marital_Status'] = df['Marital_Status'].replace(['Divorced', 'Widow','Single'],'Single')





## Data Visuals 

#Visual 1 
import plotly.express as px
Ageasc = df.sort_values(by=['Age'])
fig1= px.scatter(Ageasc, x= 'Income', y= 'Total Amount Spent', animation_frame= 'Age', animation_group= 'ID', 
           color= 'Education', hover_name= 'ID', size= 'Total Purchases', size_max= 30,range_x=[1,50000], title=('The Relationship between Age,Income and Educational Level and its effects on Total Amount spent per customer'))



#Visual 2
import plotly.graph_objects as go

labels = ['Number of Deals Purchases','Number of Web Purchases','Number of Catalog Purchases',
          'Number of Store Purchases']

values = [df.NumDealsPurchases.sum(), df.NumWebPurchases.sum(), df.NumCatalogPurchases.sum(),
          df.NumStorePurchases.sum()]

# Use `hole` to create a donut-like pie chart
fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])


#Visual 3
dff= df[['Education', 'Marital_Status', 'Number of Children', 'Total Purchases']]
bins = [0, 20, 35, np.inf]
names = ['Low Volume Purchase', 'Medium Volume Purchase', 'High Volume Purchase']

dff['Total Purchases Volume'] = pd.cut(dff['Total Purchases'], bins, labels=names)

dff.drop('Total Purchases', axis= 1,inplace= True)

fig3 = px.parallel_categories(dff)


#Visual 4
import plotly.graph_objects as go

fig4 = go.Figure(go.Bar(
            x=[df.NumWebVisitsMonth.mean(), df.NumWebPurchases.mean()],
            y=['Average Number of Web Visits per Month', 'Average Number of Web Purchases per Month'],
            orientation='h'))
fig4.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)'})


#Visual 5
bins = [0,50000, 80000, np.inf]
names = ['Low Salary', 'Moderate Salary', 'High Salary']

df['Income'] = pd.cut(df['Income'], bins, labels=names)

df1= (
    df.groupby(df['Income']
    ).agg({'NumDealsPurchases':'mean', 'NumWebPurchases':'mean', 'NumCatalogPurchases':'mean', 'NumStorePurchases': 'mean',
          })
)    
df1.reset_index(inplace=True)

import plotly.express as px
fig5 = px.histogram(df1, x="Income", y=["NumStorePurchases","NumCatalogPurchases","NumWebPurchases", "NumDealsPurchases"], barmode='group',
             height=400)
fig5.update_layout(legend=dict(
    title="Differnt Places of Purchasing"
))
fig5.update_yaxes(title='y', visible=False, showticklabels=True)
fig5.update_xaxes(title='', visible=True, showticklabels=True)
fig5.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)'})


#Visual 6
fig6= px.scatter(df, x="Recency", y="Total Purchases",
           size="Total Amount Spent", hover_name="ID",
           log_x=True, size_max=30,range_x=[0.9,130], range_y=[0,50],labels={
                     "Recency": "Recency (Days)",
                     "TotalPurchases": " Total Number items Purchased",
                 },
                title="Recency Versus Total Number of Items Purchased")

fig6.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)'})



########################################################################################################################################################################################################################################################
#Streamlit app 
import streamlit as st
import hydralit as ht
import hydralit_components as hc
from streamlit_lottie import st_lottie
import streamlit_card as st_card
from pathlib import Path
import base64
import requests 




st.set_page_config(layout='wide' ,page_title= 'Customer Behavior Trends',
page_icon= '💲', initial_sidebar_state= 'expanded',)


def display_app_header(main_txt,sub_txt,is_sidebar = False):
    """
    function to display major headers at user interface
    ----------
    main_txt: str -> the major text to be displayed
    sub_txt: str -> the minor text to be displayed 
    is_sidebar: bool -> check if its side panel or major panel
    """

    html_temp = f"""
    <h2 style = "color:#010101; text_align:center; font-weight: bold;"> {main_txt} </h2>
    <p style = "color:#010101; text_align:center;"> {sub_txt} </p>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(html_temp, unsafe_allow_html = True)
    else: 
        st.markdown(html_temp, unsafe_allow_html = True)


# specify the primary menu definition
menu_data = [
    {'icon': "fas fa-eye", 'label':"Data",'ttip':"discover"},
    {'icon': "fas fa-chart-line", 'label':"Visuals",'ttip':"discover"}
]

#html= """<div id="root"><div><style>:root {--menu_background: #357af7;--txc_inactive: #f0f2f6;--txc_active:#31333F;--option_active:#ffffff;}</style><nav class="navbar navbar-expand-custom navbar-mainbg w-100 py-0 py-md-0"><button class="navbar-toggler" type="button" aria-expanded="false"><i class="fas fa-bars text-white"></i></button><div class="navbar-collapse" id="complexnavbarSupportedContent" style="display: none;"><ul class="navbar-nav py-0"><div class="hori-selector" style="top: 0px; left: 203.683px; height: 56px; width: 129.5px;"><div class="left"></div><div class="right"></div></div><li class="nav-item py-0"><a class="nav-link" href="#0" data-toggle="tooltip" data-placement="top" data-html="true" title="Home"><i class="fa fa-home"></i>  Home</a></li><li class="nav-item py-0"><a class="nav-link" href="#1" data-toggle="tooltip" data-placement="top" data-html="true" title="eda"><i class="fas fa-tachometer-alt"></i> Explore</a></li><li class="nav-item py-0 active"><a class="nav-link" href="#2" data-toggle="tooltip" data-placement="top" data-html="true" title="dash"><i class="fas fa-chart-line"></i> Dashboard</a></li><li class="nav-item py-0"><a class="nav-link" href="#3" data-toggle="tooltip" data-placement="top" data-html="true" title="discover"><i class="fas fa-eye"></i> Discover</a></li><li class="nav-item py-0"><a class="nav-link" href="#4" data-toggle="tooltip" data-placement="top" data-html="true"><i class="fas fa-robot"></i> Machine Learning</a></li></ul></div>
#<img src="https://valoores.com/images/logo.png" style="float:left" width="400" height="100"></nav></div></div>"""
#st.markdown(html, unsafe_allow_html=True)


over_theme = {'menu_background':'#18134A'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home', #will show the st hamburger as well as the navbar now!
    sticky_nav=False, #at the top or not
    hide_streamlit_markers=False,
    sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
)

def load_lottieurl(url):
    r= requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie= load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_qdiq7qa5.json')

#get the id of the menu item clicked
if menu_id== 'Home':
    left, right= st.columns((1,1))
    with left:
        st.title('Customer Behavior Trends')
        display_app_header(main_txt='About Customer Analysis and Trends',
        sub_txt= 'Customers personalities, behavioral and purchase trends vary based on different factors. Such factors may include their age, income, their relationship status and weither they have kids or not. These factors can affect their purchasing or shopping trends alternating their combination of products and the amounts of each product they buy. Insights provided from the analysis on this data will help the business better understand its customers making it easier to modify products to target customers specific needs, behaviors and their concerns.')
        display_app_header(main_txt='About this App',
        sub_txt= 'The following Streamlit app was created to visualize some graphical insights on a marketing campaign dataset that inlcudes information about different customers and their product purchases. The app includes three sections, the home page including a small introduction, a section that describes the dataset and a final section that includes the visuals produced to provide some insight from analyzing the data. This app is a submission for the Data Visualization and Communication (MSBA 325) course assignment submission.')

    with right:
        st_lottie(lottie, height= 350,key= 'coding')

#second page 
if menu_id== 'Data':
    col1, col2= st.columns([1,1])
    
    with col1:
        display_app_header(main_txt='Data Used and Data Preperation',
        sub_txt='')
        st.header('About the Data-set')
        st.write('The following dataset is retrieved from a company including different inofrmation about their customers. The data provides insight on when did the customers start engaing with the company, the different amount that each customer spends on each product, the number of purchases of each product, the relationship status of the customer and the number of children they have. ')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.header('Data Preprocessing')
        st.write('Step1: Identifying Null Values and dropping them using drop.na')
        st.write('Step2: Dropping rare marital status from the Marital_status column')
        st.write('Step3: Adding a column for the total amount spent on products by each customer')
        st.write('Step4: Adding a column for the total amount of purchases for each customer')
        st.write('Step5: Adding a column for the total number of children per customer')
        st.write('Step6: Changing the categories under education column to PG (Post-Graduate) and UG (Undergraduate)')
        st.write('Step7: Dropping unrequired columns')
        st.write('Step8: Adding a new column for the age of each customer')
        st.write('Step9: Changing Marital Status to categories of Relationship and single')

    with col2:
        st.header('Sample of the data')
        df20 = df.head(20)
        df20


#third page
if menu_id== 'Visuals':
    col11, col22= st.columns([1,1])

    with col11:
        display_app_header(main_txt='Plotly Visuals',
        sub_txt='')
        st.write('')

        st.plotly_chart(fig4)
        st.write('')
        st.write('')
        st.plotly_chart(fig5)
        st.write('')
        st.write('')
        st.plotly_chart(fig6)

    with col22:
        st.write('')
        st.plotly_chart(fig2)
        st.write('')
        st.write('')
        st.plotly_chart(fig3)
        st.write('')
        st.write('')
        st.plotly_chart(fig1)






