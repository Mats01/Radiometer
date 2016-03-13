import os
import csv
#import winsound
import numpy as np
import time
import datetime
from subprocess import call
import shutil


def analyze():
    start = time.time()

    average_array = np.array([])
    stan_dev_array = np.array([])
    minimum_array = np.array([])
    maximum_array = np.array([])
    f_average_array = np.array([])
    f_stan_dev_array = np.array([])
    f_minimum_array = np.array([])
    f_maximum_array = np.array([])
    file_name_array = np.array([])


    #folder = '6.-7.3.2016'
    result_file = '%s-characteristics.csv' % str(datetime.datetime.now().date())
    
    for file_name in os.listdir('/home/pi/Documents/radiometer'):
        data = []
        if file_name.endswith(".csv"):
            print file_name
            f = open('/home/pi/Documents/radiometer/' + file_name, 'rt')
            try:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
            finally:
                f.close()

            values = []
            if data:
                for i in data:
                    values.append(float(i[1]))

                averages = []
                for i in range(0, len(values) - 10):
                    temp = [int(values[i]), int(values[i + 1]), int(values[i + 2]), int(values[i + 3]), int(values[i + 4]),
                            int(values[i + 5]), int(values[i + 6]), int(values[i + 7]), int(values[i + 8]), int(values[i + 9])]
                    avg = reduce(lambda x, y: x + y, temp) / len(temp)
                    averages.append(avg)

                file_name_array = np.append(file_name_array, ['.'.join(file_name.split('.')[:-1])])
                average_array = np.append(average_array, [str(reduce(lambda x, y: x + y, values) / len(values)).replace('.',',')])
                stan_dev_array = np.append(stan_dev_array, [str(np.std(values)).replace('.',',')])
                minimum_array = np.append(minimum_array, [str(min(values)).replace('.',',')])
                maximum_array = np.append(maximum_array, [str(max(values)).replace('.',',')])
                f_average_array = np.append(f_average_array, [str(reduce(lambda x, y: x + y, averages) / len(averages)).replace('.',',')])
                f_stan_dev_array = np.append(f_stan_dev_array, [str(np.std(averages)).replace('.',',')])
                f_minimum_array = np.append(f_minimum_array, [str(min(averages)).replace('.',',')])
                f_maximum_array = np.append(f_maximum_array, [str(max(averages)).replace('.',',')])

    output = np.column_stack((average_array.flatten(), stan_dev_array.flatten(), minimum_array.flatten(), maximum_array.flatten(),
                                 f_average_array.flatten(), f_stan_dev_array.flatten(), f_minimum_array.flatten(), f_maximum_array.flatten(),
                                 file_name_array.flatten()))
    np.savetxt(result_file.replace(':', '.'), output, fmt=['%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'], delimiter='-')

    result_file = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Documents/radiometer/%s-characteristics.csv %s-characteristics.csv" % (str(datetime.datetime.now().date()), str(datetime.datetime.now().date()))
    call([result_file], shell=True)
    time.sleep(10)
    shutil.move("/home/pi/Documents/radiometer/%s-characteristics.csv" % str(datetime.datetime.now().date()),
                        "/home/pi/Documents/radiometer/characteristics-folder/")
    print time.time() - start

# signals the script has finished analyzing the night
#winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
#winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
