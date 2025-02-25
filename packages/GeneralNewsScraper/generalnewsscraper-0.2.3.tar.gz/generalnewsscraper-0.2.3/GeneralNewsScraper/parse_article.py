import datetime
import re
from urllib.parse import urljoin, urlparse
from lxml import etree
from GeneralNewsScraper.utils import is_valid_url, get_width, handle_exception
from bs4 import BeautifulSoup

LENGTH_RATE = 0.7
DISTANCE_RATE = 0.3


async def pre_process_article(page_html):
    """
    文章内容预处理
    :param article_html:
    :return:
    """
    regex_patterns = [
        # r'<script[^>]*?>.*?</script>',
        r'<style[^>]*?>.*?</style>',
        r'<!--.*?-->',
        r'Notice: The content above \(including the pictures and videos if any\) is uploaded and posted by a user of \
        NetEase Hao, which is a social media platform and only provides information storage services.',

        # kitv.com
        # figcaption标签为-给图片/视频添加的描述，可以优先过滤掉
        r'<figcaption[^>]*?>.*?</figcaption>',
        # aside是推荐内容，与文章主内容互补影响，但可能会影响算法定位，过滤掉
        r'<aside[^>]*?>.*?</aside>',

        # 特殊：apnews-有轮播图的
        # 轮播图信息 CarouselSlide-info-content，CarouselOverlay-info-description
        r'<div[^>]*?class="CarouselSlide-info-content"[^>]*?>.*?</div>',
        r'<div[^>]*?class="CarouselOverlay-info-description"[^>]*?>.*?</div>',

        # wp-caption-text 同样为图片的解释说明，过滤掉
        # 包含该类名的过滤掉
        # r'<[^>]*?class="[^"]*\bwp-caption-text\b[^"]*"[^>]*?>.*?</[^>]+>',

        # footer
        r'<footer[^>]*?>.*?</footer>',

        # aside
        r'<aside[^>]*?>.*?</aside>',

    ]
    for regex in regex_patterns:
        page_html = re.sub(regex, '', page_html, flags=re.S)
    return page_html


@handle_exception
async def parse_time(html):
    """
    html 中提取时间
    :param html:
    :return: 字符串类型时间
    """
    regex_patterns = [
        r'"(20[012]\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])[ T]+[012]\d:[0-5]\d:[0-5]\d)',
        r'"(20[012]\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])[ T]+[012]\d:[0-5]\d)',
        r'(20[012]\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])[ T]+[012]\d:[0-5]\d:[0-5]\d)',
        r'(20[012]\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])[ T]+[012]\d:[0-5]\d)',
        r'(20[012]\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))',
    ]
    for regex in regex_patterns:
        match = re.findall(regex, html)
        if match:
            for m in match:
                pub_time = m.strip()
                pub_time = pub_time.replace('T', ' ')
                if not re.search(r'\d{2}:\d{2}:\d{2}', pub_time):
                    if not re.search(r'\d{2}:\d{2}', pub_time):
                        pub_time = pub_time + ' 00:00:00'
                    elif re.search(r'\d{2}:\d{2}', pub_time):
                        pub_time = pub_time + ':00'
                if datetime.datetime.strptime(pub_time,
                                              '%Y-%m-%d %H:%M:%S').timestamp() > datetime.datetime.now().timestamp():
                    continue
                return pub_time


async def get_node_text(html, node_name):
    # 如果节点下是strong标签，就匹配strong标签的文本
    node_list = html.xpath(f'//{node_name}[strong]/strong/text() | //{node_name}[not(strong)]/text()')
    text_list = []

    for node in node_list:
        # 央视新闻标题下方的时间信息  如果正文较短，会影响定位
        if 'cookies' in node or 'copyright' in node or 'Copyright' in node or re.search(
                r'(20[012]\d年[01]\d月[0-3]\d日 [012]\d:[0-5]\d)', node):
            # print(node)
            continue
        if node.replace('\r', '').replace('\n', '').strip() != '':
            # 确保解析的title一致 没有\n \t \r等字符 以便算法真确匹配
            if node_name == 'title':
                node = node.replace('\n', '').replace('\r', '').replace('\t', '').strip()
            text_list.append(node)
    return text_list


# 获取最长文本
# 有关长度的操作把所有空字符去掉，再进行比较等操作
async def _get_width(text):
    return await get_width(re.sub(r'\s+', ' ', text).strip())


