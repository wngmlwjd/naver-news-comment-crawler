import pandas as pd

from collect_article_urls_keyword import collect_article_urls_keyword
from collect_comments import collect_all_comments

from utils import save_articles_to_txt
    
'''
collect_article_urls_keyword.py
'''
articles_file_name = "test"

# 1. 기사 목록 및 URL 수집
data = collect_article_urls_keyword(
    keyword="AI",
    start_date="2025.01.01",
    end_date="2025.01.20",
    
    max_pages=5
)

# 2. 결과 저장
if data["articles"]:
    save_path = f"results/articles/{articles_file_name}.txt"
    save_articles_to_txt(data, save_path)
    print(f"\n[성공] 총 {len(data['articles'])}개의 URL 목록이 '{save_path}'에 저장되었습니다.")
else:
    print("\n[실패] 수집된 기사가 없습니다.")
    

# 3. 저장된 txt 파일을 읽어서 댓글 수집 시작
txt_path = f"results/articles/{articles_file_name}.txt" # 아까 생성된 파일명
print("\n" + "="*50)
print("댓글 수집을 시작합니다...")
print("="*50)

final_comments = collect_all_comments(txt_path)

# 4. 엑셀로 저장 (Pandas 활용)
if final_comments:
    df = pd.DataFrame(final_comments)
    
    # 컬럼 순서 정리
    cols = ['기사URL', '작성일', '작성자', '댓글내용', '공감수', '비공감수', '답글수']
    df = df[cols]
    
    excel_path = "results/comments/test.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"\n[최종 완료] 총 {len(df)}개의 댓글이 '{excel_path}'에 저장되었습니다!")
else:
    print("\n[알림] 수집된 댓글이 없습니다.")
    
