import os
from os import path
import re
import json
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape
# import logging
# logging.basicConfig(filename="autotrans.log",level=logging.INFO)
# logger = logging.getLogger(__name__)
import toml
import pandas as pd
import deepl
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

config_path = os.path.join(os.path.dirname(__file__), "config.txt")
with open(config_path, "a+") as f:
    f.seek(0)  # 移动文件指针到文件开头
    config = toml.load(f)

    model = config.get("Model")
    api_key = config.get("Model_API_key")
    deepl_auth_key = config.get("DeepL_API_key") # 5225af3e-9652-80ce-c74e-307ead3e9880:fx

    if model == 'GPT (OpenAI)':
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=api_key)
    elif model == 'Claude (Anthropic)':
        from langchain_anthropic  import ChatAnthropic
        llm = ChatAnthropic(model_name="claude-3-5-haiku-latest", api_key=api_key)
    elif model == 'Gemini (Google)':
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro-002', api_key=api_key)

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    nltk.download('punkt')
    nltk.download('wordnet')

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="AutoTrans")

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)



cwd = path.abspath(path.dirname(__file__))
templates = Jinja2Templates(directory=cwd)
app.mount("/static", StaticFiles(directory=cwd+"/static"), name="static")
chat_bot = None

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def to_json(text, paragraph_segment, paragraph_start=1):
    # Split the text into paragraphs
    if paragraph_segment:
        text = text.split("\n\n")
        text = {f"p_{paragraph_start+i}": text[i] for i in range(len(text))}

    # Convert the text to JSON format
    json_data = json.dumps({"article": text}, ensure_ascii=False, indent=4)
    return json_data

def fill_prompt(prompt, data):
    # make the key-value pairs in the data dict available as variables
    locals().update(data)
    # fill in the prompt with the data
    for match in re.findall(r"@.*?@", prompt):
        executed = eval(match[1:-1])
        prompt = prompt.replace(match, executed)
    return prompt

def LLMchat(prompt_template, data, structure):
    print('Received chat request.', flush=True)

    prompt = fill_prompt(prompt_template, data)
    structured_llm = llm.with_structured_output(structure)

    # 发送消息到 ChatGPT
    response = dict()

    while True:
        print('\nsending prompt:\n', truncate_string(prompt, 250) + '\n\n...\n...\n\n' + truncate_string(prompt, -250) + '\n')
        response_cur = structured_llm.invoke(prompt).content

        print(response_cur)

        # 如果不符合json要求，尝试截断后转为json

        for key in structure.keys():
            response[key] = response_cur[key]
        else:
            break

    print('Chat done.')
    return response


class SummaryRequest(BaseModel):
    text: str

@app.api_route('/summary', methods=['POST'])
def summarize(req: SummaryRequest):
    print('Summarization started.')
    text = to_json(req.text, paragraph_segment=False)






class TranslationRequest(BaseModel):
    text: str
    target_lang: str
    source_lang: str
    annotations: str

@app.api_route('/translate', methods=['POST'])
def translate(req: TranslationRequest):
    print('Translation started.')
    escaped_annotations = re.sub(r'>([^<>]+)<', lambda m: f'>{escape(m.group(1))}<', req.annotations) # escape some characters for the parsing issue
    collection = parseString(escaped_annotations).documentElement
    # 生成翻译参考词汇表
    entries = {}
    if glossary := collection.getElementsByTagName("翻译词汇表")[0].firstChild:
        for pair in glossary.data.split(';'):
            pair = pair.strip()
            if len(pair) > 0:
                k,v = pair.split(':')
                k = k.strip()
                v = v.strip()
                entries[k] = v
    if untranslatable := collection.getElementsByTagName("不可译项")[0].firstChild:
        for k in untranslatable.data.split(';'):
            k = k.strip()
            if len(k) > 0:
                entries[k] = k

    if len(entries) == 0:
        entries = {'none': 'none'}

    # 生成翻译参考上下文
    context = re.sub(r'<翻译词汇表>.*?</翻译词汇表>', '', req.annotations, flags=re.S)
    context = re.sub(r'<不可译项>.*?</不可译项>', '', context, flags=re.S)
    context = context.replace('<注释>','').replace('</注释>','').strip()

    # 建立临时词汇表
    translator = deepl.Translator(deepl_auth_key)
    temp_glossary = translator.create_glossary(
        "temp",
        source_lang="EN",
        target_lang="ZH",
        entries=entries,
    )
    glossary_id = temp_glossary.glossary_id
    print('Glossary created.')

    # 开始翻译
    translator = deepl.Translator(deepl_auth_key)
    result = translator.translate_text(req.text, 
        source_lang=req.source_lang, target_lang=req.target_lang, 
        glossary=glossary_id, context=context)

    print('Translation done.')

    # 删除临时词汇表
    translator.delete_glossary(glossary_id)
    print('Glossary deleted.')

    return result.text

