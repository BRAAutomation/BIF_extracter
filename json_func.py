import json, os

WORKING_DIR = "./test/"

def save_to_json(data,dir_name,name):
    if not os.path.exists(WORKING_DIR + dir_name):
        os.mkdir(WORKING_DIR + dir_name)

    with open(WORKING_DIR + dir_name + '/' + name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def extract_brain_regions(text):
    # "answer" の部分を取り出す
    start = text.find("==answer==") + len("==answer==")
    answer_part = text[start:].strip()

    # クォートで囲まれた部分（脳の領域の名前）を抽出
    regions = [region.strip('"') for region in answer_part.split(",")]

    # JSON 形式で出力
    return json.dumps({"Brain Regions": regions}, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    pass
