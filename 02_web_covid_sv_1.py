"""
Created on Wed Jun 10 17:05:58 2020

@author: Marc
"""
#Project Covid Scan on Web 
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date, datetime, timedelta
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
from pdf2image import convert_from_path
from PIL import Image




#locpath1 = "C:/Users/Marc Wellner/01_projects/streamlit/01_covid_scan/01_data/"

locpath1 = "/home/ubuntu/01_covid_scan/01_data/"

td = date.today().strftime("%d/%m/%Y")


st.title('Covid19 Scan'+' - '+td)

st.subheader('Analysis of the historical development of new Covid19 infections for all worldwide countries')

@st.cache(allow_output_mutation=True)
def load_data():
    fulldat = pd.read_excel(locpath1+"covid_ana_tsa1.xlsx", keep_default_na=False,error_bad_lines=False)
    fulldat = fulldat.sort_values(['Rank_Pop', 'datum'], ascending=[True, True])
    return fulldat


fulldat = load_data()

#load_data()

selcntr = pd.read_excel(locpath1+"covid_ana_day1.xlsx", keep_default_na=False,error_bad_lines=False)
selcntr = selcntr.loc[:,['Country/Region']]
selcntr = selcntr.sort_values(['Country/Region'], ascending=[True])
#print(selcntr)
selcntr_str = selcntr['Country/Region'].astype(str).values.tolist()
#print(selcntr_str)

selectbox_1 = st.selectbox(
    'Choose a country?',
    (selcntr_str)
)


#@st.cache
def movavganalysis(cntrynam):

    cnsel = fulldat['Country/Region'] == cntrynam
    #cnsel = cnsel.sort_values(['datum'], ascending=[True])
    dat_ts = fulldat[cnsel]
    dat_ts = dat_ts.set_index('datum')

    #20 days to represent the 22 trading days in a month
    dat_ts['ma3d'] = dat_ts['confi_new'].rolling(3).mean()
    dat_ts['ma7d'] = dat_ts['confi_new'].rolling(7).mean()
    dat_ts['ma14d'] = dat_ts['confi_new'].rolling(14).mean()
    dat_ts['ma21d'] = dat_ts['confi_new'].rolling(21).mean()
    
    
    fig, ax = plt.subplots()
    l1, = ax.plot(dat_ts.index, dat_ts.confi_new, linewidth=0.3, label='new cases')
    l2, = ax.plot(dat_ts.index, dat_ts.ma3d, linewidth=0.3, label='3daysavg')
    l3, = ax.plot(dat_ts.index, dat_ts.ma7d, linewidth=1, label='7daysavg')
    l4, = ax.plot(dat_ts.index, dat_ts.ma14d, linewidth=1, label='14daysavg')
    l5, = ax.plot(dat_ts.index, dat_ts.ma21d, linewidth=1, label='21daysavg')
    plt.legend(handles=[l1, l2, l3, l4, l5])
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    #format the ticks
    plt.grid(True)
    plt.axis('tight')
    #plt.show()
    plt.title(cntrynam + ': New Covid-19 Cases up to: ' + datetime.today().strftime('%Y-%m-%d'))
    #plt.ylabel('Cases')
    #plt.close()


movavganalysis(selectbox_1)

st.pyplot()


st.subheader('In order to get a quick overview on the Covid19 status for all countries world wide we place each country according to its current Covid19 situation at a representativ position on the typical (i.e. bell shaped) covid curve of new infections')

st.subheader('Based on the current level and historical development of new infections countries are grouped into 6 possible clusters along the typical covid curve')

st.text("Cluster 0: Current cumulative Covid19 infections are < 1.000 cases""\n"
        "Cluster 1: Increasing new daily Covid19 infections""\n"
        "Cluster 2: Potentialy reaching the peak of new daily Covid19 infections""\n"
        "Cluster 3: Indication of decreasing new daily Covid19 infections""\n"
        "Cluster 4: Decreased number of new daily Covid19 infections (compared to historical peak)""\n" 
        "Cluster 5: Low number of new daily Covid19 infections (compared to historical peak)")

