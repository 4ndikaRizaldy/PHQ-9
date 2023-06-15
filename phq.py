import streamlit as st
import pandas as pd
import json
import requests
from streamlit_lottie import st_lottie
from datetime import datetime

# Fungsi untuk menghitung skor PHQ-9 dan interpretasinya
def calculate_phq9_score(answers):
    score = sum(answers)
    return score

def interpret_phq9_score(score):
    if score < 5:
        interpretation = "Tidak ada gejala depresi"
    elif score < 10:
        interpretation = "Depresi ringan"
    elif score < 15:
        interpretation = "Depresi sedang"
    else:
        interpretation = "Depresi berat"
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
        nama = st.text_input("Masukkan Nama")
        umur = st.number_input("Masukkan Umur", min_value=0, max_value=150, step=1)

        if nama and umur:
            questions = [
                "1. Merasa sedih atau tidak tertarik pada hal-hal yang biasa Anda nikmati?",
                "2. Kesulitan tidur atau tidur terlalu banyak?",
                "3. Merasa lelah atau kekurangan energi?",
                "4. Kurang nafsu makan atau makan terlalu banyak?",
                "5. Merasa buruk tentang diri sendiri — atau merasa bahwa Anda adalah seorang pengecewak atau menjadi beban bagi orang lain?",
                "6. Kesulitan berkonsentrasi pada hal-hal seperti membaca atau menonton televisi?",
                "7. Bergerak atau bicara begitu lamban sehingga orang lain dengan mudahnya melihatnya? Atau sebaliknya — merasa gelisah dan tidak bisa diam?",
                "8. Berpikir bahwa Anda akan lebih baik jika Anda sudah tidak ada di dunia ini atau memiliki pikiran bahwa Anda ingin melukai diri sendiri?",
                "9. Melakukan tindakan untuk melukai diri sendiri, seperti mencoba bunuh diri, berpikir untuk melukai diri, atau memiliki rencana untuk melukai diri?"
            ]

            answers = []
            for i, question in enumerate(questions):
                st.write(question)
                answer = st.radio(
                    f"Pilih jawaban untuk pertanyaan {i+1}",
                    options=["Tidak sama sekali", "Hampir setiap hari", "Beberapa hari", "Lebih dari setengah hari"]
                )
                if answer == "Tidak sama sekali":
                    answer_value = 0
                elif answer == "Beberapa hari":
                    answer_value = 1
                elif answer == "Lebih dari setengah hari":
                    answer_value = 2
                else:
                    answer_value = 3
                answers.append(answer_value)

            # Tombol untuk menghitung skor dan menampilkan hasil
            if st.button("Cek Hasil"):
                phq9_score = calculate_phq9_score(answers)
                interpretation = interpret_phq9_score(phq9_score)

                st.write(f"Skor PHQ-9: {phq9_score}")
                st.write(f"Interpretasi: {interpretation}")

                # Menyimpan hasil tes ke menu History Tes
                history_df = pd.DataFrame({
                    "Nama": [nama],
                    "Umur": [umur],
                    "Skor PHQ-9": [phq9_score],
                    "Interpretasi": [interpretation],
                    "Tanggal Tes": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                })
                history_df.to_csv("history.csv", mode="a", index=False, header=False)
        else:
            st.warning("Mohon lengkapi input nama dan umur sebelum mengecek hasil tes.")

    elif menu == "History Tes":
        # Membaca data history dari file CSV
        history_df = pd.read_csv("history.csv")

        # Menampilkan data history dalam bentuk tabel
        st.table(history_df)

# Menjalankan aplikasi utama
if __name__ == "__main__":
    main()
