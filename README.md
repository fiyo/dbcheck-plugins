# DBCheck 插件市场

> 🌐 [DBCheck](https://github.com/fiyo/DBCheck) 的官方插件市场。  
> 在这里发布、发现和安装社区贡献的巡检规则、通知渠道、报告模板等插件。

## 快速开始

### 安装插件

在 DBCheck Web UI 左侧导航 → **🧩 插件市场** → 浏览并一键安装。

### 发布你的插件

1. Fork 本仓库
2. 在 `plugins/` 目录下创建你的插件目录（参考 `demo-ascii-table-check`）
3. 编辑 `registry.json`，在 `plugins` 数组中添加你的插件条目
4. 提 PR → CI 自动验证 → 合并后上架 🎉

详见 [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

## 插件列表

| 插件 | 版本 | 作者 | 类型 | 下载 |
|------|------|------|------|------|
| [ASCII字符集表检测](plugins/demo-ascii-table-check) | 0.1.0 | DBCheck Team | 巡检 | - |

## 目录结构

```
dbcheck-plugins/
├── registry.json          # 市场索引
├── plugins/               # 插件源码
│   └── demo-ascii-table-check/
│       ├── plugin.json    # 清单
│       ├── __init__.py     # 入口
│       └── README.md       # 说明
├── .github/workflows/     # CI 自动验证
└── README.md
```