#st.subheader("Conceptual cluster description")

#image = Image.open(locpath1+"Description_Covid_Scan_page1.jpg")
#st.image(image, use_column_width=True)

#st.subheader("Conceptual description of placing each countrie into a cluster")

#image = Image.open(locpath1+"Description_Covid_Scan_page2.jpg")
#st.image(image, use_column_width=True)

st.subheader("Within each cluster countries are sorted by the size of population, i.e. countries with larger population appear before countries with a smaller population. For further details pls. see below")

st.subheader("Moreover the cluster dynamic is shown via color coding: (A) Countries which have shifted since last snapshot to a higher (i.e. better) cluster (e.g. C1 to C2) are in green. (B) Countries which have shifted since last snapshot to a lower (i.e. worse) cluster (e.g. C4 to C3) are in red. (C) Countries which have remained since last snapshot in the same cluster are in blue")

st.subheader('')

##################################################################################################
#### Covid Curve Scan 

#### All Online Countries  
df = pd.read_excel(locpath1+"covid_ana_day1.xlsx", keep_default_na=False,error_bad_lines=False)

#df = df[(df.index<=78) & (df.confi>=1000)] 
#df = df[(df.index<=78)] 
df.loc[(df['clusterdev'] == 1), 'clusterdevc'] = 'g'
df.loc[(df['clusterdev'] == 0), 'clusterdevc'] = 'b'
df.loc[(df['clusterdev'] == -1), 'clusterdevc'] = 'r'
df = df.loc[:,['Country/Region', 'Cntry_CD', 'cluster', 'clusterdev', 'clusterdevc', 'Rank_Pop']]
df['rnk_plot'] = df.groupby(['cluster']).cumcount()+1


def posi(clus,xst,xincr,yst,yincr,spaln):
    
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']<=1*spaln), 'x'] = xst + (df['rnk_plot']-1)*xincr
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>1*spaln) & (df['rnk_plot']<=2*spaln), 'x'] = xst + (df['rnk_plot']-1*spaln-1)*xincr
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>2*spaln) & (df['rnk_plot']<=3*spaln), 'x'] = xst + (df['rnk_plot']-2*spaln-1)*xincr
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>3*spaln) & (df['rnk_plot']<=4*spaln), 'x'] = xst + (df['rnk_plot']-3*spaln-1)*xincr
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>4*spaln) & (df['rnk_plot']<=5*spaln), 'x'] = xst + (df['rnk_plot']-4*spaln-1)*xincr
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>5*spaln) & (df['rnk_plot']<=6*spaln), 'x'] = xst + (df['rnk_plot']-5*spaln-1)*xincr
    
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']<=1*spaln), 'y'] = yst
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>1*spaln) & (df['rnk_plot']<=2*spaln), 'y'] = yst-1*yincr
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>2*spaln) & (df['rnk_plot']<=3*spaln), 'y'] = yst-2*yincr
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>3*spaln) & (df['rnk_plot']<=4*spaln), 'y'] = yst-3*yincr
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>4*spaln) & (df['rnk_plot']<=5*spaln), 'y'] = yst-4*yincr
    df.loc[(df['cluster'] == clus) & (df['rnk_plot']>5*spaln) & (df['rnk_plot']<=6*spaln), 'y'] = yst-5*yincr
    
posi('q0',  -6,0.5,0.15,0.03,8)
posi('q1',  -6,0.5,0.35,0.03,8)
posi('q2',-1.5,0.5,0.55,0.03,6)
posi('q3',   2,0.5,0.45,0.03,8)
posi('q4',   2,0.5, 0.3,0.03,8)
posi('q5',   3,0.5, 0.1,0.03,8)

df = df.loc[:,['Cntry_CD', 'x', 'y','cluster','clusterdev','clusterdevc','rnk_plot']]
#print(df)

#print(td)

     

