"""
Demo插件 —— ASCII字符集表检测

这是 DBCheck 插件系统的入门示例，展示 InspectionPlugin 的完整开发流程：
1. 继承 InspectionPlugin
2. 实现 get_queries() 返回 SQL 列表
3. 实现 analyze() 分析结果返回风险
4. 调用 register() 注册

更多文档: https://github.com/fiyo/dbcheck-plugins
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from plugin_core import InspectionPlugin, InspectionQuery, RiskItem, register


class ASCIITableChecker(InspectionPlugin):
    id = "demo-ascii-table-check"
    name = "ASCII字符集表检测（Demo）"
    version = "0.1.0"
    db_types = ["mysql", "oracle", "postgresql", "dm8"]
    author = "DBCheck Team"
    description = "检测数据库中非ASCII字符集的表，评估多语言兼容性风险"

    def get_queries(self):
        return [
            InspectionQuery(
                key="non_ascii_tables",
                sql="""
                    SELECT table_schema, table_name, table_collation
                    FROM information_schema.tables
                    WHERE table_collation IS NOT NULL
                      AND table_collation NOT LIKE 'ascii%'
                      AND table_collation NOT LIKE 'utf8%'
                      AND table_collation NOT LIKE 'latin1%'
                    ORDER BY table_schema, table_name
                    LIMIT 100
                """,
                desc_zh="非ASCII字符集的表（MySQL）",
                desc_en="Tables with non-ASCII collation (MySQL)",
                db_type="mysql"
            ),
            InspectionQuery(
                key="non_ascii_tables_pg",
                sql="""
                    SELECT schemaname, tablename
                    FROM pg_catalog.pg_tables
                    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                    ORDER BY schemaname, tablename
                    LIMIT 100
                """,
                desc_zh="表列表（PG字符集检测入口）",
                desc_en="Table list for charset check (PG)",
                db_type="postgresql"
            ),
        ]

    def analyze(self, context):
        risks = []
        for key in ['non_ascii_tables', 'non_ascii_tables_pg']:
            data = context.get(key, {})
            rows = data.get('rows', []) if isinstance(data, dict) else []
            if len(rows) > 50:
                risks.append(RiskItem(
                    level="MEDIUM",
                    title=f"发现 {len(rows)} 个非标准字符集的表",
                    description="大量表使用非ASCII字符集，可能在数据迁移或跨平台时引起编码问题",
                    suggestion="建议评估这些表是否必须使用特殊字符集，统一为 utf8mb4 / AL32UTF8",
                    category="plugin"
                ))
            elif rows:
                risks.append(RiskItem(
                    level="LOW",
                    title=f"发现 {len(rows)} 个非标准字符集的表（数量较少）",
                    description="少量表使用非ASCII字符集，请确认是否为业务需要",
                    suggestion="如非必要，建议统一字符集",
                    category="plugin"
                ))
        return risks


# 注册插件
register(ASCIITableChecker())
