import streamlit as st
from datetime import date, time, timedelta
import calendar  # для названий дней недели

st.set_page_config(page_title="Система записи", layout="wide")

# --- Верхнее меню (сайдбар) ---
main_menu = st.sidebar.radio(
    "Навигация:",
    ["Администрирование", "Мои записи", "Лист ожидания", "Ожидание"]
)

# --- Содержимое ---
if main_menu == "Мои записи":
    st.title("📌 Мои записи")
    st.write("Здесь будут показаны все записи пользователя.")

elif main_menu == "Лист ожидания":
    st.title("📋 Лист ожидания")
    st.write("Список людей, ожидающих запись.")

elif main_menu == "Ожидание":
    st.title("⏳ Ожидание")
    st.write("Информация о текущем ожидании.")

elif main_menu == "Администрирование":
    st.title("⚙️ Администрирование")

    admin_tab = st.radio(
        "Выберите раздел:",
        ["Мероприятия", "Услуги", "Записи", "Лист ожидания"],
        horizontal=True
    )

    # ---------------- Вкладка Мероприятия ----------------
    if admin_tab == "Мероприятия":
        st.subheader("🎉 Управление мероприятиями")

        if st.button("➕ Создать мероприятие"):
            st.info("Форма для создания мероприятия появится здесь (макет).")

        event_name = st.text_input("Название мероприятия")

        # --- Список городов с галочками ---
        st.markdown("**Города проведения:**")
        city_options = ["Липецк", "Заринск", "Москва"]
        selected_cities = st.multiselect("Выберите города", city_options)

        # Возможность добавить свой город
        custom_city = st.text_input("Добавить свой город")
        if custom_city:
            selected_cities.append(custom_city)

        st.write(f"Выбраны города: {', '.join(selected_cities) if selected_cities else 'Нет выбранных городов'}")

        st.subheader("📅 Даты и время проведения")
        start_date = st.date_input("Дата начала мероприятия", date.today())
        end_date = st.date_input("Дата окончания мероприятия", date.today())
        start_time = st.time_input("Время начала", time(9, 0))
        end_time = st.time_input("Время окончания", time(18, 0))

        description = st.text_area("Описание мероприятия")

        if st.button("💾 Сохранить мероприятие"):
            st.success("Мероприятие сохранено (макет).")

    # ---------------- Вкладка Услуги ----------------
    elif admin_tab == "Услуги":
        st.subheader("🛠 Управление услугами")

        if st.button("➕ Создать услугу"):
            st.info("Форма для создания услуги появится здесь (макет).")

        st.markdown("### Основная информация об услуге")
        service_name = st.text_input("Название услуги")
        event_name = st.selectbox("Мероприятие", ["Здоровый выбор", "Семейные высоты", "Что-то еще"])
        city = st.selectbox("Город", ["Липецк", "Москва", "Заринск", "+Другой"])
        if city == "+Другой":
            city = st.text_input("Введите свой город")
        address = st.text_input("Адрес")
        description = st.text_area("Описание услуги")

        st.subheader("📅 Даты проведения")
        start_date = st.date_input("Дата начала мероприятия", date.today())
        end_date = st.date_input("Дата окончания мероприятия", date.today())

        # ---------------- Настройка слотов ----------------
        st.subheader("⏱ Настройка слотов")
        slot_mode = st.radio("Настройка слотов:", ["Одинаково для всех дней", "Отдельно для каждого дня"])
        delta = (end_date - start_date).days + 1

        if slot_mode == "Одинаково для всех дней":
            st.markdown("**Общие параметры слотов для всех дней**")
            start_time = st.time_input("Время начала слотов", time(9, 0))
            end_time = st.time_input("Время окончания слотов", time(18, 0))
            slot_duration = st.number_input("Длительность слота (мин)", 15, 180, 60)
            slot_capacity = st.number_input("Количество человек в слоте", 1, 100, 22)
            break_duration = st.number_input("Перерыв между слотами (мин)", 0, 120, 30)
            lunch_break = st.checkbox("Большой обеденный перерыв")
            if lunch_break:
                lunch_start = st.time_input("Начало обеда", time(13, 0))
                lunch_end = st.time_input("Конец обеда", time(14, 0))

        elif slot_mode == "Отдельно для каждого дня":
            for i in range(delta):
                current_day = start_date + timedelta(days=i)
                weekday_name = calendar.day_name[current_day.weekday()]
                st.markdown(f"**День {i+1} — {current_day.strftime('%d.%m.%Y')}, {weekday_name}**")
                start_time = st.time_input(f"Время начала слотов - {current_day}", time(9, 0), key=f"start_{i}")
                end_time = st.time_input(f"Время окончания слотов - {current_day}", time(18, 0), key=f"end_{i}")
                slot_duration = st.number_input(f"Длительность слота (мин) - {current_day}", 15, 180, 60, key=f"duration_{i}")
                slot_capacity = st.number_input(f"Количество человек в слоте - {current_day}", 1, 100, 22, key=f"capacity_{i}")
                break_duration = st.number_input(f"Перерыв между слотами (мин) - {current_day}", 0, 120, 30, key=f"break_{i}")
                lunch_break = st.checkbox(f"Большой обеденный перерыв - {current_day}", key=f"lunch_check_{i}")
                if lunch_break:
                    lunch_start = st.time_input(f"Начало обеда - {current_day}", time(13, 0), key=f"lunch_start_{i}")
                    lunch_end = st.time_input(f"Конец обеда - {current_day}", time(14, 0), key=f"lunch_end_{i}")

        if st.button("💾 Сохранить услугу"):
            st.success("Услуга сохранена (макет).")

    # ---------------- Вкладка Записи ----------------
    elif admin_tab == "Записи":
        st.subheader("📑 Управление записями")
        st.write("Здесь администратор видит все записи.")

    # ---------------- Вкладка Лист ожидания ----------------
    elif admin_tab == "Лист ожидания":
        st.subheader("📋 Управление листом ожидания")
        st.write("Здесь администратор управляет очередью.")