def ploti(sele):
    # As many times as you like, create a figure fig and save it:
    fig, ax = plt.subplots()
    fig.suptitle('Covid19 Scan for: ' + sele, fontsize=12, fontweight='bold')
    
    a = np.linspace(-6, 0.8, 1000)
    ax.plot(a, 1 / np.sqrt(2*np.pi) * np.exp(-(a**2)/2), color = 'red', label='high level', linewidth=8)
    
    b = np.linspace(0.8, 1.8, 1000)
    ax.plot(b, 1 / np.sqrt(2*np.pi) * np.exp(-(b**2)/2), color = 'orange', label='mid level', linewidth=8)
    
    c = np. linspace(1.8, 6, 1000)
    ax.plot(c, 1 / np.sqrt(2*np.pi) * np.exp(-(c**2)/2), color = 'green', label='low level', linewidth=8)

    d = np. linspace(-6, 6, 1000)
    ax.plot(d, 1 / np.sqrt(2*np.pi) * np.exp(-(d**2)/2)+0.15, color = 'black', label='low level', linewidth=0)
    
    #ax.set_xticks([])
    #ax.set_yticks([])
    ax.axis('off')
    
    rows, cols = df.shape
    for i in range(rows):
            ax.annotate('{}'.format(df.iloc[i, 0]), xy=(df.iloc[i, 1], df.iloc[i, 2]),fontsize=7,fontname='Sans', color = df.iloc[i, 5]) 
        #ax.text(df.iloc[i, 1], df.iloc[i, 2], '{}'.format(df.iloc[i, 0]), fontsize=8) 

        # When no figure is specified the current figure is saved
    
ploti('All Countries')

st.pyplot()



#######################################################################
# Selectionen nach REgionen AF AP EU NA NO SA 

######### AP
df = pd.read_excel(locpath1+"covid_ana_day1.xlsx", keep_default_na=False,error_bad_lines=False)
#df = confirmed_cntpselday    

df = df[(df.Region_CD == 'AP')] 
df.loc[(df['clusterdev'] == 1), 'clusterdevc'] = 'g'
df.loc[(df['clusterdev'] == 0), 'clusterdevc'] = 'b'
df.loc[(df['clusterdev'] == -1), 'clusterdevc'] = 'r'
df = df.loc[:,['Country/Region', 'Cntry_CD', 'cluster', 'clusterdev', 'clusterdevc', 'Rank_Pop']]
df['rnk_plot'] = df.groupby(['cluster']).cumcount()+1


posi('q0',  -6,0.5,0.15,0.03,8)
posi('q1',  -6,0.5,0.35,0.03,8)
posi('q2',-1.5,0.5,0.55,0.03,6)
posi('q3',   2,0.5,0.45,0.03,8)
posi('q4',   2,0.5, 0.3,0.03,8)
posi('q5',   3,0.5, 0.1,0.03,8)

df = df.loc[:,['Cntry_CD', 'x', 'y','cluster','clusterdev','clusterdevc','rnk_plot']]

ploti('Asia Pacific')

st.pyplot()

######### AF/NO
df = pd.read_excel(locpath1+"covid_ana_day1.xlsx", keep_default_na=False,error_bad_lines=False)
#df = confirmed_cntpselday    

df = df[(df.Region_CD == 'AF') | (df.Region_CD == 'NO')] 
df.loc[(df['clusterdev'] == 1), 'clusterdevc'] = 'g'
df.loc[(df['clusterdev'] == 0), 'clusterdevc'] = 'b'
df.loc[(df['clusterdev'] == -1), 'clusterdevc'] = 'r'
df = df.loc[:,['Country/Region', 'Cntry_CD', 'cluster', 'clusterdev', 'clusterdevc', 'Rank_Pop']]
df['rnk_plot'] = df.groupby(['cluster']).cumcount()+1


posi('q0',  -6,0.5,0.15,0.03,8)
posi('q1',  -6,0.5,0.35,0.03,8)
posi('q2',-1.5,0.5,0.55,0.03,6)
posi('q3',   2,0.5,0.45,0.03,8)
posi('q4',   2,0.5, 0.3,0.03,8)
posi('q5',   3,0.5, 0.1,0.03,8)

