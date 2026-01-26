import pandas as pd
import os

from collect_article_urls_comment import run_integrated_crawler


# 1. 설정
press_to_crawl = ['KBS', 'MBC', 'SBS', 'JTBC', '중앙일보', '조선일보', '한겨레', '경향신문']
dates_to_crawl = pd.date_range(start='2025-12-01', end='2025-12-31').strftime('%Y%m%d').tolist()
top_n = 10

# 데이터를 저장할 폴더 생성 (없으면 만듦)
result_file_dir = "results/20260126"
if not os.path.exists(result_file_dir):
        os.makedirs(result_file_dir)
        
# 2. 언론사별로 루프를 돌며 수집 및 즉시 저장
for press_name in press_to_crawl:
    print(f"\n{'='*30}")
    print(f"🚀 {press_name} 수집 시작")
    print(f"{'='*30}")
    
    # 해당 언론사 한 곳에 대해서만 수집 함수 호출
    press_results = run_integrated_crawler([press_name], dates_to_crawl, top_n)
    
    if press_results:
        df = pd.DataFrame(press_results)
        # 컬럼 순서 고정
        cols = ["언론사", "검색기준날짜", "기사순위", "기사제목", "댓글내용", "좋아요수", "싫어요수", "답글수", "댓글작성일", "댓글작성자", "기사링크"]
        df = df[cols]
        
        filename = os.path.join(result_file_dir, f"{press_name}_202512.xlsx")
        df.to_excel(filename, index=False)
        print(f"\n✅ {press_name} 완료! 저장됨: {filename}")
    else:
        print(f"\n❌ {press_name} 수집된 데이터가 없습니다.")

print("\n[모든 언론사 수집 프로세스 종료]")