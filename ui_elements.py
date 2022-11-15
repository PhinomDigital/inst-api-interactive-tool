import dash_trich_components as dtc
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash
from dash import Input, Output, dcc, html,ctx
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dash_table
import phdapi_class as phdapi

class UiProcess:
    def __init__(self,key,secret,load_instuments=True):
        self.phd_api = phdapi.PhDAPI(api_key=key,
                                     secret = secret,
                                     url = 'https://ins.phinom-digital.dev')
        self.instruments = pd.DataFrame()
        self.instruments['id'] = []
        self.instruments['symbolId'] = []
        if load_instuments == True:
            try:
                tmp1 = self.phd_api.instruments(symbol='BTC',option_type='CALL')
                tmp2 = self.phd_api.instruments(symbol='BTC',option_type='PUT')
                tmp3 = self.phd_api.instruments(symbol='ETH',option_type='CALL')
                tmp4 = self.phd_api.instruments(symbol='ETH',option_type='PUT')
                self.instruments = pd.concat([tmp1, tmp2,tmp3,tmp4], ignore_index=True)[['id','symbolId']]
            except:
                pass

#HEADERS
header = html.Div(html.H2('InstitutionalApi'),style={'text-align':'center',})
img_obj = html.Div(html.Img(src = '/assets/logo.png',height=60),style={'text-align':'center',})
img_row = dbc.Row([dbc.Col([img_obj],style = {'padding-top':'20px'},
                           width={"size": 12, "offset": 0}),],id = 'logo',
                  style={ 'width':'100%',"overflowX": "hide","overflowY": "hide"},)

#AUTORIZATION
input_key = dbc.InputGroup(
    [
        dbc.InputGroupText("APIkey"),
        dbc.Input(placeholder="Input apikey..",
                  type = 'text',
                  id='key_input'),
    ],

),
input_secret = dbc.InputGroup([ dbc.InputGroupText("Secret"),
                                dbc.Input(placeholder="Input secret..",
                                          type = 'text',
                                          id='secret_input'),],)
auth_input = html.Div(children=[html.Div(input_key,style={'margin-top':'25px'}),
                                html.Div(input_secret,style={'margin-top':'25px'})],)
auth_card = dbc.Card(dbc.CardBody([ html.H5("Autorization", className="card-title"),
                                    auth_input,
                                    dbc.Button("save",
                                               id = 'save',
                                               style={'background-color':'#3d7d72','margin-top':'25px',
                                                      'border-color':'#91d8df',
                                                      'align':'right'})]))
auth_row = dbc.Row(dbc.Col(auth_card,
                           width={'size':6,'offset':3},),
                   style={'text-align':'center','margin-top':'150px'})
layout_setting = html.Div([img_row,auth_row,])

#INSTRUMENTS
collapse_output = html.Div([ dbc.Button("Output",
                                        id="collapse-button",
                                        size = 'sm',
                                        color="primary",
                                        n_clicks=0,),
                             dbc.Collapse(dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
                                          id="collapse",
                                          is_open=False,)],
                           style = {'padding-top':'20px'})

label_symbol = html.Label('Symbol:',style={'background-color':'rgb(237, 242, 242)'})
dropdown_symbol = dcc.Dropdown(options=['BTC', 'ETH'],
                               id = 'instruments_symbol')
param_symbol = html.Div([label_symbol,dropdown_symbol])
label_type = html.Label('Option Type:',style={'background-color':'rgb(237, 242, 242)'})
dropdown_type = dcc.Dropdown(options=['CALL', 'PUT'],
                             id = 'instruments_optype')
param_symbol = html.Div([label_symbol,dropdown_symbol],style={'display':'inline'})
param_optype = html.Div([label_type,dropdown_type],style={'display':'inline'})
instruments_params_row = dbc.Row([ dbc.Col(param_symbol,width=4),
                                   dbc.Col(param_optype,width=4)]),

inst_button = html.Div([html.Label('Method:',style={'background-color':'rgb(237, 242, 242)'}),
                        dbc.Button('Instruments',size='sm',
                                   id = 'instuments_button',
                                   style={'vertical-align':'center','display':'block',
                                          'background-color':'#3d7d72','border-color':'#91d8df',})])
function_row = dbc.Row([ dbc.Col([inst_button],width=2),
                         dbc.Col(instruments_params_row,width=10)],
                       style = {'padding-top':'10px'})

func_output = dbc.Row([ dbc.Col(children=[],width={'size':12,'offset':0},id='instuments_output')],
                      style = {'padding-top':'10px'})
row_label = dbc.Row(dbc.Col(html.Label('Output:',style={'background-color':'rgb(237, 242, 242)'}),width=1),
                    style = {'padding-top':'10px'})
collapse_func = html.Div([ html.Button("Get list of Instruments",
                                       id="collapse-button-instruments",
                                       n_clicks=0,
                                       style = {'align':'center','width':'100%'}),
                           dbc.Collapse([ function_row,row_label,func_output],
                                        id="collapse-instruments",
                                        is_open=False,)],
                         style = {'padding-top':'10px'})

