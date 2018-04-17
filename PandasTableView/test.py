#coding=utf-8
# Python 获取KSM 命令表格到词典中

import xlrd
import codecs

def Excel2Json(file_path):
    # 打开excel文件
    if get_data(file_path) is not None:
        book = get_data(file_path)
        # 抓取所有sheet页的名称
        sheet = book.sheet_by_index(0)
        nrows = sheet.nrows  # 行号
        #数据存放地点
        result={}
        for row in range(2,nrows):

        # 获取ID 和 命令号
            id = "<00-"+str(sheet.row_values(row)[8])+">"
            command = str(sheet.row_values(row)[9])

        # 获取其他信息
            info = {}
            info['card'] = str(sheet.row_values(row)[0])
            info['module'] = str(sheet.row_values(row)[1])
            info['command'] = str(sheet.row_values(row)[2])
            info['para'] = str(sheet.row_values(row)[10])
            info['description']= str(sheet.row_values(row)[11])
            result[id,command]=info

        print(result)
        print(result['<00-80>','09'])

def get_data(file_path):
    """获取excel数据源"""
    return xlrd.open_workbook(file_path)


def saveFile(file_path, file_name, data):
    output = codecs.open(file_path + "/" + file_name + ".json", 'w', "utf-8")
    output.write(data)
    output.close()


if __name__ == '__main__':
    file_path = '6000.xlsx'
    json_data = Excel2Json(file_path)