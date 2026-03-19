# 📰 naver-news-comment-crawler

네이버 뉴스에서 언론사별 **댓글 많은 순 기사**의 댓글을 자동으로 수집하는 Python 크롤러입니다.

---

## 🔍 개요

네이버 뉴스 미디어 페이지(`media.naver.com`)에서 특정 언론사의 날짜별 댓글 많은 순 기사 상위 N개를 선정하고, 각 기사의 댓글 내용·반응·작성자 정보를 수집하여 Excel 파일로 저장합니다.

---

## 📁 프로젝트 구조

```
naver-news-comment-crawler/
├── run.py                          # 크롤러 실행 진입점 (언론사, 날짜 범위, 저장 경로 설정)
├── collect_article_urls_comment.py # 기사 URL 수집 및 댓글 크롤링 핵심 로직
├── utils.py                        # 언론사 코드 매핑, URL 파싱 유틸리티
└── results/                        # 수집 결과 Excel 파일 저장 폴더
```

---

## 🛠️ 기술 스택

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

---

## ✨ 주요 기능

- 복수의 언론사를 순차적으로 크롤링
- 지정한 날짜 범위 내 일별 댓글 많은 순 기사 수집
- 기사별 상위 댓글 100개 수집 (네이버 댓글 API 활용)
- 수집 결과를 언론사별 Excel 파일로 자동 저장

---

## 📊 수집 데이터 항목

| 컬럼 | 설명 |
|------|------|
| 언론사 | 기사를 게재한 언론사 이름 |
| 검색기준날짜 | 랭킹 조회 기준 날짜 |
| 기사순위 | 해당 날짜의 댓글 많은 순 기사 순위 |
| 기사제목 | 기사 제목 |
| 댓글내용 | 댓글 본문 |
| 좋아요수 | 댓글 공감 수 |
| 싫어요수 | 댓글 비공감 수 |
| 답글수 | 댓글에 달린 답글 수 |
| 댓글작성일 | 댓글이 작성된 날짜 |
| 댓글작성자 | 마스킹 처리된 작성자 ID |
| 기사링크 | 원문 기사 URL |

---

## ⚙️ 설치 방법

**1. 저장소 클론**

```bash
git clone https://github.com/wngmlwjd/naver-news-comment-crawler.git
cd naver-news-comment-crawler
```

**2. 의존 패키지 설치**

```bash
pip install selenium webdriver-manager requests pandas openpyxl
```

> Chrome 브라우저가 설치되어 있어야 합니다. ChromeDriver는 `webdriver-manager`가 자동으로 관리합니다.

---

## 🚀 사용 방법

`run.py` 상단의 설정값을 원하는 대로 수정한 후 실행합니다.

```python
# run.py

# 수집할 언론사 목록
press_to_crawl = ['KBS', 'MBC', 'SBS', 'JTBC', '중앙일보', '조선일보', '한겨레', '경향신문']

# 수집할 날짜 범위 (start ~ end 전체 기간)
start_date = '2025-10-01'
end_date   = '2025-11-30'

# 언론사별 상위 N개 기사 수집
top_n = 10

# 결과 저장 최상위 폴더
result_file_dir = "results/20260126"
```

설정 완료 후 실행:

```bash
python run.py
```

---

## 📂 출력 결과

지정한 날짜 범위가 **월 단위로 자동 분할**되어, `results/<폴더명>/<월>/` 구조로 저장됩니다.

```
results/
└── 20260126/
    ├── 202510/
    │   ├── KBS_202510.xlsx
    │   ├── MBC_202510.xlsx
    │   └── ...
    └── 202511/
        ├── KBS_202511.xlsx
        ├── MBC_202511.xlsx
        └── ...
```

---

## 🛠️ 동작 방식

1. `run.py`에서 언론사 목록과 수집 기간(`start_date` ~ `end_date`)을 설정합니다.
2. 전체 날짜를 **월별로 그룹화**하고, 월마다 하위 폴더(`results/.../YYYYMM/`)를 자동 생성합니다.
3. 월별 × 언론사별로 순차 반복하며 `run_integrated_crawler()`를 호출합니다.
4. Selenium으로 네이버 미디어 랭킹 페이지에 접속해 댓글 많은 순 상위 N개 기사 URL을 수집합니다.
5. 각 기사에 대해 네이버 댓글 API를 호출하여 댓글 데이터를 가져옵니다.
6. 결과를 `언론사명_YYYYMM.xlsx` 파일로 해당 월 폴더에 저장합니다.

---

## ⚠️ 주의 사항

- 본 프로젝트는 **학술·연구 목적**으로만 사용하시기 바랍니다.
- 네이버 서비스 정책 및 이용 약관을 준수하여 사용해 주세요.
- 과도한 요청은 IP 차단으로 이어질 수 있으니, 기본 딜레이 설정을 유지하는 것을 권장합니다.
- 네이버 댓글 API 구조 변경 시 크롤러가 정상 동작하지 않을 수 있습니다.

---

## 📌 지원 언론사

`utils.py`의 `press_dict`에 정의된 언론사를 지원합니다.

| 분류 | 언론사 |
|------|--------|
| 지상파 / 종편 | KBS, MBC, SBS, OBS, JTBC, TV조선, 채널A, MBN, YTN, 연합뉴스TV |
| 주요 일간지 | 조선일보, 중앙일보, 동아일보, 문화일보, 경향신문, 한겨레, 한국일보, 서울신문, 세계일보 |
| 경제지 | 매일경제, 한국경제, 서울경제, 헤럴드경제, 파이낸셜뉴스, 아시아경제, 머니투데이, 이데일리 |
| 통신사 / 기타 | 연합뉴스, 뉴시스, 뉴스1, 노컷뉴스, 오마이뉴스 |
| IT / 기술 | 전자신문, 아이뉴스24, 디지털데일리, 블로터, ZDNetKorea |

목록에 없는 언론사는 `utils.py`의 `press_dict`에 네이버 언론사 코드를 직접 추가하여 확장할 수 있습니다.
