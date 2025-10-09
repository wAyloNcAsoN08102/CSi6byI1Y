# 代码生成时间: 2025-10-10 02:53:21
import sanic
from sanic.response import json
from sanic.exceptions import ServerError, NotFound, abort

# 创建Sanic应用
app = sanic.Sanic(__name__)

# 定义一个简单的薪资计算器类
class SalaryCalculator:
    """薪资计算器类，用于计算员工的薪资。"""

    def __init__(self, base_salary):
        """初始化方法，设置员工的底薪。"""
        self.base_salary = base_salary

    def calculate(self, hours_worked, overtime_rate):
        """计算员工的总薪资。
        
        Args:
            hours_worked (int): 员工工作的小时数。
            overtime_rate (float): 加班费率。
        
        Returns:
            float: 员工的总薪资。
        """
        if hours_worked <= 40:
            return self.base_salary
        else:
            overtime_hours = hours_worked - 40
            overtime_pay = overtime_hours * overtime_rate
            return self.base_salary + overtime_pay

# 定义API端点，用于接收薪资计算请求
@app.route('/calculate_salary', methods=['POST'])
async def calculate_salary(request):
    """处理薪资计算请求。"""
    
    # 解析请求体
    try:
        data = request.json
        base_salary = data.get('base_salary')
        hours_worked = data.get('hours_worked')
        overtime_rate = data.get('overtime_rate')
        
        # 验证输入数据
        if not all([base_salary, hours_worked, overtime_rate]):
            abort(400, 'Missing required fields')
        
        # 创建薪资计算器实例并计算薪资
        calculator = SalaryCalculator(base_salary)
        total_salary = calculator.calculate(hours_worked, overtime_rate)
        
        # 返回计算结果
        return json({'total_salary': total_salary})
    
    except ValueError:
        abort(400, 'Invalid JSON payload')
    except Exception as e:
        raise ServerError('Internal Server Error', status_code=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)