import os
import re
import math
import jieba

# 将输入的词字典进行降序排序，返回列表
def sorted_words_dict(all_words_dict):
    all_words_tuple_list = sorted(all_words_dict.items(), key=lambda f: f[1],
                                  reverse=True)  # 内建函数sorted参数需为list
    all_words_list = zip(*all_words_tuple_list)
    all_words_list = list(all_words_list)[0]
    return all_words_list

# 以文档为单位 获取所有评论的数据 做成列表 用于IDF计算
def get_total_comments_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read()
    comments = []
    lines = lines.split("******")
    for line in lines:
        try:
            line = line.split("**评论区**")
            line[1]  =  re.sub("\d+:", "", line[1])
            list_comment_tmp = line[1].split("*评论*")
            for unit in list_comment_tmp:
                if unit == '':
                    continue
                comments.append(unit)
        except:
            pass
    return comments

# 以文档为单位 统计所有评论的数量 用于IDF计算
def get_num_of_comments_in_total(file_path):
    return  len(get_total_comments_list(file_path))

# 选取路径的语料库.txt档案的内容，制作成词语集合（重复者不计入）并且返回
# 可用于生成词集合，
# 停用词stopwords_set、
# 心态：正面心态test_positive_set、负面心态test_negative_set、
# 心态：高兴与爱happy_love_set、难过与内疚（同情也包括）sad_guilty_set
#      生气与憎angry_hatred_set、惊喜与害怕surprise_afraid_set
def make_word_set(words_file):
    words_set = set()
    with open(words_file, 'r') as fp:
        for line in fp.readlines():
            word = line.strip()
            if len(word)>0 and word not in words_set: # 去重
                words_set.add(word)
    return words_set

# 从提供词列表筛选出特征词（即前n个）
def words_dict(all_words_list):
    # 选取特征词
    feature_words = []
    n = 1
    for t in range(len(all_words_list)):
        if n > 20:  # 选取20个以内的特征词
            break
        feature_words.append(all_words_list[t])
        n += 1
    return feature_words

