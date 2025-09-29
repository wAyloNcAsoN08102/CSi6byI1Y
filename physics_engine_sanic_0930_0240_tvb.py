# 代码生成时间: 2025-09-30 02:40:23
import math
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request

# 定义一个物理引擎类
class PhysicsEngine:
    def __init__(self):
        # 初始化物理引擎的参数
        self.earth_gravity = 9.81  # 地球重力加速度

    def calculate_trajectory(self, velocity, angle):
        # 计算物体的轨迹
        """
        计算物体在给定速度和角度下的轨迹。

        :param velocity: 物体的初始速度
        :param angle: 物体发射的角度（以度为单位）
        :return: 飞行时间，最大高度和射程
        """
        try:
            # 将角度转换为弧度
            angle_rad = math.radians(angle)
            # 计算飞行时间
            time_of_flight = (2 * velocity * math.sin(angle_rad)) / self.earth_gravity
            # 计算最大高度
            max_height = (velocity ** 2 * math.sin(angle_rad) ** 2) / (2 * self.earth_gravity)
            # 计算射程
            range_ = (velocity ** 2 * math.sin(2 * angle_rad)) / self.earth_gravity
            return time_of_flight, max_height, range_
        except Exception as e:
            # 处理错误
            raise ServerError("Error calculating trajectory: " + str(e))

# 创建Sanic应用
app = Sanic("PhysicsEngineApp")

# 创建物理引擎实例
physics_engine = PhysicsEngine()

@app.route("/trajectory", methods=["GET"])
async def calculate_trajectory(request: Request):
    # 从请求中获取速度和角度
    velocity = request.args.get("velocity", type=float, default=0)
    angle = request.args.get("angle", type=float, default=0)

    # 如果速度或角度无效，则返回错误
    if velocity <= 0 or angle <= 0 or angle > 90:
        return response.json({"error": "Invalid velocity or angle."}, status=400)

    # 调用物理引擎计算轨迹
    time_of_flight, max_height, range_ = physics_engine.calculate_trajectory(velocity, angle)

    # 返回计算结果
    return response.json({"time_of_flight": time_of_flight, "max_height": max_height, "range": range_})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)