df = df.loc[:,['Cntry_CD', 'x', 'y','cluster','clusterdev','clusterdevc','rnk_plot']]

ploti('Africa/Middle East')

st.pyplot()

######### NA/SA
df = pd.read_excel(locpath1+"covid_ana_day1.xlsx", keep_default_na=False,error_bad_lines=False)
#df = confirmed_cntpselday    

df = df[(df.Region_CD == 'NA') | (df.Region_CD == 'SA')] 
df.loc[(df['clusterdev'] == 1), 'clusterdevc'] = 'g'
df.loc[(df['clusterdev'] == 0), 'clusterdevc'] = 'b'
df.loc[(df['clusterdev'] == -1), 'clusterdevc'] = 'r'
df = df.loc[:,['Country/Region', 'Cntry_CD', 'cluster', 'clusterdev', 'clusterdevc', 'Rank_Pop']]
df['rnk_plot'] = df.groupby(['cluster']).cumcount()+1


posi('q0',  -6,0.5,0.15,0.03,8)
posi('q1',  -6,0.5,0.35,0.03,8)
posi('q2',-1.5,0.5,0.55,0.03,6)
posi('q3',   2,0.5,0.45,0.03,8)
posi('q4',   2,0.5, 0.3,0.03,8)
posi('q5',   3,0.5, 0.1,0.03,8)

df = df.loc[:,['Cntry_CD', 'x', 'y','cluster','clusterdev','clusterdevc','rnk_plot']]

ploti('Americas')

st.pyplot()


######### NA/SA
df = pd.read_excel(locpath1+"covid_ana_day1.xlsx", keep_default_na=False,error_bad_lines=False)
#df = confirmed_cntpselday    

df = df[(df.Region_CD == 'EU') ] 
df.loc[(df['clusterdev'] == 1), 'clusterdevc'] = 'g'
df.loc[(df['clusterdev'] == 0), 'clusterdevc'] = 'b'
df.loc[(df['clusterdev'] == -1), 'clusterdevc'] = 'r'
df = df.loc[:,['Country/Region', 'Cntry_CD', 'cluster', 'clusterdev', 'clusterdevc', 'Rank_Pop']]
df['rnk_plot'] = df.groupby(['cluster']).cumcount()+1


posi('q0',  -6,0.5,0.15,0.03,8)
posi('q1',  -6,0.5,0.35,0.03,8)
posi('q2',-1.5,0.5,0.55,0.03,6)
posi('q3',   2,0.5,0.45,0.03,8)
posi('q4',   2,0.5, 0.3,0.03,8)
posi('q5',   3,0.5, 0.1,0.03,8)

df = df.loc[:,['Cntry_CD', 'x', 'y','cluster','clusterdev','clusterdevc','rnk_plot']]

ploti('Europe')

st.pyplot()


df_agg_fin = pd.read_excel(locpath1+"covid_ana_day_agg.xlsx", keep_default_na=False,error_bad_lines=False)
#print(df_agg_fin)
df_agg_fin = df_agg_fin.loc[:,[ 'Region', 'Pct_Countries_C5', 'Pct_Countries_C5_dif',
                                          'Pct_Population_C5', 'Pct_Population_C5_dif',
                                          'New_Infections_7davg', 'New_Infections_7davg_dif',
                                          'Incedent_rate', 'Incedent_rate_dif',
                                          'Population']]            