async def get_best_text(html, title):
    '''
    1.拿取title，h1，p，div等可能包含正文内容的标签内容
    2.从标题处分割出一个新的列表
    2.遍历列表 分别求出列表中每个元素的 单位距离 和 单位文本长度  再计算出总得分
    3.返回得分最高的那个元素文本
    :param html:
    :return:
    '''

    # print(title)
    html = etree.HTML(html)
    AllTextList = []

    # 按照文章结构  p 标签内容往往比div标签内容要重要且有用
    # 新增存在文本的标签section--东亚日报 span b h3
    tags_to_extract = ['title', 'h1', 'p', 'div', 'span', 'b', 'h3', 'section']
    for tag in tags_to_extract:
        text_list = await get_node_text(html, tag)
        AllTextList.extend(text_list)

    # print(AllTextList)
    PreliminaryList = []
    for i, item in enumerate(AllTextList):
        if item == title:
            PreliminaryList = AllTextList[i + 1:]
            break
    # print(PreliminaryList)
    MaxListLength = len(PreliminaryList)

    # MaxText = max(PreliminaryList, key=lambda x: )
    # 遍历PreliminaryList，找到最长的文本

    MaxTextLength = 0
    for i, item in enumerate(PreliminaryList):
        length = await _get_width(item)
        if length > MaxTextLength:
            MaxTextLength = length

    for i in range(len(PreliminaryList)):
        # 单位距离计算
        UnitDistance = 1 - i / MaxListLength
        # PreliminaryList[i] = PreliminaryList[i] + '--UnitDistance--' + str(UnitDistance)

        # 单位文本长度计算
        # Unitlength = len(re.sub(r'\s+', ' ', PreliminaryList[i]).strip()) / MaxTextLength
        Unitlength = await _get_width(PreliminaryList[i]) / MaxTextLength

        # PreliminaryList[i] = PreliminaryList[i] + '--Unitlength--' + str(Unitlength)

        # 得分计算
        score = LENGTH_RATE * Unitlength + DISTANCE_RATE * UnitDistance

        PreliminaryList[i] = PreliminaryList[i] + 'SCORE' + str(score)

        if PreliminaryList[i].startswith('http'):
            PreliminaryList[i] = PreliminaryList[i] + 'SCORE' + str(0)

    # 按照score的大小排序
    PreliminaryList.sort(key=lambda x: float(x.split('SCORE')[-1]), reverse=True)

    # 返回得分最高的文本
    best_node_text = PreliminaryList[:3]

    return best_node_text


@handle_exception
async def parse_article_title(article_html):
    """
    获取文章标题
    优先拿h1标签，如果在title中存在h1标签内容，则取h1标签内容，否则取title标签内容
    :param article_html:
    :return:
    """

    h1_text = re.search(r'<h1[^>]*?>(.+?)<', article_html)
    title_text = re.search(r'<title[^>]*?>\s*(.+?)\s*</title>', article_html)

    if h1_text and h1_text.group(1).strip() in title_text.group(1).strip():
        title = h1_text.group(1).strip()
    else:
        title = title_text.group(1).strip()
    if not h1_text and not title_text:
        title = re.search(r'<meta property="[^"]*?title" content="([^"]+?)">', article_html).group(1)

    if not h1_text and not title_text and not re.search(r'<meta property="[^"]*?title" content="([^"]+?)">',
                                                        article_html):
        raise Exception("未匹配到标题")
    # 特殊情况
    title = re.sub(r'&amp;', '&', title)

    title = re.sub(r'<[^>]+>', '', title)
    # title = title.split('-')[0].strip()
    # title = title.split('_')[0].strip()
    # title = title.split('|')[0].strip()
    return title


async def get_content_by_best_text(html, best_text):
    # 找到所有节点 ，谁的文本内容等于best_text,确定这个节点的tag
    html = etree.HTML(html)
    node_list = html.xpath('//*')

    target_node = None
    target_node_tag = None
    target_node_class = None
    for node in node_list:
        if best_text in node.xpath('./text()'):
            target_node = node
            target_node_tag = node.tag
            if target_node_tag == 'strong':
                target_node = node.getparent()
                target_node_tag = node.getparent().tag
            target_node_class = target_node.get('class')
            break
    if not target_node_tag:
        raise Exception('匹配文章内容失败')

    same_node_text_list = []
    if target_node_class:
        same_node_list = html.xpath(f'//{target_node_tag}[@class="{target_node_class}"]')
        for same_node in same_node_list:
            same_node_text = same_node.xpath('./text()')
            same_node_text_list.append('\n'.join(i.strip() for i in same_node_text))

        # 依次往上寻找父节点 直到某个节点包含same_node_text_list 中所有内容为止
        while True:
            father_node = target_node.getparent()
            father_node_text = father_node.xpath(f'.//{target_node_tag}/text()')
            father_node_text = '\n'.join(i.strip() for i in father_node_text)
            for same_node_text in same_node_text_list:
                if same_node_text not in father_node_text:
                    break
            else:
                break
            target_node = father_node
        best_node = father_node
        content = '\n'.join(i.strip() for i in same_node_text_list)

    else:
        # 最佳节点没有class属性  就往上找，直到一个有类名的父节点 取其文本内容
        while True:
            father_node = target_node.getparent()
            if father_node is None:
                return father_node, ''
            father_node_class = father_node.get('class')
            father_node_id = father_node.get('id')
            if father_node_class or father_node_id:
                break
            target_node = father_node
        best_node = father_node

        content = '\n'.join(i.strip() for i in best_node.xpath('.//*/text()'))
        content = re.sub(r'[\n]+', '\n', content).strip()
    return best_node, content


