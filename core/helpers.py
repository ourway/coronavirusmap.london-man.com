#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import models
from core.database import db_session, r
from sqlalchemy import text
import requests
import json

REQ_URL = "https://locator-service.api.bbci.co.uk/locations/{pcode}/details/gss-council?op=intersect&format=json&api_key=GdwOsOqSc8G016hlXFV6GdpGI7aJTD81"
CASE_URL = "https://www.bbc.co.uk/indepthtoolkit/data-sets/coronavirus_lookup/json"


def pcodes_around_latlong(lat: int, longt: int) -> str:
    """ converts location latitude and longitude to a postcode """
    code = (
        db_session.query(models.Postcode)
        .filter(
            text(
                f"( 3959 * acos( cos( radians({lat}) ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians({longt}) ) + sin( radians({lat}) ) * sin( radians( latitude ) ) ) ) < 0.05"
            )
        )
        .first()
    )
    return code.postcode


def pcode_to_geoname(pcode: str) -> str:
    """ converts postcode to geo name from external API """
    cached_data = r.get(f"C-GEONAME-{pcode}")
    geoname = dict()
    if cached_data:
        geoname = json.loads(cached_data)
    else:
        geoname = requests.get(
            REQ_URL.format(pcode=pcode.replace(" ", "").upper())
        ).json()
        r.setex(f"C-GEONAME-{pcode}", 7200, json.dumps(geoname))

    return geoname["response"]["details"][0]["data"]["geographyName"]


def get_case_data(geoname: str) -> list([int, int]):
    """ gets case data from external API 
        
        :returns [cases, population]
    """
    cached_data = r.get("C-CASES")
    casedata = dict()
    if cached_data:
        casedata = json.loads(cached_data)
    else:
        casedata = requests.get(CASE_URL).json()
        r.setex("C-CASES", 3600, json.dumps(casedata))

    for g in casedata:
        _, gname, cases, population = g
        if gname == geoname:
            return [cases, population]


def get_cases_by_latlong(lat: float, longt: float) -> list([int, int]):
    """ get infection cases by lat and long """

    pcode = pcodes_around_latlong(lat, longt)
    gname = pcode_to_geoname(pcode)
    return get_case_data(gname)
