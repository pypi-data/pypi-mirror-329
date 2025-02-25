# -*- coding: utf-8 -*-
import re
from collections import namedtuple

from common.entity.document import DEFAULT_DOCUMENT_AVG_LEN
from common.entity.timeline import Timeline

TIME_SEG = r'[\d半一两二三四五六七八九十]\d{0,3}十?\+?\-?.?[多|年|月|周|天|日|时]\d{0,2}[月|周|天|日]?半?余?\+?前'
PRE_TIME_SEG = r'入院前[\d半一两二三四五六七八九十]\d{0,3}十?\+?\-?.?[多|年|月|周|天|日|时]\d{0,2}[月|周|天|日]?半?余?\+?'
CHINESE_TIME_THESE_DAYS = r'[近昨今当前][天日早晚]'
CHINESE_TIME_SEG = r'[同今去前]年[一二三四五六七八九十]{0,2}\d{0,2}月'
TIME_STAMP = r'(?:\d{4}[年|\-|.|/][ ]?\d{1,2}[月|\-|.|/][ ]?\d{1,2}日?|\d{4}[年|\-|.|/]\d{1,2}月?|\d{1,2}[月]\d{1,2}日)'
TIME_RANGE_HALF = r'(?:\d{4}[年|\-|.|/]\d{1,2}[月|\-|.|/]\d{1,2}日?|\d{4}[年|\-|.|/]\d{1,2}月?|\d{1,2}[月|.|\-]\d{1,2}日?)'
SPECIAL_DOT_TIME_STAMP = r'(\d{1,2}[\-|.]\d{1,2}|\d{4})'
ABBR_TIME_STAMP = r'2\d[-.]\d\d[-.]\d\d'
TIME_STAMP_RANGE = TIME_RANGE_HALF + '[-~～至]' + TIME_RANGE_HALF
TIME_STAMP_COMPACT = r'20\d{6}'
TIME_STAMP_COMPACT_RANGE = r'\d{4}[-~至]\d{4}'
TIME_YEAR = r'20\d{2}年[初中底末尾终]?'
NOW = r'^[今现为].[2,8]院$'
FROM = r'^.{0,2}自?.{2,6}来$'
MIN_SEG_LEN = 6
BEST_LEN = 15


# 常见的单字和复姓列表
common_surnames = [
    "李", "王", "张", "刘", "陈", "杨", "黄", "赵", "周", "吴",
    "徐", "孙", "马", "朱", "胡", "林", "郭", "何", "高", "罗",
    "郑", "梁", "谢", "宋", "唐", "许", "韩", "冯", "邓", "曹",
    "彭", "曾", "肖", "田", "董", "袁", "潘", "于", "蒋", "蔡",
    "余", "杜", "叶", "程", "苏", "魏", "吕", "丁", "任", "沈",
    "姚", "卢", "姜", "崔", "钟", "谭", "陆", "汪", "范", "金",
    "石", "廖", "贾", "夏", "韦", "傅", "方", "白", "邹", "孟",
    "熊", "秦", "邱", "江", "尹", "薛", "闫", "段", "雷", "侯",
    "龙", "史", "陶", "黎", "贺", "顾", "毛", "郝", "龚", "邵",
    "万", "钱", "严", "赖", "覃", "洪", "武", "莫", "孔", "汤",
    "习", "尤", "苗", "俞", "鲍", "章", "施", "窦", "岑", "乐",
    "成", "詹", "欧阳", "司马", "端木", "上官",  # 复姓
]


def any_match(string, match_list):
    result = []
    for match in match_list:
        if string.find(match) != -1:
            result.append(match)
    return result


def any_match_bool(string, match_list):
    for match in match_list:
        if string.find(match) != -1:
            return True
    return False


def extract_digit(string):
    result = ""
    for ch in string:
        if ch.isdigit():
            result += ch
    return result


def find_all(string, substring):
    positions = []
    start = string.find(substring)

    while start != -1:
        positions.append(start)

        # 更新起始位置为当前子串后面的位置
        start += len(substring)
        next_pos = string[start:].find(substring)
        if next_pos == -1:
            break
        start = next_pos + start

    return positions


# 去掉所有的空格、回车等特殊符号
def remove_special_symbols(string):
    return string.replace("\n", "").replace("\r", "").replace("\b", "").replace("\t", "").replace(" ", "").replace('',
                                                                                                                   '')


def remove_bracket(string):
    return string.replace("(", "").replace(")", "").replace("（", "").replace("）", "")


def has_chinese(sentence):
    for ch in sentence:
        if is_chinese(ch):
            return True
    return False


# ---------------------------功能:判断字符是不是汉字-------------------------------
def is_chinese(char):
    if '\u4e00' <= char <= '\u9fff':
        return True
    return False


def handle_short_sentence(segment_list):
    temp_split_pos_list = []
    i = 0
    while i < len(segment_list) - 1:
        cur_seg_begin, cur_seg_end = segment_list[i]
        next_seg_begin, next_seg_end = segment_list[i + 1]
        if cur_seg_end - cur_seg_begin < BEST_LEN and next_seg_end - next_seg_begin < BEST_LEN:
            temp_split_pos_list.append((cur_seg_begin, next_seg_end))
            i += 2
        else:
            temp_split_pos_list.append((cur_seg_begin, cur_seg_end))
            i += 1
    if i < len(segment_list):
        temp_split_pos_list.append(segment_list[i])
    return temp_split_pos_list


def fetch_text(text, begin, end):
    return text[begin: end]


def fetch_index_and_text(text, begin, end):
    return begin, end, text[begin: end]


def split_text(text, pattern="。", fetch_func=fetch_text):
    if text == '-' or text == '——':
        return []
    split_pos_list = []
    begin = 0
    for match in re.finditer(pattern, text):
        pos = match.start()
        split_pos_list.append((begin, pos))
        begin = pos + 1
    split_pos_list.append((begin, len(text)))
    split_text_list = []
    for begin, end in split_pos_list:
        if begin >= end:
            continue
        split_text_list.append(fetch_func(text, begin, end))
    return split_text_list


