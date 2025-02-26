# flake8: noqa
from scriptcontext import sticky as st

from aixd_ara.gh_ui import dataset_summary
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "DatasetSummary")

if get:
    st[cid] = dataset_summary(session_id())

if cid in st.keys():
    if st[cid]["msg"]:
        summary = st[cid]["msg"]  # error
    else:
        summary = st[cid]["summary"]
