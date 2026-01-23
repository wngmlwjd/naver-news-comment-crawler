import pandas as pd

from collect_article_urls_comment import run_integrated_crawler

'''
collect_article_urls_comment.py
'''
# 설정값
press_to_crawl = ['KBS', 'MBC', 'SBS', 'JTBC', '중앙일보', '조선일보', '한겨레', '경향신문'] 
dates_to_crawl = ['20260122', '20260123'] 
top_n_rank = 5

# 실행
final_results = run_integrated_crawler(press_to_crawl, dates_to_crawl, top_n_rank)

# 엑셀 저장
if final_results:
    df = pd.DataFrame(final_results)
    
    # 엑셀 파일명에 날짜 포함
    save_name = f"results/20260123.xlsx"
    df.to_excel(save_name, index=False)
    
    print(f"\n[성공] '{save_name}' 파일에 {len(df)}개의 데이터 저장 완료!")
else:
    print("\n[실패] 수집된 데이터가 없습니다.")