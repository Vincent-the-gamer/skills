# 提示词优化：从需求到可粘贴的 Flow 提示词

方法改编自 [agbelemi/google-flow-scripting-skill](https://github.com/agbelemi/google-flow-scripting-skill)（MIT）。上游面向 Flow/Veo 的多镜头视频与分镜；这里只取适用于**免费图片生成**的部分：production profile、`@` 句柄、连续性、文字政策、自包含提示词和机械校验。没有复制上游代码；方法、术语和模板按 MIT 许可做了改写和精简。

主文件第 2 步是执行摘要；本文件是展开版，补上前后的对照、分镜模板和排错细节。如果本机已经装了上游 skill，需要多镜头/视频连续性时直接调用它；免费图片流程用本文件的精简版。

核心前提：**独立生成之间没有可靠的隐式记忆。** 角色会漂、服装会变、场景会重排。连续性要靠参考图、固定句柄和每一条都写全的提示词来承载，不能靠“它应该记得”。

## 1. Production profile

写提示词前先填：

```text
SURFACE: Google Flow
MODEL: Nano Banana 2.1（或页面显示的免费图片模型）
MODE: Text to Image / Image Edit / Multi-reference
ASPECT RATIO: 16:9 / 9:16 / 1:1
OUTPUT: 1 / 2 / n
PURPOSE: 单图 / 分镜 / 后续视频的帧
TEXT: 无文字 / 指定原文
```

改图再加：

```text
EDIT TARGET: @image.png
KEEP: 人物、服装、构图、已有文字
```

## 2. 固定连续性

### 2.1 `@PascalCase` 句柄

每个反复出现的角色、地点、道具都起一个稳定句柄：`@Mara`、`@RainyBookstore`、`@BlackUmbrella`。逻辑句柄只用字母和数字，不要空格、连字符或标点。

Flow 的 `@` 选择器可能插入的是带扩展名的文件名（如 `@Mara.png`）。**以选择器实际插入的文本为准**，后续每一轮保持同一写法；不要在同一项目里混用 `@Mara` 和 `@Mara.png`。

提示词、素材文件名、交付说明用同一个拼写。Flow 的 `@` 选择器绑定到具体素材；把文件命名成 `Mara.png` 这类稳定名字，引用时不容易选错。

### 2.2 连续性小表

| 句柄 | 锁定的外观/布局 | 参考图 |
| --- | --- | --- |
| `@Mara` | 40 多岁，短发，灰色风衣，黑伞 | 第一张满意的图 |
| `@RainyBookstore` | 绿门、左侧大窗、门前湿人行道、室内暖光 | 场景参考图 |

第一轮没有参考图时：先生成一张干净的单图（提示词里用普通文字描述，不写未定义的 `@` 句柄），选中它，再把它作为后续角度/场景的 `@` 参考。**参考图承载身份，文字只描述参考图没展示的状态和变化。**

### 2.3 Set anchor

固定地点写一段可复述的锚点，每次用到都重复：

```text
LOCATION @RainyBookstore: green door on the back wall, large window to its left,
wet sidewalk in front, warm tungsten light inside.
```

### 2.4 不要模糊回头引用

不要写“同一个”“照旧”“上一张那样”“和之前一样”。要么点名 `@` 附件，要么把当前状态重新写全。独立生成不会自动继承上一张图。

## 3. 提示词结构

从上到下：

1. **文字政策**（第一行）
2. 主体/身份 + 当前状态
3. 构图：景别、机位、主体位置、留白
4. 环境 + set anchor
5. 光线/风格
6. 细节和必要约束。

提示词语言跟用户一致；中英混写也可以，`@` 句柄和专有名词保持原样。

### 3.1 文字政策

无文字：

```text
NO TEXT IN THE IMAGE: do not render words, labels, captions, or watermarks.
```

指定文字：

```text
INTENTIONAL TEXT IN THE IMAGE: only the exact words "轨企画 01" in white sans-serif
type, bottom center; no other text.
```

改图：

```text
NO NEW TEXT IN THE IMAGE: do not add words, labels, captions, or watermarks.
Keep all existing text unchanged.
```

### 3.2 一条只做一件事

一张图只做一个时刻；一次改图只改一处。要多个时刻，生成多张图，或走下面的分镜 contact sheet。

### 3.3 正向描述优先

先写要出现的东西；负向约束只留给真实可能出现的失败（多余人物、错误文字、水印）。不要用一长串“不要”代替构图。

### 3.4 避免文字渗入

下面这些 token 容易被模型当成要渲染的文字：

- hex 色号（`#00FF00`）
- 色温数值（`5600K`）
- 方括号标签（`[SCENE 2]`）
- 裸时间码（`00:03`）

用自然语言代替：`solid chroma-key green`、`warm tungsten light`、`night`。色号真的重要时，先接受它可能出现在画面文字里的风险。

### 3.5 长度和注意力

- 最重要的约束放最前面。
- 一条只保留一个主要变化。
- 模型忽略中段时，先缩短，再重写。
- 参考图数量不要超过页面/模型的槽位；每张图分配一个角色（人物、物体、场景、风格）。

## 4. 前后对照

用户需求：

```text
雨夜书店门口的灰风衣女人，电影感，16:9，两张。
```

Production profile：

```text
SURFACE: Google Flow
MODEL: Nano Banana 2.1
MODE: Text to Image
ASPECT RATIO: 16:9
OUTPUT: 2
PURPOSE: 单图，之后可作为 @Mara 的参考
TEXT: 无文字
```

优化后的提示词：

```text
NO TEXT IN THE IMAGE: do not render words, labels, captions, or watermarks.
@Mara, a woman in her forties with short dark hair, wearing a grey trench coat,
stands at the entrance of @RainyBookstore, holding a closed black umbrella.
Medium shot, eye level, subject on the right, the green door and wet sidewalk
open on the left. Night rain, warm tungsten light from inside the store,
cool streetlight reflections, 35mm film grain, muted palette. 16:9.
```

改了什么：

- 把“电影感”拆成可拍的构图、光线、介质。
- 锁定人物外观和手持物。
- 加 set anchor，让地点可复用。
- 第一行文字政策，避免水印和乱码文字。
- 不写 hex 或色温数值，避免文字渗入。

如果这是第一张、还没有 `@Mara` 和 `@RainyBookstore` 的素材，先把这两个句柄换成普通文字描述（如 `a woman in her forties...`、`a rainy bookstore entrance...`）；生成并选中后再建立句柄。

如果 Flow 的 `@` 选择器插入的是 `@Mara.png`，把示例里的 `@Mara` 全部换成 `@Mara.png`，保持一致。

两张图不要指望一次出两个一致的人：先生成一张，选中最像的，命名成 `Mara.png`，再用 `@Mara` 生成第二张或后续编辑。

## 5. 改图提示词

```text
NO NEW TEXT IN THE IMAGE: do not add words, labels, captions, or watermarks.
Keep all existing text unchanged.
Change only the background of @image.png to solid chroma-key green.
Keep the person, clothing, composition, and all existing text unchanged.
Do not change anything else.
```

规则：

- 点名 `@` 目标。
- `Change only X` + `Keep Y unchanged`。
- 一次只改一处；改完再引用新图继续。
- 如果改坏了别处，缩小范围，不要整张重掷。

## 6. 机械检查

发送前逐项过：

1. Production profile 填完；模型/模式是图片，不是视频。
2. 每个 `@` 句柄都有定义，拼写一致；素材名一致。
3. 没有模糊回头引用；引用的是具体句柄/附件。
4. 第一行是文字政策；指定文字用引号写全；没有 hex、色温数值、方括号标签、裸时间码。
5. 没有视频词：镜头运动、时长、音频、视频、做成动画、Veo。
6. 参考图数量在槽位内；每张图角色明确；没有互相抢主角的参考。
7. 画幅、张数与页面一致。
8. 一张图只有一个时刻/一个改动。
9. 真人、品牌、地点、敏感内容已确认使用权。
10. 用户已经看过并接受，或明确说“直接生成”。

任何一项不通过：先改提示词，不发送。

## 7. 分镜 / 多格图（可选）

用户明确要 storyboard / contact sheet 时，用上游的硬规则：

- 第一句必须是 `GENERATE THE STORYBOARD IMAGE NOW.`
- 声明精确的面板数量和布局。
- 禁止规划性回复、场景拆解、素材清单和反问。
- 禁止自行添加未写的动作或多余面板。
- 结尾只要求完成的分镜图。

模板：

```text
GENERATE THE STORYBOARD IMAGE NOW.
Create exactly one contact sheet with four panels in a 2x2 grid, reading order left
to right, top to bottom.
Panel 1: @Mara steps out of the rain into @RainyBookstore.
Panel 2: @Mara closes the black umbrella and looks toward the shelves.
Panel 3: @Mara picks a book from the middle shelf.
Panel 4: @Mara turns toward the counter with the book in hand.
NO TEXT IN THE IMAGE: no labels, captions, numbers, or watermarks.
Do not write a storyboard, scene breakdown, asset list, or ask questions.
Do not add panels or invented actions. Return only the completed contact-sheet image.
```

默认面板数参考上游：4 秒 2 格（2x1）、6/8 秒 3 格（3x1）、10 秒 4 格（2x2）。只有明确写了 9 个不同画面时才用 3x3。图片流程不需要视频时长；如果用户只是要一张图，不要套分镜模板。

## 8. 上游校验器

上游的 `scripts/validate.py` 面向视频/分镜包，能检查模糊回头引用、`@` 句柄、文字政策、面板契约、时长兼容等；它不校验静态图片提示词。做图片时用上面的机械检查；做付费视频时，按 [video.md](video.md) 并参考上游 README 的 validator 用法。

---
