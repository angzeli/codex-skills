import csv
import json
import math
from pathlib import Path


def run(a,b,c,d,e=None):
    x=[]
    y=[]
    z=[]
    f=[]
    for i in range(len(a)):
        if float(a[i])>=0 and float(b[i])>=0:
            x.append(float(a[i]))
            y.append(float(b[i]))
            z.append(float(c[i]))
            f.append(float(d[i]))

    if len(x)==0: raise ValueError("empty")

    yy=[]
    for i in range(len(y)):
        if z[i]!=0:
            yy.append((y[i]-f[i])/z[i])
        else:
            yy.append(0)

    m=sum(yy)/len(yy)
    q=[]
    for i in range(len(yy)):
        if abs(yy[i]-m)<0.05:q.append(0)
        else:q.append(yy[i]-m)

    r=0
    for i in range(len(x)):
        if x[i]>0:
            r+=q[i]/x[i]

    r=r/len(x)

    k=[]
    for i in range(len(x)):
        try:
            k.append(
                math.log(
                    1+q[i]
                )
            )
        except:
            k.append(0)

    out={
        "time":x,
        "concentration":q,
        "rate":r,
        "fit":k
    }

    if e:
        Path(e).write_text(
            json.dumps(out)
        )

    if e:
        with open(
            str(e)+".csv",
            "w"
        ) as h:
            w=csv.writer(h)
            w.writerow(
                [
                    "t",
                    "value"
                ]
            )
            for i in range(len(x)):
                w.writerow(
                    [
                        x[i],
                        q[i]
                    ]
                )

    return out