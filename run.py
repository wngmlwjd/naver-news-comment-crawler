import pandas as pd
import os
from collect_article_urls_comment import run_integrated_crawler

# 1. 설정
press_to_crawl = ['KBS', 'MBC', 'SBS', 'JTBC', '중앙일보', '조선일보', '한겨레', '경향신문']
start_date = '2025-10-01'
end_date = '2025-11-30'
top_n = 10

# 메인 결과 폴더 생성
result_file_dir = "results/20260126"

# 전체 날짜 생성 및 월별 그룹화
all_dates = pd.date_range(start=start_date, end=end_date)
months = all_dates.strftime('%Y-%m').unique()

# 2. 월별 루프
for month_str in months:
    # 해당 월 날짜 리스트 (YYYYMMDD)
    current_month_dates = all_dates[all_dates.strftime('%Y-%m') == month_str].strftime('%Y%m%d').tolist()
    file_suffix = month_str.replace('-', '') # '202510'
    
    # 📁 월별 하위 폴더 경로 설정 (예: results/20260126/202510)
    month_dir = os.path.join(result_file_dir, file_suffix)
    
    # 폴더가 없으면 생성 (exist_ok=True는 이미 폴더가 있어도 에러를 내지 않음)
    if not os.path.exists(month_dir):
        os.makedirs(month_dir, exist_ok=True)
        print(f"\n📂 새 폴더 생성됨: {month_dir}")

    print(f"\n\n" + "#"*50)
    print(f"📅 {month_str} 기간 수집 시작")
    print("#"*50)

    # 3. 언론사별 루프
    for press_name in press_to_crawl:
        print(f"\n{'='*30}")
        print(f"🚀 {press_name} | {month_str} 수집 시작")
        print(f"{'='*30}")
        
        press_results = run_integrated_crawler([press_name], current_month_dates, top_n)
        
        if press_results:
            df = pd.DataFrame(press_results)
            cols = ["언론사", "검색기준날짜", "기사순위", "기사제목", "댓글내용", "좋아요수", "싫어요수", "답글수", "댓글작성일", "댓글작성자", "기사링크"]
            
            # 존재하는 컬럼만 필터링
            existing_cols = [c for c in cols if c in df.columns]
            df = df[existing_cols]
            
            # 💾 최종 파일 경로 (예: results/20260126/202510/KBS_202510.xlsx)
            filename = os.path.join(month_dir, f"{press_name}_{file_suffix}.xlsx")
            df.to_excel(filename, index=False)
            print(f"✅ 저장 완료: {filename} (데이터: {len(df)}건)")
        else:
            print(f"❌ {press_name} | {month_str} 수집된 데이터가 없습니다.")

print("\n" + "!"*50)
print("🎉 모든 월별 폴더 분류 및 수집 종료!")
print("!"*50)