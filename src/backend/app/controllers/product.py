from flask import current_app, jsonify, Response, request
from flask_restful import Resource
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import select, union_all, literal_column

from app.models.product import Product
from app.models.chat import Chat, CreatedBy
from app.models.user import User

from app.middlewares.auth import Auth

from app.utils.common import map_row

from app.db import db
from seeds import products

# 跟职业相关的功能，用于处理职业信息
auth = Auth()


# 将数据库记录映射为字典形式，把career_path的对象属性映射为字典的键值对，然后从JSON格式返回
# def map_career_path(career_path):
#     return map_row(career_path) | {
#         'source': map_row(career_path.source),
#         'target': map_row(career_path.target)
#     }
def map_product(product):
    return map_row(product) | {
        "source": map_row(product.source),
        "target": map_row(product.target),
    }


# 将职业相关的教育项目信息映射为字典形式
# def map_programs(cip_occupations):
#     programs_dict = {}
#     programs = []
#     if cip_occupations:
#         for cip_occupation in cip_occupations:
#             for cip_program in cip_occupation.cip.cip_programs:
#                 program = cip_program.program
#                 if str(program.id) not in programs_dict:
#                     programs_dict[str(program.id)] = 1
#                     program_dict = map_row(program)
#                     program_dict['programTrends'] = list(map(
#                         map_row, program.program_trends))
#                     programs.append(program_dict)
#     return programs


# 获取前10个职业记录，返回json_not_this_one
class ProductsApi(Resource):
    @auth.middleware
    def get(token_data, self):
        products = db.session.query(Product).first(10)
        products_dict = map(map_row, products)
        return jsonify(products_dict)


class ProductApi(Resource):
    @auth.middleware
    def get(token_data, self, id):
        product = db.session.query(Product).filter_by(index=id).first()
        product_dict = map_row(product)
        # product_description = db.session.query(Product).filter_by(index=id).first()

        # SSOC Jobs
        # ssoc_jobs = db.session.query(SsocJob).filter(
        # SsocJob.occupation_id == id).all()
        # ssoc_jobs_dict = list(map(map_row, ssoc_jobs))
        # occupation_dict["ssocJobs"] = ssoc_jobs_dict

        # # Educational Programs
        # programs = map_programs(occupation.cip_occupations)
        # occupation_dict["programs"] = programs
        # print(jsonify(occupation_dict))
        return jsonify(product_dict)