class LLMRequest(BaseModel):
    prompt: str
    completion_mark: str
    new_chat: bool
    close: bool

# 截取字符串，保留给定位置pos最近的换行符前/后的部分
def truncate_string(s, pos):
    if len(s) <= pos:
        return s
    
    # 查找pos前后的最近换行符
    before_newline = s[:pos].rfind('\n')
    after_newline = s[pos:].find('\n')
    
    # 返回最近的换行符前的部分
    return s[:before_newline] if (pos > 0 and before_newline != -1) else s[pos+after_newline:] if (pos < 0 and after_newline != -1) else s

@app.api_route('/LLMchat', methods=['POST'])
def LLMchat(req: LLMRequest):
    print('Received chat request.', flush=True)

    prompt = req.prompt
    print('\nsending prompt:\n', truncate_string(prompt, 250) + '\n\n...\n...\n\n' + truncate_string(prompt, -250) + '\n')
    # 发送消息到 ChatGPT
    response = ''
    finished_check = lambda x, response: x in response if x!='' else True

    pattern = re.compile(r'<(.*?_)(\d+)>(.*?)<\/\1\2>', re.DOTALL)
    prompt_paragraph_last = max([int(idx) for _, idx, text in pattern.findall(prompt)])
    
    while True:
        response_cur = llm.invoke(prompt).content
        print('\nresponse_cur:\n', truncate_string(response_cur, 250) + '\n\n...\n...\n\n' + truncate_string(prompt, -250) + '\n')
        
        if len(pattern.findall(response_cur)) > 0:
            if '[原文]' in response_cur and '[机翻]' in response_cur:
                response += ''.join([f'<p_{idx}>{text.split("[修正]")[-1][1:]}</p_{idx}>\n' 
                    for _, idx, text in pattern.findall(response_cur)])
            else:
                response += ''.join([f'<p_{idx}>{text}</p_{idx}>\n' for _, idx, text in pattern.findall(response_cur)])

            if finished_check(req.completion_mark, response):
                break
            else:
                output_paragraph_last = max([int(idx) for _, idx, text in pattern.findall(response_cur)])
                n = output_paragraph_last + 1
                prompt = re.sub(r"(<\*任务介绍\*>\n## 目标)([\s\S]*)", 
                            lambda m: m.group(1) + re.sub(r"<p_1>", f"<p_{n}>", 
                                            re.sub(r"</p_1>", f"</p_{n}>", 
                                            re.sub(r"<p_2>", f"<p_{n+1}>", 
                                            re.sub(r"</p_2>", f"</p_{n+1}>", m.group(2))))), 
                            prompt)
        else:
            response += response_cur
            break

    print('Chat done.')
    return response

class GlossaryRequest(BaseModel):
    article: str

