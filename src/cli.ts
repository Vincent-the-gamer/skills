import cac, { CAC } from "cac";
import pkgJson from '../package.json'
import restoreCursor from 'restore-cursor'
import { logger } from "./utils/logger";
import axios from "./utils/axios";
import { downloadSkillFromGitHub } from "./utils/github";

const cli: CAC = cac("skills")

const { version } = pkgJson

const skillList: string[] = [
  "base64",
  "discipline",
  "fast-dirpy",
  "heihua",
  "ncmdump",
  "weather"
]

cli.command("list", "List skills.")
  .alias("ls")
  .action(() => {
    logger.success(skillList.join(", "))
  })

cli.command("download <skill:string>", "Download specific skill.")
  .alias("dl")
  .option("savePath <path>", "The path to save the skill to.")
  .action(async (skill: string, options: Record<string, any>) => {
    if (!skillList.includes(skill)) {
      logger.error(`${skill} not found!`)
      return
    } else {
      let savePath: string
      if (!options.savePath) {
        savePath = process.cwd() + `/skills/${skill}`
        logger.warn(`--savePath not provided! Defaulting to ${savePath}`)
      } else {
        savePath = options.savePath
      }
      await downloadSkillFromGitHub(`skills/${skill}`, savePath)
    }
  })

cli.help()
cli.version(version)
cli.parse()

restoreCursor()