#PUT_ORDER
label_productid_putordr = html.Div(html.Label('Instrument:',style={'background-color':'rgb(237, 242, 242)'}))
input_prdid_putordr = dcc.Dropdown(options=[],
                                   id = 'productid_input_putordr')
param_prdid_putordr = html.Div([label_productid_putordr,input_prdid_putordr])

label_quant_putordr = html.Div(html.Label('Quantity:',style={'background-color':'rgb(237, 242, 242)'}))
input_quant_putordr = html.Div(dbc.Input(placeholder="Input quantity..",id='quant_input_putordr',type='number'),)
param_quant_putordr = html.Div([label_quant_putordr,input_quant_putordr])

label_price_putordr = html.Div(html.Label('Price:',style={'background-color':'rgb(237, 242, 242)'}))
input_price_putordr = html.Div(dbc.Input(placeholder="Input price..",id='price_input_putordr',type='number'),)
param_price_putordr = html.Div([label_price_putordr,input_price_putordr])

label_side_putordr = html.Div(html.Label('Side:',style={'background-color':'rgb(237, 242, 242)'}))
side_drpdwn_putordr = dcc.Dropdown(options=['BUY', 'SELL'],id = 'putordr_side')
param_side_putordr = html.Div([label_side_putordr,side_drpdwn_putordr],style={'display':'inline'})
putordr_params_row = dbc.Row([ dbc.Col(param_prdid_putordr,width=3),
                               dbc.Col(param_quant_putordr,width=3),
                               dbc.Col(param_price_putordr,width=3),
                               dbc.Col(param_side_putordr,width=3)])

putordr_button = html.Div([ html.Label('Method:',style={'display':'block','background-color':'rgb(237, 242, 242)'}),
                            dbc.Button('Post',
                                       size='sm',
                                       id = 'putordr_button',
                                       style={'vertical-align':'center','display':'block',
                                              'background-color':'#3d7d72','border-color':'#91d8df',})])
function_row_putordr = dbc.Row([ dbc.Col([putordr_button],width=1),
                                 dbc.Col(putordr_params_row,width=11)],
                               style = {'padding-top':'10px'})
func_output_putordr = dbc.Row([ dbc.Col([],width=12,id='output_putordr')],style = {'padding-top':'10px'})
collapse_func_putordr = html.Div([ html.Button("Post order",
                                               id="collapse-button-putordr",
                                               n_clicks=0,
                                               style = {'align':'center','width':'100%'},),
                                   dbc.Collapse([ function_row_putordr,
                                                  row_label,
                                                  func_output_putordr],
                                                id="collapse-putordr",
                                                is_open=False,)],
                                 style = {'padding-top':'20px'})

#DELETE ORDER
label_orderid_delordr = html.Div(html.Label('Order Id:',style={'background-color':'rgb(237, 242, 242)'}))
input_orderid_delordr = html.Div(dbc.Input(placeholder="Input order id..",id='orderid_input_delordr',type='text'),)
param_orderid_delordr = html.Div([label_orderid_delordr,input_orderid_delordr])

delordr_params_row = dbc.Row([ dbc.Col(param_orderid_delordr,width=5)]),

delordr_button = html.Div([html.Label('Method:',style={'display':'block','background-color':'rgb(237, 242, 242)'}),
                           dbc.Button('Delete',size='sm',
                                      id = 'delordr_button',
                                      style={'background-color':'#3d7d72',
                                             'border-color':'#91d8df',
                                             'display':'block'})])
function_row_delordr = dbc.Row([ dbc.Col([delordr_button],width=1),
                                 dbc.Col(delordr_params_row,width=11)],
                               style = {'padding-top':'10px'})
func_output_delordr = dbc.Row([ dbc.Col(children=[],width=12,id='output_delordr')],
                              style = {'padding-top':'10px'})
collapse_func_delordr = html.Div([ html.Button("Delete order",
                                               id="collapse-button-delordr",
                                               n_clicks=0,
                                               style = {'align':'center','width':'100%'}),
                                   dbc.Collapse([ function_row_delordr,
                                                  row_label,
                                                  func_output_delordr],
                                                id="collapse-delordr",
                                                is_open=False,)],
                                 style = {'padding-top':'20px'},)
#PRICE
label_productid_price = html.Div(html.Label('Instrument:',style={'background-color':'rgb(237, 242, 242)'}))
input_prdid_price = dcc.Dropdown(options=[],
                                 id = 'productid_input_price')
param_prdid_price = html.Div([label_productid_price,input_prdid_price])

price_params_row = dbc.Row([ dbc.Col(param_prdid_price,width=5)])
price_button = html.Div([ html.Label('Method:',style={'display':'block','background-color':'rgb(237, 242, 242)'}),
                          dbc.Button('Price',
                                     size='sm',
                                     id = 'price_button',
                                     style={'background-color':'#3d7d72',
                                            'border-color':'#91d8df',
                                            'display':'block'})])
