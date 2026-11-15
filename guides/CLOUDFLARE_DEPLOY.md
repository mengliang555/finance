# 部署到 Cloudflare Workers（静态资源）

## 为什么需要构建步骤

`docs/` 是站点的源目录，但报告正文（`reports/**/*.md`、`guides/**/*.md`）在仓库其他位置。
Workers 只上传 `assets.directory` 指定的目录，访问不到仓库里的其他文件。

所以部署前先运行 `scripts/build_site.py`，把三类内容合并成一个自包含目录：

```
dist/
├── index.html                  # 复制自 docs/
├── css/ js/ images/
├── reports_index.html
├── reports/                    # docs/reports/*.html + reports/**/*.md
├── guides/                     # guides/*.md
└── _headers                    # Workers 静态资源原生支持的响应头
```

报告中心优先从同源加载 Markdown，GitHub raw 只作为兜底，因此站点运行时不再依赖
`raw.githubusercontent.com`。

## 连接 Git：Workers Builds

在 **Workers & Pages → Create → Connect to Git** 表单中按下表填写（与 `wrangler.toml`
里的 `[assets] directory` 配套）：

| 表单字段 | 值 |
|---|---|
| Project name | `finance` |
| Build command | `python3 scripts/build_site.py` |
| Deploy command | `npx wrangler deploy`（默认值，保持不动） |
| Preview command | `npx wrangler preview`（默认值，保持不动） |
| Root directory | 留空 |
| Build variables | 可选：`PYTHON_VERSION=3.13`（仓库已提交 `.python-version`，通常不需要） |

点击部署后，首次构建会执行构建命令，再由 `wrangler deploy` 把 `dist/` 作为静态资源上传。
成功后地址形如 `https://finance.<你的 workers.dev 子域>.workers.dev`。

> 关键点：`wrangler.toml` 必须使用 Workers 的 `[assets] directory = "./dist"`。
> 如果误用 Pages 的 `pages_build_output_dir`，`wrangler deploy` 不会把它当作静态资源目录，
> 部署会失败或发布一个空站点。

Workers Builds 的构建镜像自带 Python 3.13/3.14，无需安装依赖；每次推送到 `main`
（含每日分析机器人的提交）都会触发生产部署，其他分支可按需开启预览构建。

## 本地运行

```bash
# 1. 组装产物
python scripts/build_site.py

# 2. 本地预览（默认 http://localhost:8787）
npx wrangler dev

# 3. 登录并发布
npx wrangler login
npx wrangler deploy
```

本地也可以用 `python -m http.server -d dist 8000` 快速查看，但它不会应用 `_headers`。

## 自定义域名

Workers 的自定义域名要求域名的 **NS 托管在 Cloudflare**（Pages 支持外部域名 CNAME，
Workers 不支持这一点）：

1. 进入 Worker → **Settings** → **Domains & Routes** → **Add custom domain**；
2. 选择已托管在 Cloudflare 的域名或子域，确认后自动签发证书。

绑定后建议同步更新 `README.md`、`NAVIGATION.md` 中的站点地址，以及
`scripts/daily_analysis_config.json` 里的 `monitoring.health_check_url`。

## 缓存与响应头

`_headers` 由构建脚本生成，位于 `dist/_headers`：

- 全站：`X-Content-Type-Options`、`Referrer-Policy`、`X-Frame-Options`；
- `*.md`：`Cache-Control: public, max-age=300`，保证报告更新后较快生效。

HTML 与 JS/CSS 沿用 Cloudflare 默认缓存；每日报告文件名带日期，不会互相覆盖。

## 与 GitHub Pages 并存

两套部署可以同时运行：

- GitHub Pages 继续发布 `docs/`，报告中心回退到 GitHub raw 加载 Markdown；
- Cloudflare Workers 发布 `dist/`，同源加载 Markdown，速度更快，也不要求仓库公开。

## 故障排查

| 现象 | 原因与处理 |
|---|---|
| 部署报错提到 `pages_build_output_dir` | 配置混用了 Pages 语法，改成 `[assets] directory = "./dist"` |
| 构建日志 `python3: command not found` | 在 Build variables 中设置 `PYTHON_VERSION=3.13` |
| 部署成功但访问 404 | `[assets] directory` 不是 `./dist`，或构建命令没有产出 `dist/` |
| 预览构建失败 | Preview 命令保留默认 `npx wrangler preview`；若想用版本 URL，可改为 `npx wrangler versions upload` |
| 报告中心仍在请求 `raw.githubusercontent.com` | 产物里没有 `reports/*.md`，检查构建日志 |
| 自定义域名添加失败 | Workers 要求域名 NS 在 Cloudflare；外部域名只能用 Pages |

## 如果更想用 Pages

Pages 仍然可用，但需要把配置换回 Pages 语法，并在创建流程里填 **Build output directory = `dist`**：

```toml
name = "finance"
pages_build_output_dir = "dist"
```

两种方式只能选一种配置，不要在同一份 `wrangler.toml` 里混用。

## 限制

- 静态资源请求免费；Workers 免费计划每天的请求额度只作用于 Worker 脚本调用，纯静态站点不产生这类调用。
- `*.workers.dev` 在中国大陆的可达性不稳定，面向国内用户时建议绑定自有域名并实测。
