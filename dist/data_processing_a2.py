

#%%
import pandas as pd 
import geopandas as gpd

employment_df = pd.read_csv('geo_data_cleaned.csv')
geojson_data = gpd.read_file('us-states.json')

# %%
#geo_df = gpd.GeoDataFrame.from_features(geojson_data['Feature'])
geo_df = geo_df.rename(columns={'name':'Area Name'})

# %%
merged_gdf = geo_df.merge(employment_df, on = 'Area Name', how = 'left')

#%%
output_geojson_file = 'merged_us_ds_employment.geojson'
merged_gdf.to_file(output_geojson_file, driver='GeoJSON')




# %%
