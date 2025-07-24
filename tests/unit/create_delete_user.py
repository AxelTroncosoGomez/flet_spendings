import os
import sys
import uuid
import time
import flet as ft
from icecream import ic
from faker import Faker
from pathlib import Path
from dotenv import load_dotenv
from gotrue.errors import AuthApiError
from supabase import create_client, Client
from postgrest.exceptions import APIError
from supabase._sync.client import SupabaseException

print(f'ENV folder: {os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))}')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.utils.logger import logger

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)
print(f".env file {env_path}")

fake = Faker()
Faker.seed(44)

# email = fake.email()
# password = fake.password()
email = "troncoso.axel.dev@gmail.com"
password = "12345678"

print(f"Email: {email}")
print(f"Password: {password}")

supabase_table_name = "spendings"
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = "sb_secret_hsvsjvEq2qZzins-K95Sww_wUwKK3Id"

try:
	supabase_admin: Client = create_client(
		SUPABASE_URL, 
		"SUPABASE_ANON_KEY"
	)
except SupabaseException as e:
	if "Invalid URL" in repr(e):
		logger.debug("Invalid Supabase URL")
	else:
		raise


# Creating a user ...
# try:
# 	register_response = supabase_admin.auth.admin.create_user({
# 		"email": email,
# 		"password": password,
# 		"user_metadata": {
# 			"name": "groverius"
# 		},
# 		"email_confirm": True
# 	})
# 	register_user_id = register_response.user.id
# 	logger.debug(f"User Created ID: {register_user_id}")
# except AuthApiError as e:
# 	if "A user with this email address has already been registered" in repr(e):
# 		logger.error("User already exists, skipping ...")
# 	elif "Invalid login credentials" in repr(e):
# 		logger.error("User does not exits, try register first ...")
# 	elif "User not allowed" in repr(e):
# 		logger.error("Supabase client not allow to cast this expression!")
# 	elif "Invalid API key" in repr(e):
# 		logger.error("Invalid API Key, you dont have the permissions to cast this expression!")
# 	elif "Email not confirmed" in repr(e):
# 		logger.error("User email not confirmed")		
# 	else:
# 		raise

# Log-in a user in admin mode ...
# try:
# 	login_response = (
# 		supabase_admin
# 		.auth
# 		.sign_in_with_password({
# 			"email": email, 
# 			"password": password,
# 		})
# 	)
# 	logger.debug("Log-in sucessfull ...")
# 	user_id = login_response.user.id
# 	ic(user_id)
# 	ic(login_response.user.user_metadata)
# 	# ic(login_response.user.identities[0].identity_data)
# 	# ic(login_response)
# 	ic(login_response.session.access_token)
# except AuthApiError as e:
# 	if "A user with this email address has already been registered" in repr(e):
# 		logger.error("User already exists, skipping ...")
# 	elif "Invalid login credentials" in repr(e):
# 		logger.error("User does not exits, try register first ...")
# 	elif "User not allowed" in repr(e):
# 		logger.error("Supabase client not allow to cast this expression!")
# 	elif "Invalid API key" in repr(e):
# 		logger.error("Invalid API Key, you dont have the permissions to cast this expression!")
# 	elif "Email not confirmed" in repr(e):
# 		logger.error("User email not confirmed")		
# 	else:
# 		raise

# Log-in a user in user mode ...
try:
	login_response = (
		supabase_admin
		.auth
		.sign_in_with_password({
			"email": email, 
			"password": password,
		})
	)
	logger.debug("Log-in sucessfull ...")
	user_id = login_response.user.id
	ic(user_id)
	ic(login_response.user.user_metadata)
	ic(login_response.session.access_token)
except AuthApiError as e:
	if "A user with this email address has already been registered" in repr(e):
		logger.error("User already exists, skipping ...")
	elif "Invalid login credentials" in repr(e):
		logger.error("User does not exits, try register first ...")
	elif "User not allowed" in repr(e):
		logger.error("Supabase client not allow to cast this expression!")
	elif "Invalid API key" in repr(e):
		logger.error("Invalid API Key, you dont have the permissions to cast this expression!")
	elif "Email not confirmed" in repr(e):
		logger.error("User email not confirmed")		
	else:
		raise

#######   FETCH ALL DATA ENTRIES WITHIN A USER LOGGED SUCESSFULLY (CHECKED)  ##########
"""
Si el usuario o el programa en general intenta capturar todas las entries del usuario
actual que ya inicio sesion, el response en este caso corresponde a un
<class 'postgrest.base_request_builder.APIResponse[~_ReturnT]'> que contiene dentro
data (List[Dict]): contiene una lista de los entries encontrados, en este caso con formato json
count (): Por ahora solo se conoce que siempre es None

Para acceder a cada uno de estos items, no es necesario agregar una condicion dentro de la
query de supabase que diga `.eq("user_id", user_id)`, dado que al parecer ya se encuentra
implicito debido a que el usuario a inicio sesion y sus credenciales se encuentran dentro de la
session de supabase. Por otra parte la base de datos "spendings" contiene dentro RLS Policies
que indican estrictamente que solo se pueden leer (SELECT) desde el ID del usuario actual.

Los items son una lista de diccionarios, y se pueden acceder a ellos como se muestra a
continuacion

logger.debug(f"Fetching all data for user: {user_id}")
rows = (
	supabase_admin
	.table(supabase_table_name)
	.select("*")
	.eq("user_id", user_id) # This line can be skipped
	.execute()
)
for item in rows.data:
	logger.debug(f"Data: {item}")
"""


