# Học thêm tại: https://dash.plotly.com/

# Run this app with `python app.py` and

# visit http://127.0.0.1:8050/ in your web browser.

# BẤM CTRL '+' C ĐỂ TẮT APP ĐANG CHẠY

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate(
    "./iuh-20048971-firebase-adminsdk-datxn-bc3a5e4a0a.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(
    u'tbl20048971').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

# df = pd.read_csv('orginal_sales_data_edit.csv', encoding='utf-8', header=0)

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")
df["PROFIT"] = df["SALES"]-(df["QUANTITYORDERED"]*df["PRICEEACH"])

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__)

server = app.server

app.title = "Danh Mục Sản Phẩm Tiềm Năng"

# tổng doanh số
sales = sum(df['SALES'])

# tổng lợi nhuận
profit = sum(df['PROFIT'])

# top doanh số
topSales = df['SALES'].max()

# top lợi nhuận
topProfit = df['PROFIT'].max()

# bar chart doanh số từng năm
data1 = df.groupby(['YEAR_ID']).sum('SALES').reset_index()
figDoanhSo = px.bar(data1, x='YEAR_ID', y='SALES', labels={'YEAR_ID': 'Năm', 'SALES': 'Doanh số'},
                    title='DOANH SỐ BÁN HÀNG THEO NĂM')

# line chart lợi nhuận từng năm
data2 = df.groupby(['YEAR_ID']).sum('PROFIT').reset_index()
figLoiNhuan = px.line(data2, x='YEAR_ID', y='PROFIT', markers=True, labels={'YEAR_ID': 'Năm', 'PROFIT': 'Lợi Nhuận'},
                      title='LỢI NHUẬN BÁN HÀNG THEO NĂM')

# sunburst tỉ lệ doanh số theo danh mục và năm
figTiLeDoanhSo = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
                             color='SALES',
                             labels={'parent': 'Năm',
                                     'labels': 'Danh Mục', 'SALES': 'Doanh Số'},
                             title='TỈ LỆ DOANH SỐ THEO DANH MỤC VÀ NĂM')

# sunburst tỉ lệ lợi nhuận theo danh mục và năm
figTiLeLoiNhuan = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='PROFIT',
                              color='PROFIT',
                              labels={
                                  'parent': 'Năm', 'labels': 'Danh Mục', 'PROFIT': 'Lợi Nhuận'},
                              title='TỈ LỆ LỢI NHUẬN THEO DANH MỤC VÀ NĂM')

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3(
                    "XÂY DỰNG SẢN PHẨM DANH MỤC TIỀM NĂNG", className="header-title"
                ),
                html.H3(
                    "IUH - DHHTTT16A - 20048971 - BÙI NGUYỄN PHƯƠNG DUYÊN", className="header-title"
                )
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=html.Div(
                        children=[
                            html.H4(
                                "DOANH SỐ SALE",
                            ),
                            "{:.2f}".format(sales)
                        ],
                        className="label"
                    ), className="card c1"
                ),
                html.Div(
                    children=html.Div(
                        children=[
                            html.H4(
                                "LỢI NHUẬN",
                            ),
                            "{:.2f}".format(profit)
                        ],
                        className="label"
                    ), className="card c1"
                ),
                html.Div(
                    children=html.Div(
                        children=[
                            html.H4(
                                "TOP DOANH SỐ",
                            ),
                            "{:.2f}".format(topSales)
                        ],
                        className="label"
                    ), className="card c1"
                ),
                html.Div(
                    children=html.Div(
                        children=[
                            html.H4(
                                "TOP LỢI NHUẬN",
                            ),
                            "{:.2f}".format(topProfit)
                        ],
                        className="label"
                    ), className="card c1"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=figDoanhSo,
                        className="hist"
                    ), className="card c2"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=figTiLeDoanhSo,
                        className="hist"
                    ), className="card c2"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=figLoiNhuan,
                        className="hist"
                    ), className="card c2"
                ),
                html.Div(
                    children=dcc.Graph(
                        figure=figTiLeLoiNhuan,
                        className="hist"
                    ), className="card c2"
                )
            ], className="wrapper"
        )
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=1111)