df_agg_fin = df_agg_fin.rename(columns={"Pct_Countries_C5": "Cntry_C5", "Pct_Countries_C5_dif": "Cntry_C5_dif", 
                                        "Pct_Population_C5": "Pop_C5", "Pct_Population_C5_dif": "Pop_C5_dif", 
                                        "New_Infections_7davg": "New_Inf_7davg", "New_Infections_7davg_dif": "New_Inf_7davg_dif", 
                                        "Incedent_rate": "Inc_rate", "Incedent_rate_dif": "Inc_rate_dif"                                      
                                        })

 
 
 #print(df_agg_fin)
 
 #df_agg_fin['Pct_Cntry_C5'] = 100*df_agg_fin.Pct_Countries_C5.round(3)
 #df_agg_fin['Pct_Cntry_C5_dif'] = 100*df_agg_fin.Pct_Countries_C5_dif.round(3)
 
 #df_agg_fin['Pct_Pop_C5'] = 100*df_agg_fin.Pct_Population_C5.round(3)
 #df_agg_fin['Pct_Pop_C5_dif'] = 100*df_agg_fin.Pct_Population_C5_dif.round(3)
 
 #df_agg_fin['New_Inf_7davg'] = df_agg_fin.New_Infections_7davg.round(0)
 #df_agg_fin['New_Inf_7davg_dif'] = df_agg_fin.New_Infections_7davg_dif.round(0)
 
 #df_agg_fin['New_Inf_7davg'] = df_agg_fin['New_Inf_7davg'].astype(int)
 #df_agg_fin['New_Inf_7davg_dif'] = df_agg_fin['New_Inf_7davg_dif'].astype(int)
 
 #df_agg_fin['New_Inf_7davg'] = df_agg_fin.apply(lambda x: "{:,}".format(x['New_Inf_7davg']), axis=1)
 #df_agg_fin['New_Inf_7davg_dif'] = df_agg_fin.apply(lambda x: "{:,}".format(x['New_Inf_7davg_dif']), axis=1)
 
 #df_agg_fin['Inced_rate'] = df_agg_fin.Incedent_rate.round(1)
 #df_agg_fin['Inced_rate_dif'] = df_agg_fin.Incedent_rate_dif.round(1)
 
 #df_agg_fin['Population'] = df_agg_fin.apply(lambda x: "{:,}".format(x['Population']), axis=1)
 
 
 #df_agg_fin = df_agg_fin.loc[:,[ 'Region', 'Pct_Cntry_C5', 'Pct_Cntry_C5_dif',
 #                                          'Pct_Pop_C5', 'Pct_Pop_C5_dif',
 #                                          'New_Inf_7davg', 'New_Inf_7davg_dif',
 #                                          'Inced_rate', 'Inced_rate_dif',
 #                                          'Population']]            
 
 
st.subheader('And now some descriptive statistics in order to compare the regions.')
 
st.text("For the five regions above (1) Africa/Middle East (2) Americas (3) Asia Pacific""\n""(4) Europe and (5) World following figures have been defined""\n"
         "- Cntry_C5: Share of countries in Cluster 5 (in %)""\n"
         "- Cntry_C5_dif: Difference to Cntry_C5 7 days before (in %p)""\n"
         "- Pop_C5: Share of population in Cluster 5 (in %)""\n"
         "- Pop_C5_dif: Difference to Pop_C5 7 days before (in %p)""\n"
         "- New_Inf_7davg: 7 days average of new infections (in persons)""\n"
         "- New_Inf_7davg_dif: Difference to New_Inf_7davg 7 days before (in persons)""\n"
         "- Inc_rate: New_Infections_7davg/Population (in persons)""\n"
         "- Inc_rate_dif: Difference to Inc_rate 7 days before (in persons)""\n"
         "- Population (in persons)""\n")
 
 
st.dataframe(df_agg_fin.style.format({'Cntry_C5': "{:.1%}", 'Cntry_C5_dif': "{:.1%}p",
                                      'Pop_C5': "{:.1%}", 'Pop_C5_dif': "{:.1%}p",
                                      'New_Inf_7davg': "{:0<1.0f}", 'New_Inf_7davg_dif': "{:0<1.0f}",
                                      'Inc_rate': "{:0<.1f}", 'Inc_rate_dif': "{:0<.1f}",
                                      'Population': "{:0<1.0f}"
                                      }))
 
    

#st.markdown(
#"""        
#[DE](C:/Users/Marc Wellner/01_projects/streamlit/01_covid_scan/trend_DE.pdf)
#
#[Voila](https://github.com/voila-dashboards/voila)
#
#"""        
#        )

    
###### Graphische Darstellung der Clusterverteilung der 3 Regionen #################
#df_aggreg.to_excel(locpath1+"covid_ana_day_agg_cluster.xlsx", sheet_name='Tabelle1')

