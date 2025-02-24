from pathlib import Path
from typing import Annotated
import fnmatch

import pandas as pd
from geojson import Feature, Point
from fastapi import APIRouter, Request, Query, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.datastructures import URL

from sageodata_db import connect as connect_to_sageodata
from sageodata_db import load_predefined_query
from sageodata_db.utils import parse_query_metadata

import dew_gwdata as gd
from dew_gwdata.sageodata_datamart import get_sageodata_datamart_connection

from dew_gwdata.webapp import utils as webapp_utils
from dew_gwdata.webapp.models import queries


router = APIRouter(prefix="/app", include_in_schema=False)

templates_path = Path(__file__).parent.parent / "templates"

templates = Jinja2Templates(directory=templates_path)


@router.get("/geophys_logs_summary")
def geophys_logs_summary(
    request: Request,
    query: Annotated[queries.GeophysLogJobs, Depends()],
):
    db = connect_to_sageodata(service_name=query.env)
    df, title, query_params = query.find_jobs()

    df = df.sort_values(query.sort, ascending=query.order == "ascending")

    title_series = df.apply(
        lambda well: (
            f'<nobr><a href="/app/well_summary?dh_no={well.dh_no}&env={query.env}">'
            f'{webapp_utils.make_dh_title(well, elements=("unit_no", "obs_no"))}</a></nobr>'
        ),
        axis=1,
    )
    df.insert(0, "title", title_series)
    df = df.drop(["well_id", "unit_hyphen", "obs_no"], axis=1)
    df.insert(4, "suburb", gd.locate_wells_in_suburbs(df))

    df = df.drop(
        [
            "log_hdr_no",
            "log_easting",
            "log_northing",
            "log_zone",
            "log_latitude",
            "log_longitude",
            "unit_long",
            "easting",
            "northing",
            "zone",
            "latitude",
            "longitude",
        ],
        axis=1,
    )

    table = webapp_utils.frame_to_html(df)

    return templates.TemplateResponse(
        "geophys_logs_summary.html",
        {
            "request": request,
            "env": query.env,
            "redirect_to": "group_summary",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_summary",
            "query": query,
            "df": df,
            "table": table,
        },
    )

