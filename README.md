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

其余 DOI 来自所有者提供的简历；未提供 DOI 的条目使用期刊链接或标明为“检索文献”的 Crossref 查询链接，不能将检索链接视作唯一匹配记录。首页图片均为本地生成的抽象研究主题示意，非论文图件或实测数据。

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

公开内容省略个人电话、生日、详细地址、籍贯、政治面貌和邮箱。语言由页面 URL 确定，默认英文，不依赖浏览器语言，也不使用 Cookie 或本地存储。无追踪脚本、第三方字体或访客表单。交流入口为所有者公开 GitHub 页面。GitHub Pages 及外部链接有各自的服务隐私政策。
