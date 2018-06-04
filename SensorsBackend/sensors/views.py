import datetime
import re

import pandas as pd
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sensors.models import SensorConfiguration, Sensor


def calculate_measure(df):
    """
    Calculate the measurements of the sensors based on the configuration
    :param df: Dataframe with data
    :return: Dataframe with new information about the readings
    """
    list_signals = list(df['id_señal'].unique())
    df_final = pd.DataFrame()
    for signal in list_signals:
        measure_type = SensorConfiguration.objects.get(id_signal=signal).signal_type
        df_final = df_final.append(
            df.groupby(['id_sensor', 'id_señal', 'timestamp_lectura']).agg(measure_type).reset_index())
        df_final['acquisition_date'] = df['acquisition_date']
    return df_final


def validate_filename(file):
    """
    Validate the format of the input file
    :param file: Input file
    :return: String with signal id and acquisition date
    """
    res = re.search("(.*)-([\d]{8}).csv", file.name)
    if res:
        try:
            acquisition_date = datetime.datetime.strptime(res.group(2), "%d%m%Y")
        except ValueError as ex:
            raise Exception("Date {} of file {} is not a valid date".format(res.group(2), file.name))
        else:
            return res.group(1), acquisition_date
    else:
        raise Exception("Name of file {} doesn't match the pattern.".format(file.name))


def parse_files(files):
    """
    Read the input files and process the files
    :param files: Input files
    """
    df_all = pd.DataFrame(columns=['id_señal', 'timestamp_lectura', 'valor_lectura', 'acquisition_date', 'id_sensor'])
    for f in files:
        try:
            id_signal, acquisition_date = validate_filename(f)
        except Exception as ex:
            print(ex)
        else:
            df = pd.read_csv(f, sep=',', header=None, names=['id_señal', 'timestamp_lectura', 'valor_lectura'],
                             dtype={2: float})
            df['acquisition_date'] = acquisition_date.date()
            df['id_sensor'] = id_signal
            df_all = df_all.append(df)
    df_all = df_all.sort_values(by=['id_señal', 'acquisition_date']).drop_duplicates(
        subset=['id_señal', 'timestamp_lectura', 'id_sensor'], keep='first').reset_index(drop=True)
    df_all['timestamp_lectura'] = df_all['timestamp_lectura'].apply(
        lambda x: datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d"))
    df_grouped = calculate_measure(df_all)
    df_grouped.apply(
        lambda row: Sensor.objects.update_or_create(id_sensor=row['id_sensor'], signal_type=row['id_señal'],
                                                    reading_date=row['timestamp_lectura'],
                                                    defaults={"acquisition_date": row['acquisition_date'],
                                                              "reading_value": row['valor_lectura']}), axis=1)


@csrf_exempt
def read_csv(request):
    """
    POST method to upload files
    :param request:
    :return: JsonResponse with info about the process
    """
    parse_files(request.FILES.getlist('files'))
    return JsonResponse({"message": "Files loaded correctly."}, status=201)


def get_sensors(request):
    """
    GET method to get senors
    :param request:
    :return: JsonResponse with info about sensors
    """
    sensors = Sensor.objects.values_list('id_sensor', flat=True).distinct()
    return JsonResponse({"sensors": list(sensors)}, status=200)


def get_signals(request, sensor_id):
    """
    GET method to get signals types
    :param request:
    :param sensor_id: Id of sensor
    :return: JsonResponse with info about signals
    """
    signals = Sensor.objects.filter(id_sensor=sensor_id).values_list('signal_type', flat=True).distinct()
    return JsonResponse({"signals": list(signals)}, status=200)


def get_readings(request, sensor_id):
    """
    GET method to get readings
    :param request:
    :param sensor_id: Id of sensor
    :return: JsonResponse with info about readings
    """
    signals = request.GET.getlist('signals')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    response = []
    for signal in signals:
        query_set = list(Sensor.objects.filter(id_sensor=sensor_id, signal_type=signal, reading_date__gt=start_date,
                                               reading_date__lt=end_date).values(name=F('reading_date'),
                                                                                 value=F('reading_value')))
        if query_set:
            response.append({"name": signal, "series": query_set})
    return JsonResponse({"data": response}, status=200)
