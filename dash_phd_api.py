import dash_trich_components as dtc
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash
from dash import Input, Output, dcc, html,ctx
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dash_table
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import phdapi_class as phdapi
import ui_elements as ui
from waitress import serve

ui_process = ui.UiProcess('','')

#LAYOUT_SETTINGS
layout_setting = html.Div([ui.img_row,ui.auth_row,])

#LAYOUT_API
layout_api = html.Div([ ui.img_row,
                        html.Div(dbc.Row([dbc.Col(ui.header,width=12,style = {'margin-top':'0px'})])),
                        html.Div(ui.collapse_func,style = {'padding-top':'35px'}),
                        html.Div(ui.collapse_func_orders,style = {'padding-top':'5px'}),
                        html.Div(ui.collapse_func_price,style = {'padding-top':'5px'}),
                        html.Div(ui.collapse_func_position,style = {'padding-top':'5px'}),
                        html.Div(ui.collapse_func_putordr,style = {'padding-top':'5px'}),
                        html.Div(ui.collapse_func_delordr,style = {'padding-top':'5px'})])

content_api = html.Div(layout_api,style={'margin-left':'40px','margin-bottom':'50px'})
content_auth = html.Div([layout_setting])
layout = html.Div([ dtc.SideBar([ dtc.SideBarItem(id='id_3', label="API", icon="far fa-list-alt"),
                                  dtc.SideBarItem(id='id_5', label="Settings", icon="fa-solid fa-lock")]),
                    dcc.Store(id='secret_value', storage_type='session'),
                    dcc.Store(id='key_value', storage_type='session'),
                    html.Div([ ],
                             style={'width':'90%',
                                    "overflowX": "hide",
                                    "overflowY": "hide"},
                             id="page_content")])
#APP SERVER
app = dash.Dash(external_stylesheets=[dbc.icons.FONT_AWESOME])
server = app.server
app.layout = layout

#CALLBACKS
@app.callback(
    Output("page_content", "children"),
    Input("id_3", "n_clicks_timestamp"),
    Input("id_5", "n_clicks_timestamp"),
    State('key_value','data'),
    State('secret_value','data'),
)
def toggle_collapse(input3,input5,key,secret):
    btn_df = pd.DataFrame({"input3": [input3],
                           "input5": [input5]})
    btn_df = btn_df.fillna(0)
    if btn_df.idxmax(axis=1).values == "input3":
        return content_api,
    if btn_df.idxmax(axis=1).values == "input5":
        ui_process = ui.UiProcess(key,secret,False)
        input_key = dbc.InputGroup([ dbc.InputGroupText("APIkey"),
                                     dbc.Input(placeholder="Input apikey..",
                                               type = 'text',
                                               value = ui_process.phd_api.api_key,
                                               id='key_input')])
        input_secret = dbc.InputGroup([ dbc.InputGroupText("Secret"),
                                        dbc.Input(placeholder="Input secret..",
                                                  type = 'text',
                                                  value = ui_process.phd_api.secret,
                                                  id='secret_input')])
        auth_input = html.Div(children=[html.Div(input_key,style={'margin-top':'25px'}),
                                        html.Div(input_secret,style={'margin-top':'25px'})],)
        auth_card = dbc.Card(dbc.CardBody([ html.H5("Autorization", className="card-title"),
                                            auth_input,
                                            dbc.Button("save",
                                                       id = 'save',
                                                       style={'background-color':'#3d7d72',
                                                              'border-color':'#91d8df',
                                                              'margin-top':'25px','align':'right'})]))
        auth_row = dbc.Row(dbc.Col(auth_card,
                                   width={'size':6,'offset':3},),
                           style={'text-align':'center','margin-top':'150px'})
        layout_setting = html.Div([ ui.img_row, auth_row,])
        content_auth = html.Div([layout_setting])
        return content_auth,

#AUTORIZATION
@app.callback(
    Output("save", "n_clicks"),
    Output("key_input", "value"),
    Output("secret_input", "value"),
    Output('key_value','data'),
    Output('secret_value','data'),
    Input("key_input", "value"),
    Input("secret_input", "value"),
    Input("save", "n_clicks"),
    State('key_value','data'),
    State('secret_value','data'),
)
def autorize(key,secret,n,key_value,secret_value):
    triggered_id = ctx.triggered_id
    if triggered_id == 'save':
        ui_process = ui.UiProcess(key_value,secret_value,False)
        if n >= 1:
            if (key is not None) or (secret is not None):
                new_key = ui_process.phd_api.api_key
                new_secret = ui_process.phd_api.secret
                if key is not None:
                    new_key = key
                    key_value = new_key
                if secret is not None:
                    new_secret = secret
                    secret_value = new_secret
                ui_process = ui.UiProcess(new_key,new_secret,False)
                n = 0
                return n,key,secret,key_value,secret_value
    raise dash.exceptions.PreventUpdate("cancel the callback")
