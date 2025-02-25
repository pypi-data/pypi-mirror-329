from xl_factory.template import module, project, resources
from sqlalchemy import create_engine, MetaData
import json


class Factory:
    def __init__(self, mysql_config):
        self.mysql_config = mysql_config
        self.grouped_tables = {}
        self.engine = self.create_engine()

    def create_engine(self):
        DATABASE_URL = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4'.format(**self.mysql_config)
        return create_engine(DATABASE_URL)

    def run(self):
        # 使用MetaData读取数据库中的所有表信息
        metadata = MetaData()
        metadata.reflect(bind=self.engine)

        # 遍历每个表
        for table_name, table in metadata.tables.items():
            columns = [f"""
                {{
                    label: "{column.comment if column.comment else ''}",
                    prop: "{column.name}",
                }}""" for column in table.columns
            ]
            columns = '[' + ','.join(columns) + ']'
            table_comment = table.comment if table.comment else ""

            resources, table_english = table_name.split('_', 1) if '_' in table_name else (table_name, '')

            data = {
                "table": table_name,
                "english": table_english,
                "chinese": table_comment,
                "api_name": ''.join(word.capitalize() for word in table_english.split('_')),
                "api_path": table_name.replace('_', '/'),
                "columns": columns
            }
            if table_comment:
                if resources not in self.grouped_tables:
                    self.grouped_tables[resources] = {
                        "table_names": [{
                            "name": table_name,
                            "chinese": table_comment
                        }], 
                        "tables": [table_english], 
                        "modules": [data]
                    }
                else:
                    self.grouped_tables[resources]['table_names'] += [{
                        "name": table_name,
                        "chinese": table_comment
                    }]
                    self.grouped_tables[resources]['tables'] += [table_english]
                    self.grouped_tables[resources]['modules'] += [data]

        for resources, data in self.grouped_tables.items():
            table_names = data.get('table_names', [])
            tables = data.get('tables', [])
            apis = '\n'.join([f"export {{ default as {''.join(word.capitalize() for word in item.split('_'))} }} from './{item.replace('_', '/')}'" for item in tables])
            routes = []
            for item in table_names:
                table_name = item.get('name', '')
                table_chinese = item.get('chinese', '')
                resources, table_english = table_name.split('_', 1) if '_' in table_name else (table_name, '')
                routes += [f"['/{table_english}', '{table_chinese}', () => import('#/{table_name.replace('_', '/')}/views/list.vue')]"]
            routes = "export default [" + ',\n'.join(routes) + ']'
            resources.copy(resources, {
                "resources": resources,
                "apis": apis,
                "routes": routes
            })
            for item in data['modules']:
                english = item.get('english', '')
                module.copy(f'{resources}/{"/".join(english.split("_"))}', item)

if __name__ == '__main__':
    MYSQL_CONFIG = {
        'host': '110.40.133.185',
        'port': 3306,
        'user': 'root',
        'password': 'iQyfnWOfM#hPHy^t',
        'db': 'stock'
    }

    factory = Factory(MYSQL_CONFIG)
    factory.run()
