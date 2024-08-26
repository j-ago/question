import streamlit as st
import pandas as pd

# Load the Excel file
file_path = 'daiagnosis_rawdata.xlsx'
df = pd.read_excel(file_path)

# Function to calculate dosha percentages
def calculate_dosha_percentages(df, responses):
    df_responses = df.copy()
    df_responses['回答'] = responses['Vata']
    df_responses['回答.1'] = responses['Pitta']
    df_responses['回答.2'] = responses['Kapha']
    
    vata_score = df_responses['回答'].sum()
    pitta_score = df_responses['回答.1'].sum()
    kapha_score = df_responses['回答.2'].sum()
    
    total_score = vata_score + pitta_score + kapha_score
    vata_percentage = (vata_score / total_score) * 100
    pitta_percentage = (pitta_score / total_score) * 100
    kapha_percentage = (kapha_score / total_score) * 100
    
    return vata_percentage, pitta_percentage, kapha_percentage

# Streamlit UI
st.title('体質診断質問票（簡易版2024）')

st.write('各質問内容を見て、最も自分に当てはまる「状況・状態」に「はい」を押してください。')

responses = {
    'Vata': [],
    'Pitta': [],
    'Kapha': []
}

for i in range(len(df)):
    st.write(df.iloc[i, 1])  # Display the question
    vata_col, pitta_col, kapha_col = st.columns(3)
    
    with vata_col:
        response_vata = st.radio(df.iloc[i, 2], ["はい", "いいえ"], index=1, key=f'vata_{i}')
        responses['Vata'].append(1 if response_vata == "はい" else 0)
    
    with pitta_col:
        response_pitta = st.radio(df.iloc[i, 4], ["はい", "いいえ"], index=1, key=f'pitta_{i}')
        responses['Pitta'].append(1 if response_pitta == "はい" else 0)
    
    with kapha_col:
        response_kapha = st.radio(df.iloc[i, 6], ["はい", "いいえ"], index=1, key=f'kapha_{i}')
        responses['Kapha'].append(1 if response_kapha == "はい" else 0)

if st.button('診断結果を表示'):
    vata_percentage, pitta_percentage, kapha_percentage = calculate_dosha_percentages(df, responses)
    
    st.write(f'Vata: {vata_percentage:.2f}%')
    st.write(f'Pitta: {pitta_percentage:.2f}%')
    st.write(f'Kapha: {kapha_percentage:.2f}%')
    
    # Determine Dosha
    if 28 <= vata_percentage <= 38 and 28 <= pitta_percentage <= 38 and 28 <= kapha_percentage <= 38:
        st.write('あなたの体質は: Tri Dosha')
    elif vata_percentage > pitta_percentage and vata_percentage > kapha_percentage:
        st.write('あなたの体質は: Vata')
    elif pitta_percentage > vata_percentage and pitta_percentage > kapha_percentage:
        st.write('あなたの体質は: Pitta')
    elif kapha_percentage > vata_percentage and kapha_percentage > pitta_percentage:
        st.write('あなたの体質は: Kapha')
    else:
        st.write('診断に失敗しました。')