#INSTUMENTS
@app.callback(
    Output("instuments_button", "n_clicks"),
    Output('instuments_output', "children"),
    Output('instruments_symbol', "value"),
    Output('instruments_optype', "value"),
    Input("instuments_button", "n_clicks"),
    Input('instuments_output', "children"),
    Input('instruments_symbol', "value"),
    Input('instruments_optype', "value"),
    State('key_value','data'),
    State('secret_value','data'),
)
def instruments_callback(n,output,symbol,optype,key,secret):
    if n==1:
        ui_process = ui.UiProcess(key,secret)
        df = ui_process.phd_api.instruments(symbol,option_type=optype)
        if (df is None) or (df.shape[0]==0):
            output = dbc.Alert(ui_process.phd_api.client.err, color="danger"),
            ui_process.phd_api.client.err = None
        else:
            table = html.Div(dbc.Table.from_dataframe(df,
                                                      striped=True,
                                                      bordered=True,
                                                      hover=True,),
                             style={"maxHeight": "400px", "overflow": "auto"})
            output = table
        n = 0
        return n,output,symbol,optype
    raise dash.exceptions.PreventUpdate("cancel the callback")
#ORDERS
@app.callback(
    Output('orders_button', "n_clicks"),
    Output('output_orders', "children"),
    Input('orders_button', "n_clicks"),
    Input('output_orders', "children"),
    Input('productid_input_orders', "value"),
    Input('start_input_orders', "value"),
    Input('end_input_orders', "value"),
    Input('limit_input_orders', "value"),
    Input('orders_active', "value"),
    State('key_value','data'),
    State('secret_value','data'),
)
def orders_callback(n,output,productid,start,end,limit,active,key,secret):
    if n==1:
        ui_process = ui.UiProcess(key,secret)
        id_numb = 0
        try:
            id_numb = ui_process.instruments[ui_process.instruments.symbolId == productid]['id'].values.tolist()[0]
        except:
            pass
        df = ui_process.phd_api.orders(product_id=id_numb,is_active=active,start_time=start,end_time=end,limit=limit)
        if (df is None) or (df.shape[0]==0):
            output = dbc.Alert(ui_process.phd_api.client.err, color="danger"),
            ui_process.phd_api.client.err = None
        else:

            table = html.Div(dbc.Table.from_dataframe(df,
                                                      striped=True,
                                                      bordered=True,
                                                      hover=True,),
                             style={"maxHeight": "400px", "overflow": "auto"})
            output = table
        n = 0
        return n,output,
    raise dash.exceptions.PreventUpdate("cancel the callback")

#PRICE
@app.callback(
    Output('price_button', "n_clicks"),
    Output('output_price', "children"),
    Input('price_button', "n_clicks"),
    Input('output_price', "children"),
    Input('productid_input_price', "value"),
    State('key_value','data'),
    State('secret_value','data'),
)
def price_callback(n,output,productid,key,secret):
    if n==1:
        ui_process = ui.UiProcess(key,secret)
        id_numb = 0
        try:
            id_numb = ui_process.instruments[ui_process.instruments.symbolId == productid]['id'].values.tolist()[0]
        except:
            pass
        df = ui_process.phd_api.price(product_id=id_numb)
        if (df is None):
            output_new = dbc.Alert(ui_process.phd_api.client.err, color="danger"),
            ui_process.phd_api.client.err = None
            n = 0
            return n,output_new
        else:
            table = html.Div(dbc.Table.from_dataframe(df,
                                                      striped=True,
                                                      bordered=True,
                                                      hover=True,),
                             style={"maxHeight": "400px", "overflow": "auto",})
            output_new = table
        n = 0
        return n,output_new
    raise dash.exceptions.PreventUpdate("cancel the callback")

#POSITION
@app.callback(
    Output('position_button', "n_clicks"),
    Output('output_position', "children"),
    Input('position_button', "n_clicks"),
    Input('output_position', "children"),
    Input('productid_input_position', "value"),
    State('key_value','data'),
    State('secret_value','data'),
)
def positions_callback(n,output,productid,key,secret):
    if n==1:
        ui_process = ui.UiProcess(key,secret)
        id_numb = 0
        try:
            id_numb = ui_process.instruments[ui_process.instruments.symbolId == productid]['id'].values.tolist()[0]
        except:
            pass
        df = ui_process.phd_api.positions(product_id=id_numb)
        if (df is None):
            output_new = dbc.Alert(ui_process.phd_api.client.err, color="danger"),
            ui_process.phd_api.client.err = None
            n = 0
            return n,output_new
        else:
            table = html.Div(dbc.Table.from_dataframe(df,
                                                      striped=True,
                                                      bordered=True,
                                                      hover=True,),
                             style={"maxHeight": "400px", "overflow": "auto",})
            output_new = table
        n = 0
        return n,output_new
    raise dash.exceptions.PreventUpdate("cancel the callback")