# 文本处理
# 统计出心态：正面/负面/无中性 三种心态标签 新闻为单位 计算总量
# 统计出心态：高兴与爱happy_love、难过与内疚（同情也包括）sad_guilty
#           生气与憎angry_hatred、惊喜与害怕surprise_afraid 四种心态标签 新闻为单位 计算总量
def text_processing(file_path):
    mentality_list_num = {"happy_love": 0, "sad_guilty": 0, "angry_hatred": 0, "surprise_afraid": 0, "other_emotion":0}
    positive_num = 0
    negative_num = 0
    neutral_num = 0
    # 获取档案里面需要特征词（关键词）的数量，用于IDF的计算
    words_dict_in_total = {}
    # 获取档案里面所有评论的数量、之后用于IDF的计算中
    comments_in_total = get_num_of_comments_in_total(file_path)
    # 获取所有档案里所有的评论，用于IDF的计算中
    comments = get_total_comments_list(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read()
    # 数据的格式化处理，将每则新闻分开
    lines = re.sub(r"\d+-\d+-\d+", "", lines)
    lines = lines.replace(' ', "")
    lines = lines.split("******")
    for line in lines:
        # 分离出评论区，之后都是对于评论区做讨论
        line = line.split("**评论区**")
        try:
            # 将评论区格式"*评论*d+"消除
            line[1] = re.sub("\*\w+\*\d+:", "", line[1])
            # 使用jieba分词软件对于对于文本进行词语切分
            # 开启并行分词模式，参数为并行进程数，
            # 精确模式，返回的结构是一个可迭代的genertor，
            # genertor转化为list，每个词unicode格式，
            # 关闭并行分词模式
            jieba.enable_parallel(4)
            word_cut = jieba.cut(line[1], cut_all=False)
            word_list = list(word_cut)
            jieba.disable_parallel()

            all_words_dict = {}
            mentality_words_dict = {}
            emotion_words_dict = {}

            # jieba切词出来，进行一次筛选，然后统计词数放入all_words_dict
            for word in word_list:
                if not word.isdigit() and word not in stopwords_set and 1 < len(word) < 5:
                    if word in all_words_dict:
                        all_words_dict[word] += 1
                    else:
                        all_words_dict[word] = 1

            # 获得词总数，用于计算TF词频
            word_num = len(word_list)
            for word in all_words_dict:
                if word not in words_dict_in_total:
                    count = 0
                    for comment in comments:
                        if word in comment:
                            count += 1
                    words_dict_in_total[word] = count
                # 心态：TF * IDF：
                # TF————>新闻为单位 出现关键词的个数/ 新闻为单位 词语总个数
                # IDF————>log（档案为单位 总评论数量 / 档案为单位 出现关键词的评论数量 + 1）
                mentality_words_dict[word] = all_words_dict[word]/word_num * math.log(comments_in_total/(words_dict_in_total[word]+1))

            # 进行从高到低排序获得新闻为单位 统计出来的心态列表mentality_words_list、心态列表emotion_words_list
            mentality_words_list = sorted_words_dict(mentality_words_dict)

            # 筛选最前20名的词，构成特征词列表
            mentality_feature_words = words_dict(mentality_words_list)

            # 依据心态特征词统计新闻的性质，使用score量化量化每则新闻观众心态
            # 即 若在正面心态词集合中score+=TFIDF值，若在负面心态词集合中score-=TFIDF值
            score = 0
            mentality_score_list = {"happy_love":0, "sad_guilty":0, "angry_hatred":0, "surprise_afraid":0}

            for unit in mentality_feature_words:
                if unit in test_positive_set:
                    score += mentality_words_dict[unit]
                if unit in test_negative_set:
                    score -= mentality_words_dict[unit]

            # 根据score参数，逐一统计正面/负面/中性 三种心态状态的新闻总量
            if score > 0:
                positive_num += 1
            elif score == 0:
                neutral_num += 1
            else:
                negative_num += 1

            # 依据心态特征词统计新闻的性质，使用字典emotion_score_list的元素 量化量化每则新闻观众心态
            # 即 若在某一心态词集合中，若在负面心态词集合中元素+=1
            for unit in mentality_feature_words:
                if unit in happy_love_set:
                    mentality_score_list["happy_love"] += mentality_words_dict[unit]
                if unit in sad_guilty_set:
                    mentality_score_list["sad_guilty"] += mentality_words_dict[unit]
                if unit in angry_hatred_set:
                    mentality_score_list["angry_hatred"] += mentality_words_dict[unit]
                if unit in surprise_afraid_set:
                    mentality_score_list["surprise_afraid"] += mentality_words_dict[unit]

            # 如果字典emotion_score_list元素值都为0，第五类other_emotion+=1
            if (mentality_score_list["happy_love"] == mentality_score_list["sad_guilty"] == mentality_score_list["angry_hatred"] == mentality_score_list["surprise_afraid"] == 0):
                mentality_list_num["other_emotion"] += 1
            # 将字典emotion_score_list元素值比较大小，最大者在字典emotion_list_num元素值+=1，若有两者相同两者同+=1/2，类推下去
            else:
                number = 0
                top_item_list = []
                for item in mentality_score_list:
                    if mentality_score_list[item] == mentality_score_list[max(mentality_score_list, key=mentality_score_list.get)]:
                        number += 1
                        top_item_list.append(item)
                for item in mentality_score_list:
                    if item in top_item_list:
                        mentality_list_num[item] += 1 / number
        except:
            pass
    return positive_num, neutral_num, negative_num, mentality_list_num


if __name__  == "__main__":
    data_list = []

    # 生成心态归类使用的集合：正面心态词集合test_positive_set、负面心态词集合test_negative_set
    positive_file = 'mentality_word_bank/positive_word.txt'
    test_positive_set = make_word_set(positive_file)

    negative_file = 'mentality_word_bank/negative_word.txt'
    test_negative_set = make_word_set(negative_file)

    # 生成心态归类使用的集合：
    # 高兴与爱happy_love_set、难过与内疚（同情也包括）sad_guilty_set
    # 生气与憎angry_hatred_set、惊喜与害怕surprise_afraid_set
    happy_love_file = 'mentality_word_bank/happy_love.txt'
    happy_love_set = make_word_set(happy_love_file)

    sad_guilty_file = 'mentality_word_bank/sad_guilty.txt'
    sad_guilty_set = make_word_set(sad_guilty_file)

    angry_hatred_file = 'mentality_word_bank/angry_hatred.txt'
    angry_hatred_set = make_word_set(angry_hatred_file)

    surprise_afraid_file = 'mentality_word_bank/surprise_afraid.txt'
    surprise_afraid_set = make_word_set(surprise_afraid_file)

    # 生成筛选使用的停用词集合：stopwords_set
    stopwords_file = 'stop_word_cn.txt'
    stopwords_set = make_word_set(stopwords_file)


    # 逐一选取微博爬取下来的新闻以及评论档案，
    # 以新闻为单位归类心态：正面、中性、负面心态三种标签，最终数量以参数positive_num、neutral_num、negative_num储存
    # 以新闻为单位归类心态：高兴与爱happy_love、难过与内疚（同情也包括）sad_guilty
    # 生气与憎angry_hatred、惊喜与害怕surprise_afraid四种标签，统计最终数量以  字典emotion_list_num 储存
    new_folder_path = "news_comments_bank/"
    files = os.listdir(new_folder_path)
    files.sort()
    for file in files:
        folder_path = os.path.join(new_folder_path, file)
        positive_num, neutral_num, negative_num, emotion_list_num= text_processing(folder_path)

        # 打印四个阶段新闻评论统计的最终结果
        print("%s的详细资讯\n"%file)

        print("民众心态统计：")
        sum = positive_num + neutral_num + negative_num
        print("正面心态比例（单位：百分比）%f" % (positive_num/sum  * 100))
        print("中性心态比例（单位：百分比）%f" % (neutral_num/sum * 100))
        print("负面心态比例（单位：百分比）%f" % (negative_num/sum * 100))
        print("")
        sum = 0
        for item in emotion_list_num:
            sum += emotion_list_num.get(item)
        for item in emotion_list_num:
            print("%s的新闻是比例（单位：百分比): %f" % (item, emotion_list_num.get(item) / sum * 100))
        print("")

