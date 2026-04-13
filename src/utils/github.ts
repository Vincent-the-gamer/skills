import axios from "./axios";
import fs from "fs";
import path from "path";
import { logger } from "./logger";

async function getBranchContent(repo: string, branch: string = 'main', recursive: boolean = false) {
  const { data } = await axios.get(`https://api.github.com/repos/${repo}/git/trees/${branch}`, {
    headers: {
      'Accept': 'application/json',
    },
    params: {
      recursive: recursive ? 1 : 0,
    },
  });

  return data;
}

export async function downloadSkillFromGitHub(filePath: string, savePath: string, branch: string = 'main', mirror?: string) {
  try {
    const { tree } = await getBranchContent("Vincent-the-gamer/skills", branch, true);

    let skillFiles = tree.filter((item: any) => {
      return item.path.startsWith(filePath)
    });

    logger.info(`${skillFiles.length} files found to download.`);

    if(mirror?.endsWith('/')) {
      mirror = mirror.slice(0, -1);
    }

    // 创建所有下载任务的 Promise 数组
    const downloadPromises = skillFiles.map(async (file: any) => {
      const url = `${mirror ?? 'https://raw.githubusercontent.com'}/Vincent-the-gamer/skills/${branch}/${file.path}`;

      // 构建完整的本地保存路径
      const localFilePath = path.join(savePath, file.path.replace(filePath, ''));

      logger.info(`Downloading ${url} -> ${localFilePath}`);

      const response = await axios({
        method: 'get',
        url,
        responseType: 'stream',
        headers: {
          'Accept': 'application/vnd.github.v3.raw'
        }
      });

      if (response.status === 404) {
        logger.error(`GitHub content not found: ${url}`)
        return Promise.reject(new Error(`GitHub content not found: ${url}`))
      }

      // 确保目录存在
      const dirName = path.dirname(localFilePath);
      if (!fs.existsSync(dirName)) {
        fs.mkdirSync(dirName, { recursive: true });
      }

      const writer = fs.createWriteStream(localFilePath);
      response.data.pipe(writer);

      // 返回 Promise，等待单个文件下载完成
      return new Promise((resolve, reject) => {
        writer.on('finish', () => {
          logger.info(`File Downloaded: ${localFilePath}`);
          resolve(localFilePath);
        });
        writer.on('error', reject);
      });
    });

    // 等待所有文件下载完成
    const results = await Promise.allSettled(downloadPromises);

    logger.success(`All files downloaded successfully, ${results.length} files in total.`);
    return results;

  } catch (error: any) {
    console.error('Download failed:', error.message);
    throw error;
  }
}