function_row_price = dbc.Row([ dbc.Col([price_button],width=1),
                               dbc.Col(price_params_row,width=11)],
                             style = {'padding-top':'10px'})

func_output_price = dbc.Row([ dbc.Col(children=[],width=12,id='output_price')],
                            style = {'padding-top':'10px'})
collapse_func_price = html.Div([ html.Button("Price",
                                             id="collapse-button-price",
                                             n_clicks=0,
                                             style = {'align':'center','width':'100%'}),
                                 dbc.Collapse([ function_row_price,
                                                row_label,
                                                func_output_price],
                                              id="collapse-price",
                                              is_open=False)],
                               style = {'padding-top':'20px'})
#POSITIONS
label_productid_position = html.Div(html.Label('Instrument:',style={'background-color':'rgb(237, 242, 242)'}))
input_prdid_position = dcc.Dropdown(options=[],
                                    id = 'productid_input_position')
param_prdid_position = html.Div([label_productid_position,input_prdid_position])
position_params_row = dbc.Row([ dbc.Col(param_prdid_position,width=5)])
position_button = html.Div([html.Label('Method:',style={'display':'block','background-color':'rgb(237, 242, 242)'}),
                            dbc.Button('Positions',
                                       size='sm',
                                       id = 'position_button',
                                       style={'background-color':'#3d7d72','display':'block','border-color':'#91d8df',})])
function_row_position = dbc.Row([ dbc.Col([position_button],width=1),
                                  dbc.Col(position_params_row,width=11)],
                                style = {'padding-top':'10px'})

func_output_position = dbc.Row([ dbc.Col([],width=12,id='output_position')],
                               style = {'padding-top':'10px'})
collapse_func_position = html.Div([ html.Button("Positions",
                                                id="collapse-button-position",
                                                n_clicks=0,
                                                style = {'align':'center','width':'100%'}),
                                    dbc.Collapse([ function_row_position,
                                                   row_label,
                                                   func_output_position],
                                                 id="collapse-position",
                                                 is_open=False)],
                                  style = {'padding-top':'20px'})

#ORDERS
label_productid_orders = html.Div(html.Label('Instrument:',style={'background-color':'rgb(237, 242, 242)'}))
input_prdid_orders = dcc.Dropdown(options=[],
                                  id = 'productid_input_orders')
param_prdid_orders = html.Div([label_productid_orders,input_prdid_orders])

label_start_orders = html.Div(html.Label('Start time:',style={'background-color':'rgb(237, 242, 242)'}))
input_start_orders = html.Div(dbc.Input(placeholder="YYYY-MM-DD",id='start_input_orders'),)
param_start_orders = html.Div([label_start_orders,input_start_orders])

label_end_orders = html.Div(html.Label('End time:',style={'background-color':'rgb(237, 242, 242)'}))
input_end_orders = html.Div(dbc.Input(placeholder="YYYY-MM-DD",id='end_input_orders'),)
param_end_orders = html.Div([label_end_orders,input_end_orders])

label_limit_orders = html.Div(html.Label('Limit:',style={'background-color':'rgb(237, 242, 242)'}))
input_limit_orders = html.Div(dbc.Input(placeholder="Input limit..",id='limit_input_orders'),)
param_limit_orders = html.Div([label_limit_orders,input_limit_orders])

label_active_orders = html.Div(html.Label('Active:',style={'background-color':'rgb(237, 242, 242)'}))
ative_drpdwn_orders = dcc.Dropdown(options=['True', 'False'],
                                   id = 'orders_active')
param_active_orders = html.Div([label_active_orders,ative_drpdwn_orders],style={'display':'inline'})
orders_params_row = dbc.Row([ dbc.Col(param_prdid_orders,width=4),
                              dbc.Col(param_start_orders,width=2),
                              dbc.Col(param_end_orders,width=2),
                              dbc.Col(param_limit_orders,width=2),
                              dbc.Col(param_active_orders,width=2)]),

orders_button = html.Div([html.Label('Method:',style={'display':'block','background-color':'rgb(237, 242, 242)'}),
                          dbc.Button('Orders',size='sm',
                                     id = 'orders_button',
                                     style={'vertical-align':'center','display':'block',
                                            'border-color':'#91d8df',
                                            'background-color':'#3d7d72'})])
function_row_orders = dbc.Row([ dbc.Col([orders_button],width=1),
                                dbc.Col(orders_params_row,width=11)],
                              style = {'padding-top':'10px'})
func_output_orders = dbc.Row([ dbc.Col([],width=12,id='output_orders')],
                             style = {'padding-top':'20px'})
collapse_func_orders = html.Div([ html.Button("Get orders list",
                                              id="collapse-button-orders",
                                              n_clicks=0,
                                              style = {'align':'center','width':'100%'}),
                                  dbc.Collapse([ function_row_orders,
                                                 row_label,
                                                 func_output_orders],
                                               id="collapse-orders",
                                               is_open=False)],
                                style = {'padding-top':'20px'})

