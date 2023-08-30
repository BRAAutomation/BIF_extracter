import os, sys, re
import platform
import json, ast
import prompt
import json_func

import openai
import chromadb
import langchain

from prompt_ver2 import agentA, agentB, agentC, answer_format_A, answer_format_B, answer_format_C
from json_func import extract_brain_regions, save_to_json, WORKING_DIR

from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader

# OPENAI_APIKEY = "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"
OPENAI_APIKEY = "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"

#Agent A
def run_Agent_A(llm,pages,dir_name):
    prompt_template = PromptTemplate.from_template(" {agent} the article is below. {content}")

    merged = []; region_pageNo_dict = {}
    for i,page in enumerate(pages):
        answer = llm(prompt = prompt_template.format(agent=agentA, content=page.page_content) + answer_format_A)
        match = re.search(r'(\[.*?\])', answer)
        if match: extracted_list = match.group(1)
        ext_list = ast.literal_eval(extracted_list)
        merged += ext_list

        # ページ番号とセットで脳領域名を記録（エージェントBにて使用）
        for region in ext_list:
            if region in region_pageNo_dict:
                region_pageNo_dict[region].append(i)
            else:
                region_pageNo_dict[region] = [i]

    brain_region_list = list(set(merged))
    brain_region_list = sorted(brain_region_list, key=merged.index)

    data = {"Brain Regions": brain_region_list}
    save_to_json(data,dir_name,'brain_regions.json')
    save_to_json(region_pageNo_dict,dir_name,'region_pageNo.json')

    return brain_region_list

#Agent B
def run_Agent_B(llm,pages,dir_name):
    with open(WORKING_DIR + dir_name + '/region_pageNo.json', 'r') as file:
        data = json.load(file)
    prompt_template = PromptTemplate.from_template(" {agent} the article is below. {content}")
    find_descrip_prompt = PromptTemplate(input_variables=["region_name","content"],template = agentB + " the article is below. {content}")

    final_list = {}
    for region, values in data.items():
        print(region)
        related_pages = ""
        for value in values[:3] :
            related_pages += pages[value].page_content
        answer = llm(prompt = find_descrip_prompt.format(region_name = region, content = related_pages) + answer_format_B)
        result = json.loads(answer)
        for item in result:
            if item["connection description"] == "YES": final_list[region] = result
    save_to_json(final_list,dir_name,'connection.json')

#Agent C
def run_Agent_C(llm,pages,dir_name):
    prompt_template = PromptTemplate.from_template(" {agent} the article is below. {content}")
    first_few = pages[0].page_content + pages[1].page_content + pages[2].page_content
    answer = llm(prompt = prompt_template.format(agent=agentC, content=first_few))
    save_to_json(json.loads(answer),dir_name,'metadata.json')

# Main function
if __name__ == "__main__":
    pdf_path = sys.argv[1]
    pdf_name = os.path.basename(pdf_path)
    dir_name = pdf_name.replace('.pdf', '')

    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    llm = OpenAI(openai_api_key=OPENAI_APIKEY,model_name="gpt-4",temperature=0)

    run_Agent_A(llm,pages,dir_name)
    run_Agent_B(llm,pages,dir_name)
    run_Agent_C(llm,pages,dir_name)