st.subheader('And now the distribution of the 5 cluster for the four regions.')    
    
df_aggreg = pd.read_excel(locpath1+"covid_ana_day_agg_cluster.xlsx", keep_default_na=False,error_bad_lines=False)
df_aggreg = df_aggreg.loc[:,['Region_GRP', 'pctpop', 'pctcntr']]            

#print(df_aggreg)
df_aggregAFNO = df_aggreg[df_aggreg['Region_GRP'].isin(['AFNO'])]
df_aggregAP = df_aggreg[df_aggreg['Region_GRP'].isin(['AP'])]
df_aggregEU = df_aggreg[df_aggreg['Region_GRP'].isin(['EU'])]
df_aggregNASA = df_aggreg[df_aggreg['Region_GRP'].isin(['NASA'])]


labels = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5']

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots()
##rects1 = ax.bar(x - width/2, men_means, width, label='Men')
rects1 = ax.bar(x - width/1, df_aggregAFNO['pctpop'], width, label='AFNO')
rects2 = ax.bar(x , df_aggregAP['pctpop'], width, label='AP')
rects3 = ax.bar(x + width/1, df_aggregEU['pctpop'], width, label='EU')
rects4 = ax.bar(x + 2*width/1, df_aggregNASA['pctpop'], width, label='NASA')

ax.set_ylabel('Percentage Population')
ax.set_title('Cluster Distribution of Population by Region')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()
st.pyplot(fig)
#plt.show()


fig, ax = plt.subplots()
##rects1 = ax.bar(x - width/2, men_means, width, label='Men')
rects1 = ax.bar(x - width/1, df_aggregAFNO['pctcntr'], width, label='AFNO')
rects2 = ax.bar(x , df_aggregAP['pctcntr'], width, label='AP')
rects3 = ax.bar(x + width/1, df_aggregEU['pctcntr'], width, label='EU')
rects4 = ax.bar(x + 2*width/1, df_aggregNASA['pctcntr'], width, label='NASA')

ax.set_ylabel('Percentage Countries')
ax.set_title('Cluster Distribution Countries by Region')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()
st.pyplot(fig)
#plt.show()
    

#
#st.subheader('')
#
#st.subheader('And now a graphical representation for the development of some selected countries.' 
#             'The graphs are grouped by the areas above, i.e. Asia Pacific, Africa/Middle East, Americas and Europe.'
#             'Within each area countries are sorted by population'
#             )
#
#
####### Asia Pacific #################
#df = pd.read_excel(locpath1+"covid_ana_day.xlsx", keep_default_na=False,error_bad_lines=False)
#
#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 40)
#
#dfs = df[(df.Region_CD == 'AP')] 
##print(dfs)
#dfs = dfs[dfs['Cntry_CD'].isin(['CN','IN','ID','PK','JP','PH','TH','KR'])]
##print(dfs)
#
#st.subheader("Asia Pacific")
#
#rows, cols = dfs.shape
#
#for i in range(rows):
#    image = Image.open(locpath1+"trend_"+dfs.iloc[i,4]+".jpg")
#    capi = dfs.iloc[i,4]+"("+dfs.iloc[i,3]+")"
#    st.image(image, caption=capi, use_column_width=True)
#
####### Africa / Middle East #################
##df = pd.read_excel(locpath1+"covid_ana_day.xlsx", keep_default_na=False,error_bad_lines=False)
#
#dfs = df[(df.Region_CD == 'AF') | (df.Region_CD == 'NO')] 
##print(dfs)
#dfs = dfs[dfs['Cntry_CD'].isin(['NG','ET','EG','IR','IQ'])]
##print(dfs)
#
#
#st.subheader("Africa / Middle East")
#
#rows, cols = dfs.shape
#
#for i in range(rows):
#    image = Image.open(locpath1+"trend_"+dfs.iloc[i,4]+".jpg")
#    capi = dfs.iloc[i,4]+"("+dfs.iloc[i,3]+")"
#    st.image(image, caption=capi, use_column_width=True)
#
####### Americas #################
##df = pd.read_excel(locpath1+"covid_ana_day.xlsx", keep_default_na=False,error_bad_lines=False)
#dfs = df[(df.Region_CD == 'NA') | (df.Region_CD == 'SA')] 
##print(dfs)
#dfs = dfs[dfs['Cntry_CD'].isin(['US','BR','MX','CO','AR','CA'])]
##print(dfs)
#
#
#st.subheader("Americas")
#
#rows, cols = dfs.shape
#
#for i in range(rows):
#    image = Image.open(locpath1+"trend_"+dfs.iloc[i,4]+".jpg")
#    capi = dfs.iloc[i,4]+"("+dfs.iloc[i,3]+")"
#    st.image(image, caption=capi, use_column_width=True)
#
####### Europe #################
##df = pd.read_excel(locpath1+"covid_ana_day.xlsx", keep_default_na=False,error_bad_lines=False)
#dfs = df[(df.Region_CD == 'EU')] 
##print(dfs)
#dfs = dfs[dfs['Cntry_CD'].isin(['RU','DE','TR','FR','GB','IT','ES','PL','NL','BE','GR','PZ','SE','AT','CH','DK','FI','NO'])]
#
#st.subheader("Europe")
#
#rows, cols = dfs.shape
#
#for i in range(rows):
#    image = Image.open(locpath1+"trend_"+dfs.iloc[i,4]+".jpg")
#    capi = dfs.iloc[i,4]+"("+dfs.iloc[i,3]+")"
#    st.image(image, caption=capi, use_column_width=True)
#





