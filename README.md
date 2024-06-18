# 友情链接检测工具

## 项目简介
本项目是一个用来检测 Butterfly 主题友情链接 YAML 文件中的链接是否可以访问的工具。

## 项目功能
1. 使用 Python 脚本读取 Butterfly 主题的友情链接 YAML 文件。
2. 逐一测试每个链接的访问情况。
3. 将不可访问的链接输出到 `index.html` 文件中。
4. 利用 GitHub Actions 自动运行脚本,并将结果部署到 Vercel、GitHub Pages 或 Cloudflare Pages 上,以网页形式呈现。
5. github是国外的服务，所以有些域名屏蔽国外后，会出现在`index.html` 文件中，请手动检查是否可以访问，以便准确性。
## 使用方法
请看 [这篇文章](https://hexo.shangskr.top/posts/20.html) 了解如何使用本项目。

## 部署平台
- [Vercel](https://vercel.com/)
- [GitHub Pages](https://pages.github.com/)
- [Cloudflare Pages](https://pages.cloudflare.com/)

## 贡献代码
如果您有任何建议或发现问题,欢迎提交 Issue 或 Pull Request。

## 2024年6月18日16:05:55修复BUG
如果`index.html`文件没有任何变化，会导致action不能强制重新创建`index.html`文件从而导致action报错，所以在创建html之前使用touch命令确保文件的修改时间更新，避免工作流因没有变化而失败。
