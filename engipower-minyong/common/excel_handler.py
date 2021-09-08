"""
    @File: excel_handler.py
    @Description: 对Excel文件的读取和写入操作
    @Author: wangk
    @UPDATED BY: wangk
@   UPDATED: 2021/03/22
"""
import openpyxl


class ExcelHandler:
    def __init__(self, fpath):
        self.fpath = fpath

    def read(self, sheet_name):
        # 打开文件
        wb = openpyxl.open(self.fpath)
        # 获取工作表
        ws = wb[sheet_name]
        ws_data = list(ws.values)
        title = ws_data[0]
        all_data = []
        for d in ws_data[1:]:
            row = dict(zip(title, d))
            all_data.append(row)
            # print(row)

        return all_data

    def write(self, sheet_name, content, row, column):
        # 写入excel
        wb = openpyxl.load_workbook(self.fpath)
        ws = wb[sheet_name]
        ws.cell(row=row, column=column).value = content
        wb.save(self.fpath)


if __name__ == '__main__':
    excel = ExcelHandler(r'D:\WorkspaceForPython\engipower-minyong\cases\test_cases.xlsx')
    data = excel.read('功能模块')
    # print(data)
