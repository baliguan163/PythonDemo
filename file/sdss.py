import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqldb://root:123456@192.168.1.101:3306/test")
Session = sessionmaker(bind=engine)

# sql1 = "INSERT INTO `china_administration` VALUES ('1', '安徽省淮北市市辖区', '340601')"
# sql2 = "INSERT INTO `china_administration` VALUES ('2', '安徽省淮北市市辖区', '340602')"

def eachFile(filepath):
    """ 读取文件夹下面的所有文件 的路径"""
    pathDir = os.listdir(filepath)
    file_path_list = list()
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        file_path_list.append(child)
    return file_path_list


path_files_ = os.path.dirname(os.path.realpath(__file__)) + "\\files\\"
file_path_list = eachFile(path_files_)
print(file_path_list)

# for file_path in file_path_list:
#     with open(file_path, 'r', encoding="utf8") as ch:
#         reader = ch.readlines()
#
#         field_list = list()
#         for line in reader:
#             if line.startswith("DROP"):
#                 db_name = line.replace("`", "").replace(";", " ").split(" ")[4]
#
#             if line.strip().startswith("`"):
#                 ziduan = line.strip().replace("`", " ").split(" ")[1]
#                 if ziduan == "key":
#                     ziduan = db_name + "." + ziduan
#                 field_list.append(ziduan)
#         # print(field_list)
#         field_str = ", ".join(f for f in field_list)
#         field_str = "(" + field_str + ")"
#
#         for line in reader:
#             if line.startswith("DROP"):
#                 db_name = line.replace("`", "").replace(";", " ").split(" ")[4]
#                 sql_del = "delete from " + db_name
#                 session.execute(sql_del)
#
#             if line.startswith("INSERT"):
#                 sql = line.strip().replace(";", "")
#                 s_s_sql = sql.replace("` ", field_str + "` ").replace("`", "")
#                 print(s_s_sql)
#                 session.execute(s_s_sql)
# #
# session.commit()