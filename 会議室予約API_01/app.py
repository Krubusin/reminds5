import streamlit as st
import datetime
import requests
import json
import pandas as pd


def notify_message(message):
    url = 'https://notify-api.line.me/api/notify'
    LINE_NOTIFY_TOKEN = 'bQkJGsPyTpHGDVvYmSZdpbLOzkdxlFUqv7Pgg9MGsA3'
    # messagge = 'これはテストメッセージです'
    headers ={
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'
    }

    data = {
        'message': message
    }

    requests.post(
        url,
        headers =headers,
        data=data

    )





page = st.sidebar.selectbox('ページ選択',['教科登録','リマインド予約'])
if page == '教科登録':

    st.title('教科登録画面')

    with st.form(key='subject'):
        subjectname: str = st.text_input('教科名',max_chars=20)
        data = {
            'subjectname': subjectname
        }
        submit_button = st.form_submit_button(label='登録')

    if submit_button:
        st.write('## 送信データ')
        st.write('## レスポンス結果')
        url = 'http://127.0.0.1:8000/subjects'
        res = requests.post(
            url,
            data = json.dumps(data)
        )
        if res.status_code ==200:
            st.success('教科登録完了')
        st.write(res.status_code)
        st.json(res.json())


elif page == 'リマインド予約':
    st.title('リマインド予約画面')
    # 教科一覧取得
    url_subjects = 'http://127.0.0.1:8000/subjects'
    res = requests.get(url_subjects)
    subjects = res.json()
    # 教科名をキー、教科IDをバリュー
    subjects_name = {}
    for subject in subjects:
        subjects_name[subject['subjectname']] = subject['subject_id']



    url_bookings = 'http://127.0.0.1:8000/bookings'
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)

    subjects_id = {}
    for subject in subjects:
        subjects_id[subject['subject_id']] = subject['subjectname']



    # # IDを各値に変更
    to_subjectname = lambda x: subjects_id[x]
    to_date = lambda x: datetime.date.fromisoformat(x).strftime('%Y/%m/%d')
    #
    # # 特定の列に適用
    df_bookings['subject_id'] = df_bookings['subject_id'].map(to_subjectname)
    df_bookings['end_date'] = df_bookings['end_date'].map(to_date)

    df_bookings = df_bookings.rename(columns={
        'subject_id': '教科',
        'subject_num': '講義番号',
         'end_date': '期限日',
        'booking_id': '予約番号'
    })



    st.write('### リマインダー予約一覧')
    st.table(df_bookings)


    with st.form(key='booking'):
        # booking_id: int = random.randint(0, 10)
        subjectname: str = st.selectbox('教科名',subjects_name.keys())
        subject_num: int = st.number_input('講義番号', step=1, min_value=1)
        end_date = st.date_input('締切日の選択: ',min_value=datetime.date.today())

        submit_button = st.form_submit_button(label='登録')

    if submit_button:
        subject_id: int = subjects_name[subjectname]

        data = {
            'subject_id': subject_id,
            'subject_num': subject_num,
            'end_date': datetime.date(
                year=end_date.year,
                month=end_date.month,
                day=end_date.day,
            ).isoformat()
        }

        url = 'http://127.0.0.1:8000/bookings'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        if res.status_code == 200:
            st.success('予約完了しました')
            message = f'今日は{subjectname}の{subject_num}番のミニッツペーパー提出日です。'
            notify_message(message)
        st.write(res.status_code)
        st.json(res.json())