#######   UPDATE AN ENTRY WITHIN A USER BASED ON ITEM ID (CHECKED)   ##########
"""
Si el usuario o el programa en general intenta actualizar un item, donde el
item_id no corresponde al usuario correcto (user_id), entonces no se produce
ninguna actualizacion del entry dentro del database. Por otra parte, tanto
como user como admin, dependiente del supabase cliente, se pueden hacer
estas actualizaciones. El template de abajo funciona sin problemas.

response en este caso corresponde a <class 'postgrest.base_request_builder.APIResponse[~_ReturnT]'>
que tiene dos llaves dentro
data (List[Dict]): contiene una lista de los entry modificados, en este caso con formato json
count (): Por ahora solo se conoce que siempre es None


fixed_item_id = "7e6f1030-cb15-4994-8978-acd103772198"
logger.debug(f"Updating a value inside user: {user_id} for an item with ID {fixed_item_id}")
updated_item = {
	# "user_id": self.user_id,
	"date": "22-07-2025",
	"store": "Lider",
	"product": "Zapatillas",
	"amount": 1,
	"price": 23000
}
response = (
	supabase_admin
	.table(supabase_table_name)
	.update(updated_item)
	.eq("item_id", fixed_item_id)
	.execute()
)
logger.debug(response)
"""

#######   INSERT AN ENTRY WITHIN A USER (CHECKED)   ##########
"""
Tanto el cliente de supabase anon como private service puede realizar la insersion de un entry en
un "spendings". Se debe ingresar un item en formato json, donde se indiquen los valores en el
entry que se quiere agregar. Por otra parte, no se a verificado que se pueda ingresar un entry dentro
de otro user ID. Se muestra un ejemplo de como ingresar un valor, luego de iniciar sesion:

"""
# logger.debug(f"Inserting a new value inside user: {user_id}")
# time.sleep(3)
# try:
# 	new_item = {
# 		"item_id": str(uuid.uuid4()),
# 		"user_id": user_id,
# 		"date": "21-07-2025",
# 		"store": fake.company(),
# 		"product": fake.word(),
# 		"amount": 100,
# 		"price": 34000.0
# 	}
# 	ic(new_item)
# 	response = (
# 		supabase_admin
# 		.table(supabase_table_name)
# 		.insert(new_item)
# 		.execute()
# 	)
# 	logger.debug(response)
# except APIError as err:
# 	# This error comes from adding a new row violating the RLS policy, code 42501
# 	if err.message == 'new row violates row-level security policy for table "spendings"':
# 		logger.error(f"Error code {err.code}: You dont have the permissions to add this entry into \"spendings\"")
# 	# This error comes from a duplicated unique key value from a given column, code 23505
# 	elif err.message == "duplicate key value violates unique constraint \"spendings_pkey\"":
# 		logger.error(f"Error code {err.code}: Duplicate key violates schema from \"spendings\"")
# 	# This error comes from set an empty value for a NOT NULL column, code 23502
# 	elif err.message == "null value in column \"amount\" of relation \"spendings\" violates not-null constraint":
# 		logger.error(f"Error code {err.code}: Empty \"spendings\"")
# 	else:
# 		raise
# except Exception as err:
# 	raise


time.sleep(5)
# Log-out a user in admin mode...
try:
	logout_response = (
		supabase_admin
		.auth
		.sign_out()
	)
	logger.debug("Log-out sucessfull ...")
except Exception as err:
	logger.error(f"Smh went wrong on login ...")
	logger.error(repr(err))

# Deleting a user in admin mode ...
# try:
# 	deliting_response = supabase_admin.auth.admin.delete_user(
# 		user_id
# 	)
# 	logger.debug("User deleted sucessfully")
# except AuthApiError as e:
# 	if "A user with this email address has already been registered" in repr(e):
# 		logger.error("User already exists, skipping ...")
# 	elif "Invalid login credentials" in repr(e):
# 		logger.error("User does not exits, try register first ...")
# 	elif "User not allowed" in repr(e):
# 		logger.error("Supabase client not allow to cast this expression!")
# 	elif "Invalid API key" in repr(e):
# 		logger.error("Invalid API Key, you dont have the permissions to cast this expression!")
# 	elif "Email not confirmed" in repr(e):
# 		logger.error("User email not confirmed")		
# 	else:
# 		raise
