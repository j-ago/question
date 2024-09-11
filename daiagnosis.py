import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'daiagnosis_rawdata.xlsx'  # 実際のExcelファイルのパスに変更してください
df = pd.read_excel(file_path, sheet_name=0)

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

# Function to display the dosha description
def display_dosha_description(dosha):
    descriptions = {
        'Vata': 'Vataは風や空気のエネルギーを持つ体質で、動きや変化を象徴します。想像力豊かで活動的ですが、不安や不眠になりやすい傾向があります。',
        'Pitta': 'Pittaは火と水のエネルギーを持つ体質で、変換や代謝を象徴します。強いリーダーシップと決断力を持ちますが、怒りっぽくなることがあります。',
        'Kapha': 'Kaphaは水と地のエネルギーを持つ体質で、安定性や持久力を象徴します。穏やかで忍耐強いですが、怠けがちになることがあります。',
        'Tri Dosha': 'Tri DoshaはVata、Pitta、Kaphaがバランスよく存在する理想的な体質です。健康と安定が保たれやすいですが、全体のバランスが重要です。'
    }
    st.write(descriptions[dosha])

# Streamlit UI
st.title('体質診断質問票（簡易版2024）')

st.write('各質問内容を見て、最も自分に当てはまる「状況・状態」を選んでください。')

responses = {
    'Vata': [],
    'Pitta': [],
    'Kapha': []
}

# Display each question with radio buttons
for i in range(len(df)):
    st.write(f"質問 {i+1}: {df.iloc[i, 1]}")  # Display the question
    
    # Display options with empty radio buttons for selection
    choice = st.radio(
        "選択してください:", 
        options=['Vata', 'Pitta', 'Kapha'], 
        format_func=lambda x: {'Vata': df.iloc[i, 2], 'Pitta': df.iloc[i, 4], 'Kapha': df.iloc[i, 6]}[x], 
        key=f'choice_{i}',
        label_visibility="collapsed"  # Hide the label to keep the UI clean
    )
    
    # Count responses based on selection
    responses['Vata'].append(1 if choice == 'Vata' else 0)
    responses['Pitta'].append(1 if choice == 'Pitta' else 0)
    responses['Kapha'].append(1 if choice == 'Kapha' else 0)

if st.button('診断結果を表示'):
    vata_percentage, pitta_percentage, kapha_percentage = calculate_dosha_percentages(df, responses)
    
    st.write(f'Vata: {vata_percentage:.2f}%')
    st.write(f'Pitta: {pitta_percentage:.2f}%')
    st.write(f'Kapha: {kapha_percentage:.2f}%')
    
    # Display Pie Chart
    labels = ['Vata', 'Pitta', 'Kapha']
    sizes = [vata_percentage, pitta_percentage, kapha_percentage]
    colors = ['#ff9999','#66b3ff','#99ff99']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.pyplot(fig)
    
    # Determine Dosha and Display Description
    if 28 <= vata_percentage <= 38 and 28 <= pitta_percentage <= 38 and 28 <= kapha_percentage <= 38:
        dosha = 'Tri Dosha'
    elif vata_percentage > pitta_percentage and vata_percentage > kapha_percentage:
        dosha = 'Vata'
    elif pitta_percentage > vata_percentage and pitta_percentage > kapha_percentage:
        dosha = 'Pitta'
    elif kapha_percentage > vata_percentage and kapha_percentage > pitta_percentage:
        dosha = 'Kapha'
    else:
        dosha = None
    
    if dosha:
        st.write(f'あなたの体質は: {dosha}')
        display_dosha_description(dosha)
    else:
        st.write('診断に失敗しました。')
