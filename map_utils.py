import plotly.express as px
import numpy as np
import math


# TODO increase num of ticks
# TODO fix ticks scale
def gen_choropleth_log(
    log,
    df,
    geo,
    loc,
    featureid,
    color,
    hover_cols,
    title,
    str_format="",
    postfix="",
    hover_name="City",
    scale="viridis",
):
    log_col = f"{color}_log"
    df[log_col] = np.emath.logn(log, df[color].astype("float") + 1)

    hover_cols.update(
        {
            f"{color}_log": (False, None),
        }
    )
    map = gen_choropleth(
        df,
        geo,
        loc,
        featureid,
        log_col,
        hover_cols,
        title,
        hover_name,
        scale=scale,
    )

    # round to the number of digits
    # watch there was an easier way
    min_val = np.min(df[log_col])
    max_val = np.max(df[log_col])
    l_range = max_val - min_val
    tickvals = [(l_range / 6) * n + min_val for n in range(1, 7)]
    ticktext = [math.pow(log, num) for num in tickvals]
    ticktext = [round(num, -len(str(num).split(".")[0]) + 2) for num in ticktext]
    # TODO why does nested work like this
    ticktext = [f"{int(val):{str_format}}{postfix}" for val in ticktext]

    map.update_layout(
        coloraxis_colorbar=dict(
            tickvals=tickvals,
            # ticktext=[
            #    f"{int(np.power(log, num)):{str_format}}{postfix}" for num in tickvals
            # ],
            ticktext=ticktext,
        ),
        coloraxis=dict(
            cmin=min_val,
            cmax=max_val,
        ),
    )

    return map


def gen_choropleth(
    df,
    geo,
    loc,
    featureid,
    color,
    hover_cols,
    title,
    str_format="",
    postfix="",
    hover_name="City",
    scale="viridis",
    **params,
):
    df[color] = df[color].astype("float")
    hover_data = {f"{hover_name}": False}
    hover_data.update({col: name[0] for col, name in hover_cols.items()})

    map = px.choropleth(
        df,
        geojson=geo,
        locations=loc,
        featureidkey=featureid,
        color=color,
        color_continuous_scale=scale,
        hover_name=hover_name,
        hover_data=hover_data,
        labels={col: name[1] for col, name in hover_cols.items()},
    )

    map.update_geos(fitbounds="locations", visible=False)

    map.update_layout(
        title=dict(
            text=title,
            font=dict(size=20),
            automargin=True,
            yref="paper",
        ),
        coloraxis_colorbar=dict(
            title="",
        ),
        title_x=0.5,
        margin={"r": 0, "t": 35, "l": 0, "b": 0},
    )

    if "colorbar_scale" in params:
        map.update_layout(
            coloraxis=params["colorbar_scale"],
        )

    return map
