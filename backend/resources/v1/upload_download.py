# coding=utf-8
# auther：Liul5
# date：10/30/2019 2:32 PM
# tools：PyCharm
# Python：3.7.3
from flask_restful import Resource, reqparse
from flask import request, send_from_directory, make_response, Response, send_file
from urllib.parse import quote
import sys
import pyexcel
import werkzeug
from werkzeug.utils import secure_filename
import os
from common.utils import response
from common.excel_utils import write_to_excel
from config import run_config


class UploadDownloadResource(Resource):

    def get(self):
        """下载文件"""
        file_name = r'房子.jpg'
        tmp = send_from_directory(run_config.UPLOAD_FOLDER, file_name, as_attachment=True)
        return tmp

    def post(self):
        """第一种,以文件流的方式"""
        data = request.files
        file = data.get("file")
        if not file:
            return response("Arguments file don`t exist!", 400)
        stream = file.stream
        filename = secure_filename(file.filename)
        file_path = os.path.join(run_config.UPLOAD_FOLDER, filename)
        if self.allowed_file(filename):
            with open(file_path, "wb") as out:
                out.write(stream.read())
            return response({"path": file_path})
        return response(f"Allowed file types are: {run_config.ALLOWED_EXTENSIONS}", 400)

    # def post(self):
    #     """第二种写法"""
    #     if 'file' not in request.files:
    #         return response("Arguments file don`t exist!", 400)
    #     file = request.files['file']
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         return response("No selected file", 400)
    #     if file and self.allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(run_config.UPLOAD_FOLDER, filename))
    #         return response("File successfully uploaded")
    #     else:
    #         return response(f"Allowed file types are: {run_config.ALLOWED_EXTENSIONS}", 400)
    #
    # def post(self):
    #     """与第二种类似，只是传参处理不一样"""
    #     parse = reqparse.RequestParser()
    #     parse.add_argument('file', required=True, help="Arguments file don`t exist!", type=werkzeug.datastructures.FileStorage, location='files')
    #     data = parse.parse_args()
    #     file = data.get("file")
    #     if self.allowed_file(file.filename):
    #         file.save(os.path.join(run_config.UPLOAD_FOLDER, file.filename))
    #         return response("File successfully uploaded")
    #     return response(f"Allowed file types are: {run_config.ALLOWED_EXTENSIONS}", 400)

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in run_config.ALLOWED_EXTENSIONS


class ExcelUploadDownload(Resource):
    def get(self):
        # 使用pyexcel库
        # data = [
        #     ["a", "b", "c"],["a1", "b1", "c1"],["a2", "b2", "c2"],
        # ]
        # sheet = pyexcel.Sheet(data, colnames=["姓名","性别", "昵称", "电话"])
        # output = make_response(sheet.csv)
        # output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        # output.headers["Content-type"] = "text/csv"
        # return output

        # 使用xlsxwriter库
        xlsx_data = write_to_excel()
        response = make_response(xlsx_data.getvalue())
        # 文件名中文显示
        response.headers['Content-Disposition'] = "attachment; filename={0}; filename*=utf-8''{0}".format(quote("测试.xlsx"))
        # response.headers['Content-Disposition'] = 'attachment; filename=Report.xlsx'
        response.headers["Content-type"] = 'application/x-xlsx'
        # response.headers["Content-type"] = "text/csv"
        return response
        # return send_file(xlsx_data,attachment_filename="testing.xlsx", as_attachment=True)

        # 第三种保存CSV
        # csv_file = "姓名" + ',' + "性别" + ',' + "test3" + '\n'
        # response = Response(csv_file, mimetype='text/csv',
        #                     headers={'Content-disposition': 'attachment; filename=file_name.csv'})
        # return response

    def post(self):
        """读取本地excel to json"""
        if 'excel' in request.files:
            # 获取上传的文件
            filename = request.files['excel'].filename
            # 获取文件的扩展名和内容
            extension = filename.split(".")[-1]
            content = request.files['excel'].read()
            sheet = pyexcel.get_sheet(file_type=extension, file_content=content)
            # 将第一行当做headers
            sheet.name_columns_by_row(0)
            # sheet.save_to_database()
            # 返回json
            return response({"result": sheet.dict})
        else:
            return response("Arguments excel file don`t exist!", 400)
