import os
from core.database import r, db_session
from core.models import Postcode
from io import BytesIO
from zipfile import ZipFile
import pandas
import requests

POSTCODES_URL = "https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip"


def get_postcodes():
    """Downloads postcodes from URL and parses it
    :returns: dataframe
    """
    if r.get("POSTCODES_RETRIVAL_LOCK") == 1:
        return "LOCKED"

    r.set("POSTCODES_RETRIVAL_LOCK", 1)
    content = requests.get(POSTCODES_URL)
    zf = ZipFile(BytesIO(content.content))
    for item in zf.namelist():
        print("file in zip: " + item)

    match = [s for s in zf.namelist() if ".csv" in s][0]
    df = pandas.read_csv(zf.open(match), low_memory=False)
    for i in df.itertuples():
        p = Postcode(i.postcode, i.latitude, i.longitude)
        db_session.add(p)
        print(p)
    d = db_session.commit()
    r.delete("POSTCODES_RETRIVAL_LOCK")
    return df
