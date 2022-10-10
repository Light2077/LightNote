import psycopg2
import logging
logger = logging.getLogger(__name__)


class DataBase:
    def __init__(self, dbname=None, user=None, password=None, host=None, port=None):
        # self.database_params = database_params
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        logger.info(f"正在连接({self.host}:{self.port})...")
        
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                connect_timeout=5,
            )
            logger.info('数据库连接成功!')
        except Exception as e:
            logger.warning('数据库连接失败!')
            self.conn = None
    
    def execute(self, sql):
        """ 执行sql，执行失败自动rollback """
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                data = cur.fetchall()
            return data
        except psycopg2.errors.SyntaxError as e:
            logger.exception('语法错误')
            self.conn.rollback()
        except Exception as e:
            logger.exception('')
            self.conn.rollback()
    
    def df_to_sql(self, df, table):
        """ pandas dataframe入库 
        df -- 要入库的DataFrame，其columns要与数据库表中的字段对应
        table -- strings, 数据库表名
        """
        
        if len(df) == 0:
            logger.warning('传入的dataframe为空')
            return
        # 获取dataframe的columns作为要插入的字段名，如果columns与数据库里的字段名不同，则插入失败
        self.check_columns_in_table(table, df.columns)
        fields = ','.join([f'"{c}"' for c in df.columns])
        num_columns = df.shape[1]
        
        with conn.cursor() as cur:
            args = ','.join(
                cur.mogrify(f'({",".join(["%s"] * num_columns)})', i).decode('utf-8')
                for i in df.values.tolist()
            )
            
            sql = f'INSERT INTO {table}({fields}) VALUES ' + (args)
            if self.conn is None:
                return sql
            self.execute(sql)
        return sql

    # 获取所有表的名称
    def get_all_table_names(self):
        sql = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """
        data = self.execute(sql)
        table_names = [d[0] for d in data]
        return table_names

    # 获取某个表的所有列名
    def get_table_column_names(self, table_name):
        sql = f"""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='{table_name}'
        """
        data = self.execute(sql)
        column_names = [d[0] for d in data]
        return column_names
    
    def check_columns_in_table(self, table_name, columns):
        """ 输入表名、字段列表，确认是否所有字段都属于该表 """
        if len(columns) == 0:
            raise ValueError('字段列表不能为空!')
        table_columns = self.get_table_column_names(table_name)
        for c in columns:
            if c not in table_columns:
                raise ValueError(f'表"{table_name}"中，不存在字段:"{c}"')