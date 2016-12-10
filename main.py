import brazil28k as br

df = br.read_file()

#df_sp = br.get_data_by_state(df, 'SP')
#sp_map = br.get_map(df_sp)
#sp_map.show()	

df_sudeste = br.get_data_by_region(df, 'Nordeste')
sudeste_map = br.get_map(df_sudeste)
sudeste_map.show()
