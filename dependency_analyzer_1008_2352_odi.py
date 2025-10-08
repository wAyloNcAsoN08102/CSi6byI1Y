# 代码生成时间: 2025-10-08 23:52:50
import sanic
from sanic.response import json
# 改进用户体验

# 定义依赖关系分析器类
# 增强安全性
class DependencyAnalyzer:
    def __init__(self):
# 改进用户体验
        # 初始化依赖关系数据结构
        self.dependency_graph = {}

    def add_dependency(self, package_name, dependencies):
        '''
        添加一个包及其依赖到图中
        :param package_name: 包名
        :param dependencies: 依赖列表
# NOTE: 重要实现细节
        '''
        if package_name not in self.dependency_graph:
            self.dependency_graph[package_name] = []
        self.dependency_graph[package_name].extend(dependencies)

    def get_dependencies(self, package_name):
        '''
        获取包的依赖列表
# NOTE: 重要实现细节
        :param package_name: 包名
        :return: 依赖列表
        '''
# TODO: 优化性能
        if package_name in self.dependency_graph:
            return self.dependency_graph[package_name]
        else:
            return []

    def get_transitive_dependencies(self, package_name):
        '''
        递归获取包的传递依赖
        :param package_name: 包名
        :return: 传递依赖列表
# 添加错误处理
        '''
        visited = set()
        return self._get_transitive_dependencies_helper(package_name, visited)
# 扩展功能模块

    def _get_transitive_dependencies_helper(self, package_name, visited):
        '''
        递归获取传递依赖的辅助函数
        :param package_name: 包名
# 扩展功能模块
        :param visited: 已访问的包集合
        :return: 传递依赖列表
        '''
        if package_name in visited:
            return []
        visited.add(package_name)
        dependencies = []
        if package_name in self.dependency_graph:
            dependencies.extend(self.dependency_graph[package_name])
            for dependency in self.dependency_graph[package_name]:
                dependencies.extend(self._get_transitive_dependencies_helper(dependency, visited))
        return dependencies

# 创建Sanic应用
app = sanic.Sanic('DependencyAnalyzerApp')
# 增强安全性

# 依赖关系分析器实例
analyzer = DependencyAnalyzer()

# 添加依赖
# 改进用户体验
analyzer.add_dependency('A', ['B', 'C'])
analyzer.add_dependency('B', ['D'])
analyzer.add_dependency('C', ['D', 'E'])
analyzer.add_dependency('D', ['F'])
analyzer.add_dependency('E', ['F'])

# 获取包的依赖
@app.route('/api/dependencies/<package_name>', methods=['GET'])
async def get_dependencies(request, package_name):
    try:
        dependencies = analyzer.get_dependencies(package_name)
        return json({'package_name': package_name, 'dependencies': dependencies})
    except Exception as e:
        return json({'error': str(e)}, status=500)

# 获取包的传递依赖
@app.route('/api/transitive_dependencies/<package_name>', methods=['GET'])
async def get_transitive_dependencies(request, package_name):
    try:
        transitive_dependencies = analyzer.get_transitive_dependencies(package_name)
        return json({'package_name': package_name, 'transitive_dependencies': transitive_dependencies})
    except Exception as e:
        return json({'error': str(e)}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)