@app.api_route('/access_glossary', methods=['POST'])
def access_glossary(req: GlossaryRequest):
    article = req.article
    # Initialize the lemmatizer
    lemmatizer = WordNetLemmatizer()
    # Tokenize and lemmatize the article text
    tokens = word_tokenize(article.lower())  # Tokenize and convert to lower case
    lemmatized_article = ' '.join([lemmatizer.lemmatize(token) for token in tokens])

    glossary = pd.read_csv('https://docs.google.com/spreadsheets/d/1cHl0FzJkc8-_LENPcz1ZDLlk03ZgnAlkbJnPrHyzaYg/export?gid=0&format=csv')
    terms = set(glossary.Term)

    # find the terms in the article
    current = '| 英文 | 领域 | 翻译 |\n|---|---|---|\n'
    for term in terms:
        if isinstance(term, str) and len(term) > 0:
            # Lemmatize the target expression (which could be a MWE)
            target_tokens = word_tokenize(term.lower())
            target_lemma_expression = ' ' + ' '.join([lemmatizer.lemmatize(token) for token in target_tokens]) + ' '
            if target_lemma_expression in lemmatized_article:
                group = glossary[glossary.Term==term]
                for idx, row in group.iterrows():
                    category = row.Category
                    if pd.isna(category):
                        category = '\t'
                    current += f'| {group.Term.iloc[0]} | {category} | {row.Translation} |\n'

    print('Glossary accessed.')
    return current


def combine_articles(texts, languages, names, sentence_segment):
    if len(languages) == 1:
        languages = [languages[0] for i in range(len(texts))]
    if len(names) == 1:
        names = [names[0] for i in range(len(texts))]

    new_texts = dict()
    # find all matches to groups
    pg_pattern = re.compile(r"<p_(\d+)>\n{0,}([\s\S]*?)\n{0,}<\/p_\d+>")
    for text, language in zip(texts, languages):
        for pg in pg_pattern.finditer(text):
            
            pg_idx, content = int(pg.group(1)), pg.group(2).strip()
            if pg_idx not in new_texts:
                new_texts[pg_idx] = []
            
            if '<s_1>' in content:
                matches = re.findall(r'<(s_\d+)>(.*?)</\1>', content, flags=re.DOTALL)
                content = [sent for tag, sent, *_ in matches]
            elif sentence_segment:
                if language == 'chinese':
                    # Regular expression to match sentence-ending punctuation
                    pattern = re.compile(r'(?<=[。！？])')
                    # Split text using the pattern
                    sentences = pattern.split(content)
                    # Remove any empty strings from the result
                    content = [sentence.strip() for sentence in sentences if sentence.strip()]
                else:
                    content = nltk.sent_tokenize(content, language=language)

            new_texts[pg_idx].append(content)

    version_number = len(names)
    xml = '<文章>\n'
    for pg_idx, versions in new_texts.items():
        xml += f"<p_{pg_idx}>\n"

        if sentence_segment:
            # Check if the number of sentences is the same in all versions
            num_sentences = len(versions[0])
            if not all(len(version) == num_sentences for version in versions):
                # combine the sentences in each version
                versions = [[' '.join(version)] for version in versions]
                num_sentences = 1
            
            for sent_idx in range(num_sentences):
                xml += f"\t[s_{sent_idx+1}]:\n"

                versions_ = [version[sent_idx] for version in versions]
                names_ = names
                if len(names_[0]) > 0:
                    if len(set(names)) == 1:
                        versions_ = set(versions_)
                        names_ = [f'{names[0]}_{i+1}' for i in range(len(versions_))]
                    for v_name, v_sent in zip(names_, versions_):
                        xml += f"\t\t[{v_name}]: {v_sent}\n"
                else:
                    for v_sent in versions_:
                        xml += f"\t\t{v_sent}\n"
        else:
            names_ = names
            if len(names_[0]) > 0:
                for v_name, v_pg in zip(names_, versions):
                    xml += f"\t[{v_name}]: {v_pg}\n"
            else:
                for v_sent in versions:
                    xml += f"\t\t{v_sent}\n"

        xml += f"</p_{pg_idx}>\n"
    xml += '</文章>'

    return xml