def locate_two_word(content, word1, word2, keep_order=True):
    word1_index_list = find_all(content, word1)
    word2_index_list = find_all(content, word2)

    if not word1_index_list or not word2_index_list:
        return None

    index_tuple_list = []
    for word1_index in word1_index_list:
        for word2_index in word2_index_list:
            index_tuple_list.append((word1_index, word2_index))

    index_tuple_list.sort(key=lambda ele: abs(ele[0] - ele[1]))
    if keep_order:
        for index_tuple in index_tuple_list:
            if index_tuple[0] < index_tuple[1]:
                return index_tuple
    return index_tuple_list[0]


def cut_from_back_to_front(text, length):
    if length <= len(text):
        return text[-length:]
    return text


def is_chinese_name(name):
    # 正则表达式检查全部为中文字符
    if not re.match(r'^[\u4e00-\u9fa5]+$', name):
        return False

    # 检查名字长度为2到4个汉字
    if len(name) < 2 or len(name) > 4:
        return False

    # 检查是否以常见姓氏开头
    if any(name.startswith(surname) for surname in common_surnames):
        return True

    return False


START_WITH_WORDS = ['', ' ', '患者', '患儿', '病人', '住院期间', '期间']
PREFIX_WORDS = ['于', '(', '（']
FREQUENCY_LIST = ['次', '颗', '个', '粒', '片', '声', '年', '月', '周', '天', '时', '分', '秒', '小', '碗', '瓶', '餐', '万', '千', '百',
                  '串', '点', '椎', '只', '数']
SYMBOL_LIST = [')', ' ', '、', '）', ':', '：', '(', '（', '/']


def search_special_dot_time(seg):
    def locate_by_keywords(text, keywords, locate_func):
        for keyword in keywords:
            pos = locate_func(text, keyword)
            if pos == -1:
                continue
            if pos < len(text) and text[pos].isdigit():
                return keyword, pos
        return None, -1

    keyword, location = locate_by_keywords(seg, START_WITH_WORDS,
                                           lambda text, keyword: len(keyword) if text.startswith(keyword) else -1)
    if location == -1:
        keyword, location = locate_by_keywords(seg, PREFIX_WORDS,
                                               lambda text, keyword: text.find(keyword) + len(keyword))
    if location == -1:
        return None
    fragment = seg[location: location + MIN_SEG_LEN]
    match = re.search(SPECIAL_DOT_TIME_STAMP, fragment)

    if not match or match.span()[0] != 0:
        return None
    next_ch_pos = match.span()[1]
    if next_ch_pos < len(fragment):
        next_ch = fragment[next_ch_pos]
        check_flag = False
        if keyword == '(' or keyword == '（':
            if next_ch in SYMBOL_LIST:
                check_flag = True
        else:
            if next_ch in SYMBOL_LIST or (is_chinese(next_ch) and next_ch not in FREQUENCY_LIST):
                check_flag = True

        if not check_flag:
            if (keyword == '' or keyword == ' ') and any_match_bool(seg, ['：', ':']):
                return TimeMatch(location, match.group())
            return None

    return TimeMatch(location, match.group())


TimeMatch = namedtuple('TimeMatch', ['timePos', 'timeText'])


def parse_match(match):
    if match:
        return TimeMatch(match.span()[0], match.group())
    return None


SEARCH_TIME_FUNC_DICT = {
    '时间范围': [
        lambda seg: parse_match(re.search(TIME_STAMP_RANGE, seg)),
        lambda seg: parse_match(re.search(TIME_STAMP_COMPACT_RANGE, seg))
    ],
    '时间戳': [
        lambda seg: parse_match(re.search(TIME_STAMP, seg)),
        lambda seg: parse_match(re.search(TIME_STAMP_COMPACT, seg)),
        search_special_dot_time,
        lambda seg: parse_match(re.search(TIME_YEAR, seg)),
        lambda seg: parse_match(re.search(ABBR_TIME_STAMP, seg))
    ],
    '时间段': [
        lambda seg: parse_match(re.search(TIME_SEG, seg)),
        lambda seg: parse_match(re.search(PRE_TIME_SEG, seg)),
        lambda seg: parse_match(re.search(CHINESE_TIME_THESE_DAYS, seg)),
        lambda seg: parse_match(re.search(CHINESE_TIME_SEG, seg))
    ],
    # '入院时间': [
    #     lambda seg: parse_match(re.search(NOW, seg)),
    # ],
    # '模糊时间': [
    #     lambda seg: parse_match(re.search(FROM, seg)),
    # ]
}


def search_time(seg):
    for time_type, search_time_func_list in SEARCH_TIME_FUNC_DICT.items():
        best_time_match = None
        for search_func in search_time_func_list:
            time_match = search_func(seg)
            if not time_match:
                continue
            if time_match.timePos <= 5:
                return time_type, time_match

            if not best_time_match or time_match.timePos < best_time_match.timePos:
                best_time_match = time_match
        if best_time_match:
            return time_type, best_time_match
    return None, None


def cut_by_time(text, admission_time=None, avg_len=None):
    def check_sentence_len(sentence_len):
        if not avg_len:
            return True
        return sentence_len < avg_len
    seg_list = split_text(text, "。|,|，|；|\n", fetch_func=fetch_index_and_text)
    results = []

    for start_index, end_index, seg in seg_list:
        last_timeline = results[-1][2] if results else None
        timeline = None
        time_type, time_match = search_time(seg)
        if time_match:
            timeline = Timeline(time_match.timeText, time_type, admission_time, last_timeline)
            timeline.start_index = time_match.timePos + start_index
            timeline.end_index = timeline.start_index + len(time_match.timeText)
            timeline.content = seg
        if timeline:
            results.append((start_index, end_index, timeline))
        else:
            if results and check_sentence_len(results[-1][1] - results[-1][0]):
                results[-1] = (results[-1][0], end_index, results[-1][2])
            else:
                results.append((start_index, end_index, last_timeline))

    return results