#DELETE
@app.callback(
    Output('delordr_button', "n_clicks"),
    Output('output_delordr', "children"),
    Input('delordr_button', "n_clicks"),
    Input('output_delordr', "children"),
    Input('orderid_input_delordr', "value"),
    State('key_value','data'),
    State('secret_value','data'),
)
def delete_order(n,output,id,key,secret):
    if n == 1:
        ui_process = ui.UiProcess(key,secret)
        df = ui_process.phd_api.delete_order(order_id=id)
        if ui_process.phd_api.client.err is None:
            table = html.Div(dbc.Table.from_dataframe(df,
                                                      striped=True,
                                                      bordered=True,
                                                      hover=True,),
                             style={"maxHeight": "400px", "overflow": "auto",})
            output = table
            n = 0
            return n,output
        else:
            output_new = dbc.Alert(ui_process.phd_api.client.err, color="danger"),
            ui_process.phd_api.client.err = None
            n = 0
            return n,output_new
    raise dash.exceptions.PreventUpdate("cancel the callback")

#POST
@app.callback(
    Output('putordr_button', "n_clicks"),
    Output('output_putordr', "children"),

    Input('putordr_button', "n_clicks"),
    Input('output_putordr', "children"),
    Input('productid_input_putordr', "value"),
    Input('quant_input_putordr', "value"),
    Input('price_input_putordr', "value"),
    Input('putordr_side', "value"),
    State('key_value','data'),
    State('secret_value','data'),
)
def post_order(n,output,id,quant,price,side,key,secret):
    if n == 1:
        ui_process = ui.UiProcess(key,secret)
        id_numb = 0
        try:
            id_numb = ui_process.instruments[ui_process.instruments.symbolId == id]['id'].values.tolist()[0]
        except:
            pass
        df = ui_process.phd_api.post_order(product_id=id_numb,quantity=quant,price=price,side=side)
        if ui_process.phd_api.client.err is None:
            table = html.Div(dbc.Table.from_dataframe(df,
                                                      striped=True,
                                                      bordered=True,
                                                      hover=True,),
                             style={"maxHeight": "400px", "overflow": "auto",})
            output = table
            n = 0
            return n,output
        else:
            output_new = dbc.Alert(ui_process.phd_api.client.err, color="danger"),
            ui_process.phd_api.client.err = None
            n = 0
            return n,output_new
    raise dash.exceptions.PreventUpdate("cancel the callback")

#REFRESH INSTRUMENTS OPTIONS
@app.callback(
    Output('productid_input_putordr','options'),
    Output('productid_input_price','options'),
    Output('productid_input_position','options'),
    Output('productid_input_orders','options'),
    Input('productid_input_putordr','options'),
    Input('productid_input_price','options'),
    Input('productid_input_position','options'),
    Input('productid_input_orders','options'),
    State('key_value','data'),
    State('secret_value','data'),

)
def refresh_options(options1,options2,options3,options4,key,secret):
    ui_process = ui.UiProcess(key,secret)
    options_arr = ui_process.instruments['symbolId'].values
    options1 = options_arr
    options2 = options_arr
    options3 = options_arr
    options4 = options_arr
    return options1,options2,options3,options4

#COLLAPSE
@app.callback(
    Output("collapse-instruments", "is_open"),
    [Input("collapse-button-instruments", "n_clicks")],
    [State("collapse-instruments", "is_open")],
)
def toggle_collapse_instruments(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-position", "is_open"),
    [Input("collapse-button-position", "n_clicks")],
    [State("collapse-position", "is_open")],
)
def toggle_collapse_position(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-price", "is_open"),
    [Input("collapse-button-price", "n_clicks")],
    [State("collapse-price", "is_open")],
)
def toggle_collapse_price(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(
    Output("collapse-orders", "is_open"),
    [Input("collapse-button-orders", "n_clicks")],
    [State("collapse-orders", "is_open")],
)
def toggle_collapse_orders(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-putordr", "is_open"),
    [Input("collapse-button-putordr", "n_clicks")],
    [State("collapse-putordr", "is_open")],
)
def toggle_collapse_putordr(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-delordr", "is_open"),
    [Input("collapse-button-delordr", "n_clicks")],
    [State("collapse-delordr", "is_open")],
)
def toggle_collapse_delordr(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=False,port=8080,host='0.0.0.0')