import re
# 递归函数：将XML字符串解析为字典
def xml_to_dict(xml_string):
    xml_string = xml_string.strip('\n')
    # 匹配标签对
    if re.search(r'\s*<.*?>\n', xml_string): # 如果是成对xml标签
        # 正则表达式：1. 匹配<xx>的内容； 2. 匹配 <xx>...</xx> 之间的内容
        matches = re.findall(r'<(.*?)>(.*?)</\1>', xml_string, flags=re.DOTALL)
        return {tag.strip()+'|xml': xml_to_dict(content) 
                    for tag, content in matches}
    elif re.search(r'\s*\[.+?\]:', xml_string): # 如果是键值对
        # 正则表达式：1. 匹配[xx]:的内容； 2. 匹配 [xx]: 之后的所有内容，直到下一个 [xx]: 、</xx>、或文本结束
        matches = re.findall(r"\[(.+?)\]:\s*(.+?)(?=(\s*\[.+?\]:)|(\s*$)|(\s*</))", xml_string, flags=re.DOTALL)
        return {tag.strip()+'|kv': xml_to_dict(content) 
                    for tag, content, *_ in matches}
    else: # 如果是普通单行，则返回空字符串（或处理为叶节点）
        return xml_string.strip()

# 递归函数：将字典解析为XML字符串
def dict_to_xml(data, level=0):
    indent = '\t'*level
    # print(data)
    if isinstance(data, str):
        return indent + data # 引进替代换行符，避免被concat合并误伤
    elif isinstance(data, list):
        return indent + indent.join(data) # 引进替代换行符，避免被concat合并误伤

    xml_string = ""
    for idx, (key, value) in enumerate(data.items()):
        tag, tag_type = key.lstrip().split('|')
        sub_content = dict_to_xml(value, level+1)
        print(sub_content)
        if tag_type == 'xml':
            xml_string += f"{indent}<{tag}>\n{sub_content}\n{indent}</{tag}>\n"
        elif tag_type == 'kv':
            xml_string += f"{indent}[{tag}]:\n{sub_content}\n"
                
    return xml_string

# 
def dict_filter(data, operations, level=0):
    if isinstance(data, str):
        return data
    
    operation = operations.split(',')[level]

    if operation[0] == '+':
        if len(operation) == 1:
            return {key: dict_filter(value, operations, level+1) for key, value in data.items()}
        elif len(operation) > 1:
            return {key: dict_filter(value, operations, level+1) for key, value in data.items() if key.split('|')[0] == operation[1:]}
    if operation[0] == '-':
        if len(operation) == 1:
            li = [dict_filter(value, operations, level+1) for key, value in data.items()]
            if isinstance(li[0], str) and operations.split(',')[-1] == 'concat':
                return ' '.join(li)
        elif len(operation) > 1:
            li = [dict_filter(value, operations, level+1) for key, value in data.items() if key.split('|')[0] == operation[1:]]
            if len(li) == 1:
                li = li[0]
        return li

# 确保缩进量是4的倍数
def standardize_indentation(text):
    lines = text.splitlines()
    indents = set()

    # 统计所有缩进量
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line:  # 忽略空行
            indent = len(line) - len(stripped_line)
            indents.add(indent)

    indents_map = {indent: ' '*i*4 for i, indent in enumerate(indents)}
    
    # 标准化缩进
    standardized_lines = []
    for line in lines:        
        stripped_line = line.lstrip()
        if stripped_line:
            indent = len(line) - len(stripped_line)
            standardized_lines.append(indents_map[indent] + stripped_line)
    
    return "\n".join(standardized_lines)

def xml_reformat(xml, operations):
    if "<文章>" not in xml_string:
        xml_string = "<文章>" + xml_string + "</文章>"
    xml_dict = xml_to_dict(xml_string)
    xml_dict = dict_filter(xml_dict, operations) # 去除、筛选某些层级
    xml_string = dict_to_xml(xml_dict)
    # xml_string = dict_to_xml(xml_dict, operations) # 去除、筛选某些层级
    xml_string = standardize_indentation(xml_string) # 去除某些过度的缩进
    xml_string = xml_string.replace('྾', '\n') # 把dict_to_xml这一步引进的替代换行符改回来
    return xml_string