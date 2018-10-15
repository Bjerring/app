# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 11:53:36 2018

@author: Thomas
"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from plotly import graph_objs as go
from datetime import datetime as dt
import json
import pandas as pd
import ftplib

import math as m
import numpy as np


df_fund_data = pd.read_csv('https://plot.ly/~jackp/17534.csv')
df_cal_year = pd.read_csv('https://plot.ly/~jackp/17528.csv')
perf_pc = pd.read_csv('https://plot.ly/~jackp/17532.csv')
df_perf_summary = pd.read_csv('https://plot.ly/~jackp/17530.csv')
df_perf_pc = pd.read_csv('https://plot.ly/~jackp/17532.csv')

def make_dash_table( df ):
    ''' Return a dash definition of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append( html.Td([ row[i] ]) )
        table.append( html.Tr( html_row ) )
    return table

modifed_perf_table = make_dash_table( df_perf_summary )

modifed_perf_table.insert( 
    0, html.Tr( [ 
            html.Td([]), 
            html.Td(['Cumulative'], colSpan=4, style=dict(textAlign="center")), 
            html.Td(['Annualised'], colSpan=4, style=dict(textAlign="center")) 
        ], style = dict( background='white', fontWeight=600 )
    ) 
)
    
df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544.csv')
df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542.csv')
df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540.csv')
df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538.csv')


#################################################
# FTP server infor
server_add = 'trier.io'
username = 'data@trier.io'
password = 'Bjerring86'
session = ftplib.FTP(server_add,username,password)

# files to download
filename = ['NAV_CA.csv']

for i in filename:
    localfile = open(i, 'wb')
    session.retrbinary('RETR ' + i, localfile.write, 1024)
    localfile.close()

# close FTP connection
session.quit()

# read in files
NAV = pd.read_csv(filename[0],index_col=0)
NAV = NAV['NAV'].astype(float)
nav_ret = NAV.pct_change()

#################################################
# current time
cur_year = dt.now().year
cur_month = dt.now().month
cur_day = dt.now().day


app = dash.Dash('Trier Informatics')

# Describe the layout, or the UI, of the app
app.layout = html.Div([        
        
    html.Div([ # page 1

        html.A([ 'Print PDF' ], 
           className="button no-print", 
           style=dict(position="absolute", top=-40, right=0)),     
                        
        html.Div([ # subpage 1

            # Row 1 (Header)

            html.Div([

                html.Div([      
                    html.H5('Multi Asset Class Absolute Return Portfolio'),
                    html.H6('A strategy by Trier Informatics', style=dict(color='#7F90AC')),
                    ], className = "nine columns padded" ),

                html.Div([            
                    html.H4([html.Span(cur_day, style=dict(opacity=0.3)),html.Span(cur_month, style=dict(opacity=0.6)), html.Span(cur_year)]),
                    #html.H6('continuously Updated')
                ], className = "three columns gs-header gs-accent-header padded", style=dict(float='right') ),

            ], className = "row gs-header gs-text-header"),

            html.Br([]),

            # Row 2

            html.Div([     

                html.Div([
                    html.H6('Description', className = "gs-header gs-text-header padded"),

                    html.Strong('Objective'),
                    html.P('Generate absolute returns by taking long and short positions in \
                           index products tracking large equity, bond and commodity index, e.g.\
                           the S&P 500, the UK Govt Bonds 10 Year Note and/or gold.', className = 'blue-text'),

                    html.Strong('Key characteristics:'),
                    html.P('The strategy is designed to maximize return, while maintaining a \
                            daily VaR of 1%. The strategy may use leverage of up to 300%.\
                            A single position cannot carry a weight larger than 15%, and the \
                            the portfolio can only have a maximum of 50% concentrated in one \
                            asset class, i.e. Equity, Bonds and Commodities.', className = 'blue-text' ),
                    
                    html.Strong('Factor investing:'),
                    html.P('The strategy is focused on the momentum factor, and takes long  \
                            positions in assets with a positive momentum relative to other \
                            assets and vice versa. \
                            The strategy is running on an intraday scale to exploit short-term \
                            directional trends in the markets.', className = 'blue-text' ),

                ], className = "four columns" ),

                html.Div([
                    html.H6(["Performance (Indexed)"],
                            className = "gs-header gs-table-header padded"),
                    #html.Iframe(src="https://plot.ly/~jackp/17553.embed?modebar=false&link=false&autosize=true", style=dict(border=0), width="100%", height="250"),
                    dcc.Graph(
                            id='example-graph',
                            figure={
                                    'data': [
                                            #{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                            {'x': NAV.index, 'y': NAV.values, 'type': 'line', 'name': 'Strategy'},
                                            ],'layout': {'height': '250','margin' : dict(l = 30, r = 0, t = 0, b = 30)},
                                            #config={'displayModeBar': False}
                                    },
                                    config={'displayModeBar': False}
                            ),
                    html.P("This is an actively managed fund that is not designed to track its reference benchmark. \
                        Therefore the performance of the fund and the performance of its reference benchmark \
                        may diverge. In addition stated reference benchmark returns do not reflect any management \
                        or other charges to the fund, whereas stated returns of the fund do."),
                ], className = "eight columns" ),

            ], className = "row "),
                        
            # Row 2.5

            html.Div([     

                html.Div([
                    html.H6('Performance (%)', className = "gs-header gs-text-header padded"),
                    html.Table( make_dash_table( df_perf_pc ), className = 'tiny-header' )
                ], className = "four columns" ),

                html.Div([

                    html.Strong("Past performance does not guarantee future results, which may vary. \
                        The value of investments and the income derived from investments will fluctuate and \
                        can go down as well as up. A loss of capital may occur.")
                ], className = "eight columns" ),

            ], className = "row "),                        

            # Row 3

            html.Div([             

                html.Div([
                    html.H6('Fund Data', className = "gs-header gs-text-header padded"),
                    html.Table( make_dash_table( df_fund_data ) )
                ], className = "four columns" ),

                html.Div([
                    html.H6("Performance Summary (%)", className = "gs-header gs-table-header padded"),
                    html.Table( modifed_perf_table, className = "reversed" ),

                    html.H6("Calendar Year Performance (%)", className = "gs-header gs-table-header padded"),
                    html.Table( make_dash_table( df_cal_year ) )
                ], className = "eight columns" ),                      

            ], className = "row "),                

        ], className = "subpage" ),

    ], className = "page" ),  
             
    html.Div([ # page 2
                
        html.A([ 'Print PDF' ], 
           className="button no-print", 
           style=dict(position="absolute", top=-40, right=0)),                
                
        html.Div([ # subpage 2
                        
            # Row 1 (Header)
                        
            html.Div([

                html.Div([      
                    html.H5('Goldman Sachs Strategic  Absolute Return Bond II Portfolio'),
                    html.H6('A sub-fund of Goldman Sachs Funds, SICAV', style=dict(color='#7F90AC')),
                    ], className = "nine columns padded" ),

                html.Div([            
                    html.H1([html.Span('03', style=dict(opacity=0.5)), html.Span('17')]),
                    html.H6('Monthly Fund Update')
                ], className = "three columns gs-header gs-accent-header padded", style=dict(float='right') ),

            ], className = "row gs-header gs-text-header"),
                        
            # Row 2
                        
            html.Div([

                # Data tables on this page:
                # ---
                # df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544/.csv')
                # df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542/.csv')
                # df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540/.csv')
                # df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')                                
                  
                # Column 1
                                
                html.Div([      
                    html.H6('Financial Information', className = "gs-header gs-text-header padded"),
                    html.Table( make_dash_table( df_fund_info ) ),
                                        
                    html.H6('Fund Characteristics', className = "gs-header gs-text-header padded"),
                    html.Table( make_dash_table( df_fund_characteristics ) ),
                                        
                    html.H6('Fund Facts', className = "gs-header gs-text-header padded"),
                    html.Table( make_dash_table( df_fund_facts ) ),
                                        
                ], className = "four columns" ),
                                
                # Column 2

                html.Div([                                          
                    html.H6('Sector Allocation (%)', className = "gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17560.embed?modebar=false&link=false&autosize=true", style=dict(border=0), width="100%", height="300"),
                                        
                    html.H6('Country Bond Allocation (%)', className = "gs-header gs-table-header padded"),
                    html.Table( make_dash_table( df_bond_allocation ) ),
                                        
                ], className = "four columns" ),
                                
                # Column 3
                                
                html.Div([            
                    html.H6('Top 10 Currency Weights (%)', className = "gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17555.embed?modebar=false&link=false&autosize=true", style=dict(border=0), width="100%", height="300"),
                                        
                    html.H6('Credit Allocation (%)', className = "gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17557.embed?modebar=false&link=false&autosize=true", style=dict(border=0), width="100%", height="300"),                                       
                                                                                
                ], className = "four columns" ),                                

            ], className = "row"),                        
                        
        ], className = "subpage" ),
                
    ], className = "page" ),
             
])


external_css = [ "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
        "//fonts.googleapis.com/css?family=Raleway:400,300,600",
        "https://codepen.io/plotly/pen/KmyPZr.css",
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css: 
    app.css.append_css({ "external_url": css })
    
external_js = [ "https://code.jquery.com/jquery-3.2.1.min.js",
        "https://codepen.io/plotly/pen/KmyPZr.js" ]
    
for js in external_js: 
    app.scripts.append_script({ "external_url": js })
    

if __name__ == '__main__':
    app.run_server(debug=True)
    
    # Open browser and go to 
    # http://127.0.0.1:8050/
    # or
    # http://127.0.0.1:5000/
    