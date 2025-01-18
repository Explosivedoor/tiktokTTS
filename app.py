import requests, base64
import streamlit as st


from youtube_transcript_api import YouTubeTranscriptApi 

st.title("Captions maker and AI Voice Maker!")
tab1, tab2= st.tabs(["Captions", "Tiktok Voice Maker"])

SESSIONID = None

with tab1:
    try:
        caption_url = st.text_input("Paste Youtube Url Here")
        if "?" in caption_url:
            trash, caption_url = caption_url.split('=',1)
        else:
            trash,caption_url = caption_url.rsplit("/",1)
        if "&" in caption_url:
            caption_url,trash =caption_url.split('&',1)

        st.write(caption_url)
        srt = YouTubeTranscriptApi.get_transcript(f"{caption_url}", 
                                            languages=['en'])




        for i in srt:
                st.write(i['text'])

    except:
        pass

with tab2:
    text = st.text_input("Input up to 100 characters of Japanese text for Tiktok Voice") 
    st.write("Current length: ",len(text))
    if len(text) > 100:
        st.write("Text too long please reduce")
    voice_dic ={
    'Japanese - Female 1':'jp_001',
    "Japanese - Female 2":'jp_003',
    "Japanese - Female 3":'jp_005',
    "Japanese - Male":'jp_006',
    'りーさ':'jp_female_fujicochan',
    '世羅鈴':'jp_female_hasegawariona',
    'Morio’s Kitchen':'jp_male_keiichinakano',
    '夏絵ココ':'jp_female_oomaeaika',
    '低音ボイス':'jp_male_yujinchigusa',
    '四郎':'jp_female_shirou',
    '玉川寿紀':'jp_male_tamawakazuki',
    '庄司果織':'jp_female_kaorishoji',
    '八木沙季':'jp_female_yagishaki',
    'ヒカキン':'jp_male_hikakin',
    '丸山礼':'jp_female_rei',
    '修一朗':'jp_male_shuichiro',
    'マツダ家の日常':'jp_male_matsudake',
    'まちこりーた':'jp_female_machikoriiita',
    'モジャオ':'jp_male_matsuo',
    'モリスケ':'jp_male_osada'}

    key = st.selectbox("Speaker",voice_dic.keys())

    speaker = voice_dic.get(key)

    
    def create_tiktok_tts_request(text, speaker):
        # Base URL ( this will be different depending on your account)
        base_url = "https://api22-normal-c-alisg.tiktokv.com/media/api/text/speech/invoke/"
        
        # These are the required parameters. 
        params = {
            'req_text': text,
            'text_speaker': speaker,
            'speaker_map_type': '1',
            'namespace': 'TTS',
            'aid': '1233',
            'device_platform': 'android',
            'os': 'android'
        }
        
        
        essential_cookies = {
            #see readme for details
            'sessionid': SESSIONID,

            
        }
        
        # Headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Android 13; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Make POST request
        response = requests.post(
            base_url,
            data=params,  # Send parameters as form data
            cookies=essential_cookies,
            headers=headers
        )
        
        return response

    if st.button("Run Tiktok Voice"):

        response = create_tiktok_tts_request(text,speaker)
        print(f"Status Code: {response.status_code}")

        voice_data = [response.json()["data"]["v_str"]][0]
        print('test ',voice_data)
        #encodes voice data
        b64d = base64.b64decode(voice_data)

        #saves file
        #with open(f'voice_{speaker}.mp3', "wb") as out:
        #    out.write(b64d)

        st.download_button(
                                    label="Click here to download",
                                    data=b64d,
                                    file_name=f'voice_{speaker}.mp3',
                                    mime="image/png",
                                    key="download_button"
                                )


