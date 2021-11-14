import os
from datetime import date, datetime
from pathlib import Path
from typing import List

import streamlit as st

_lang_dict = {
    "day": {
        "ca": "Dia",
        "de": "Tag",
        "es": "Día",
    },
    "open": {
        "ca": "Obrir",
        "de": "Öffnen",
        "es": "Abrir",
    },
    "password": {
        "ca": "Contrasenya",
        "de": "Passwort",
        "es": "Contraseña",
    },
    "enter password": {
        "ca": "Per favor, introduïx la contrasenya.",
        "de": "Bitte Passwort eingeben.",
        "es": "Por favor, introduce la contraseña.",
    },
    "password incorrect": {
        "ca": "La contrasenya és incorrecta.",
        "de": "Das Passwort ist falsch.",
        "es": "La contraseña es incorrecta.",
    },
    "you need to wait # days": {
        "ca": "Cal esperar # dies abans d'obrir aquesta porta.",
        "de": "Du musst noch # Tage warten, bevor du diese Tür öffnen kannst.",
        "es": "Debes esperar # días antes de abrir esta puerta.",
    },
    "you need to wait 1 day": {
        "ca": "Cal esperar un dia abans d'obrir aquesta porta.",
        "de": "Du musst noch einen Tag warten, bevor du diese Tür öffnen kannst.",
        "es": "Debes esperar un día antes de abrir esta puerta.",
    },
}


_lang_to_code = {"Català": "ca", "Deutsch": "de", "Español": "es"}


def today(query_params: dict) -> date:
    if "today" in query_params:
        return datetime.strptime(query_params["today"][0], "%Y-%m-%d").date()
    return datetime.utcnow().date()


def day_date(day: int):
    return date(year=2021, month=12, day=day)


def get_drawings_of_day(day: int) -> List[str]:
    files = Path("data", "drawings").glob(f"image_{day:02}*jpg")
    return [str(f) for f in files]


def get_audios_of_day(day: int) -> List[str]:
    files = Path("data", "audio").glob(f"audio_{day:02}*ogg")
    return [str(f) for f in files]


def main():

    st.set_page_config(
        page_title="Kalender4", page_icon="🎄", initial_sidebar_state="expanded"
    )

    query_params = st.experimental_get_query_params()

    if "lang" in query_params:
        lang_code = query_params["lang"][0]
    else:
        lang = st.sidebar.selectbox("", sorted(_lang_to_code.keys()))
        lang_code = _lang_to_code[lang]

    def tr(x: str) -> str:
        return _lang_dict[x][lang_code]

    st.markdown("# 🎄 Kalender 4")

    if "passwd" in query_params:
        passwd = query_params["passwd"][0]
    else:
        passwd = st.sidebar.text_input(tr("password"), type="password")
    if not passwd:
        st.write(tr("enter password"))
        return
    if passwd != os.getenv("PASSWORD", "1234"):
        st.write(tr("password incorrect"))
        return

    day = st.slider(tr("day"), min_value=1, max_value=24)

    button_col, door_col = st.columns(2)
    with button_col:
        open = st.button(tr("open"))

    if open:
        delta = day_date(day) - today(query_params)
        if delta.total_seconds() > 0:
            days_to_wait = delta.days
            if days_to_wait == 1:
                st.write(
                    tr("you need to wait 1 day").replace("#", str(days_to_wait))
                )
            else:
                st.write(
                    tr("you need to wait # days").replace(
                        "#", str(days_to_wait)
                    )
                )
        else:
            for audio in get_audios_of_day(day):
                st.audio(audio)
            for drawing in get_drawings_of_day(day):
                st.image(drawing, use_column_width=True)

    else:

        st.image(f"data/doors/door_{day:02}.jpg", use_column_width=True)


main()
