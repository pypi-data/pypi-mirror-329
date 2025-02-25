import os
from urllib.parse import urlparse, parse_qs
import yaml
import portalocker
from qg_toolkit.tools.qg_log import logger


class QGFile:
    @staticmethod
    def save_to_file(file_path, log):
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f'{log}\n')
            f.close()

    @staticmethod
    def save_to_file_deduplicate(file_path, log):
        """去重插入行"""
        if not os.path.exists(file_path):
            QGFile.save_to_file(file_path, "")
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if not log.endswith('\n'):
            log += '\n'
        lines.append(log)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(dict.fromkeys(lines))

    @staticmethod
    def txt_to_array(file_path: object, split: object = '----') -> list:
        lines = open(file_path, 'r', encoding='utf-8').readlines()
        arr = [[z.strip() for z in x.split(split)] for x in lines]
        return arr

    @staticmethod
    def delete_lines_in_txt(file_path: str, keyword: str, is_fuzzy=False):
        """
        根据内容删除指定行的数据，支持精确匹配和模糊匹配。
        读删合并一起，避免多次操作文件。

        :param file_path: TXT 文件路径
        :param keyword: 要删除的关键字
        :param is_fuzzy: 是否使用模糊匹配，默认为 False（精确匹配）
        """
        # 读取文件内容并过滤行
        with open(file_path, 'r', encoding='utf-8') as file:
            if is_fuzzy:
                # 模糊匹配：保留不包含关键字的行
                filtered_lines = [line for line in file if keyword not in line.strip()]
            else:
                # 精确匹配：保留不等于关键字的行（去除换行符）
                filtered_lines = [line for line in file if line.strip() != keyword]

        # 将修改后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(filtered_lines)
        logger.info(f"已删除符合条件的行，并保存到文件: {file_path}")

    @classmethod
    def get_row_from_file_index(cls, file_path: object, split: object = '----', index: int = 1):
        return cls.txt_to_array(file_path, split)[index - 1]

    @staticmethod
    def array_to_txt(arr, to_file_path) -> list:
        with open(to_file_path, 'a', encoding='utf-8') as f:
            for cols in arr:
                log = "----".join(cols)
                f.write(f'{log}\n')
            f.close()
        lines = open(to_file_path, 'r', encoding='utf-8').readlines()
        arr = [[z.strip() for z in x.split(to_file_path)] for x in lines]
        return arr

    @staticmethod
    def url_params_to_object(url, keyword=None):
        # 解析URL
        parsed_url = urlparse(url)
        # 获取查询字符串参数并转换为字典对象
        query_params = parse_qs(parsed_url.query)
        # 处理字典对象，将每个参数的值转换为单个值而不是数组
        for key, value in query_params.items():
            query_params[key] = value[0]
        # 返回转换后的字典对象
        if keyword:
            return query_params.get(keyword)
        return query_params

    @staticmethod
    def read_yaml(file_path):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                # 你可以在这里写入一些初始内容，或者留空
                pass
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def save_to_yaml(to_path, full_data):
        with open(to_path, 'w') as file:
            portalocker.lock(file, portalocker.LOCK_EX)  # 加锁
            yaml.safe_dump(full_data, file, default_flow_style=False)
            portalocker.unlock(file)  # 解锁
            file.close()
        logger.info("数据已成功修改并写回到YAML文件。")

    @staticmethod
    def excel_to_file(source_path, to_path, is_sort=False):
        """
        excel转成其他格式
        """
        try:
            import pandas as pd
            import json
            df = pd.read_excel(source_path)
            rows = df.to_json(orient='records')
            rows = json.loads(rows)
            if is_sort:
                rows = [{k: row[k] for k in sorted(row.keys())} for row in rows]
                df = pd.DataFrame(rows)
            # 判断to_path的文件类型，如果是json文件，则直接写入，如果是其他文件类型，则先将数据转换为目标文件类型，再写入。
            if to_path.endswith('.json'):
                with open(to_path, 'w') as file:
                    file.write(rows)
            elif to_path.endswith('.txt'):
                with open(to_path, 'w', encoding='utf-8') as file:
                    log = "----".join([str(val) for row in rows for key, val in row.items()])
                    file.write(f'{log}\n')
                    file.close()
            elif to_path.endswith('.csv'):
                df.to_csv(to_path, index=False)
            logger.info(f"数据已成功保存到 {to_path} 文件中。")
        except Exception as ex:
            logger.error(f"读取 {source_path} 文件时出现解析错误，请确保文件格式正确且数据完整。{ex}")

    @staticmethod
    def read_excel(file_path):
        """
        读取excel成list对象
        """
        try:
            import pandas as pd
            import json
            df = pd.read_excel(file_path)
            json_data = df.to_json(orient='records')
            json_list = json.loads(json_data)
            logger.info(json_list)
            return json_list
        except Exception as ex:
            logger.info(f"将Excel数据转换为JSON格式时出现解码错误，请检查数据内容是否符合JSON规范。")
            return None

    @staticmethod
    def save_to_excel(file_path, data, is_sort=False):
        try:
            # logger.info("入参数据:", data)
            import pandas as pd
            if is_sort:
                if isinstance(data, list):
                    data = [{k: row[k] for k in sorted(row.keys())} for row in data]
                    # logger.info("入参数据2:", data)
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            logger.info(f"数据已成功保存到 {file_path} 文件中。")
        except Exception as e:
            logger.info(f"保存数据到 {file_path} 文件时出错：{e}")

    @staticmethod
    def read_json(file_path):
        try:
            import json
            if not os.path.exists(file_path):
                logger.info(f"文件 {file_path} 不存在，请检查文件路径是否正确。")
                return None
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except Exception as e:
            logger.info(f"文件 {file_path} 不是一个有效的JSON文件，请检查文件内容是否正确。{e}")
            return None

    @staticmethod
    def save_to_json(file_path, data):
        try:
            import json
            with open(file_path, 'w') as file:
                portalocker.lock(file, portalocker.LOCK_EX)  # 加锁
                json.dump(data, file, indent=4)
                portalocker.unlock(file)  # 解锁
                logger.info(f"数据已成功保存到 {file_path} 文件中。")
        except Exception as e:
            logger.info(f"保存数据到 {file_path} 文件时出错：{e}")


if __name__ == '__main__':
    # accounts = QGFile.read_json("aa.json")
    # logger.info(accounts)
    # QGFile.save_to_excel("aa.xlsx", accounts,is_sort=True)
    # excel转yaml
    # QGFile.excel_to_file("aa.xlsx", "aa.csv", is_sort=True)
    QGFile.delete_lines_in_txt("aa.txt", "fas21")
