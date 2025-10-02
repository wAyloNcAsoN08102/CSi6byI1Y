# 代码生成时间: 2025-10-03 03:23:26
import sanic
from sanic.response import json
from sanic.exceptions import ServerError, NotFound, abort

# 定义一个用于存储电子病历的类
class ElectronicHealthRecord:
    def __init__(self, patient_id, patient_name, records):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.records = records  # 病历记录列表

# 定义一个管理电子病历的类
class HealthRecordService:
    def __init__(self):
        self.records = {}  # 存储所有电子病历

    def add_record(self, patient_id, patient_name, record):
        """添加一个病历记录"""
        if patient_id in self.records:
            self.records[patient_id].append(record)
        else:
            self.records[patient_id] = [record]

    def get_record(self, patient_id):
        """获取一个患者的所有病历记录"""
        return self.records.get(patient_id, [])

    def update_record(self, patient_id, record_index, new_record):
        """更新特定患者的病历记录"""
        if patient_id in self.records and record_index < len(self.records[patient_id]):
            self.records[patient_id][record_index] = new_record
        else:
            raise NotFound('Record not found')

    def delete_record(self, patient_id, record_index):
        """删除特定患者的病历记录"""
        if patient_id in self.records and record_index < len(self.records[patient_id]):
            del self.records[patient_id][record_index]
        else:
            raise NotFound('Record not found')

# 创建Sanic应用
app = sanic.Sanic('Electronic Health Record System')

# 实例化病历服务
health_record_service = HealthRecordService()

# 添加病历记录的路由
@app.route('/records/<patient_id:int>', methods=['POST'])
async def add_record(request, patient_id):
    try:
        record = request.json
        health_record_service.add_record(patient_id, request.json['patient_name'], record)
        return json({'message': 'Record added successfully'})
    except Exception as e:
        raise ServerError('Failed to add record', explanation=str(e))

# 获取病历记录的路由
@app.route('/records/<patient_id:int>', methods=['GET'])
async def get_records(request, patient_id):
    try:
        records = health_record_service.get_record(patient_id)
        if not records:
            raise NotFound('No records found for patient')
        return json({'records': records})
    except Exception as e:
        raise ServerError('Failed to retrieve records', explanation=str(e))

# 更新病历记录的路由
@app.route('/records/<patient_id:int>/<record_index:int>', methods=['PUT'])
async def update_record(request, patient_id, record_index):
    try:
        new_record = request.json
        health_record_service.update_record(patient_id, record_index, new_record)
        return json({'message': 'Record updated successfully'})
    except Exception as e:
        raise ServerError('Failed to update record', explanation=str(e))

# 删除病历记录的路由
@app.route('/records/<patient_id:int>/<record_index:int>', methods=['DELETE'])
async def delete_record(request, patient_id, record_index):
    try:
        health_record_service.delete_record(patient_id, record_index)
        return json({'message': 'Record deleted successfully'})
    except Exception as e:
        raise ServerError('Failed to delete record', explanation=str(e))

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)