"""Render a concise coaching review card from filled JSON."""

import argparse
import html
import json
import sys
from pathlib import Path


def render(data):
    fields = ("title", "context", "current_focus", "initial_judgment", "turning_point", "current_judgment", "coach_feedback", "next_experiment")
    missing = [key for key in fields if not isinstance(data.get(key), str) or not data[key].strip()]
    if missing:
        raise ValueError("缺少非空文字字段：" + "、".join(missing))
    esc = lambda value: html.escape(str(value), quote=True)
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(data['title'])}｜陪练回看卡</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f4f5f2;color:#1f2b28;font:16px/1.65 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}}
main{{max-width:780px;margin:32px auto;padding:28px;background:white;border-radius:20px;box-shadow:0 8px 28px #14251b12}}
h1{{font-size:clamp(25px,4vw,36px);line-height:1.25;margin:8px 0 10px}}h2{{font-size:16px;margin:0 0 7px;color:#176c56}}p{{margin:0}}.meta{{color:#56645e;font-size:14px}}
.lead{{border-left:5px solid #16846b;padding:12px 18px;background:#ecf7f2;margin:22px 0;font-size:19px;font-weight:650}}
.flow{{display:grid;gap:12px}}section{{border:1px solid #dae4dc;border-radius:14px;padding:17px;background:#fff}}
section.now{{background:#eaf4ed}}.tag{{color:#176c56;font-weight:650;font-size:13px}}footer{{border-top:1px solid #dae4dc;margin-top:20px;padding-top:15px}}
@media(max-width:620px){{main{{margin:0;padding:20px;border-radius:0}}}}
</style></head><body><main>
<div class="tag">经营判断 · 陪练回看</div><h1>{esc(data['title'])}</h1>
<div class="meta">{esc(data['context'])}</div><div class="lead">{esc(data['current_focus'])}</div>
<div class="flow"><section><h2>起初怎么想</h2><p>{esc(data['initial_judgment'])}</p></section>
<section><h2>哪一问让判断更清楚</h2><p>{esc(data['turning_point'])}</p></section>
<section class="now"><h2>现在怎么想</h2><p>{esc(data['current_judgment'])}</p></section></div>
<footer><h2>教练的一句反馈</h2><p>{esc(data['coach_feedback'])}</p>
<h2 style="margin-top:16px">下一次怎么试</h2><p>{esc(data['next_experiment'])}</p></footer>
</main></body></html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("输入内容须为 JSON 对象")
        result = render(data)
        Path(args.output).write_text(result, encoding="utf-8")
    except FileNotFoundError:
        print("生成回看卡失败：找不到输入文件或输出目录。请核对路径；也可改用五栏文字回看卡。", file=sys.stderr)
        return 1
    except PermissionError:
        print("生成回看卡失败：没有读取或写入权限。请换一个可访问的位置；也可改用五栏文字回看卡。", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"生成回看卡失败：输入不是有效 JSON（第 {exc.lineno} 行）。请检查内容；也可改用五栏文字回看卡。", file=sys.stderr)
        return 1
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"生成回看卡失败：{exc}。请检查输入内容或文件位置；也可改用五栏文字回看卡。", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
