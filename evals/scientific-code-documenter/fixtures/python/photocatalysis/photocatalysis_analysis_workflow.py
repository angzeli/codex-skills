import json
import numpy as np
from pathlib import Path


def analyse(a, b, c, d, out=None):

    x = []
    y = []

    for i in range(len(a)):

        if a[i] > 0:

            if b[i] > 0:

                z = -np.log10(
                    b[i] /
                    (c[i] + 1e-12)
                )

                if abs(z) < 0.015:
                    z = 0

                x.append(
                    a[i] * 1e-9
                )

                y.append(z)


    q = np.array(y)

    if len(q) > 10:

        m = np.mean(q[:10])

        q = q - m


    if d == "h2o2":

        q = q * 0.85

    elif d == "co2":

        q = q * 1.15


    result = {
        "time": x,
        "value": q.tolist(),
        "average": float(
            np.mean(q)
        ),
        "maximum": float(
            np.max(q)
        )
    }


    if out:

        Path(out).write_text(
            json.dumps(result)
        )


    return result