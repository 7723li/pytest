import xlwt
import re
import shutil
import os

def sql_2_xls(sqlfilename):
    with open(sqlfilename, "rb") as sqlfile:
        sqlbyte = sqlfile.read()
        sqlstr = str(sqlbyte, encoding="utf-8")

    # 新建Excel表格
    ExcelBook = xlwt.Workbook(encoding='utf-8')
    ExcelSheet = ExcelBook.add_sheet('sheet1')

    # 处理sql文本并对应写入到表格
    row_idx = 0
    print('\n')
    tables = sqlstr.split('CREATE TABLE')
    for table in tables:
        if table == '':
            continue

        # 初始化原始数据 删除多余的字符
        ignorepos = 0
        while table[ignorepos] == ' ':                              #  "AgeType" ("ID" INTEGER,"Num" TEXT,"Type" TEXT NOT NULL,PRIMARY KEY ("Type") ) 数据头部有可能存在1~n个多余空格
            ignorepos += 1
            continue
        table = table[ignorepos : len(table)]
        table = table.replace("\r", "")
        table = table.replace("\n", "")
        table = table.replace(";", "")
        # print("table : " + table)
        
        # 表格名
        tablenamepos = table.find(' ')                              # "AgeType" ("ID" INTEGER,"Num" TEXT,"Type" TEXT NOT NULL,PRIMARY KEY ("Type") ) 寻找第一个空格
        tablename = table[0 : tablenamepos].replace('"', '')        # "AgeType" => AgeType
        print("tablename : " + tablename)
        table = table[tablenamepos + 1 : len(table)]                # ("ID" INTEGER,"Num" TEXT,"Type" TEXT NOT NULL,PRIMARY KEY ("Type") )
        # print("table : " + table)
        ExcelSheet.write_merge(row_idx, row_idx, 0, 4, tablename)
        row_idx += 1
        
        # 寻找主键 有可能主键不存在 或 存在多个主键
        primarykeypos = table.find('PRIMARY KEY')                   # 寻找'PRIMARY KEY'所在位置 如果存在 返回第一个P所在的位置
        if primarykeypos != -1:                                     # ("ID" INTEGER,"Num" TEXT,"Type" TEXT NOT NULL,PRIMARY KEY ("Type") )
                                                                    # PRIMARY KEY ("Type") ) => Type
            primarykeys = table[primarykeypos : len(table)].replace("PRIMARY KEY", '').replace(' ', '').replace('"', '').replace('(','').replace(')', '')
            if ',' in primarykeys:
                primarykeys = primarykeys.split(',')                  # BatchNo,Qc_Level => ['BatchNo', 'Qc_Level']
            else:
                primarykeys = [primarykeys]                           # Type => ['Type']
            print("primarykeys : " + str(primarykeys))
            table = table[1 : primarykeypos - 1]                    # "ID" INTEGER,"Num" TEXT,"Type" TEXT NOT NULL
        else:                                                       # 主键不存在
            table = table.replace('(', '')                          # 例如("ID" INTEGER,"Num" TEXT,"Type" TEXT NOT NULL )
            table = table.replace(')', '')
            ignorepos = len(table) - 1                              # 注意必须-1 python对内存的管理没有C++严格 因此更容易出现一些奇怪的问题
            while table[ignorepos] == ' ':                          # "ID" INTEGER,"Num" TEXT,"Type" TEXT NOT NULL  数据尾部有可能存在0~n个多余空格
                ignorepos -= 1
            table = table[0 : ignorepos + 1]                        # "ID" INTEGER,"Num" TEXT,"Type" TEXT NOT NULL
            primarykeys = []
            print("primarykeys do not exist")
        # print("table : " + table)
        
        # 处理数据库各字段 包括名称、类型、最大长度、是否非空
        print("name\t\t\ttype\t\t\tprimary\t\t\tmax_len\t\t\tnot_null")
        ExcelSheet.write(row_idx, 0, "name")
        ExcelSheet.write(row_idx, 1, "type")
        ExcelSheet.write(row_idx, 2, "primary")
        ExcelSheet.write(row_idx, 3, "max_len")
        ExcelSheet.write(row_idx, 4, "not_null")
        row_idx += 1
        fields = table.split(',')                                   # [ '"ID" INTEGER', '"Num" TEXT', '"Type" TEXT NOT NULL' ]
        for field in fields:
            _name = str()
            _type = str()
            _primary = False
            _max_len = str()
            _not_null = False

            _not_null_pos = field.find('NOT NULL')
            if -1 != _not_null_pos:
                _not_null = True
                field = field[0 : _not_null_pos - 1]

            content = field.split(' ')
            assert(2 == len(content))
            _name = content[0].replace('"', '')
            _type = content[1]

            _primary = ( len(primarykeys) > 0 and (_name in primarykeys) )

            _max_len_pos_left = _type.find('(')
            if _max_len_pos_left != -1:
                _max_len_pos_right = _type.find(')')
                _max_len = _type[_max_len_pos_left + 1 : _max_len_pos_right]
                _type = _type[0 : _max_len_pos_left]

            print(_name, end = '\t\t\t')
            print(_type, end = '\t\t\t')
            print(_primary, end = '\t\t\t')
            print(_max_len, end = '\t\t\t')
            print(str(_not_null))

            ExcelSheet.write(row_idx, 0, _name)
            ExcelSheet.write(row_idx, 1, _type)
            if _primary:
                ExcelSheet.write(row_idx, 2, "True")
            else:
                ExcelSheet.write(row_idx, 2, "")
            ExcelSheet.write(row_idx, 3, _max_len)
            if _not_null:
                ExcelSheet.write(row_idx, 4, "True")
            else:
                ExcelSheet.write(row_idx, 4, "")
            row_idx += 1

        for i in range(5):
            ExcelSheet.write(row_idx, i, '')
        row_idx += 1
        print('\n')

    ExcelName = "sql_2_xls.xls"
    CopyPath = os.path.join(os.path.expanduser("~"),"Desktop/lzx_share")
    ExcelBook.save(ExcelName)
    try:
        shutil.move(ExcelName, CopyPath)
    except shutil.Error:
        os.unlink(os.path.join(CopyPath, ExcelName))
        shutil.move(ExcelName, CopyPath)

    return CopyPath