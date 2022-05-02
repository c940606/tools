import os
import re
import subprocess
import click
from baiduspider import BaiduSpider
from random import choice


def get_url(path):
    if not os.path.isfile(os.path.abspath(path)): return path
    cmd = fr'picgo upload "{path}"'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    command_output = process.stdout.read().decode("gbk")
    url = re.findall(r"\[PicGo SUCCESS]:\s*(.*)", command_output)[0]
    if not url.strip():
        return os.path.join(r"https://gitee.com/powcai/picture/raw/master/img/", os.path.split(path)[1])
    return url


@click.command()
@click.option("--path", default=".", help="file path")
@click.option("--tag", default="美女 清纯", help="file path")
def main(path, tag):
    # 实例化BaiduSpider
    spider = BaiduSpider()
    dir_name, file_name = os.path.split(os.path.abspath(path))
    os.chdir(dir_name)  # 改变当前工作目录到指定的路径
    img_set = spider.search_pic(tag).plain
    with open(path, mode="r", encoding="utf8") as f:
        result = f.readlines()
    pattern = re.compile(r'(?<=]\().*(?=\))')
    word_num = 0
    visited_set = set()
    with open(os.path.join(dir_name, "convert.md"), "w", encoding="utf8") as f:
        for word in result:
            word = re.sub(pattern, lambda matched: get_url(matched.group(0)), word) # 将本地图片上传picgo
            f.write(word)
            word_num += len(re.findall(r"[\u4e00-\u9fa5]", word)) # 汉字的个数
            if word_num > 300:
                img = choice(img_set)
                img_url = img.get("url")
                while img_url in visited_set and "token" in img_url:
                    img = choice(img_set)
                    img_url = img.get("url")
                f.write(f"\n![{img.get('title', tag)}]({img_url})\n")
                word_num = 0
                visited_set.add(img_url)
    click.echo("生成成功")


if __name__ == '__main__':
    main()