async def parse_article_content(html, url):
    """
    获取文章内容
    思路：
    1.依次获取title，h1，p，div 的文本（文章结构）
    2.根据算法，求出得分最高的那个文本
    3.再求得该文本所属的标签 p/div  (如果是strong的话，就取该节点父节点的tag)
    4.根据 所得到的tag_name 和 best_text  向上取得节点  即为文本内容定位位置
    :param html:
    :param url:
    :return:
    """
    if isinstance(html, str):
        html_str = re.sub(r'<script[^>]*?>.*?</script>', '', html, flags=re.S)
        html_str = re.sub(r'<style[^>]*?>.*?</style>', '', html_str, flags=re.S)
        html_str = re.sub(r'<path[^>]*?>.*?</path>', '', html_str, flags=re.S)

        # 使用bs4 删除loginfort 等无关干扰项的 整段div
        soup = BeautifulSoup(html_str, 'html.parser')
        div_to_remove_id = soup.findAll('div', id=['loginFloat', 'page_bottom', 'module-moreStories', 'footer-content'])
        if div_to_remove_id:
            for div in div_to_remove_id:
                div.decompose()
        # div_to_remove_class = soup.findAll('div', class_=['index_copyRight_A74B5'])
        # if div_to_remove_class:
        #     for div in div_to_remove_class:
        #         div.decompose()
        html = str(soup)

    title = await parse_article_title(html)

    max_content = ''
    best_node = None
    result = await get_best_text(html, title)
    for r in result:
        best_text = r.split('SCORE')[0]
        # print(best_text)
        # 返回得分前三个的文本
        # 把获取文本父节点的方法单独拿出来
        # 每个文本都去执行这个方法，方法返回content内容 再对其content内容进行比较 长度最长的内容作为文章text 并且后续的图片视频解析也在该div块内

        pre_best_node, content = await get_content_by_best_text(html, best_text)

        content_length = await _get_width(content)

        if content_length > await _get_width(max_content):
            max_content = content
            best_node = pre_best_node

    content = max_content

    img_list = []
    video_list = []
    if best_node is None:
        raise Exception('HTML内容异常')
    _img_list = best_node.xpath('.//img/@src')
    for img in _img_list:
        if ('.log' in img or '.ico' in img or '.gif' in img or 'data:image' in img or '.svg' in img or
                'base64' in img or ' ' in img):
            continue
        if img in img_list or img == url:
            continue
        if not img.startswith('http'):
            img = urljoin(url, img)
        if await is_valid_url(img):
            img_list.append(img)

    _video_list = best_node.xpath('.//video/@src')
    for video in _video_list:
        if not ('.mp4' in video) or ' ' in video:
            continue
        if video in video_list:
            continue
        if not video.startswith('http'):
            video = urljoin(url, video)
        if await is_valid_url(video):
            video_list.append(video)

    return {"content": content, "imageList": img_list, 'videoList': video_list}


@handle_exception
async def parse_top_image(html):
    image = re.findall('<meta[^>]*?content="([^"]*?)"[^>]*?property="[^"]*?image"', html)
    if not image:
        image = re.findall('<meta[^>]*?property="[^"]*?image"[^>]*?content="([^"]*?)"', html)
    return image[0] if image else None


@handle_exception
async def parse_site_name(html):
    """
    获取网站名称
    :param html:
    :return:
    """
    ret = re.findall('property="og:site_name" content="([^"]*?)"', html)
    if ret:
        return ret[0]
    # if not ret:
    #     ret = re.findall('<title[^>]*?>[^_\-|<]*?[_\-|](.+?)</title>', html)
    #     if not ret:
    #         return None
    # webName = ret[0]
    # if '-' in ret[0]:
    #     webName = webName.split('-')[-1]
    # if '|' in ret[0]:
    #     webName = webName.split('|')[-1]
    # if '_' in ret[0]:
    #     webName = webName.split('_')[-1]
    #
    # return webName.strip()


@handle_exception
async def parse_logo(url, html):
    """
    获取网站icon
    :param url:
    :param html:
    :return:
    """
    patterns = [
        '"([^"]*?.ico)"',
        '<[^>]*?="[^"]*?icon"[^>]*? href="([^"]*?)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            icon_url = match.group(1)
            return icon_url if icon_url.startswith("http") else urljoin(url, icon_url)
    # 获取url域名
    _url = urlparse(url)
    _hostname = _url.hostname
    _scheme = _url.scheme
    if not _hostname:
        return None
    if not _scheme:
        _scheme = "https"
    return _scheme + '://' + _url.hostname + '/favicon.ico'


@handle_exception
async def parse_domain(url):
    """
    获取域名
    :param url:
    :return:
    """
    return urlparse(url).hostname
