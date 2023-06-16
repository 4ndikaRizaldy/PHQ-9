import streamlit as st
import pandas as pd
import json
import requests
import altair as alt
from datetime import datetime
from streamlit_lottie import st_lottie

# Fungsi untuk menghitung skor PHQ-9 dan interpretasinya
def calculate_phq9_score(answers):
    score = sum(answers)
    return score

def interpret_phq9_score(score):
    if score < 4:
        interpretation = "Tidak ada gejala depresi"
    elif score < 9:
        interpretation = "Gejalan depresi ringan"
    elif score < 14:
        interpretation = "Depresi ringan"
    elif score < 19:
        interpretation = "Depresi sedang"
    else:
        interpretation = "Depresi berat"
    return interpretation

def suggestion(score):
    if score < 9:
        interpretation = "Dianjurkan terapi adalah psikoedukasi bila ada perburukan gejala"
    elif score < 14:
        interpretation = "Dianjurkan terapi adalah observasi gejala yang ada dalam 1 bulan (perbaikan atau perburukan) dan pertimbangan pemberian antidepresan atau psikoterapi singkat"
    elif score < 19:
        interpretation = "Dianjurkan untuk memberikan antidepresan atau psikoterapi"
    else:
        interpretation = "Dianjurkan untuk memberikan antidepresan secara tunggal atau kombinasikan dengan psikoterapi"
    return interpretation

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Main program
def main():
    st.markdown(
        """
        <h2 style='text-align: center; color: #FFAC08;'>Tes PHQ-9 (Patient Health Questionnaire)</h2>
        <p>PHQ-9 adalah instrumen serbaguna untuk menyaring, mendiagnosis, memantau, dan mengukur tingkat keparahan depresi</p>
        """,
        unsafe_allow_html=True
    )
    
    lottie_coding = load_lottiefile("95714-hello-orange.json")

    st_lottie(
        lottie_coding,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=None,
        width=None,
        key=None,
    )

    menu = st.sidebar.selectbox("Menu", ["Tes PHQ-9", "History Tes"])

    if menu == "Tes PHQ-9":
        nama = st.text_input("Masukkan Inisial Nama")
        umur = st.number_input("Masukkan Umur", min_value=0, max_value=150, step=1)
        gender = st.selectbox("Pilih Jenis Kelamin", ["Laki-laki", "Perempuan"])

        if nama and umur and gender:
            st.subheader("Selama 2 minggu terakhir, seberapa sering Anda terganggu oleh masalah-masalah berikut?")
            questions = [
                "1. Sedikit minat atas kesenangan dalam melakukan sesuatu",
                "2. Merasa down, depresi atau putus asa",
                "3. Kesulitan tidur, tetap tidur, atau tidur terlalu banyak",
                "4. Merasa lelah atau memiliki sedikit energi",
                "5. Nafsu makan buruk atau makan berlebihan",
                "6. Merasa buruk tentang diri sendiri - atau bahwa Anda gagal atau mengecewakan diri sendiri atau keluarga Anda",
                "7. Kesulitan berkonsentrasi pada hal-hal, seperti membaca koran atau menonton televisi",
                "8. Bergerak atau bicara sangat lambat sehingga orang lain dapat menyadarinya. Atau, sebaliknya — menjadi sangat gelisah atau gelisah sehingga Anda lebih sering berpindah-pindah dari biasanya",
                "9. Pikiran bahwa Anda lebih baik mati atau menyakiti diri sendiri dengan cara tertentu"
            ]

            answers = []
            for i, question in enumerate(questions):
                st.write(question)
                answer = st.radio(
                    f"Pilih jawaban untuk pertanyaan {i+1}",
                    options=["Tidak sama sekali", "Hampir setiap hari", "Beberapa hari", "Lebih dari separuh waktu yang dimaksud"]
                )
                if answer == "Tidak sama sekali":
                    answer_value = 0
                elif answer == "Beberapa hari":
                    answer_value = 1
                elif answer == "Lebih dari separuh waktu yang dimaksud":
                    answer_value = 2
                else:
                    answer_value = 3
                answers.append(answer_value)

            # Tombol untuk menghitung skor dan menampilkan hasil
            if st.button("Cek Hasil"):
                phq9_score = calculate_phq9_score(answers)
                interpretation = interpret_phq9_score(phq9_score)
                suggestions = suggestion(phq9_score)

                st.write(f"Skor PHQ-9: {phq9_score}")
                st.write(f"Interpretasi: {interpretation}")
                st.write(f"Saran penanganan: {suggestions}")

                # Menyimpan hasil tes ke menu History Tes
                history_df = pd.DataFrame({
                    "Nama": [nama],
                    "Umur": [umur],
                    "Gender": [gender],
                    "Skor PHQ-9": [phq9_score],
                    "Interpretasi": [interpretation],
                    "Tanggal Tes": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "Saran penanganan": [suggestions]
                })
                history_df.to_csv("history.csv", mode="a", index=False, header=False)
        else:
            st.warning("Mohon lengkapi input nama, umur, dan jenis kelamin sebelum mengecek hasil tes.")

    elif menu == "History Tes":
        # Membaca data history dari file CSV
        history_df = pd.read_csv("history.csv")

        # Menampilkan data history dalam bentuk tabel
        st.table(history_df)

# Menjalankan aplikasi utama
if __name__ == "__main__":
    main()
    #footer aplikasi
    footer_style = """
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0E1117;
    color: #FAFAFA;
    text-align: center;
    padding: 10px;
    """
    
    st.markdown(
        """
        <footer style='{}'>
            © 2023, A. Rizaldy
        </footer>
        """.format(footer_style),
        unsafe_allow_html=True
    )
