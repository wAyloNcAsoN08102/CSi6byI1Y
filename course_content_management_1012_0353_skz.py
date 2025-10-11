# 代码生成时间: 2025-10-12 03:53:25
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, BadRequest
from sanic.request import Request
from sanic.response import HTTPResponse

# 数据库模拟（在实际应用中，应替换为真实的数据库操作）
class Database:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)
        return course

    def get_course(self, course_id):
        for course in self.courses:
            if course['id'] == course_id:
                return course
        raise NotFound('Course not found')

    def update_course(self, course_id, course):
        for i, existing_course in enumerate(self.courses):
            if existing_course['id'] == course_id:
                self.courses[i] = course
                return course
        raise NotFound('Course not found')

    def delete_course(self, course_id):
        for i, course in enumerate(self.courses):
            if course['id'] == course_id:
                del self.courses[i]
                return True
        raise NotFound('Course not found')

# 课程内容管理应用
app = Sanic("Course Content Management")

# 初始化数据库
db = Database()

# 添加课程内容
@app.route("/add_course", methods=["POST"])
async def add_course(request: Request):
    data = request.json
    try:
        course = db.add_course(data)
        return response.json(course)
    except Exception as e:
        raise ServerError("Failed to add course", status_code=500)

# 获取课程内容
@app.route("/get_course/<course_id:int>", methods=["GET"])
async def get_course(request: Request, course_id: int):
    try:
        course = db.get_course(course_id)
        return response.json(course)
    except NotFound as e:
        return response.json({'error': str(e)}, status=404)

# 更新课程内容
@app.route("/update_course/<course_id:int>", methods=["PUT"])
async def update_course(request: Request, course_id: int):
    data = request.json
    try:
        course = db.update_course(course_id, data)
        return response.json(course)
    except NotFound as e:
        return response.json({'error': str(e)}, status=404)

# 删除课程内容
@app.route("/delete_course/<course_id:int>", methods=["DELETE"])
async def delete_course(request: Request, course_id: int):
    try:
        success = db.delete_course(course_id)
        if success:
            return response.json({'message': 'Course deleted successfully'})
    except NotFound as e:
        return response.json({'error': str(e)}, status=404)

# 自定义异常处理
@app.exception(NotFound)
async def not_found(request: Request, exception: NotFound):
    return response.json({'error': str(exception)}, status=404)

# 启动Sanic服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

# 自定义异常类
class NotFound(Exception):
    pass