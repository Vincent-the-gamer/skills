# skills

Vincent's Agent Skills

> [!TIP]
> Hint: `disable-model-invocation: true` means that the user need to trigger the skill manually, the agents won't trigger it automatically.

## Skill List

- [fast-dirpy](./skills/fast-dirpy/README.md)
- [discipline](./skills/discipline/README.md)
- [weather](./skills/weather/README.md)
- [base64](./skills/base64/README.md)
- [ncd](./skills/ncd/README.md)
- [slidev](./skills/slidev/README.md)

### Skills from Matt Pocock

- [writing-great-skills](./skills/writing-great-skills/README.md)

### Chinese skills

- [heihua(互联网黑话)](./heihua/README.md)

More skills are coming soon.

## Use skills in Zed

Create `.agents/skills/<skill-name>` folder，then create a SKILL.md as entry file.

## Skill Download CLI

Usage: `npx @vince-gamer/skills --help`

List available skills: `npx @vince-gamer/skills list`

Download skills:

```bash
# e.g. npx @vince-gamer/skills download ncmdump
#
# Default save path: cwd(current work directory)/<skill-name>
npx @vince-gamer/skills download <skill_name>

# custom path
npx @vince-gamer/skills download <skill_name> --save-path ./xxx

# use mirror of https://raw.githubusercontent.com
npx @vince-gamer/skills download <skill_name> --mirror https://xxx
```

## License

[Apache License 2.0](./LICENSE) | Copyright (c) 2026-PRESENT @ Vincent-the-gamer
