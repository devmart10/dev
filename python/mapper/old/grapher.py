import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# log_files = [f for f in os.listdir('.') if f.startswith('log')]
log_file = 'log_2016-09-12.txt'
output_name = 'image.png'

times = []
durs = []
with open(log_file, 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        t, d = line.split(',')
        t = t.split(' ')[-1]
        d = d.split(' ')[-1].strip()

        time = datetime.strptime(t, '%H:%M:%S')

        # h = d // 3600
        # m = (d - 3600*h) // 60
        # s = d - 3600*h - 60*m

        # duration = timedelta(seconds=int(d))

        times.append(time)
        durs.append(int(d))

fig = plt.figure()

ax = fig.add_subplot(111)
ax.plot(times, durs)

fmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(fmt)
# ax.yaxis.set_major_formatter(fmt)

# fig.autofmt_xdate(bottom=0.2, rotation=90, ha='left')

ax.grid()
plt.savefig(output_name)
