from setup import SupabaseClient
from pydantic import BaseModel


class Country(BaseModel):
    name: str


class CountryQueries:
    def __init__(self, supabase_client: SupabaseClient):
        self.supabase_client = supabase_client

    def get_countries(self, order_by_column: str = 'id'):
        try:
            response = self.supabase_client.client.table('countries').select("*").order(order_by_column).execute()
            return {"data": response, "error": None}
        except Exception as e:
            return {"data": None, "error": e}

    def get_country(self, cid: int):
        try:
            data, count = self.supabase_client.client.table('countries').select('*').eq('id', cid).execute()
            return {"data": data, "error": None}
        except Exception as e:
            return {"data": None, "error": e}

    def add_country(self, country: Country):
        try:
            last_country = (self.supabase_client.client.table('countries').
                            select('id').
                            order('id', desc=True).
                            limit(1).
                            execute())
            last_id = last_country.data[0]['id'] + 1 if last_country.data else 1

            data, count = self.supabase_client.client.table('countries').insert([{
                "id": last_id,
                "name": country.name.capitalize()
            }]).execute()

            return {"data": data, "error": None}
        except Exception as e:
            return {"data": None, "error": e}

    def update_country(self, country: Country, cid: int):
        try:
            data, count = (self.supabase_client.client.table('countries').
                           update({'name': country.name.capitalize()}).
                           eq('id', cid).
                           execute())
            return {"data": data, "error": None}
        except Exception as e:
            return {"data": None, "error": e}

    def delete_country(self, cid: int):
        try:
            data, count = self.supabase_client.client.table('countries').delete().eq('id', cid).execute()
            return {"data": data, "error": None}
        except Exception as e:
            return {"data": None, "error": e}
