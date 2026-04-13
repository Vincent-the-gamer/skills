import cac, { CAC } from "cac";
import pkgJson from '../package.json'
import restoreCursor from 'restore-cursor'
import { logger } from "./utils/logger";
import axios from "./utils/axios";

const cli: CAC = cac("skills")

const { version } = pkgJson

const skillLinkMap: Record<string, string> = {
  base64: ""
}


cli.command("list", "List skills.")
  .alias("ls")
  .action(() => {
    logger.success(Object.keys(skillLinkMap).join(", "))
  })

cli.command("download <skill:string>", "Download specific skill.")
  .alias("dl")
  .action(async (skill: string) => {
    if (!skillList.includes(skill)) {
      logger.error(`${skill} not found!`)
      return
    } else {
      const { data } = await axios.get("https://download-directory.github.io/", {
        params: {
          url
        }
      })
    }
  })

cli.help()
cli.version(version)
cli.parse()

restoreCursor()