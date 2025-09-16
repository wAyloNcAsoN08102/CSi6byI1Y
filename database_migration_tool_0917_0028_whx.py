# 代码生成时间: 2025-09-17 00:28:59
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.response import HTTPResponse
from aiopg.sa import create_engine
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from sqlalchemy.exc import SQLAlchemyError

# Define the Sanic app
app = Sanic('DatabaseMigrationTool')

# Database engine configuration
DATABASE_URI = 'postgresql://user:password@localhost:5432/mydatabase'

# Initialize the Alembic configuration
def create_alembic_config():
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', 'migrations')  # Path to the migration scripts
    alembic_cfg.set_main_option('sqlalchemy.url', DATABASE_URI)
    return alembic_cfg

# Helper function to run a database command
async def run_db_command(command_func, *args, **kwargs):
    try:
        loop = asyncio.get_event_loop()
        engine = await create_engine(DATABASE_URI)
        with engine.acquire() as conn:
            await conn.execute(command_func, *args, **kwargs)
    except SQLAlchemyError as e:
        raise ServerError("Database error", e)

# Alembic command to stamp the current revision
@app.route('/migrate/stamp', methods=['POST'])
async def migrate_stamp(request):
    alembic_cfg = create_alembic_config()
    command._stamp(alembic_cfg, 'head')  # Stamp the current revision
    return response.json({'status': 'success', 'message': 'Migration stamped successfully'})

# Alembic command to run migrations
@app.route('/migrate/upgrade', methods=['POST'])
async def migrate_upgrade(request):
    alembic_cfg = create_alembic_config()
    command.upgrade(alembic_cfg, 'head')  # Upgrade to the latest revision
    return response.json({'status': 'success', 'message': 'Migration upgraded successfully'})

# Alembic command to run down migrations
@app.route('/migrate/downgrade', methods=['POST'])
async def migrate_downgrade(request):
    alembic_cfg = create_alembic_config()
    command.downgrade(alembic_cfg, '-1')  # Downgrade to the previous revision
    return response.json({'status': 'success', 'message': 'Migration downgraded successfully'})

# Error handler for ServerError
@app.exception(ServerError)
async def server_error(request, exception):
    return HTTPResponse(body=str(exception), status=500)

# Start the Sanic app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
