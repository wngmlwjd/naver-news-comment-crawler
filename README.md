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

# 수집할 날짜 범위
dates_to_crawl = pd.date_range(start='2025-12-01', end='2025-12-31').strftime('%Y%m%d').tolist()

# 언론사별 상위 N개 기사 수집
top_n = 10

# 결과 저장 폴더
result_file_dir = "results/20260126"
```

설정 완료 후 실행:

```bash
python run.py
```

---

## 📂 출력 결과

`results/<폴더명>/` 아래에 언론사별 Excel 파일이 생성됩니다.

```
results/
└── 20260126/
    ├── KBS_202512.xlsx
    ├── MBC_202512.xlsx
    ├── SBS_202512.xlsx
    └── ...
```

---

## 🛠️ 동작 방식

1. `run.py`에서 언론사 목록과 날짜 범위를 설정합니다.
2. `collect_article_urls_comment.py`의 `run_integrated_crawler()` 함수가 Selenium으로 네이버 미디어 랭킹 페이지에 접속합니다.
3. 날짜별로 댓글 많은 순 상위 N개 기사의 URL을 수집합니다.
4. 각 기사에 대해 네이버 댓글 API를 호출하여 댓글 데이터를 가져옵니다.
5. 언론사별로 결과를 `.xlsx` 파일에 저장합니다.

---

## ⚠️ 주의 사항

- 본 프로젝트는 **학술·연구 목적**으로만 사용하시기 바랍니다.
- 네이버 서비스 정책 및 이용 약관을 준수하여 사용해 주세요.
- 과도한 요청은 IP 차단으로 이어질 수 있으니, 기본 딜레이 설정을 유지하는 것을 권장합니다.
- 네이버 댓글 API 구조 변경 시 크롤러가 정상 동작하지 않을 수 있습니다.

---

## 📌 지원 언론사

현재 `utils.py`에 정의된 언론사 코드 기반으로 동작합니다. 기본 지원 언론사 예시:

`KBS`, `MBC`, `SBS`, `JTBC`, `중앙일보`, `조선일보`, `한겨레`, `경향신문` 등

추가 언론사는 `utils.py`의 `press_dict`에 해당 언론사 코드를 등록하여 확장할 수 있습니다.
