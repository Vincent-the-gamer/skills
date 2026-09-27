#!/usr/bin/env node
/**
 * Jev —— TypeSafe AI 的 System One Model 命令行封装。
 *
 * 用 axios 请求 https://api-proxy.vince-g.xyz/jev，通过 cac 解析命令行参数，
 * 结果以 JSON 打印到 stdout，方便 Agent / Skill 直接消费。
 *
 * 用法：
 *   jev choice --state "..." --question "..." -o 账单 -o 技术支持 -o 销售
 *   jev noul   --state "..." --question "..."
 *   jev score  --state "..." --question "..." --options "极低,较低,中等,较高,极高"
 */
import axios from "axios";
import cac from "cac";

const VERSION = "1.0.0";

/** 服务端会把 http 308 跳转到 https，这里直接用 https，避免混合内容拦截。 */
const DEFAULT_API_URL = "https://api-proxy.vince-g.xyz/jev";
const DEFAULT_TIMEOUT_MS = 30_000;
const MAX_OPTIONS = 255;

/** choice 从选项中选一个；noul 返回是/否概率；score 按有序标准打分。 */
type JevType = "choice" | "noul" | "score";

const JEV_TYPES: readonly JevType[] = ["choice", "noul", "score"];

interface JevResult {
    type: JevType;
    probabilities: number[];
    decisionIndex: number;
    confidence?: number;
    score?: number;
    model: string;
    requestId: string;
    latencyMs: number;
}

interface JevApiResponse {
    code: number;
    message: string;
    data: JevResult;
}

interface JevRequestPayload {
    type: JevType;
    state: string;
    question: string;
    /** 仅 choice / score 需要，至少 2 个。 */
    options?: string[];
}

/** 整理后的输出结构，把概率和标签配对，便于直接读取决策。 */
interface JevOutput {
    type: JevType;
    decision: string;
    decisionIndex: number;
    probability: number;
    probabilities: Array<{ label: string; probability: number }>;
    confidence?: number;
    score?: number;
    model: string;
    requestId: string;
    latencyMs: number;
}

interface CallJevApiOptions {
    apiUrl?: string;
    timeoutMs?: number;
}

/** 请求 Jev 接口，返回接口的 data 字段；失败时抛出带可读信息的错误。 */
async function callJevApi(
    payload: JevRequestPayload,
    { apiUrl = DEFAULT_API_URL, timeoutMs = DEFAULT_TIMEOUT_MS }: CallJevApiOptions = {},
): Promise<JevResult> {
    try {
        const response = await axios.post<JevApiResponse>(apiUrl, payload, {
            headers: { "Content-Type": "application/json" },
            timeout: timeoutMs,
        });

        const json = response.data;
        if (!json || json.code !== 0 || !json.data) {
            throw new Error(json?.message || "接口返回了未知错误");
        }
        return json.data;
    } catch (error) {
        throw new Error(toErrorMessage(error));
    }
}

/** 把 axios / 网络 / 接口错误统一转成一句话。 */
function toErrorMessage(error: unknown): string {
    if (axios.isAxiosError(error)) {
        const message = (error.response?.data as JevApiResponse | undefined)?.message;
        if (message) return message;
        if (error.code === "ECONNABORTED") {
            return `请求超时（超过 ${error.config?.timeout ?? DEFAULT_TIMEOUT_MS} ms）`;
        }
        if (error.response) return `请求失败（HTTP ${error.response.status}）`;
        return `网络错误：${error.message}`;
    }
    return error instanceof Error ? error.message : String(error);
}

/** 把接口返回的概率分布和标签配对，得到可直接使用的决策结果。 */
function formatResult(result: JevResult, labels: string[]): JevOutput {
    const fallback = result.type === "noul" ? ["是", "否"] : [];
    const effective = labels.length > 0 ? labels : fallback;

    const probabilities = result.probabilities.map((probability, index) => ({
        label: effective[index] ?? `选项 ${index + 1}`,
        probability,
    }));

    return {
        type: result.type,
        decision: effective[result.decisionIndex] ?? `选项 ${result.decisionIndex + 1}`,
        decisionIndex: result.decisionIndex,
        probability: result.probabilities[result.decisionIndex] ?? 0,
        probabilities,
        ...(result.confidence !== undefined ? { confidence: result.confidence } : {}),
        ...(result.score !== undefined ? { score: result.score } : {}),
        model: result.model,
        requestId: result.requestId,
        latencyMs: result.latencyMs,
    };
}

