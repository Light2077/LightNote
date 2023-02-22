import logging
import psycopg2

class PostgreDataBase:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            connect_timeout=5,
            # options="-c search_path=other_db,public"
        )

    # 执行sql语句
    def execute(self, sql, return_dataframe=True):
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                data = cur.fetchall()
                columns = [col.name for col in cur.description]
        except (psycopg2.errors.SyntaxError,
                psycopg2.errors.InFailedSqlTransaction) as e:
            logging.exception(e, exc_info=False)

        if return_dataframe:
            data = pd.DataFrame(data, columns=columns)

        return data

    # 获取所有表的名称
    def get_all_table_names(self):
        sql = "SELECT table_name \n" \
              "FROM information_schema.tables \n" \
              "WHERE table_schema = 'public'"
        data = self.execute(sql)
        table_names = [d[0] for d in data]
        return table_names

    # 获取某个表的所有列名
    def get_table_column_names(self, table_name):
        sql = f"SELECT column_name FROM information_schema.columns \n" \
              f"WHERE table_name='{table_name}'"

        data = self.execute(sql)
        column_names = [d[0] for d in data]
        return column_names