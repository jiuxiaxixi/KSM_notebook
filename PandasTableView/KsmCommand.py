import xlrd


class KsmCommand:
    result = {}

    def __init__(self, filename):
        self.book = self.get_data(filename)
        self.Excel2Json(self.book)

    def get_data(self,file_path):
        """获取excel数据源"""
        return xlrd.open_workbook(file_path)

    # 传入ID和命令 格式化输出
    def get_command_res(self, address, command):
        if (address, command) in self.result:
            command_dic = self.result[address,command]
            command_res = command_dic['card']+' '+command_dic['module']+' '+command_dic['action']+' '+command_dic['description']
            return command_res
        else:
            return "未在配置中查询到该命令"



    def Excel2Json(self, book):
        # 打开excel文件
        # 抓取所有sheet页的名称
        sheet = book.sheet_by_index(0)
        nrows = sheet.nrows  # 行号
        last_card = ""
        last_module = ""
        # 数据存放地点
        for row in range(2, nrows):

            if str(sheet.row_values(row)[0]) != "":
                last_card = str(sheet.row_values(row)[0])
            if str(sheet.row_values(row)[1]) != "":
                last_module = sheet.row_values(row)[1]

            up_id = str(sheet.row_values(row)[4]).split('.')[0]
            down_id = str(sheet.row_values(row)[8]).split('.')[0]

            # 获取下发的 ID 和 命令号
            id = "<00-" + down_id + ">"
            command = str(sheet.row_values(row)[9]).split('.')[0]
            action = str(sheet.row_values(row)[2])
            # 获取其他信息
            info = {}
            info['card'] = last_card
            info['module'] = last_module
            info['action'] = action
            info['para'] = str(sheet.row_values(row)[10])
            info['description'] = str(sheet.row_values(row)[11])
            self.result[id, command] = info

            # 获取上传的ID和命令号
            id = "<" + up_id + "-" + down_id + ">"

            # 获取数据
            sendinfo = {}
            sendinfo['card'] = last_card
            sendinfo['module'] = last_module
            sendinfo['action'] = action
            sendinfo['para'] = str(sheet.row_values(row)[6])
            sendinfo['description'] = str(sheet.row_values(row)[7])
            self.result[id, command] = sendinfo





#print(kc.get_command_res('<00-80>', '09'))
