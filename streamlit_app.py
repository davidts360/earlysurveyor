import math
import streamlit as st


def gon_to_rad(gon):
    return gon * math.pi / 200


def rad_to_gon(rad):
    return rad * 200 / math.pi


def normalitza_gon(angle):
    return angle % 400


def azimut_distancia(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    distancia = math.hypot(dx, dy)

    if distancia == 0:
        raise ValueError("Els dos punts coincideixen. No es pot calcular l'azimut.")

    azimut = rad_to_gon(math.atan2(dx, dy))
    return normalitza_gon(azimut), distancia


def pantalla_password():

    st.title("T.A.E. 1 – Calculadora topogràfica")

    try:
        app_password = st.secrets["APP_PASSWORD"]
    except Exception:
        st.error("Error de configuració de l'aplicació.")
        st.stop()

    password = st.text_input(
        "Introdueix la contrasenya",
        type="password"
    )

    if st.button("Accedir"):

        if password == app_password:
            st.session_state["acces"] = True
            st.rerun()

        else:
            st.error("Contrasenya incorrecta")

def modul_azimut_distancia():
    st.header("Azimut i distància entre dos punts")

    col1, col2 = st.columns(2)

    with col1:
        x1 = st.number_input("X1", value=0.0, format="%.3f")
        y1 = st.number_input("Y1", value=0.0, format="%.3f")

    with col2:
        x2 = st.number_input("X2", value=0.0, format="%.3f")
        y2 = st.number_input("Y2", value=0.0, format="%.3f")

    if st.button("Calcular azimut i distància"):
        try:
            az, dist = azimut_distancia(x1, y1, x2, y2)
            st.success("Resultat")
            st.write(f"**Azimut:** {az:.4f} gon")
            st.write(f"**Distància:** {dist:.3f} m")
        except ValueError as e:
            st.error(str(e))


def modul_coordenades_radiacio():
    st.header("Coordenades per radiació")

    st.subheader("Estació")
    x_est = st.number_input("X estació", value=0.0, format="%.3f")
    y_est = st.number_input("Y estació", value=0.0, format="%.3f")

    st.subheader("Punt d’orientació")
    x_ref = st.number_input("X punt orientació", value=0.0, format="%.3f")
    y_ref = st.number_input("Y punt orientació", value=0.0, format="%.3f")

    st.subheader("Lectures i distància")
    lectura_orientacio = st.number_input("Lectura a orientació (gon)", value=0.0, format="%.4f")
    lectura_punt = st.number_input("Lectura al punt (gon)", value=0.0, format="%.4f")
    distancia = st.number_input("Distància al punt (m)", value=0.0, format="%.3f")

    if st.button("Calcular coordenades"):
        try:
            az_ref, _ = azimut_distancia(x_est, y_est, x_ref, y_ref)
            desorientacio = az_ref - lectura_orientacio
            az_punt = normalitza_gon(lectura_punt + desorientacio)

            x_punt = x_est + distancia * math.sin(gon_to_rad(az_punt))
            y_punt = y_est + distancia * math.cos(gon_to_rad(az_punt))

            st.success("Resultat")
            st.write(f"**Azimut al punt:** {az_punt:.4f} gon")
            st.write(f"**X punt:** {x_punt:.3f} m")
            st.write(f"**Y punt:** {y_punt:.3f} m")
        except ValueError as e:
            st.error(str(e))


def modul_interseccio_rectes():
    st.header("Intersecció de dues rectes")

    st.subheader("Recta 1")
    col1, col2 = st.columns(2)

    with col1:
        x1 = st.number_input("X1 recta 1", value=0.0, format="%.3f")
        y1 = st.number_input("Y1 recta 1", value=0.0, format="%.3f")

    with col2:
        x2 = st.number_input("X2 recta 1", value=0.0, format="%.3f")
        y2 = st.number_input("Y2 recta 1", value=0.0, format="%.3f")

    st.subheader("Recta 2")
    col3, col4 = st.columns(2)

    with col3:
        x3 = st.number_input("X1 recta 2", value=0.0, format="%.3f")
        y3 = st.number_input("Y1 recta 2", value=0.0, format="%.3f")

    with col4:
        x4 = st.number_input("X2 recta 2", value=0.0, format="%.3f")
        y4 = st.number_input("Y2 recta 2", value=0.0, format="%.3f")

    if st.button("Calcular intersecció"):
        try:
            dx1 = x2 - x1
            dy1 = y2 - y1
            dx2 = x4 - x3
            dy2 = y4 - y3

            if dx1 == 0 and dy1 == 0:
                raise ValueError("La recta 1 no és vàlida.")
            if dx2 == 0 and dy2 == 0:
                raise ValueError("La recta 2 no és vàlida.")

            determinant = dx1 * dy2 - dy1 * dx2

            if abs(determinant) < 1e-12:
                raise ValueError("Les rectes són paral·leles o coincidents.")

            t = ((x3 - x1) * dy2 - (y3 - y1) * dx2) / determinant

            x_int = x1 + t * dx1
            y_int = y1 + t * dy1

            st.success("Resultat")
            st.write(f"**X intersecció:** {x_int:.3f} m")
            st.write(f"**Y intersecció:** {y_int:.3f} m")

        except ValueError as e:
            st.error(str(e))


def modul_distancia_punt_recta():
    st.header("Distància d’un punt a una recta")

    st.subheader("Recta base")
    col1, col2 = st.columns(2)

    with col1:
        x1 = st.number_input("X1 recta", value=0.0, format="%.3f")
        y1 = st.number_input("Y1 recta", value=0.0, format="%.3f")

    with col2:
        x2 = st.number_input("X2 recta", value=0.0, format="%.3f")
        y2 = st.number_input("Y2 recta", value=0.0, format="%.3f")

    st.subheader("Punt")
    xp = st.number_input("X punt", value=0.0, format="%.3f")
    yp = st.number_input("Y punt", value=0.0, format="%.3f")

    if st.button("Calcular distància punt-recta"):
        try:
            dx = x2 - x1
            dy = y2 - y1
            longitud_recta = math.hypot(dx, dy)

            if longitud_recta == 0:
                raise ValueError("La recta no és vàlida perquè els dos punts base coincideixen.")

            t = ((xp - x1) * dx + (yp - y1) * dy) / (longitud_recta ** 2)

            x_int = x1 + t * dx
            y_int = y1 + t * dy

            distancia_perpendicular = math.hypot(xp - x_int, yp - y_int)
            distancia_des_de_base = math.hypot(x_int - x1, y_int - y1)
            distancia_fins_ref = math.hypot(x2 - x_int, y2 - y_int)

            az_base_punt, dist_base_punt = azimut_distancia(x1, y1, xp, yp)
            az_recta, dist_recta = azimut_distancia(x1, y1, x2, y2)

            st.success("Resultat")
            st.write(f"**Azimut recta:** {az_recta:.4f} gon")
            st.write(f"**Distància recta:** {dist_recta:.3f} m")
            st.write(f"**Azimut base-punt:** {az_base_punt:.4f} gon")
            st.write(f"**Distància base-punt:** {dist_base_punt:.3f} m")
            st.write(f"**Distància punt-recta:** {distancia_perpendicular:.3f} m")
            st.write(f"**Distància intersecció-base:** {distancia_des_de_base:.3f} m")
            st.write(f"**Distància intersecció-referència:** {distancia_fins_ref:.3f} m")
            st.write(f"**X intersecció:** {x_int:.3f} m")
            st.write(f"**Y intersecció:** {y_int:.3f} m")

        except ValueError as e:
            st.error(str(e))


def main():
    st.set_page_config(
        page_title="T.A.E. 1",
        page_icon="📐",
        layout="centered"
    )

    if "acces" not in st.session_state:
        st.session_state["acces"] = False

    if not st.session_state["acces"]:
        pantalla_password()
        return

    st.title("📐 T.A.E. 1 – Calculadora topogràfica")
    st.caption("Azimut, distància, radiació, intersecció de rectes i distància punt-recta")

    opcio = st.sidebar.radio(
        "Selecciona una eina:",
        [
            "Azimut i distància",
            "Coordenades per radiació",
            "Intersecció de rectes",
            "Distància punt-recta"
        ]
    )

    if st.sidebar.button("Tancar sessió"):
        st.session_state["acces"] = False
        st.rerun()

    if opcio == "Azimut i distància":
        modul_azimut_distancia()
    elif opcio == "Coordenades per radiació":
        modul_coordenades_radiacio()
    elif opcio == "Intersecció de rectes":
        modul_interseccio_rectes()
    elif opcio == "Distància punt-recta":
        modul_distancia_punt_recta()


if __name__ == "__main__":
    main()
