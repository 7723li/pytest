import pymysql

test_data = {
    '申请号': 'CN201420604639.6', 
    '申请日': '20141020', 
    '公开号': 'CN204072058U', 
    '授权公告日': '20150107', 
    '申请（专利权）人': '广州医软智能科技有限公司', 
    '发明人': '刘发杰 郑鹏飞 亚历克斯·布兰多 罗晓川', 
    '专利类型': '中国实用新型', 
    '专利名': '多层次微循环状态监测装置', 
    '法律状态': '有权-审定授权'
    }

class baidten_db:
    def __init__(self):
        self.connection = \
            pymysql.connect(host='localhost',
                            port=3306,
                            user='root',
                            password='tc0301',
                            database='baiten_db',
                            charset='utf8')
        self.cursor = self.connection.cursor()

        # 手动查询表格列表
        self.cursor.execute("show tables;")
        table_list = [tuple[0] for tuple in self.cursor.fetchall()]
        if "medsoft_baiten_db" in table_list:
            return

        create_table_sql =  "create table if not exists medsoft_baiten_db ("   # 不存在才创建
        create_table_sql += "`id` INT UNSIGNED AUTO_INCREMENT primary key,"    # 主键
        create_table_sql += "apply_num varchar(32),"                           # 申请号
        create_table_sql += "apply_date varchar(8),"                           # 申请日
        create_table_sql += "public_num varchar(32),"                          # 公开号
        create_table_sql += "public_date varchar(8),"                          # 公开日
        create_table_sql += "aplly_member varchar(128),"                       # 申请（专利权）人
        create_table_sql += "invent_member varchar(512),"                      # 发明人
        create_table_sql += "patent_type varchar(16),"                         # 专利类型
        create_table_sql += "patent_name varchar(64),"                         # 专利名称
        create_table_sql += "law_status varchar(32)"                           # 法律状态
        create_table_sql += ") character set utf8;"
        self.cursor.execute(create_table_sql)

    def insert_one(self, src_data):
        assert(type(src_data) is dict)