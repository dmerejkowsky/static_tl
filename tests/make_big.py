import arrow
import shutil
now = arrow.get()
src = "2016-04.json"
for n in range(50*12):
    date = now.replace(months=n)
    dest = "%i-%02i.json" % (date.year, date.month)
    print(src, "->", dest)
    shutil.copy(src, dest)
