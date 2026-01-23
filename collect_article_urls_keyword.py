'''
네이버 홈 화면에서 키워드로 검색해서 뉴스 기사 URL 수집
'''

import time
import re
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from utils import extract_oid_aid

def collect_article_urls_keyword(keyword, start_date, end_date, max_pages=5):
    options = Options()
    # 봇 감지 회피 설정
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    s_date = start_date.replace("-", ".").replace("/", ".")
    e_date = end_date.replace("-", ".").replace("/", ".")
    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")

    result = {"keyword": keyword, "start_date": s_date, "end_date": e_date, "articles": []}
    seen_urls = set()

    try:
        for page in range(max_pages):
            start = page * 10 + 1
            url = (f"https://search.naver.com/search.naver?where=news&query={quote(keyword)}"f"&pd=3&ds={s_date}&de={e_date}&nso=so:r,p:from{s_from}to{e_to},a:all&start={start}")
            
            driver.get(url)
            time.sleep(2.5)

            # [핵심 수정] span 태그 안에 '네이버뉴스'라는 텍스트가 있는 요소를 찾습니다.
            # 그 후, 클릭 가능한 조상 <a> 태그를 찾아 클릭합니다.
            news_buttons = driver.find_elements(By.XPATH, "//span[contains(text(), '네이버뉴스')]/ancestor::a")
            
            print(f"[Page {page+1}] '네이버뉴스' 링크 {len(news_buttons)}개 발견")

            main_window = driver.current_window_handle

            # collect_article_urls.py 내 루프 부분 수정
            for btn in news_buttons:
                try:
                    # 일반적인 btn.click()이 작동하지 않을 때, 
                    # 브라우저에게 "이 요소를 직접 클릭해!"라고 JS 명령을 내립니다.
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(2) # 새 창이 뜰 때까지 충분히 대기

                    all_windows = driver.window_handles
                    if len(all_windows) > 1:
                        driver.switch_to.window(all_windows[-1])
                        
                        # 주소창에서 드디어 '진짜 주소'를 가로챕니다.
                        curr_url = driver.current_url
                        oid, aid = extract_oid_aid(curr_url)
                        
                        if oid and aid:
                            if curr_url not in seen_urls:
                                seen_urls.add(curr_url)
                                result["articles"].append({"url": curr_url, "oid": oid, "aid": aid})
                                print(f"   [수집성공] {oid}-{aid}")

                        driver.close() # 기사 탭 닫기
                        driver.switch_to.window(main_window) # 검색 결과 탭으로 복귀
                except Exception as e:
                    print(f"   [클릭오류] {e}")
                    continue
                
            if not news_buttons: break
                
    finally:
        driver.quit()

    return result