# content = '2016.12因“发作性意识障碍2月余”就诊武汉陆军总医院，2016.12.15在全麻下行开颅肿瘤切除术，术中见肿瘤位于左侧颞枕叶交界处，进入约0.5cm即见肿瘤组织，肿瘤呈黄褐色，血供丰富，与周围组织界限不清，质地稍韧，逐步分块切除肿瘤，切除组织体积约4cm×3cm×2cm。术后病理回示：少突胶质细胞瘤（WHOII级）可能性大。基因检测：MGMT启动子无甲基化，1p/19q非联合缺失，IDH1/2无突变，TERT无突变，BRAF无突变。2017.03.03患者来我科查头颅MRI：临床示“左侧颞枕叶少突胶质瘤”术后：左侧颞叶见小片状长T1长T2信号，增强后未见明显强化信号；局部脑膜增厚并强化，硬膜下少量出血。脑室无明显扩大，脑沟、裂、池无明显增宽，中线结构居中。左侧颞枕叶肿瘤术后改变：局部脑膜增厚并强化，硬膜下少量出血。结合病史考虑肿瘤达GTR。2017.03.09开始行替莫唑胺同步放化疗（GTV=5400CGY/20F CTV=50GY/20F，替莫唑胺 75mg/㎡ 150mg po qd d1-30），过程顺利。5.5～5.9、6.3～6.8先后行第一、二周期替莫唑胺辅助化疗（150mg/㎡ 250mg 5/28d）,过程顺利。2017-06-08复查头颅MRI：与前片（2017.3.3）对比示：左侧颞枕叶肿瘤术后改变：局部脑膜增厚情况较前明显好转，硬膜下少量出血已吸收。于7.2～7.6、7.30～8.3、8.30～9.3先后完善第三、四、五周期替莫唑胺辅助化疗（200mg/㎡ 350mg 5/28d），过程顺利，现患者为求进一步诊治来我院，门诊以“脑胶质瘤术后”收入院。        起病以来，患者精神、食欲、睡眠欠佳，大小便正常，体力体重较前下降'
# content = '因“胎膜早破、双胎妊娠、妊娠合并垂体瘤”于2022-05-30 00:34在中心医院剖宫产娩出'
# content = '患者2015年因“反复腹痛伴呕吐2周”就诊海南省人民医院，在全麻下行“剖腹探查，肠套叠手术复位、小肠息肉摘除、空肠部分切除术，术后病理示：Peutz-Jeghers综合征，部分呈绒毛-管状腺瘤样结构，局部腺上皮中-重度不典型增生”，术后给予抗感染、静脉营养后患者好转出院。出院后患者仍有反复阵发性腹痛，休息可缓解，无腹泻、反酸等不适。2019年9月于我院住院行胃镜、结肠镜示：P-J综合征，行胃、肠镜下息肉高频电切除术，术后予以禁食、补液、抗感染、抑酸等治疗，术后恢复良好出院。2020年1月6日再次于我院住院治疗，行双气囊电子小肠镜检查(经口+经肛)检查： 1.P-J息肉病；2.内镜下治疗空肠部分切除术后；3.所见回肠未见明显异常大肠多发息肉。术后予以禁食、补液、抗感染、抑酸等治疗，术后恢复良好出院。07-23 于我院行胃镜、电子结肠镜检查：P-J综合征，均予高频电切除；术后予抑酸护胃、黏膜保护、补液营养支持等治疗，术后患者恢复良好。 2021-08-03 我院双气囊电子小肠镜检查(经口) PJ综合征（高频电切除术），空肠活检病理：符合增生性息肉；2021-08-03我院小肠镜下行小肠息肉切除术，好转出院。自上次出院后患者自觉无腹痛、腹胀，无反酸、嗳气，无恶心、呕吐，无腹泻、解黑便等不适。现患者为进一步诊治返院，门诊以“黑斑息肉综合征”收入我科。自发病以来，病人精神状态一般，体力情况一般，食欲食量一般，睡眠情况一般，体重无明显变化，大便1/天，小便正常。'
# content = '患者诉约2020年底因碰撞后出现右上肢疼痛，当时未重视，后疼痛逐渐加重，伴有活动受限，于12月28日在中医院行右肩关节X线检查提示右侧肱骨上段可见条片状密度增高影，建议进一步检查。今年1月8日行平扫MRI示1.右肱骨中上段肿瘤性病变(a.骨肉瘤，b.滑膜肉瘤)；2.右肩关节囊、肱二头肌长头腱周围滑囊积液。后至武汉同济医院进一步诊治，1月14日胸部CT提示双肺小结节。1月23日行AP方案化疗一周期，化疗后复查CT疗效评价SD。于2月2日行右上肢离断术，术后病理普通型骨肉瘤，主呈骨母细胞型，坏死率60%。术后复查肺部病灶增大。于3月1日行MAP方案化疗一周期。4月6日复查MRI示右侧肩关节及上肢术后改变，右上胸壁肌群及皮下软组织肿胀；右上胸壁软组织内可见结节状等T1长T2信号影，多为淋巴结影。4.7胸壁CT示双肺下叶实性结节，较前相仿，左肺上叶舌段软组织影，较前增大。4月8日完成一周期AI方案化疗，化疗后出现Ⅳ度骨髓抑制，患者因无法耐受化疗中断治疗。自诉约一周前开始出现胸闷不适，伴有咳嗽及胸痛，8月29日来我院门诊行胸部CT示双肺多发占位、部分伴钙化：转移瘤可能；左侧胸腔积液伴左肺下叶通气不良。近三天胸闷明显加重，稍活动有明显胸闷，今来我院行进一步治疗，门诊以“骨肉瘤”收入院。病程中，患者精神，食欲可，睡眠不佳，大小便正常，体力下降，体重减轻。'
# content = '因白细胞过高0302-0307行阿糖胞苷化疗，0310-0317行DAE方案+索拉菲尼化疗，0318行腰椎穿刺术及鞘注，脑脊液未及异常。0414-0423善BM+MRD示MRD15.3%，涂片见13.5%原幼单细胞，考虑骨髓部分缓解。予低剂量MAG方案化疗，期间0413行腰穿，脑脊液未及异常，0509完善BM+MRD示MRD10.6%，涂片见5.5%原幼单细胞，0513-0527行难治复发方案Dec-IDAG第一疗程化疗方案，0616完善骨髓涂片可见1.0%原幼单细胞;MRD检测<0.01%，NUP98-NSD1:融合比例25.64%，结果判定为阳性;FLT3/ITD基因突变为阴性;WT1阴性;0619-0703行Dec-IDAG第二疗程化疗方案，0624骨穿'
# content = '患儿1月余前无明显诱因出现右锁骨肿物，有压痛，右上肢活动无异常，无发热，并逐渐增大，2018年05月30于龙南县人民医院就诊，CT示：右锁骨肿瘤，考虑尤文氏肉瘤，X线提示：右锁骨骨肉瘤可疑？，5-31就诊于我院骨科，于6-4行“右锁骨肿物活检术”，术后病理结果：1、（锁骨内容物）朗格汉斯细胞组织细胞增生症（嗜酸性肉芽肿）；2、（锁骨周围骨膜）为增生的炎性纤维组织；3、（锁骨骨皮质）为骨小梁及增生的纤维组织。6-7骨扫描：1.右侧锁骨明显异常浓聚影，结合临床，考虑为骨嗜酸性肉芽肿，建议定期随访；2.双侧第12肋根呈大致对称性轻度浓聚影，考虑为良性病变可能，建议定期复查；3.骨骼其他部位未见明显异常放射性分布。6-10胸部CT:1、右侧锁骨近中段骨质病变，考虑嗜酸性肉芽肿可能；2、双侧肱骨头改变，考虑嗜酸性肉芽肿；3、右锁骨上窝淋巴结肿大；4、前上纵隔软组织影，考虑未退化胸腺组织；5、隆突下钙化影，考虑淋巴结钙化。于6-11行“右锁骨肿物切除+锁骨重建术”，术后病理：（右侧锁骨肿物）朗格汉斯细胞组织细胞增生症（嗜酸性肉芽肿），6-30开始予Arm A诱导方案化疗，07-09免疫组化：BRAF-V600E(-),07-14行Arm A（2）诱导方案化疗，现为行Arm A（3）诱导方案化疗入院，门诊拟“朗格汉斯细胞组织细胞增生症”收入我可，患儿自起病以来，精神、食欲可，胃纳一般，大小便未见异常，体重无明显减轻。'
# content = '1+周前患者无明显诱因出现双下肢皮疹，大腿及小腿均可见皮疹，色紫红，呈散在对称分布、大小不等、分布不均、边界清楚、略高出皮面，压之不褪色，无发痒，伴轻度乏力，无明显纳差，无双下肢水肿、发热、鼻塞、流涕、头晕、头痛、恶心、呕吐、腹痛、腹泻等症状。于绵阳市中心医院就诊，予以依巴斯汀抗组胺等治疗，小腿皮疹可见明显消退，5+天前，在上诉症状基础上出现中下腹部疼痛，呈持续性绞痛，伴压痛、膝关节疼痛、大腿及小腿肌肉疼痛，无明显恶心、呕吐、反酸、烧心、牙龈出血、血尿、畏寒、发热等不适，2023-10--24于我院门诊就诊完善下腹部CT未见明显异常，予加用颠茄片止痛、醋酸泼尼松片30mg抗过敏，但患者腹痛未见明显好转，今为求进一步诊治故来我院，门诊以“腹型过敏性紫癜”收入我科。自患病来，患者精神、睡眠、饮食尚可，小便正常，诉昨日解大便颜色加深，不排除黑便可能，大便性状及次数正常，体重无明显变化。'
# content = '3月余前（2021-12-05）以“间断发热、咳嗽伴血象异常1月余”为代主诉入住我科。入院后查血常规:白细胞计数25.8×109/L，红细胞计数3.96×1012/L，血红蛋白107g/L，血小板计数394×109/L，中性粒细胞百分数9.9%，淋巴细胞百分数71.6%，中性粒细胞绝对数2.55×109/L；EB病毒DNA<500copies/ml；血片检查:中性分叶核粒细胞4%，淋巴细胞80%，单核细胞2%，分类不明原幼细胞14%，细胞形态分析：1.白细胞数增高；2.粒细胞比值减低；3.成熟红细胞大致正常，计数100个白细胞未见有核红；4.淋巴细胞比值增高；5.可见分类不明细胞占14%；6.血小板散在或成堆易见。12-06行骨髓穿刺术，骨髓分析报告单：1.取材，涂片，染色良好，粒（+）油（+）。2.骨髓有核细胞增生活跃（+），其中粒系缺如，红系占1.5%。3.粒系受抑。4.红系受抑，成熟红细胞轻度大小不等。5、原始血细胞比值增高，占91%，该类细胞大小不等，圆形或椭圆形，胞浆淡蓝色，部分细胞浆内含空泡，染色质疏松，核仁隐约可见，疑似原幼淋巴细胞。6.全片见到巨核细胞85个，血小板成堆易见，形态大致正常。POX:原始血细胞阴性。PAS：原始血细胞可见弱阳性。意见：提示急性淋巴细胞白血病？骨髓白血病免疫分型报告回示：P2占8.88%，为成熟淋巴细胞，表型未见明显异常；P3占88.36%，表达CD19、CD10、CD34、CD20、HLA-DR、CD9、CD123、CD38、CD22、cCD79a，弱表达CD45，部分表达CD2（15.09%）、cIgM（45.63%），不表达CD117、CD7、CD33、CD4、CD3、CD56、CD5、CD8、CD1a、CD13、CD15、CD16、CD11b、cCD3、MPO，为异常原始B淋巴细胞，比例明显高。P5占2.23%，为成熟单核细胞。结果提示：符合急性B淋巴细胞白血病（Pre-B-ALL）。结合患儿临床症状、体征及辅助检查，诊断急性B淋巴细胞白血病明确，12-06开始性泼尼松试验，从足量的25%（10mg）起，根据临床反应逐渐加至足量，同时注意肿瘤溶解综合征的发生，给予充足水化、碱化处理。2021-12-08行二连鞘注，脑脊液常规、生化、脑脊液涂片均未见明显异常，脑脊液白血病微小残留：结果分析：1.5ml脑脊液共检测840个细胞，其细胞浓度为0.56×106个/L。主要为T淋巴细胞，可见3%的CD19+CD10+CD45dim的幼稚B淋巴细胞，不除外白血病细胞。脑脊液微小残留提示可见3%幼稚细胞，但患儿目前暂无相关高危因素，为改善患儿预后，给予调整鞘注频率，治疗及预防中枢神经系统白血病。分别于12-13、12-20、12-17、2022-01-04行三联鞘注，脑脊液常规、生化、脑脊液涂片及白血病微小残留均无异常。白血病56种融合基因：本检测以ABL基因为内对照，报告以融合基因扩增结果的阴阳性为准，检测结论：送检标本未检测到56种基因融合突变（-）。Ph-Like43种相关基因检测报告：送检标本检测到IKZF1基因表达为阳性（+）。IKZF1基因突变检测报告：送检标本检测到IKZF1基因突变为阳性（+）。IKZF1基因表达为阳性，属于高危组危险因素，但最终分组，需结合第33天MDR结果，综合评估，再定最终临床危险程度分层，目前暂升级为中危组。12-13血片检查（第8天）:中性分叶核粒细胞4%，淋巴细胞94%，单核细胞2%，细胞形态分析：1.白细胞数减低；2.粒细胞比值减低；3.成熟红细胞轻度大小不等，偶见畸形，计数100个白细胞未见有核红；4.淋巴细胞比值增高；5.血小板散在或成堆易见，偶见大血小板。第8天外周血涂片未见幼稚细胞，提示泼尼松反应佳。12-13开始给予VDLP方案化疗，12-17染色体核型分析报告单：检验结果：45,XY,dic(9;20)(p13;q11.2)[17]/46，XY[3]；实验诊断提示：此患者标本经过培养后分析20个中期相细胞，其中17个细胞核型存在由9号和20号染色体易位产生的双着丝粒染色体，仍考虑中危。12-24行（第19天）骨髓穿刺术，骨髓细胞学检查：未见幼稚淋巴细胞，白血病残留病灶：未见残存白血病细胞（<10-4）。化疗期间患儿出现骨髓抑制及感染，给予积极抗感染、粒生素升白细胞及输注红细胞等治疗后好转，2022-01-04给予办理出院手续；2022-01-11给予CAML方案化疗，01-13给予三联鞘注，化疗期间出现骨髓抑制及腹泻，给予输注红细胞及血小板、抗感染治疗后好转，2022-01-30办理出院；2022-02-09再次给予CAML方案化疗，02-10患儿应用培门冬酶后出现过敏反应，表现为恶心、呕吐，伴头面部、躯干部散在红色皮疹，伴痒感，伴烦躁、声音嘶哑、口唇及耳廓肿胀，双手及双足轻度水肿，立即给予抗过敏等对症处理，患儿心率渐下降，皮疹渐消退，化疗后出现骨髓抑制，积极应用粒生素并成分输血后好转，02-25办理出院。院外一般情况可，无发热、咳嗽、恶心、呕吐、腹泻、便血等，03-16查血常规：白细胞4.34×109/L，红细胞2.82×1012/L，血红蛋白80g/L，血小板计数159×109/L，中性粒细胞绝对数1.4×109/L，现为进一步化疗来我院，院外新冠肺炎核酸检测阴性，以“急性淋巴细胞白血病”收入我科。自上次住院以来，神志清，精神可，饮食、睡眠可，大小便正常，体重无明显变化。'
# content = '患儿于2019-4-03因“咳嗽1月余，发现颈部肿物8天余。”入院，入院后完善相关检查：T细胞亚群：抑制T细胞诱导亚群 CD4CD45RA 5.90%，余未见明显异常。PET-CT示：1、左侧肩颈部、双侧锁骨上窝、右侧胸小肌和胸大肌深面、纵膈内、右肺门、横隔上、右侧膈肌脚深面及腹膜后区多发淋巴结增大，代谢增高，考虑淋巴瘤侵犯淋巴结，其中前纵膈病灶相互融合与相邻大血管界限不清，并推压纵膈左移，同时沿着右前肋间隙向前胸壁生长侵犯；2、右侧多处胸膜增厚呈条状及结节状，代谢增高，考虑为淋巴瘤侵犯胸膜；右侧胸腔积液；右肺多发片状、斑片状密度增高影，代谢增高，考虑淋巴瘤侵犯右肺；3、全身骨髓和脾脏代谢弥漫性轻度增高，多考虑为反应性增生所致，请结合骨髓活检结果；5、双侧颈部（颈动脉鞘、颌下区）和双侧腋窝多个小淋巴结，左侧腋窝淋巴结代谢轻度增高，多考虑淋巴结炎性增生；6、肝脏增大，代谢未见增高，请结合临床；7、蝶窦慢性炎症；右肺多发慢性炎症；心包稍增厚；8、全身其他部位未见明显异常。入院后予持续水化、舒普深、更昔洛韦、阿奇霉素、伏立康唑抗感染、小剂量地塞米松静滴减瘤治疗（4-4~4-18），期间两次环磷酰胺化学治疗（4-13~4-14）等对症支持治疗，4-15复查EB病毒:FQ_EBV_DNA 7.48E+4copies/mL,肺炎支原体抗体(被动凝集法): MP-Ab 阳性(+)。4-5查骨髓形态学：1.幼淋占2.5%，部分淋巴形态不规则；2.成熟浆细胞易见；骨髓免疫分型（贝肯）：骨髓中存在0.56%CD19+CD5+CD10-的异常成熟B淋巴细胞；融合基因（贝肯）：NPM1-ALK阴性。04-04行超声引导下颈部肿物穿刺行病理活检、胸腔穿刺抽取胸腔积液100ml，气促稍好转，右肺呼吸音可闻及（较对侧减低），胸水液基细胞学：察见异型淋巴细胞。颈部穿刺标本病理：（左侧颈部包块）恶性上皮性肿瘤，结合免疫组化考虑为淋巴上皮样癌；因送检组织局限，尚不能排除胸腺癌。颈部肿物穿刺标本送中山大学附属肿瘤医院病理会诊意见：免疫组化：CD3(-),CD20(-),Ki(约70%+)，CK(+),CK5/6(+),P63(部分+),CD30+(灶+)，CD117(部分+),HCG(-),PLAP(-),SALL-4(-),OCT(-)。原位杂交：EBERs(+)。（左侧颈部包块）结合形态呼免疫组化等结果，病变诊断为低分化癌，可符合淋巴上皮瘤样癌，建议临床查鼻咽、肺及涎腺等，以排除转移瘤可能。遂于04-17行局麻下左侧颈部肿块切除活检术并送病理，术程顺利，病理结果示（左侧颈部LN）淋巴结内见恶性上皮性肿瘤，符合淋巴上皮样癌/或淋巴样上皮样癌转移。排除化疗禁忌症，已于4-23行心电监护下艾素（86mg,静滴，D1）+卡铂(0.15g，静滴，D2-3)+艾坦(1粒，口服，持续)方案化疗以及肌注苯海拉明、口服地塞米松、静滴西咪替丁预防过敏，辅以止吐、护胃、补钙、水化、碱化等对症支持治疗，化疗过程中稍感胸闷、左胸部酸胀及左背部胀痛，无皮肤瘙痒、恶心呕吐等不适，予低流量吸氧好转，完善听力检查，耳鼻喉科会诊意见：患儿无听力下降，无耳鸣，无流脓，无头晕和眩晕不适，声导抗双耳A 型曲线，纯音测听双耳听力正常，耳声发射双耳通过。2019-05-14 胸部正位片 1、上纵隔及右肺门区多发阴影，考虑淋巴瘤，较前缩小。2、两肺炎症，以右肺为著，较前稍吸收。3、左侧PICC管头端约位于上腔静脉区。2019-05-17 双肾、输尿管、膀胱彩超检查 双肾、膀胱未见明显异常。5-15开始予艾素+艾坦+卡铂（本次卡铂加量5-15至5-20）。2019-6-5患儿无明显诱因出现颈部、躯干、四肢散在水疱疹，伴瘙痒，无自觉发热，至我院查血水痘带状疱疹病毒（+）。6-26行第三次艾素+卡铂+艾坦+泰欣生方案化疗，化疗过程顺利，患儿胸闷较前改善，左侧锁骨上肿块较前明显缩小。7-2复查胸片：1、上纵隔及右肺门区多发阴影，符合淋巴上皮样癌，较前略缩小。2、两肺炎症，以右肺为著，较前吸收。3、右侧少量胸腔积液。4、左侧PICC管头端约位于上腔静脉区。2019-07-17因“胸闷”入院，B超示：右侧胸腔探及液性暗区，前后径约6.8cm，内透声差，可见大量带状分隔及肺叶漂浮，不宜定位；左侧胸腔未见明显积液，予舒普深及阿奇霉素抗感染后胸闷好转，7-18开始予泰欣生+氨磷汀+地西他滨+紫杉醇+顺铂+氟尿嘧啶化疗。今日凌晨3点患儿无明显诱因出现鼻衄，伴右上肢伸侧多处皮下瘀斑，院外期间，患儿无发热、皮疹，无胸闷、气促等不适，门诊拟“淋巴结恶性肿瘤”收入院。院外期间，患儿精神可，睡眠可，体力可，大便正常，小便正常.'
# content = '患儿于2018-03-22因咳嗽就诊东莞市东城医院，查血提示：WBC: 3*109/L,NEU:0.2*109/L,LYM：1.7*109/L，HGB:131G/L,PLT:135G/L.3-23至东莞市人民医院查感染二项未见明显异常，血象：WBC: 1.7*109/L,NEU:0.8*109/L,LYM：0.8*109/L，HGB:117,PLT:148.抗O及类风湿因子、EBV定量、流感、结核抗体等、心肝肾功未见异常。肺炎支原体抗体二项（IgM+IgG）均阳性。B 超提示：双侧腹股沟区(左侧41mmX20mm，右侧32mmX14mm)及颈部多发淋巴结肿大（左42mmX23mm,右51mmX22mm）。脾大（约肋下4cm）。遂至我院门诊就诊，拟“淋巴结肿大查因”收入我科，入院完善骨髓穿刺：03-30髓像骨髓增生极度活跃。分类不明细胞：占59%。此部位骨髓提示：AL-未定型（请结合染色质及免疫分型考虑）。流式细胞结果符合急性T淋巴细胞白血病/淋巴母细胞淋巴瘤（T-ALL/LBL）免疫表型。流式细胞术检测结果表明送检标本中CD45弱阳细胞占有核细胞总数约为52.8%，其免疫表型为CD19-，CD10+小部分，CD34+大部分，HLADR-，CD-，CD33+，CD117-，CD56+，CD2+，CD20-，CD22-，sIgm，CD5+，CD4-，CD8-，胞膜CD3-，CD66-，CD36-，CD61-，CD38+，CD7+，CD123-，CD11b+，CD13+，CD15-，CD14-，CD64-，胞内CD79a-，胞内CD22-，胞内Igm，TDT-，胞内CD3+，胞内MPQ-。未检测到AML常见基因突变。染色体核型为45，XY.-5[2]/46，XY[23]。BCR-ABL1(p210)3.890%。甲氨蝶呤用药基因检测提示：该检测者MTHFR-677C＞T为纯合突变型，MTHFR-1298A＞C为野生型。如需使用MTX，建议该患者初始剂量减少40%。巯嘌呤用药基因检测：该检测者TPMT*3(T＞C)为杂合突变型，TPMT*2（C＞G）为野生型。建议巯嘌呤应减量，起始剂量为正常剂量的30%-70%。03-29开始VDLP诱导方案化疗，化疗过程顺利，D19骨髓穿刺： 分类不明原幼稚细胞：占55.0%。MRD>55.97%.BCR/ABL基因阳性。4-24按计划行VDLP第四节化疗，5-1行CAT，化疗过程顺利。（46天）骨髓穿刺检查：ALL治疗后，此部位骨髓提示：ALL-CR。05-28予按计划行加疗化疗（长春地辛、阿糖胞苷、环磷酰胺、6-巯基嘌呤、培门冬酰胺酶）。查白细胞数稍偏低，骨髓检查提示未缓解,故CAM化疗药物足量化疗。46天T-ALL-MRD表型检测：肿瘤细胞约占骨髓有核细胞的0.97%。检测BCR-ABL1（p210）融合基因阳性（+）。（46天）骨髓穿刺检查：ALL治疗后，此部位骨髓提示：ALL-CR。患儿CAM加疗结束，目前骨髓抑制明显，予暂停达沙替尼。 06-19行HDMTX1化疗，化疗过程顺利，脑脊液常规、生化及细胞学检查未见明显异常。42小时甲氨蝶呤药物浓度监测 MTX0.78umol/l。07-02行HDMTX2化疗，脑脊液常规、生化、病理未见明显异常，42h甲氨蝶呤血药浓度为5.27umol/lmol/L，予亚叶酸钙加强解救，66H甲氨蝶呤血药浓度为1.70umol/lmol/L，予亚叶酸钙继续解救。7-17行HDMTX3（MTX减量60%)化疗，辅以水化、碱化、止吐、利尿等对症支持治疗，常规行腰穿脑脊液检查及甲氨蝶呤+阿糖胞苷+地塞米松三联鞘内注射，予亚叶酸钙含漱预防口腔粘膜损害，化疗过程顺利，脑脊液常规、生化及细胞学未见异常。42h甲氨蝶呤血药浓度为1.34umol/l。予亚叶酸钠加强解救。现为返院行HDMTX4化疗入院，遂至我院门诊就诊，拟“急性淋巴细胞白血病”收入我科。患儿上次出院至今，精神、食欲、睡眠一般，大小便正常，体重无明显改变。'
# content = '患儿于2020年9月10日因"发热5天，发现三系减少3天"第一次住院。。\n完善相关检查并行骨髓细胞学检查，骨髓报告示:急性淋巴细胞白血病,免疫分型示B淋巴细胞白血病,白血病融合基因筛查检测出ETV6/RUNX1融合基因阳性，TISH：ETV6/RUNX1易位探针可见非典型融合信号，阳性率为85%。染色体核型：46,XX[4]。诊断为急性淋巴细胞白血病（B淋巴，标危），9月23日开始VDLD方案诱导化疗，病情好转于10月13日出院。2020.10.19-10.22第二次住院治疗，10月19日开始行CAM方案化疗，辅以水化碱化、鞘注化疗及对症支持治疗，因19天MRD2.28%升中危。2020.11.09-2020.12.03第三次住院治疗，11月09日开始行CAM方案化疗，辅以水化碱化。11月29日予行大剂量甲氨蝶呤化疗。并予多拉司琼止吐，输血浆900ml纠正凝血功能，红细胞1单位纠正贫血、输血小板1个治疗量补充血小板等对症支持治疗。2020.12.14~2020.12.18第四次住院，予以甲氨蝶呤化疗，鞘注化疗及对症支持治疗。12.31-01.03第五次住院，12.31予大剂量甲氨蝶呤和鞘注化疗及对症支持治疗。2021.01.15-2021.01.19为行化疗第六次入我院住院治疗，入院后于2021.01.16予以大剂量甲氨蝶呤化疗、鞘注化疗、水化、碱化治疗及对症支持治疗。2021.01.30-2021.02.01第七次住院，予以鞘注化疗，培门冬酶化疗及对症支持治疗。2021.02.10-2021.02.24第八次住院，予巯嘌呤、长春新碱、地塞米松、柔红霉素及鞘注化疗。    =2021.03.15-2021.03.17第九次住院，予以长春新碱、柔红霉素、培门冬酶化疗和鞘注化疗及对症支持治疗。    出院后按化疗表化疗，1天前患儿出现发热，共发热3次，最高体温39.4，无寒战、抽搐，无咳嗽、咳痰、喘息、气促，无呕吐、腹泻，为求诊疗，我院门诊就诊，留观输液科予“头孢曲松”抗感染、补液等治疗，并以“急性淋巴细胞白血病”收住我科。起病以来，患儿精神、食欲尚可，大小便正常。'
# content = "患者潘宇晗，女性，13岁，主因“发现纵膈肿物3天”入院。查体：全身浅表淋巴结未及肿大，无腹痛、腹胀，肠鸣音正常。脊柱无畸形，活动自如。膝腱、跟腱反射存在，巴氏征、克氏征均未引出。入院查无禁忌后，行胸腔置管引流及心包置管引流，待无引流液流出后，复查PET-CT：1.双侧下后颈、锁骨区及纵隔内多发结节及肿物，PET显示明显放射性浓聚，考虑为恶性，恶性淋巴瘤可能性大，邻近组织可疑受累，请结合活检；2.所见体表皮下多发结节，部分PET显像略见放射性浓聚，提示局部代谢增高；3.右侧乳腺上半球似见结节影，PET显示较高放射性浓聚，提示局部代谢增高，请结合乳腺相关检查；以上2、3可疑恶性淋巴瘤，请结合活检。遂行B超引导下穿刺明确病理，病理结果回报：（纵隔肿物穿刺活检）小圆细胞恶性肿瘤，结合免疫组化结果支持为横纹肌肉瘤，FOX01基因FISH检测结果示基因分离基FOX01基因5'端缺失，可诊断为腺泡状横纹肌肉瘤，免疫组化：CK-pan（-），P63（-），CD117（-），CD5（-），CD20（-），CD3（-），TDT（-），CD1a（-），Ki-67（40%+），CD99（-），Vim（+），Syn（-），CgA（-），CD56（+），SALL4（-），ALK（+），CD30（-），LCA（-），Myo-D1（+），Myogenin（+），Desmin（+）。遂行化疗治疗，为建立静脉输液通路于2020-5-26日全麻下行手臂输液港植入术+软组织肿物切除术，术后病理回报：（右腰背部）腺泡状横纹肌肉瘤；免疫组化：Myo-D1（+），Myogenin（+），CD56（+），Ki-67（70%+），CD99（-），ALK（+），Desmin（+）。综合临床考虑诊断为腺泡状横纹肌肉瘤Ⅳ期，随后序贯给予7疗程AVCP-IEV方案化疗，第8疗程IEV方案化疗，化疗过程顺利。化疗后继续予以23次放疗及同步增敏化疗。2021-1-19予以第9周期化疗，具体：长春地辛4mg d1,8+顺铂30mg d1-5+环磷酰胺550mg d1-3，同时予以止吐保肝保心及对症支持治疗。2021-2-18予以第10周期化疗：长春地辛4mg d1,8+顺铂30mg d1-5+环磷酰胺550mg d1-3，同时予以止吐保肝保心及对症支持治疗。化疗后复查：1.与2020.8.3胸部CT比较：前上纵隔内软组织密度影较前略缩小；双上肺纵隔旁小叶间隔稍增厚；余无著变2.颈部CT检查未见明显占位征象。2021-3-16日予以下一周期化疗：放线菌素D0.74mg d1-5+长春地辛4mg d1，8+依托泊苷180mg d1-3。化疗后患儿自觉腿疼，当地医院复查MRI示示左腿部肿块，性质待定。于我院预住院期间行左大腿针吸活检，送检纤维脂肪组织内见大量中性粒细胞浸润伴脓肿形成。予以抗炎治疗后给予CI方案化疗，具体：环磷酰胺720mg d1-5+伊立替康 200mg d1-3，化疗过程顺利，准予出院。患者2021-04-26入院后完善各项病原学检查，肠道菌群分布示：革兰氏阴性菌少见，革兰氏阳性菌偶见，白介素6 226pg/ml，降钙素原4.48ng/ml，予以美罗培南经验性抗炎治疗，输血及升白细胞，升血小板治疗。口服益生菌调节肠道菌群。患儿一般情况可，骨髓抑制较前明显好转，准予出院。结束治疗10月后，于2022-02-10行输液港取出术，手术顺利。定期门诊随访未见异常。"
#    年      龄：6岁3月14天
# 科    室：血五
# 病房或病区：血五
#    病  案  号：854966
# 二、医师说明
# 【病情简介】（主要症状、体征、疾病严重程度） 横纹肌肉瘤加强化疗
#
# 【过敏史】
#
# 【检查与治疗前诊断】     横纹肌肉瘤加强化疗
# """
# print(split_text(content, "。|,|，|；|\n", fetch_func=fetch_index_and_text))
# content = '于2021年 07月 31日 09：46白细胞 0.14(10^9/L)↓；    1.恶性肿瘤维持性化学治疗 2.盆腔恶性肿瘤 横纹肌肉瘤 Ⅳ期 中危组 3.骨髓继发恶性肿瘤 4.骨继发    恶性肿瘤 5.化疗后骨髓抑制 中度贫血 中性粒细胞缺乏 血小板减少    患儿为横纹肌肉瘤恶性肿瘤，考虑白细胞下降，粒细胞缺乏与化疗后骨髓抑制相关    给予瑞白升白处理，动态复查血常规医师签名：病程签名：SIGN：'
# content = '患儿5月余前发现左侧小腿中上段肿物,如鸡蛋大小，质韧，无红肿、皮温升高及触痛， 不伴活动障碍。后患者就诊于****，查下肢超声提示：左小腿肌肉层内见实性中低回声团，大小50*22mm,边界清，有包膜回声，诊断为***，予固化治疗。后患儿左小腿肿物逐渐增大，质硬，大小约为6*8cm,不伴红肿、触痛及皮温升高。2月前患儿出现跛行，表现为左脚掌无法背屈，遂于****进行康复训练，患儿情况未好转。半月前患儿就诊于*******，查左胫腓骨平扫+增强MRI及CT提示左小腿中上段胫后肌群内见一分叶状团块影，大小约43*34*66mm,信号欠均匀，灶内可见分隔，边界较清，增强后病灶欠均质明显强化，左胫腓骨未见明显受累。考虑左小腿中上段胫后肌群内侵袭性占位可能。肺CT平扫未见异常。4天前患儿于*****行左小腿肿物活检，我院病理会诊意见：（左小腿）横纹肌肉瘤，组织形态符合腺泡型，免疫组化结果：MyoD1(+),Desmin(+),CD56(+),Ki-67(25%+),NSE(-),Vimentin(-),CgA(-),Syn(-),WT1(-),CK(AE1/AE3)(-),SATB2(-),Calponin(-),NKX2.2(-),CD99(-),LCA(-),CD20(-),CD5(-),CD3(-)。为进一步诊治，以“横纹肌肉瘤”收入院诊治。 患儿自发病以来，神清，精神状态良好，体力情况良好，食欲食量良好，睡眠情况良好，体重未减低。'

