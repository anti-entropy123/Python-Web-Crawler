# coding: utf8

import jieba
import jieba.posseg
import wordcloud
import snownlp
import re
import imageio
import pickle


def read_source_text_file(text: str = None, file: str = None):
    '''过滤掉字母, 数字, 不可见字符等'''
    txt = ''
    with open(file, 'r', encoding='utf8') as f:
        txt = f.read()
    re.sub(r'[0_9a_zA_Z\t\n ]*', ' ', txt)
    # 将此处的处理结果持久化存储至硬盘, 方便调试, 避免多次重复此步骤耗费时间. 下同
    # with open('result_read_source_text_file.txt', 'wb', encoding='utf8') as f:
    #     pickle.dump(txt, f)
    return txt


def split_text2words(text: str):
    '''利用分词器, 将整段文本分解为词汇'''
    words = jieba.posseg.cut(text)
    with open('result_split_text2words.txt', 'wb', encoding='utf8') as f:
        pickle.dump(words, f)
    return words


def useful_word_filter(words):
    '''去掉没用的词汇, 比如时间词, 副词, 还有'豆瓣'这种出现频率高但是没用的词'''
    wordlist = []
    for word in words:
        # 词性过滤
        if word.flag in ['f', 'm', 'v', 'nt', 'r', 'c', 'd']:
            pass
        # 无关词过滤
        elif word.word in ['豆瓣', '小说', '平装', '王德威']:
            pass
        # 感情色彩分析
        elif snownlp.SnowNLP(word.word).sentiments > 0.7:
            wordlist.append(word.word)
    # 以上这些可以用一行代码表示:
    # wordlist = [word.word if not(word.flag in ['f', 'm', 'v', 'nt', 'r', 'c', 'd'] and word.word in ['豆瓣', '小说', '平装', '王德威'] and snownlp.SnowNLP(word.word).sentiments <= 0.7) else '' for word in words]
    # with open('result_useful_word_filter.txt') as f:
    #     pickle.dump(wordlist, f)
    return wordlist


def generate_word_cloud(wordlist: str):
    '''生成词云图片'''
    back = imageio.imread('./background.jpg')
    w = wordcloud.WordCloud(
        background_color='white',  # 背景色
        font_path='STKAITI.TTF',  # 字体
        mask=back,  # 图片形状
        scale=5  # 字间距
    )
    w.generate(wordlist)
    w.to_file('output.png')


if __name__ == "__main__":
    # ! 此处文件名与爬虫所输出文件名保持一致
    text = read_source_text_file(file='./output.txt')
    words = split_text2words(text)
    wordlist = useful_word_filter(words)
    wordlist = ' '.join(wordlist)
    generate_word_cloud(wordlist)
