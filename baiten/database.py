import pymysql

class baidten_db_struct:
    apply_number = str()
    apply_date = str()
    public_number = str()
    public_data = str()
    apply_member = str()
    invent_member = str()

class baidten_db:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                            port=3306,
                                            user='root',
                                            password='tc0301',
                                            charset='utf8')
        self.cursor = self.connection.cursor()