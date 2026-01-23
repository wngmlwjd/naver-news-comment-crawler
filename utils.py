import re

press_dict = {
    # 지상파 / 종합편성채널
    "MBC": "214", "KBS": "056", "SBS": "055", "OBS": "075",
    "JTBC": "437", "TV조선": "448", "채널A": "449", "MBN": "057", "YTN": "052", "연합뉴스TV": "422",
    # 주요 일간지
    "조선일보": "023", "중앙일보": "025", "동아일보": "020", "문화일보": "021", 
    "경향신문": "032", "한겨레": "028", "한국일보": "469", "서울신문": "081", "세계일보": "022",
    # 경제지
    "매일경제": "009", "한국경제": "015", "서울경제": "011", "헤럴드경제": "016", 
    "파이낸셜뉴스": "014", "아시아경제": "277", "머니투데이": "008", "이데일리": "018",
    # 통신사 / 기타
    "연합뉴스": "001", "뉴시스": "003", "뉴스1": "421", "노컷뉴스": "079", "오마이뉴스": "047",
    # IT / 기술
    "전자신문": "030", "아이뉴스24": "031", "디지털데일리": "138", "블로터": "293", "ZDNetKorea": "092"
}

def extract_oid_aid(url):
    if not url: return None, None
    m = re.search(r'article/(\d+)/(\d+)', url)
    if m: return m.group(1), m.group(2)
    return None, None

def save_articles_to_txt(data, filepath):
    dir_name = os.path.dirname(filepath)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# 검색어: {data['keyword']}\n")
        f.write(f"# 기간: {data['start_date']} ~ {data['end_date']}\n")
        f.write(f"# 총 수집 기사 수: {len(data['articles'])}\n")
        f.write("-" * 80 + "\n")
        f.write("언론사코드(OID)\t기사번호(AID)\t기사연결URL\n")
        f.write("-" * 80 + "\n")

        for a in data["articles"]:
            # OID, AID, 전체 URL 순서로 저장
            f.write(f"{a['oid']}\t{a['aid']}\t{a['url']}\n")