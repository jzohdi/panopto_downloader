import requests
from typing import List
from xml.etree import ElementTree


rss_url = "https://umd.hosted.panopto.com/Panopto/Podcast/Podcast.ashx?courseid=279b0c4c-3caa-43a6-b752-ad8b0149481d&type=mp4"

class Video:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url
    
    def __repr__(self) -> str:
        return f"Video = title: {self.title}, url: {self.url}"

    def title_as_filename(self, extension: str) -> str:
        # replace spaces
        file_name = self.title.replace(" ", "_")

        # remove non-friendly characters
        keepcharacters = {'.', '_' }
        file_name = "".join(c for c in file_name if c.isalnum() or c in keepcharacters).rstrip()
        if extension != file_name[-4:]:
            return file_name + extension
        return file_name

def downloadfile(video: Video):
    url = video.url
    name = video.title_as_filename(".mp4")
    response = requests.get(url)
    print(f"Connected to {url}")

    try:
        with open(name, 'wb+') as file:
            print("Donloading...")
            for chunk in response.iter_content(chunk_size=255): 
                if chunk: # filter out keep-alive new chunks
                    file.write(chunk)            
        print("Done")
    except Exception as err:
        print("Failed: {0}".format(err))

def parse_rss_xml(file_name: str) -> List[Video]:
    xml_tree = ElementTree.parse(file_name)
    xml_root = xml_tree.getroot()
    
    videos = []

    for item in xml_root.findall("./channel/item"):
        video_details = Video(None, None)
        
        for child in item:
            if child.tag == "title":
                video_details.title = child.text
            if child.tag == "enclosure":
                video_details.url = child.attrib["url"]
        
        videos.append(video_details)

    return videos

def download_rss_feed(file_name: str, rss_url: str) -> str:
    response = requests.get(rss_url)
    with open(file_name, "wb+") as file:
        file.write(response.content)
    return file_name

def main():
    file_name = download_rss_feed("cmsc424.xml", rss_url)
    videos: List[Video] = parse_rss_xml(file_name)
    for video in videos:
        downloadfile(video)

if __name__ == "__main__":
    main()