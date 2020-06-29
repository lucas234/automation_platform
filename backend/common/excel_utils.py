# coding=utf-8
# auther：Liul5
# date：11/1/2019 1:23 PM
# tools：PyCharm
# Python：3.7.3
import xlsxwriter
from io import BytesIO


def write_to_excel():
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Summary")
    # Here we will adding the code to add data
    expenses = (
        ['Rent', 1000, 1, 2, 4],
        ['Gas', 100, 11, 22, 44],
        ['Food', 300, 111, 222, 444],
        ['Gym', 50, 1111, 2222, 4444],
    )

    header_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#f4cccc'})

    # 写入列名
    headers = ['A', 'B', 'C', 'D', 'E']
    for col, item in enumerate(headers):
        worksheet.write(0, col, item, header_format)

    # 通过迭代写入数据.
    for row, item in enumerate(expenses):
        for col in range(len(headers)):
            worksheet.write(row+1, col, item[col])

    # 使用公式，例如B列的和.
    # worksheet.write(5, 0, 'Total')
    # worksheet.write(5, 1, '=SUM(B2:B5)')
    # 设置A-E的宽
    worksheet.set_column('A:E', 10)
    workbook.close()
    # go back to the beginning of the stream
    output.seek(0)
    return output

