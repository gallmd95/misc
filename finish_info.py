import datetime
import zipfile
import os

now = datetime.datetime.now()
tail = now.strftime("%Y-%m-%d")


def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
            os.remove(absname)
    zf.close()

zip("temp_info","data_info/info_"+tail)
os.rmdir("temp_info")
