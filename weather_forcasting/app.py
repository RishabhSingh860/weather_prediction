# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 22:26:09 2020

@author: risha
"""

import streamlit as st
import datetime as datetime
import pickle
import pandas as pd
import numpy as np
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
from fbprophet import Prophet
import plotly.express as px
import cufflinks as cf
cf.go_offline()
from PIL import Image
from streamlit.script_runner import StopException,RerunException
import base64

df=pd.read_csv("weatherHistory.csv")

@st.cache(suppress_st_warning=True)
def model(df_model):
    model_fb=Prophet(interval_width=0.95)
    model_fit=model_fb.fit(df_model)
    return model_fit

@st.cache(suppress_st_warning=True)
def display(x,y,data_display):
     fig=go.Figure()
     layout = go.Layout(
            title ="Graphical_Representation",
            xaxis = dict(title = 'Date'),
            yaxis = dict(title = y+' with Time'))
     fig.update_layout(dict1 = layout, overwrite = True)
     fig.add_trace(go.Scatter(x=data_display[x], y=data_display[y], name=y))
     st.plotly_chart(fig, use_container_width=True)
     
@st.cache(suppress_st_warning=True)    
def dislay_bar(x,y,data_display):
    fig3=go.Figure()
    fig3 = px.bar(
                 data_display, 
                 x='Date',
                 y='Temperture',
                 color='Max_Temp')
    st.plotly_chart(fig3)
 
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
                            
           
    
     
     
     
   
    
def main():
    try: 

        html_temp="""
        <div style="background-color:tomato;padding:10px">
        <h1 style="color:black;test-align:center;">Weather Forcasting</h1>
        </div>
        <div style="padding:10px">
        <h3 style="color:black; test-align:center"> This App deal with future prediction of <b>weather</b>.
        User should, select one of plot, which he/she want to see to analysis future <b>weather</b> condition.
        <pre>Type of Plots</pre>
        <pre>1.Line chart <pre>Line chart Displays a series of numerical data as points which are connected by lines. It visualizes to show two data trends. The main productive feature is it can display thousands of data points without scrolling</pre>
        </pre>
        <pre>2.Barchart <pre>A bar chart presents categorical data with rectangular bars with heights or lengths proportional to the values that they represent. Bars can be displayed vertically or horizontally. It helps to show comparisons among discrete categories. </pre>
        </pre>
        <pre>3.Display DataFrame <pre> This option will display variation of wether with Time in DataFrame</pre>
        </pre>
        <pre>4.Analytical Display<pre>This opton will display different compenent wether with variation in Year,Month,Day's</pre></pre></h3>
        </div>
    
    
        """
        main_bg="backgroun2.jpg"
        main_bg_ext="jpg"
        side_bg = "images.jpg"
        side_bg_ext = "jpg"
        st.markdown(
            f"""
                <style>
                .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
        }}
        .sidebar .sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
            }}
        </style>
        """,
        unsafe_allow_html=True)
        st.markdown(html_temp,unsafe_allow_html=True)
        ds=st.sidebar.date_input('Enter future date you want prediction')
        day=st.sidebar.number_input("How many day's in future you want temperture",min_value=float(0),max_value=float(365))
        selection=st.sidebar.selectbox("What You Want to display", options=["Temperature (C)","Humidity","Wind Speed (km/h)","Visibility (km)"])
        df=pd.read_csv("weatherHistory.csv")
        df["Formatted Date"]=pd.to_datetime(df["Formatted Date"],utc=True)
        df=df.set_index("Formatted Date")
        df_new=df.resample("D").mean()
        df_new=df_new.reset_index()
        select_box=st.sidebar.checkbox("Plotly Line chart")
        select_box2=st.sidebar.checkbox("Plotly bar chart")
        select_box3=st.sidebar.checkbox("Display DataFrame")
        select_box4=st.sidebar.checkbox("Analytical display")
          
        if st.sidebar.button("Forcast"):
            if (selection=="Temperature (C)"):
                    df_new=df_new.rename(columns={"Formatted Date":"ds","Temperature (C)":"y"})
                ##lets remove time zone
                    df_new["ds"]=df_new['ds'].dt.tz_localize(None)
                    predict_fb=model(df_new)
                    ds=pd.date_range(ds,periods=day)
                    future=pd.DataFrame({"ds":ds})
                    predict=predict_fb.predict(future)
                    data_display=pd.DataFrame({"Date":predict["ds"],"Temperture":predict["yhat"],"Min_Temp":predict["yhat_lower"],"Max_Temp":predict["yhat_upper"]})
                    if (select_box==True):
                        display("Date","Temperture",data_display)
                    if(select_box2==True):
                        dislay_bar("Date","Temperture",data_display)
                    if(select_box3==True):
                          st.header("Tempaerature_Value")
                          st.write("Temperature value display for maximum and minimum range and Actual value")
                          st.write("\n")
                          st.write(data_display)
                    if(select_box4==True):
                        st.write("Component of Temperature")
                        fig2=predict_fb.plot_components(predict)
                        st.write(fig2)
                    if(select_box==False)and(select_box2==False)and(select_box3==False)and(select_box4==False):
                        st.sidebar.warning("Select Something to Display")
            
               
            elif (selection=="Humidity"):
                df_new=df_new.rename(columns={"Formatted Date":"ds","Humidity":"y"})
                ##lets remove time zone
                df_new["ds"]=df_new['ds'].dt.tz_localize(None)
                predict_fb=model(df_new)
                ds=pd.date_range(ds,periods=day)
                future=pd.DataFrame({"ds":ds})
                predict=predict_fb.predict(future)
                fig2=predict_fb.plot_components(predict)
                data_display=pd.DataFrame({"Date":predict["ds"],"Humidity":predict["yhat"],"Min_Humid":predict["yhat_lower"],"Max_Humid":predict["yhat_upper"]})
                if (select_box==True):
                    display("Date","Temperture",data_display)
                if(select_box2==True):
                    dislay_bar("Date","Temperture",data_display)
                if(select_box3==True):
                    st.header("Tempaerature_Value")
                    st.write("Temperature value display for maximum and minimum range and Actual value")
                    st.write("\n")
                    st.write(data_display)
                if(select_box4==True):
                    st.write("Component of Humidity")
                    fig2=predict_fb.plot_components(predict)
                    st.write(fig2)
                if(select_box==False)and(select_box2==False)and(select_box3==False)and(select_box4==False):
                    st.sidebar.warning("Select Something to Display")
            
            elif(selection=="Wind Speed (km/h)"):
                df_new=df_new.rename(columns={"Formatted Date":"ds","Wind Speed (km/h)":"y"})
                df_new["ds"]=df_new['ds'].dt.tz_localize(None)
                predict_fb=model(df_new)
                ds=pd.date_range(ds,periods=day)
                future=pd.DataFrame({"ds":ds})
                predict=predict_fb.predict(future)
                fig2=predict_fb.plot_components(predict)
                data_display=pd.DataFrame({"Date":predict["ds"],"Wind Speed (km/h)":predict["yhat"],"Min_Humid":predict["yhat_lower"],"Max_Humid":predict["yhat_upper"]})
                if (select_box==True):
                    display("Date","Temperture",data_display)
                if(select_box2==True):
                    dislay_bar("Date","Temperture",data_display)
                if(select_box3==True):
                    st.header("Tempaerature_Value")
                    st.write("Temperature value display for maximum and minimum range and Actual value")
                    st.write("\n")
                    st.write(data_display)
                if(select_box4==True):
                    st.write("Component of Wind speed")
                    fig2=predict_fb.plot_components(predict)
                    st.write(fig2)
                if(select_box==False)and(select_box2==False)and(select_box3==False)and(select_box4==False):
                    st.sidebar.warning("Select Something to Display")
            else:
                df_new=df_new.rename(columns={"Formatted Date":"ds","Visibility (km)":"y"})
        ##lets remove time zone
                df_new["ds"]=df_new['ds'].dt.tz_localize(None)
                predict_fb=model(df_new)
                ds=pd.date_range(ds,periods=day)
                future=pd.DataFrame({"ds":ds})
                predict=predict_fb.predict(future)
                fig2=predict_fb.plot_components(predict)
                data_display=pd.DataFrame({"Date":predict["ds"],"Visibility (km)":predict["yhat"],"Min_Humid":predict["yhat_lower"],"Max_Humid":predict["yhat_upper"]})
                if (select_box==True):
                    display("Date","Temperture",data_display)
                if(select_box2==True):
                    dislay_bar("Date","Temperture",data_display)
                if(select_box3==True):
                    st.header("Tempaerature_Value")
                    st.write("Temperature value display for maximum and minimum range and Actual value")
                    st.write("\n")
                    st.write(data_display)
                if(select_box4==True):
                
                   fig2=predict_fb.plot_components(predict)
                   st.write(fig2)
                if(select_box==False)and(select_box2==False)and(select_box3==False)and(select_box4==False):
                   st.sidebar.warning("Select Something to Display")
        
        
    except:
            st.sidebar.warning("Please check Something missing")
           # raise RerunException(st.ScriptRequestQueue.RerunData(None))
          
    
    
    
    
    
    

    
if __name__=="__main__":
    main()
    