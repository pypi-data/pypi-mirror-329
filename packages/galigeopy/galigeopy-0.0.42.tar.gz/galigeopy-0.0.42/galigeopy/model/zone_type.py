import pandas as pd
import geopandas as gpd
from sqlalchemy import text

from galigeopy.model.zone import Zone

class ZoneType:
    def __init__(
        self,
        zone_type_id:int,
        name:str,
        description:str,
        org: 'Org' # type: ignore
    ):
        # Infos
        self._zone_type_id = zone_type_id
        self._name = name
        self._description = description
        # Engine
        self._org = org

    def __str__(self):
        return self.name + " (" + str(self.zone_type_id) + ")"
    
    # Getters
    @property
    def zone_type_id(self): return self._zone_type_id
    @property
    def name(self): return self._name
    @property
    def description(self): return self._description
    @property
    def org(self): return self._org

    # Setters
    @name.setter
    def name(self, value): self._name = value
    @description.setter
    def description(self, value): self._description = value
    
    # Public Methods
    def number_of_zones(self):
        query = text(f"SELECT COUNT(*) FROM ggo_zone WHERE zone_type_id = {self.zone_type_id}")
        with self._org.engine.connect() as conn:
            result = conn.execute(query)
            return result.scalar()
        
    def getZonesList(self):
        query = text(f"SELECT * FROM ggo_zone WHERE zone_type_id = {self.zone_type_id}")
        return pd.read_sql(query, self._org.engine)
    
    def getZoneById(self, zone_id:int):
        query = f"SELECT * FROM ggo_zone WHERE zone_id = {zone_id} AND zone_type_id = {self.zone_type_id}"
        df = pd.read_sql(query, self._org.engine)
        if len(df) > 0:
            data = df.iloc[0].to_dict()
            data.update({"org": self._org})
            return Zone(**data) 
        else:
            raise Warning(f"Zone {zone_id} not found in ZoneType {self.name}")
        
    def getAllZones(self):
        query = text(f"SELECT * FROM ggo_zone WHERE zone_type_id = {self.zone_type_id}")
        gdf = gpd.read_postgis(query, self._org.engine, geom_col='geometry')
        zones = []
        for i in range(len(gdf)):
            data = gdf.iloc[i].to_dict()
            data.update({"org": self._org})
            zones.append(Zone(**data))
        return zones
        
    def add_to_model(self)-> int:
        # Add to database
        query = f"""
        INSERT INTO ggo_zone_type (
            name,
            description
        ) VALUES (
            '{self.name.replace("'", "''")}',
            '{self.description.replace("'", "''")}'
        ) RETURNING zone_type_id;
        """
        zone_type_id = self._org.query(query)[0][0]
        return zone_type_id
    
    def update(self) -> 'ZoneType':
        query = f"""
        UPDATE ggo_zone_type
        SET
            name = '{self.name.replace("'", "''")}',
            description = '{self.description.replace("'", "''")}'
        WHERE zone_type_id = {self.zone_type_id}
        """
        self._org.query(query)
        return self._org.getZoneTypeById(self.zone_type_id)
    
    def delete(self)-> bool:
        query = f"DELETE FROM ggo_zone_type WHERE zone_type_id = {self.zone_type_id}"
        self._org.query(query)
        self._zone_type_id = None
        return True

