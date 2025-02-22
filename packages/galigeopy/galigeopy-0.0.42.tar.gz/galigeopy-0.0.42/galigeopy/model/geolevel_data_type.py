import pandas as pd
import geopandas as gpd
import json

from sqlalchemy import text

class GeolevelDataType:
    # Constructor
    def __init__(
            self,
            geolevel_data_type:int,
            name:str,
            properties:dict,
            geolevel_id:int,
            description:str,
            org:'Org' # type: ignore
    ):
        self._geoleveldata_type_id = geolevel_data_type
        self._name = name
        self._properties = properties
        self._geolevel_id = geolevel_id
        self._description = description
        self._org = org

    # Getters
    @property
    def geoleveldata_type_id(self): return self._geoleveldata_type_id
    @property
    def name(self): return self._name
    @property
    def properties(self): return self._properties
    @property
    def geolevel_id(self): return self._geolevel_id
    @property
    def description(self): return self._description
    @property
    def org(self): return self._org

    # Public Methods
    def getGeolevel(self):
        return self._org.getGeolevelById(self._geolevel_id)
    
    def getDataset(self)->pd.DataFrame:
        query = text(f"SELECT * FROM ggo_geoleveldata WHERE geoleveldata_type_id = {self._geoleveldata_type_id}")
        return pd.read_sql(query, self._org.engine)
    
    def getGeoDataset(self)->gpd.GeoDataFrame:
        geolevel = self.getGeolevel()
        query = text(f"""
            SELECT
                g.*,
                geo.{geolevel.geom_field} AS geometry
            FROM ggo_geoleveldata g
            JOIN {geolevel.table_name} AS geo ON geo.{geolevel.geounit_code} = g.geounit_code
            WHERE
                geoleveldata_type_id = {self._geoleveldata_type_id}
        """)
        return gpd.read_postgis(query, self._org.engine, geom_col='geometry')
    
    def add_to_model(self) -> 'GeolevelDataType':
        # add to database
        query = f"""
            INSERT INTO ggo_geoleveldata_type (
                name,
                description,
                properties,
                geolevel_id
            ) VALUES (
                '{self._name.replace("'", "''")}',
                '{self._description.replace("'", "''")}',
                '{json.dumps(self._properties).replace("'", "''")}',
                {self._geolevel_id}
            ) RETURNING geoleveldata_type_id
        """
        geolevel_data_type_id = self._org.query(query)[0][0]
        self._geoleveldata_type_id = geolevel_data_type_id
        # return
        return self
