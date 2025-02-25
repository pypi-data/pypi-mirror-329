import certifi
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from base_utils.exception import ImproperConfigurationError
import asyncio
# from config import host, username, password, prod, db_name


client: AsyncIOMotorClient | None = None
db_name = None

async def init(test: bool, db_setup_data: dict, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()) -> None:
	global client
	global db_name

	conn_params = {
		'host': db_setup_data.get('host'),
		'username': db_setup_data.get('username'),
		'password': db_setup_data.get('password'),
	}
	prod = db_setup_data.get('prod')
	db_name = db_setup_data.get('db_name')
	
	if all(conn_params.values()):
		client = AsyncIOMotorClient(
    	host=f"mongodb+srv://{conn_params['host']}/?retryWrites=true&w=majority",
			username=conn_params['username'],
			password=conn_params['password'],
			uuidRepresentation='standard',
			tlsCAFile=certifi.where(),
			io_loop=loop,
		)
  
		print(await client.server_info())
	else:
		raise ImproperConfigurationError('Problem with MongoDB environment variables')

	if prod == 'false' and not test:
		db_name += '_dev'
	elif prod == 'false' and test:
		db_name += '_test'
  
	if db_name is not None:
		await init_beanie(
			database=client[db_name],
	    document_models=db_setup_data.get('document_models'),
      allow_index_dropping = True,
      recreate_views=True
    )
		return client, db_name
	else:
		raise ImproperConfigurationError('Problem with MongoDB environment variables')


async def close():
  try:
    global client
    client.close()
  except Exception as e:
    raise e