/** 汇总 `-o/--option`（原样保留）与 `--options`（JSON 数组或逗号分隔）传入的选项。 */
function collectOptions(options: Record<string, unknown>): string[] {
    const collected: string[] = [];

    const single = options.option;
    if (Array.isArray(single)) collected.push(...single.map(String));
    else if (single != null) collected.push(String(single));

    const list = options.options;
    if (list != null) {
        const texts = Array.isArray(list) ? list.map(String) : [String(list)];
        for (const text of texts) collected.push(...splitList(text));
    }

    return collected.map((value) => value.trim()).filter(Boolean);
}

/** 支持 `--options '["a","b"]'` 与 `--options "a,b"` 两种写法。 */
function splitList(text: string): string[] {
    const trimmed = text.trim();
    if (trimmed.startsWith("[")) {
        try {
            const parsed: unknown = JSON.parse(trimmed);
            if (Array.isArray(parsed)) return parsed.map(String);
        } catch {
            // 不是合法 JSON，退回按逗号切分
        }
    }
    return trimmed
        .split(",")
        .map((value) => value.trim())
        .filter(Boolean);
}

function fail(message: string): never {
    console.error(`jev: ${message}`);
    console.error("运行 `jev --help` 查看用法。");
    process.exit(1);
}

async function main(argv: string[] = process.argv): Promise<void> {
    const cli = cac("jev");

    cli.usage("<type> --state <state> --question <question> [options]")
        .option("--state <state>", "要评估的状态 / 上下文（必填）")
        .option("--question <question>", "要提出的问题（必填）")
        .option("-o, --option <option>", "候选选项，可重复传入（choice / score 必填，至少 2 个）")
        .option("--options <list>", "候选选项，逗号分隔或 JSON 数组字符串")
        .option("--api <url>", `Jev 接口地址（默认 ${DEFAULT_API_URL}）`)
        .option("--timeout <ms>", "请求超时毫秒数", { default: String(DEFAULT_TIMEOUT_MS) })
        .option("--raw", "输出接口原始返回，而不是整理后的结果")
        .example("jev choice --state '工单内容…' --question '交给哪个团队？' -o 账单 -o 技术支持 -o 销售")
        .example("jev noul --state '用户消息…' --question '这条消息需要立即回复吗？'")
        .example("jev score --state '待执行操作…' --question '风险有多高？' --options '极低,较低,中等,较高,极高'")
        .help()
        .version(VERSION);

    // 默认命令：把第一个位置参数当作问题类型。
    cli.command("[...args]", "问题类型：choice | noul | score").usage(
        "<type> --state <state> --question <question> [options]",
    );

    const { args, options } = cli.parse(argv, { run: false });
    // --help / --version 已由 cac 输出。
    if (options.help || options.version) return;

    const type = String(args[0] ?? "").toLowerCase() as JevType;
    if (!JEV_TYPES.includes(type)) {
        fail(type ? `未知的问题类型：${type}（可选：${JEV_TYPES.join(" | ")}）` : "缺少问题类型（可选：choice | noul | score）");
    }

    const state = String(options.state ?? "").trim();
    if (!state) fail("缺少 --state（要评估的状态 / 上下文）");

    const question = String(options.question ?? "").trim();
    if (!question) fail("缺少 --question（要提出的问题）");

    const payload: JevRequestPayload = { type, state, question };
    const labels = collectOptions(options);

    if (type === "noul") {
        if (labels.length > 0) fail("noul 类型不接受选项，只用 --state 与 --question");
    } else {
        if (labels.length < 2) fail("choice / score 至少需要 2 个选项，请用 -o 传入");
        if (labels.length > MAX_OPTIONS) fail(`选项最多 ${MAX_OPTIONS} 个，当前 ${labels.length} 个`);
        payload.options = labels;
    }

    const timeoutMs = Number(options.timeout);
    if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) fail(`--timeout 必须是正整数毫秒数`);

    const result = await callJevApi(payload, {
        apiUrl: options.api ? String(options.api) : undefined,
        timeoutMs,
    });

    const output = options.raw ? result : formatResult(result, labels);
    process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
}

main().catch((error: unknown) => {
    console.error(`jev: ${toErrorMessage(error)}`);
    process.exit(1);
});
