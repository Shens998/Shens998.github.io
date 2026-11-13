# 沈石 · Shi Shen — 学术主页

面向 GitHub Pages 的静态学术网站。原生 HTML / CSS / JavaScript，无需安装依赖或构建。

- 英文默认首页，完整中文版本位于 `/zh/`，支持语言切换并保留章节位置
- 两种语言均提供研究方向、项目、学术经历、公开学术履历与隐私说明
- 31 篇论文，按研究方向、年份、关键词组合筛选
- 科研项目、学术经历、奖励、参编专著与知识产权
- 可打印的公开版学术履历 `profile.html`
- 响应式布局、键盘操作、减少动态效果偏好及无 JavaScript 论文阅读

## 内容来源

主体内容由所有者提供的个人简历整理。原始简历及提取文本不包含在此仓库中；论文题名、作者缩写和贡献标记保留原始资料。没有刊载旧影响因子、分区或未经核实的引文量。任职沿用简历，维护者应在情况变化时更新。

额外核验的代表性论文记录：

- ST-CA: https://doi.org/10.1016/j.jag.2022.102789
- 台风海燕在线社会响应: https://doi.org/10.1057/s41599-023-01922-5 （期刊记录为 10:426，校正简历中的 Article 1）
- 高原源区径流复杂性: https://doi.org/10.1016/j.jhydrol.2020.124996 （补全文章号与 DOI）

其余 DOI 来自所有者提供的简历；未提供 DOI 的条目使用期刊链接或标明为“检索文献”的 Crossref 查询链接，不能将检索链接视作唯一匹配记录。首页研究配图来自所有者 Zotero 中的正式发表论文，保留原始配色、图例和标签；页面提供作者、图号、原文与 CC BY 4.0 许可链接。详情见 `assets/figure-sources.json`。

## 本地预览与检查

```sh
python3 scripts/check_site.py
python3 -m http.server 8000
```

打开 http://localhost:8000 。无需外部字体、CDN、API、数据库或密钥。

## GitHub Pages 部署

仓库：`Shens998/Shens998.github.io`，预期网址：https://shens998.github.io/

1. 推送网站文件和 `.github/workflows/pages.yml` 至 `hexo`（或 `main` / `master`）。
2. 在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
3. 查看 **Actions → Deploy academic website to GitHub Pages**；必要时选择 **Run workflow**。
4. 等待部署成功后打开上述网站。此地址只有部署成功后才代表本次版本已上线。

工作流通过显式白名单打包网页和所用资源，不会发布旧博客目录、脚本、README、原始简历或工作文件。仓库旧历史仍可能包含旧博客数据；白名单不能删除 Git 历史。

## 维护

论文目录有四个静态副本（中英文首页与公开履历）和一个可下载的 `assets/publications.json`。编辑 JSON 后运行 `python3 scripts/sync_publications.py`，同步四个页面和数量，再运行检查。论文无 JavaScript 也能阅读。论文题名、作者与期刊保留发表语言；英文界面中的项目、专著、专利与软件标题为说明性翻译。

中文内容编辑 `zh/index.html` 与 `zh/profile.html`；英文翻译对照在 `scripts/translations.json`。运行 `python3 scripts/build_english.py` 生成英文默认页 `index.html`、`profile.html` 和 `404.html`。不要只编辑生成后的英文页，否则下次生成会覆盖。样式见 `assets/style.css`，筛选交互见 `assets/site.js`。打印公开版履历可另存为 PDF。维护内容时不应将私人简历 PDF 放入公开仓库。

## 隐私

公开内容省略个人电话、生日、详细地址、籍贯和政治面貌。工作邮箱 `shens@bnu.edu.cn` 经所有者明确授权公开。语言由页面 URL 确定，默认英文，不依赖浏览器语言，也不使用 Cookie 或本地存储。无追踪脚本、第三方字体或访客表单。交流入口为所有者公开 GitHub 页面。GitHub Pages 及外部链接有各自的服务隐私政策。


## Google Scholar 与每月维护

公开主页：https://scholar.google.com/citations?user=qGDGTIIAAAAJ&hl=en

`assets/scholar.json` 保存有来源、日期和核验方式的指标快照。2026-11-12 的首批数字由所有者从 Scholar 提供：总计 2027 / 23 / 49，2021 年至今 1873 / 21 / 47（引用次数 / h-index / i10-index）。网页会明确区分这两列；之后不按当前年份推测 since 年份。此快照并非本次自动抓取成功的结果。

本聊天已配置 Codex 每月维护任务（每月 1 日北京时间 09:00）。这是本机 Codex 计划任务，不是 GitHub Actions 定时爬虫；执行时需要电脑开机、应用运行、项目可用及有效的网络／GitHub 凭据。权限限制或 Google Scholar 验证码可能使当月更新失败，任务将报告原因并保留旧数据。

正常公开访问更新：

```sh
python3 scripts/update_scholar.py
python3 scripts/sync_publications.py
python3 scripts/check_site.py
python3 -m unittest discover -s tests -v
```

也可用 `python3 scripts/update_scholar.py --html /path/to/exported-scholar.html` 导入从该公开 Scholar 页面保存的 HTML。不会使用 Google 登录 Cookie，不会绕过验证码或反复请求。网页不直接请求 Scholar，避免访客追踪和跨域故障。读取失败时脚本非零退出，不改已有快照；脚本只刷新指标，新增论文由每月任务依据 Scholar 和出版来源核实后再更新 `assets/publications.json`。

网站在此前参考 https://sciextremes.github.io/ 的研究导向布局基础上，于 2026-11-13 按所有者选择的 C「学术履历型」方案重构。中英文首页和公开履历统一使用暖纸色、深褐色、衬线标题与细线图标。首页将姓名、研究方向、论文原图及学术经历编排为学术档案；代表成果保留完整论文配图与来源。未使用生成的大幅装饰图，也未复制参考站的成果或图件。公开履历提供章节导航，打印时自动展开项目列表，结束后恢复原有折叠状态。

## 论文配图来源

从 Zotero 的正式发表 PDF 提取并逐图核查：

- Geng, Shen, Cheng & Dai (2022), ST-CA，图 2（PDF 第 3 页），完整图件。第 1 页注明 CC BY 4.0。
- Shen et al. (2023), Typhoon Haiyan，图 2（PDF 第 4 页），完整图件。第 15 页注明 CC BY 4.0，所用图无单独排除许可的署名。
- Sun, Shen & Xia (2025), Land 14:1892，图 5a（PDF 第 13 页），仅该子图，保留其图例与插图。第 1 页注明 CC BY 4.0。https://doi.org/10.3390/land14091892

图像只进行页面裁切和栅格化，没有改变数据、配色或图中标注。点击首页配图可打开完整尺寸图片；DOI 入口提供论文全文上下文。原始 PDF、Zotero 私人附件路径及阅读笔记不随网站发布。2020 年径流研究继续保留在论文目录中；其 PDF 标记 All rights reserved，本次未使用其图件。

新增配图时同时更新 `assets/figure-sources.json`、中英文配图说明、`scripts/check_site.py` 和部署白名单；不要直接打包整个 Zotero 附件目录。
