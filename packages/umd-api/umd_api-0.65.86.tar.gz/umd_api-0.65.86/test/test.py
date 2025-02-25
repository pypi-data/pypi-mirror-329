from umd_api.weather import Weather

weather = Weather()

weather.download_data(['vmh', 'atlantic'], 'csv', "saved_files", data=['dateTime', 'outTemp'], start_time="2/1/25")
weather.download_data(['chem'], 'xlsx', "saved_files", data=['dateTime', 'outTemp'], start_time="2/1/25")