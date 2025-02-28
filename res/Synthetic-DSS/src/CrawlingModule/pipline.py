from bs4 import BeautifulSoup
import re
            
import html2text
class Pipline():
    def __init__(self):
        self.h = html2text.HTML2Text()
    def get_pipline(self,case):
        cases = {
            'XueQiu': self.__xq_pipline,
            'JiuYan': self.__jy_pipline
        }
        return cases.get(case)
    def __xq_pipline():
        pass
    def __jy_pipline(self,item):
        html_content = item["text"]
        # 创建 BeautifulSoup 对象
        soup = BeautifulSoup(html_content, 'html.parser')

        script_tag = None
        for script in soup.find_all('script'):
            if 'window.__NUXT__' in script.text:
                script_tag = script
                break
        
        pattern = r'content:(.*?),url|,stock_list'

        #print(script_tag)
        matches = re.findall(pattern, script_tag.text)
        #print(url)
        data_str = matches[0]

        unescaped_str = data_str.encode('raw_unicode_escape').decode('unicode_escape')
        # 将 HTML 转换为 Markdown
        self.h.body_width = 0
        markdown = self.h.handle(unescaped_str)

        return markdown