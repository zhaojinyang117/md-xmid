from typing import List, Optional, Union
import xmind
import markdown
from bs4 import BeautifulSoup
from bs4.element import Tag
from xmind.core.topic import TopicElement
from xmind.core.workbook import WorkbookDocument
from xmind.core.sheet import SheetElement
import tempfile
import os

class MindMap:
    def __init__(self) -> None:
        # 创建临时文件
        temp_dir = tempfile.gettempdir()
        self.temp_file = os.path.join(temp_dir, "temp.xmind")
        self.workbook: WorkbookDocument = xmind.load(self.temp_file)
        self.sheet: SheetElement = self.workbook.getPrimarySheet()
        self.root: TopicElement = self.sheet.getRootTopic()

    def parse_markdown(self, md_file: str) -> None:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content: str = f.read()
        
        html: str = markdown.markdown(md_content)
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        
        headers: List[Tag] = []
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            headers.extend(soup.find_all(tag))

        if headers:
            self.root.setTitle(headers[0].get_text())
            self._process_headers(headers[1:], self.root)

    def _process_headers(self, headers: List[Tag], parent_topic: TopicElement) -> Optional[int]:
        if not headers:
            return None

        current_level: int = int(headers[0].name[1])
        parent_level: int = int(parent_topic.getTitle().split('|')[1]) if '|' in parent_topic.getTitle() else 1

        i: int = 0
        while i < len(headers):
            header: Tag = headers[i]
            level: int = int(header.name[1])
            text: str = header.get_text()

            if level <= parent_level:
                return i

            if level == parent_level + 1:
                sub_topic: TopicElement = parent_topic.addSubTopic()
                sub_topic.setTitle(f"{text}|{level}")
                
                consumed: Optional[int] = self._process_headers(headers[i+1:], sub_topic)
                if consumed:
                    i += consumed
            i += 1
        
        return None

    def save(self, output_file: str) -> None:
        if not output_file.endswith('.xmind'):
            output_file += '.xmind'
        self._clean_titles(self.root)
        xmind.save(self.workbook, output_file)
        # 清理临时文件
        try:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
        except:
            pass

    def _clean_titles(self, topic: TopicElement) -> None:
        title: str = topic.getTitle()
        if '|' in title:
            topic.setTitle(title.split('|')[0])
        
        for sub_topic in topic.getSubTopics():
            self._clean_titles(sub_topic)

def generate_mind_map(md_file_path: str, output_image: str = 'output.xmind') -> None:
    mind_map: MindMap = MindMap()
    mind_map.parse_markdown(md_file_path)
    mind_map.save(output_image)
    print(f"思维导图已生成: {output_image}")

if __name__ == "__main__":
    generate_mind_map("./input.md", "./output.xmind")
