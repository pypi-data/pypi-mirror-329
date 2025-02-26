# flake8: noqa
from scriptcontext import sticky as st

from aixd_ara.gh_ui import model_setup
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "ModelSetup")

settings = {
    "model_type": model_type,
    "inputML": features,
    "outputML": targets,
    "latent_dim": latent_dim,
    "hidden_layers": hidden_layers,
    "batch_size": batch_size,
}


# TODO: make default settings a bit more smart
default_settings = {
    "model_type": "CAE",
    "inputML": "design_parameters",
    "outputML": "performance_attributes",
    "latent_dim": 8,
    "hidden_layers": [512, 256, 128, 64],
    "batch_size": 16,
}

for k in default_settings.keys():
    if (k not in settings) or (k in settings and settings[k] == None) or (k in settings and settings[k] == []):
        settings[k] = default_settings[k]
        print(k, default_settings[k])


if set:
    st[cid] = model_setup(session_id(), settings)


if cid in st.keys():
    quick_summary = st[cid]["quick_summary"]["summary"]
    model_dims = st[cid]["model_dims"]["summary"]
    ghenv.Component.Message = st[cid]["msg"]
