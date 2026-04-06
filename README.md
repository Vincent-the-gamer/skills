# skills

Vincent's Agent Skills

## Skill List

### fast-dirpy

Tool Repo: [fast-dirpy](https://github.com/Vincent-the-gamer/fast-dirpy)

<div>
    <img src=".github/examples/fast-dirpy-example.jpg" style="width: 120px;"/>
</div>

Trigger words:

```
# English
The xxx folder contains a fast-dirpy.config.json configuration file and a params.json parameter file. Please use the fast-dirpy skill to download the video for me. Do not read the parameter file; just call the download method in the skill. If you encounter any errors, please let me know.

# Chinese
在xxx文件夹有fast-dirpy.config.json配置文件，和params.json参数文件，请调用fast-dirpy skill，帮我下载视频，不要读取参数文件，直接调用skill中的下载方法就好，如果报错了，告诉我。
```

### discipline

> [!IMPORTANT]
> This skill is for security and disables the most automation requests, so consider yourself if you need it.

The skill that blocks dangerous operations like file system, network requests, etc.

This skill only allows the skills enabled in your Agent and skills whitelisted in `discipline` skill itself.

add these into your Agent's persona/system prompts to use.

> [!INFO]
> Tell something like this is OK. The prompt are not fixed words.

```
## Important

- Before you control the computer, call discipline skill first, and understand the rules.

```

#### Allowed Operations

See [discipline skill](./discipline/SKILL.md)

### More

More skills are coming soon.

## License

[Apache License 2.0](./LICENSE) | Copyright (c) 2026-PRESENT @ Vincent-the-gamer
