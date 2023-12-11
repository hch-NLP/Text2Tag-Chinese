import requests
from text_parsing.get_content import get_Word,get_PDF,get_Json,get_Text
from video2text.video2text import video2textImpl
from image2text.OCR2Text.api.OCR2text_API import img2textImpl
from speech2text.speech2text import speech2textImpl
from LAC import LAC
def get_tag(doc):#利用UIE框架完成实体标签的识别
    url = 'http://172.20.14.51:5000/ner/' + '?text='
    #doc= "2022年9月23日，宁波的红艳姐姐说最近都没有任务，每天玩腾讯公司的王者荣耀排位赛都是玩到禁赛为止！"
    res = requests.get(url + doc).text
    return res
def  get_key_info_POS(doc):#利用LAC工具完成实体识别
    # 装载词语重要性模型
    tag={}
    POS=['PER','LOC','ORG','TIME','nr','ns','nt','nz','nw','n','vn','v'] #定义全部实体类型和核心类词性
    _POS = ['PER', 'LOC', 'ORG','nr','ns','nt','nz','nw']#定义加权实体及词性
    lac = LAC(mode='rank')
    rank_result = lac.run(''.join(doc))
    print(rank_result)
    if len(rank_result)==0:
        return []
    for index in range(0,len(rank_result[0])):
        if rank_result[1][index] in POS:
            if  rank_result[1][index] in _POS:
                if rank_result[0][index] not in tag.keys():
                    tag[rank_result[0][index]] = 2
                else:
                    tag[rank_result[0][index]] = tag[rank_result[0][index]] + 2
            else:
                if rank_result[0][index] not in tag.keys():
                    tag[rank_result[0][index]] = 1
                else:
                    tag[rank_result[0][index]] = tag[rank_result[0][index]] + 1
    return dict((key, value) for key, value in sorted(tag.items(), key=lambda x: x[1], reverse=True))

def  get_key_info_L2(doc):#利用LAC工具完成词语重要性排序并做2级过滤
    # 装载词语重要性模型
    tag={}
    lac = LAC(mode='rank')
    rank_result = lac.run(''.join(doc))
    if len(rank_result)==0:
        return []
    for index in range(0,len(rank_result[0])):
        if rank_result[2][index]>=2:
            if rank_result[0][index] not in tag.keys():
                tag[rank_result[0][index]]=1
            else:
                tag[rank_result[0][index]] = tag[rank_result[0][index]]+1
    return dict((key, value) for key, value in sorted(tag.items(), key=lambda x: x[1], reverse=True))

def  get_key_info_L3(doc):#利用LAC工具完成词语重要性排序并做3级过滤
    # 装载词语重要性模型
    tag={}
    lac = LAC(mode='rank')
    rank_result = lac.run(''.join(doc))
    if len(rank_result)==0:
        return []
    for index in range(0,len(rank_result[0])):
        if rank_result[2][index]>=3:
            if rank_result[0][index] not in tag.keys():
                tag[rank_result[0][index]]=1
            else:
                tag[rank_result[0][index]] = tag[rank_result[0][index]]+1
    return dict((key, value) for key, value in sorted(tag.items(), key=lambda x: x[1], reverse=True))
if __name__ == '__main__':
    print('<普通字符串内容及标签提取>')
    tags = get_key_info_POS(doc='Test:卡尔普陪外孙玩滑梯。')
    #tags=get_key_info_POS(doc='2022-23赛季的CBA联赛结束后，中国男篮将在六月下旬重新集结， 备战将在八月底进行的男篮世界杯。')
    print(tags)
    # print('<文本文档内容解析及标签提取>')
    # texts = get_Word(filename='C:/Users/lenovo/桌面/数据需求说明文档.docx')
    # tags = get_key_info_POS(doc=texts)
    # print(tags)
    # print('<音频内容解析及标签提取>')
    # tags = get_key_info_POS(doc=speech2textImpl(speechpath='C:/Users/lenovo/桌面/000001.wav'))
    # print(tags)
    # print('<图片内容解析及标签提取>')
    # tags = get_key_info_POS(doc=img2textImpl(imgpath='F:/pycharm/data/Mutimodal2Text/image2text/OCR2Text/data/sg.jpg'))
    # print(tags)
    # print('<视频内容解析及标签提取>')
    # 视频转文本标签
    # tags = get_key_info_POS(
    #     doc=video2textImpl(video_path='F:/pycharm/data/Mutimodal2Text/video2text/data/videos/demo0.flv'))
    # print(tags)

