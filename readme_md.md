# 📊 단어 빈도 시각화 프로그램 (Word Frequency Visualizer)

Streamlit과 Kiwipiepy를 활용하여 텍스트 파일(.txt)을 업로드하면 핵심 명사를 추출하고, 빈도 분석 및 시각화(가로 막대그래프, 워드클라우드)를 수행하는 웹 애플리케이션입니다.

---

## 🛠️ 주요 기능

1. **텍스트 파일 업로드**: 분석 대상 `.txt` 파일 업로드 (UTF-8 및 CP949 인코딩 지원)
2. **텍스트 전처리**: Kiwi 형태소 분석기를 통해 2글자 이상의 명사만 자동 추출
3. **단어 빈도 분석**: 슬라이더를 통해 상위 단어 개수를 조절하며 빈도 데이터 확인
4. **시각화 (탭 구성)**:
   - **가로 막대그래프**: 상위 단어 빈도를 시각화
   - **워드클라우드**: 전체 추출 명사의 빈도 기반 워드클라우드 생성
5. **한글 폰트 지원**: Matplotlib 및 WordCloud의 한글 깨짐 방지를 위해 `NanumGothic.ttf` 적용

---

## 📁 프로젝트 구조

```text
.
├── app.py              # Streamlit 메인 애플리케이션 코드
├── requirements.txt    # 의존성 패키지 목록
├── NanumGothic.ttf     # 한글 지원 폰트 파일
└── README.md           # 프로젝트 안내 문서
```

---

## 🚀 설치 및 실행 방법

### 1. 나눔고딕 폰트 준비
프로젝트 루트 디렉토리에 `NanumGothic.ttf` 파일이 있어야 합니다.

### 2. 가상환경 구축 및 패키지 설치
```bash
# 필수 라이브러리 설치
pip install -r requirements.txt
```

### 3. Streamlit 앱 실행
```bash
streamlit run app.py
```

---

## 📦 기술 스택

- **UI Framework**: Streamlit
- **NLP / Tokenizer**: Kiwipiepy (Kiwi)
- **Data Handling**: Pandas
- **Visualization**: Matplotlib, WordCloud