#def autolabel(rects):
#    """Attach a text label above each bar in *rects*, displaying its height."""
#    for rect in rects:
#        height = rect.get_height()
#        ax.annotate('{}'.format(height),
#                    xy=(rect.get_x() + rect.get_width() / 2, height),
#                    xytext=(0, 3),  # 3 points vertical offset
#                    textcoords="offset points",
#                    ha='center', va='bottom')


#autolabel(rects1)
#autolabel(rects2)




# =============================================================================
# st.markdown(
# """
# # Country Indicators
# 
# ## Introduction
# 
# This example is a Streamlit implementation of an interactive Country Indicator plot.
# 
# The purpose of this example is to test what we can do and cannot (yet) do in Streamlit compared
# to the combination of [Jupyter Notebook](https://jupyter.org/) and [Voila](https://github.com/voila-dashboards/voila).
# 
# 
# As of today (2019-10-20) both Voila and Streamlit are released for Beta Testing only.
# """
#     )
# 
# =============================================================================



st.subheader('Finally some detailed information on the definitions of the 6 clusters as well as on the data source.')
 
 
st.text("Cluster 0: Current cumulative Covid19 infections are < 1.000 cases""\n""\n"
         
        "Cluster 1: Increasing new daily Covid19 infections""\n"
         "          -> Avg 7 days level > 70% of max avg 7 days level so far""\n"
         "          -> Avg 7 days level > Avg 14 days level""\n"
         "          -> Avg 7 days level increases""\n""\n"
         
        "Cluster 2: Potentialy reaching the peak of new daily Covid19 infections""\n"
        "           -> Avg 7 days level > 70% of max avg 7 days level so far""\n"
        "           -> Avg 7 days level > Avg 14 days level""\n"
        "           -> Avg 7 days level decreases""\n""\n"
                
        "Cluster 3: Indication of decreasing new daily Covid19 infections""\n"
        "           -> Avg 7 days level > 70% of max avg 7 days level so far""\n"
        "           -> Avg 7 days level < Avg 14 days level""\n""\n"
        
        "Cluster 4: Decreased number of new daily Covid19 infections (compared to historical peak)""\n" 
        "           -> Avg 7 days level between 30% and 70% of max avg 7 days level so far""\n""\n" 
                
        "Cluster 5: Low number of new daily Covid19 infections (compared to historical peak)""\n" 
        "           -> Avg 7 days level < 30% max avg 7 days level so far")



st.text("Data source: D2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by""\n""Johns Hopkins CSSE")

 

