# Flow 图片提示词

先按 [prompt-optimizer.md](prompt-optimizer.md) 把需求优化成 production-ready 提示词，再用下面的模板改写。一次性图片可以不起句柄；要连续生成、改图或保持角色一致时，用稳定的 `@PascalCase` 句柄，并在每条提示词里点名。

## 公式

```text
文字政策 + 主体/身份 + 构图/景别 + 环境 + 光线 + 风格/介质 + 细节
```

| 槽位 | 写什么 | 例 |
| --- | --- | --- |
| 文字政策 | 有没有文字，原文是什么 | `NO TEXT IN THE IMAGE` |
| 主体 | 谁/什么，外观特征 | `@Mara`，短发，灰色风衣 |
| 构图 | 景别、机位、主体位置 | 中景，平视，人物在画面右侧 |
| 环境 | 地点、时间、天气 | `@RainyBookstore`，雨夜 |
| 光线 | 光源、方向、色温 | 店内暖色钨丝灯，街灯冷色反光 |
| 风格 | 介质、年代、色调 | 35mm 胶片颗粒，低饱和 |
| 细节 | 必须出现/必须保留的东西 | 黑伞、门框、画面无文字 |

画幅和张数在页面里设置；提示词里写 `16:9` 也可以，但以 UI 为准。

## 规则

- 第一行先写文字政策：`NO TEXT IN THE IMAGE...` 或 `INTENTIONAL TEXT IN THE IMAGE...`；改图写 `NO NEW TEXT...` 并保留已有文字。
- 用具体名词。“电影感”“史诗感”单独出现不产生画面。
- 只写静态画面。**镜头推进、摇镜、8 秒、视频、做成动画、对白、音效、Veo、让画面动起来**都属于视频分支；出现时先问用户，确认后才转 [video.md](video.md)。
- 画面文字用引号写出原文，并说明位置和风格；文字越短越稳。
- 多张参考图要分配角色：人物、场景、道具、风格各司其职。
- 改图写清“只改什么、保留什么、其他不动”，一次只改一处。
- 反复出现的角色/地点/道具用同一个 `@` 句柄；不要写“同一个”“照旧”“上一张那样”。
- 不写 hex 色号、色温数值、方括号标签、裸时间码；这些容易被渲染成画面文字。
- 重要约束放前面；模型忽略中段时先缩短，再重写。

## 模板

### 文生图

```text
NO TEXT IN THE IMAGE: do not render words, labels, captions, or watermarks.
@Mara, a woman in her forties with short dark hair, wearing a grey trench coat,
stands at the entrance of @RainyBookstore, holding a closed black umbrella.
Medium shot, eye level, subject on the right, the green door and wet sidewalk
open on the left. Night rain, warm tungsten light from inside the store,
cool streetlight reflections, 35mm film grain, muted palette. 16:9.
```

### 改背景

```text
NO NEW TEXT IN THE IMAGE: do not add words, labels, captions, or watermarks.
Keep all existing text unchanged.
Change only the background of @image.png to solid chroma-key green.
Keep the person, clothing, composition, and all existing text unchanged.
Do not change anything else.
```

### 移除/替换元素

```text
NO NEW TEXT IN THE IMAGE: do not add words, labels, captions, or watermarks.
Change only the left side of @image.png: remove the passerby and rebuild the hidden street.
Keep the other people, composition, lighting, and all existing text unchanged. Do not change anything else.
```

### 改光线/风格

```text
NO NEW TEXT IN THE IMAGE: do not add words, labels, captions, or watermarks.
Change only the lighting of @image.png to warm orange side light at dusk, soft shadows.
Keep the person, composition, and all existing text unchanged. Do not change anything else.
```

### 多图合成

```text
NO TEXT IN THE IMAGE: do not render words, labels, captions, or watermarks.
Use the person from @Mara, place them on the street from @RainyStreet,
holding the white cup from @WhiteCup.
Keep face, clothing, and scene lighting consistent. Medium shot, eye level, 16:9.
```

### 角色一致性

```text
NO TEXT IN THE IMAGE: do not render words, labels, captions, or watermarks.
@Mara, using the face, short dark hair, and grey trench coat from @Mara.png,
sits by a cafe window. Medium shot, soft side light, blurred background, 16:9.
```

### 海报文字

```text
INTENTIONAL TEXT IN THE IMAGE: only the exact words "轨企画 01" in white sans-serif
type, bottom center; no other text.
A minimalist film poster: deep blue background, a character silhouette in the
upper half, generous negative space. 16:9.
```

### 风格迁移

```text
NO TEXT IN THE IMAGE: do not render words, labels, captions, or watermarks.
Keep the composition and @Mara unchanged; render the image in 1990s Japanese
anime cel style, soft shadows, warm palette, light film grain.
```

## 首轮结果不对时

| 问题 | 先改什么 |
| --- | --- |
| 文字错/糊 | 缩短文字，用引号写原文，指定位置和字体；一次只放一处文字 |
| 画面出现色号/标签 | 删掉 hex、色温数值、方括号标签；换成自然语言 |
| 人物不像 | 换更干净、主体更大的参考图；用 `@` 明确“参考这张脸/这套衣服” |
| 构图乱 | 补景别、机位、主体位置和留白 |
| 背景像贴上去 | 写清光源方向、色温和阴影；用改图统一光线 |
| 多出元素 | 用改图移除，保留其他部分 |
| 风格不稳 | 写具体介质/年代/色调，少堆抽象形容词 |
| 改图把别处改坏 | 缩小范围：“只改 X，保留 Y”；一次只改一处 |
| 多图风格冲突 | 减少参考图；让一张主导人物，一张主导场景 |

## 要视频

先读 [video.md](video.md)，并确认用户同意付费。图片模板里的镜头运动、时长、音频都属于视频分支。

---

本文件由 AI agent 起草，尚未经人类审阅。