# content = '-'
# for start_index, end_index, timeline in cut_by_time(content, '2020-12-01 00:00:00'):
#     print(content[start_index: end_index])
#     if timeline:
#         print("原时间：" + timeline.base_time + ", 标准化时间：" + timeline.base_time_convert)
#     print('---------------------------')

# if __name__ == '__main__':
#     test = "　子宫:子宫位置、形态、大小正常，呈幼稚型，宫体厚约4.7mm，内膜线可见，宫壁回声分布均匀，宫颈局部膨大，厚约7.1mm，内回声欠均匀。因气体遮挡，双侧卵巢显示不清。双侧附件区未见明显异常回声团块。　阴道:经会阴探查：阴道可显示段未见明显异常回声。浅表部位:左大腿根部皮肤及皮下软组织层探查：未见明显异常回声团块及囊性暗区，可见数个小淋巴结回声，其中一个大小约7.7×3.3mm，内回声尚均，皮髓质分界清，未见明显液性暗区。CDFI：淋巴结内可见点状血流信号。　"
#     s = "肝脏:肝脏大小、形态正常，肋下0mm，包膜光滑，实质回声均匀，下缘角锐利，肝内管系走行正常。门静脉主干内径约6.9mm，透声良好，血流通畅，呈入肝血流。肝内外胆管无明显扩张。　脾脏:厚径约20.3mm，肋下未及，包膜光滑，回声均匀。脾静脉血流通畅。　肾脏:双肾大小、形态正常，包膜光滑，实质厚度及回声未见异常，集合系统无分离。CDFI：血流灌注正常。　肠套叠:目前未见明显典型“同心圆”征及“套筒”征。　阑尾:右下腹腔内未见明显阑尾显示，未探及明显异常回声团块及无回声区。肠系膜淋巴结:腹腔内未见明显肿大淋巴结回声。　子宫:子宫位置、形态、大小正常，呈幼稚型，宫体厚约4.7mm，内膜线可见，宫壁回声分布均匀，宫颈局部膨大，厚约7.1mm，内回声欠均匀。因气体遮挡，双侧卵巢显示不清。双侧附件区未见明显异常回声团块。　阴道:经会阴探查：阴道可显示段未见明显异常回声。浅表部位:左大腿根部皮肤及皮下软组织层探查：未见明显异常回声团块及囊性暗区，可见数个小淋巴结回声，其中一个大小约7.7×3.3mm，内回声尚均，皮髓质分界清，未见明显液性暗区。CDFI：淋巴结内可见点状血流信号。　"
#     print(s[258:490] == test)

