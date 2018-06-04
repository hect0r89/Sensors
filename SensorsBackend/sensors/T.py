import datetime
import random

import pandas as pd

if __name__ == '__main__':
    signals = {"temperatura" : (-10.0, 48.0), "humedad": (0.0,100.0), "presion_atmosferica" : (750.0,1200.0), "volumen_lluvias": (0.0, 100.0)}
    # date_list = [datetime.datetime.strptime("2016-04-01", ("%Y-%m-%d")) - datetime.timedelta(days=x) for x in range(0, numdays)]
    datelist = pd.date_range(pd.datetime.strptime("2016-04-01", "%Y-%m-%d"), periods=30).tolist()
    sensors = {"sensor1": "20022014", "sensor2" : "16052016", "sensor3": "01012015"}
    for k_sensor, v_sensor in sensors.items():
        df_total = pd.DataFrame()
        for k,v in signals.items():
            date = pd.datetime.strptime("2016-04-01", "%Y-%m-%d")
            lis = []
            for i in range(960):
                lis.append({"id": k,  "time" : date.timestamp(), "value" : random.uniform(signals[k][0], signals[k][1])})
                date = date + datetime.timedelta(minutes=45)
            df_total = df_total.append(pd.DataFrame(lis))
        df_total.to_csv("{}-{}.csv".format(k_sensor, sensors[k_sensor]).format(), sep=",", decimal=".", index=False, header=None)
        print()
