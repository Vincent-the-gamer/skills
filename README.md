# skills

Vincent's Agent Skills

## Skill List

- [fast-dirpy](./skills/fast-dirpy/README.md)
- [discipline](./skills/discipline/README.md)
- [weather](./skills/weather/README.md)
- [base64](./skills/base64/README.md)
- [ncmdump](./skills/ncmdump/README.md)

### Chinese skills

- [heihua(互联网黑话)](./heihua/README.md)

More skills are coming soon.

## Skill Download CLI

Usage: `npx @vince-gamer/skills --help`

List available skills: `npx @vince-gamer/skills lisst`

Download skills:

```bash
# e.g. npx @vince-gamer/skills download ncmdump
#
# Default save path: cwd(current work directory)/<skill-name>
npx @vince-gamer/skills download <skill_name>

# custom path
npx @vince-gamer/skills download <skill_name> --save-path ./xxx

# use mirror of raw.githubusercontent.com
npx @vince-gamer/skills download <skill_name> --mirror https://xxx
```

## License

[Apache License 2.0](./LICENSE) | Copyright (c) 2026-PRESENT @ Vincent-the-gamer
