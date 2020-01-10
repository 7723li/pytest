import pymysql, os, datetime

class baidten_db:
    def __init__(self, sys_platform):
        self.check_running(sys_platform)                    # 开启服务

        self.connection = pymysql.connect(host='localhost', # 无库连接
                                        port=3306,
                                        user='root',
                                        password='tc0301',
                                        charset='utf8')
        self.cursor = self.connection.cursor()

        self.check_database()                               # 建库 并 使用
        self.check_table()                                  # 建表

    def check_running(self, sys_platform):
        if sys_platform == "linux":
            os.popen("service start mysql").read()
        elif sys_platform == "win32":
            os.popen("net start mysql").read()

    def check_database(self):
        self.cursor.execute("create database if not exists baiten_db;")
        self.cursor.execute("use baiten_db;")

    def check_table(self):
        # 手动查询表格列表
        self.cursor.execute("show tables;")
        table_list = [tuple[0] for tuple in self.cursor.fetchall()]
        if "medsoft_baiten_db" in table_list:
            return

        create_table_sql =  "create table if not exists medsoft_baiten_db ("   # 不存在才创建
        create_table_sql += "`id` INT UNSIGNED AUTO_INCREMENT primary key,"    # 主键
        create_table_sql += "check_datetime DATETIME,"                         # 插入数据的查询时间戳
        create_table_sql += "apply_num varchar(32),"                           # 申请号
        create_table_sql += "apply_date varchar(32),"                          # 申请日
        create_table_sql += "public_num varchar(32),"                          # 公开号
        create_table_sql += "public_date varchar(32),"                         # 公开日
        create_table_sql += "aplly_member varchar(128),"                       # 申请（专利权）人
        create_table_sql += "invent_member varchar(512),"                      # 发明人
        create_table_sql += "patent_type varchar(64),"                         # 专利类型
        create_table_sql += "patent_name varchar(64),"                         # 专利名称
        create_table_sql += "law_status varchar(32),"                          # 法律状态
        create_table_sql += "enable tinyint(1) NOT NULL DEFAULT 0,"            # 确认状态
        create_table_sql += "affirm_time DATETIME DEFAULT NULL"                # 确认时间
        create_table_sql += ") character set utf8;"
        self.cursor.execute(create_table_sql)

    def insert_one_by_dict(self, datetime, src_data):
        assert(type(src_data) is dict)

        data = list(src_data.values())
        assert(len(data) == 9)

        insert_sql = "insert into medsoft_baiten_db \
        (check_datetime, apply_num, apply_date, public_num, public_date, aplly_member, invent_member, patent_type, patent_name, law_status) \
        values  \
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        data.insert(0, datetime)
        self.cursor.execute(insert_sql, data)
        self.connection.commit()        # 数据库事务

    def insert_one_by_list(self, src_data):
        assert(type(src_data) is list)
        assert(len(src_data) == 10)

        insert_sql = "insert into medsoft_baiten_db \
        (check_datetime, apply_num, apply_date, public_num, public_date, aplly_member, invent_member, patent_type, patent_name, law_status) \
        values  \
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        self.cursor.execute(insert_sql, src_data)
        self.connection.commit()        # 数据库事务

    def get_all(self):
        self.cursor.execute("select * from medsoft_baiten_db;")
        all = self.cursor.fetchall()
        return all

    def test_get_member_rank(self):
        date_time = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = 'SELECT invent_member FROM medsoft_baiten_db WHERE locate("' + date_time + '", check_datetime)'
        self.cursor.execute(sql)
        all_member_list = self.cursor.fetchall()

        dict_member_times = dict()
        for member_list in all_member_list:
            members = member_list[0].split(';')
            for member in members:
                if dict_member_times.get(member) == None:
                    dict_member_times[member] = 1
                else:
                    dict_member_times[member] += 1

        li = str()
        for member_name in list(dict_member_times.keys()):
            li += member_name  + " : " + str(dict_member_times[member_name]) + ", "
            sql = 'SELECT patent_name FROM medsoft_baiten_db WHERE locate("' + member_name + '", invent_member);'
            self.cursor.execute(sql)
            li += str(self.cursor.fetchall()).replace('(', '').replace(')', '').replace(',,', ',')
            li += "\n"
        with open("member_list.txt", "wb") as file:
            file.write(li.encode("utf-8"))

def test_main():
    db = baidten_db("win32")
    db.test_get_member_rank()
