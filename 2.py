import streamlit as st
import pandas as pd
from collections import Counter
from kiwipiepy import Kiwi
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud

# --- 0. 폰트 및 설정 ---
FONT_PATH = "NanumGothic.ttf"


def setup_font():
    """Matplotlib 한글 폰트 설정"""
    try:
        font_name = font_manager.FontProperties(fname=FONT_PATH).get_name()
        rc('font', family=font_name)
    except Exception:
        pass


setup_font()


# --- 1. 기능별 함수 정의 ---

@st.cache_resource
def load_kiwi():
    """Kiwi 형태소 분석기 로드 (캐싱 적용)"""
    return Kiwi()


def preprocess_text(text, kiwi):
    """Kiwi를 사용하여 명사만 추출하고 2글자 이상인 단어만 필터링"""
    tokens = kiwi.tokenize(text)
    # N으로 시작하는 태그(체언/명사류)이면서 글자수가 2 이상인 단어 추출
    nouns = [token.form for token in tokens if token.tag.startswith('N') and len(token.form) >= 2]
    return nouns


def calculate_word_freq(nouns):
    """추출된 명사 리스트의 빈도수를 계산하여 DataFrame으로 반환"""
    counts = Counter(nouns)
    df = pd.DataFrame(counts.most_common(), columns=['단어', '빈도'])
    return df


def plot_bar_chart(df_top):
    """상위 단어 빈도를 가로 막대그래프로 시각화"""
    fig, ax = plt.subplots(figsize=(10, 6))
    # 상위 단어가 위쪽에 오도록 역순 정렬
    df_sorted = df_top.sort_values(by='빈도', ascending=True)
    ax.barh(df_sorted['단어'], df_sorted['빈도'], color='skyblue')
    ax.set_xlabel('빈도수')
    ax.set_ylabel('단어')
    ax.set_title('상위 단어 빈도 가로 막대그래프')
    st.pyplot(fig)


def plot_wordcloud(freq_dict):
    """단어 빈도 데이터를 기반으로 워드클라우드 생성 및 시각화"""
    wc = WordCloud(
        font_path=FONT_PATH,
        width=800,
        height=400,
        background_color='white',
        max_words=100
    )
    wc.generate_from_frequencies(freq_dict)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)


# --- 2. 메인 Streamlit 애플리케이션 ---
def main():
    st.title("📊 단어 빈도 시각화 프로그램")
    st.write("텍스트 파일을 업로드하여 형태소 분석 및 단어 빈도/시각화 결과를 확인하세요.")

    kiwi = load_kiwi()

    # [순서 1] 텍스트 파일 업로드
    st.subheader("1. 텍스트 파일 업로드")
    uploaded_file = st.file_uploader("분석할 텍스트 파일(.txt)을 선택하세요", type=["txt"])

    if uploaded_file is not None:
        # 파일 인코딩 자동 처리 (UTF-8 우선, 실패시 CP949)
        file_bytes = uploaded_file.read()
        text = ""
        for encoding in ['utf-8', 'cp949', 'euc-kr']:
            try:
                text = file_bytes.decode(encoding)
                break
            except UnicodeDecodeError:
                continue

        if not text:
            st.error("파일 인코딩을 읽지 못했습니다. UTF-8 또는 CP949 형식의 파일인지 확인해주세요.")
            return

        # [순서 2] 파일 내용 보기
        st.subheader("2. 파일 내용 보기")
        with st.expander("업로드된 텍스트 미리보기", expanded=False):
            st.text_area("파일 내용", text, height=150, disabled=True)

        # [순서 3] 전처리 결과
        st.subheader("3. 전처리 결과")
        nouns = preprocess_text(text, kiwi)
        st.write(f"추출된 2글자 이상 명사 총 개수: **{len(nouns)}개**")

        with st.expander("추출된 명사 샘플 보기", expanded=False):
            st.write(", ".join(nouns[:150]) + ("..." if len(nouns) > 150 else ""))

        if not nouns:
            st.warning("분석할 명사가 충분하지 않습니다. 다른 텍스트 파일을 업로드해주세요.")
            return

        # 빈도 분석 데이터 생성
        df_freq = calculate_word_freq(nouns)

        # [순서 4] 단어 빈도 (슬라이더 및 표)
        st.subheader("4. 단어 빈도")
        max_slider_val = min(50, len(df_freq))
        top_n = st.slider("표 및 시각화에 표시할 상위 단어 개수 선택", min_value=1, max_value=max_slider_val,
                          value=min(10, max_slider_val))

        df_top = df_freq.head(top_n)
        st.dataframe(df_top, use_container_width=True)

        # [순서 5] 시각화 (탭 2개)
        st.subheader("5. 시각화")
        tab1, tab2 = st.tabs(["가로 막대그래프", "워드클라우드"])

        with tab1:
            st.markdown("#### 📉 상위 단어 빈도 막대그래프")
            plot_bar_chart(df_top)

        with tab2:
            st.markdown("#### ☁️ 단어 워드클라우드")
            # 전체 빈도 데이터를 딕셔너리로 변환하여 워드클라우드 생성
            freq_dict = dict(zip(df_freq['단어'], df_freq['빈도']))
            plot_wordcloud(freq_dict)


if __name__ == "__main__":
    main()