import asyncio
import json
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from common.config import appConfig


@dataclass
class SemgrepResult:
    """Semgrep 扫描结果封装"""

    success: bool
    output: Optional[Any] = None
    stderr: Optional[str] = None
    returncode: Optional[int] = None
    errors: List[str] = field(default_factory=list)

    @property
    def has_findings(self) -> bool:
        """是否有发现问题"""
        if not isinstance(self.output, dict):
            return False
        return len(self.output.get("results", [])) > 0

    @property
    def findings_count(self) -> int:
        """问题数量"""
        if not isinstance(self.output, dict):
            return 0
        return len(self.output.get("results", []))

    @property
    def findings(self) -> List[Dict[str, Any]]:
        """所有发现的问题"""
        if not isinstance(self.output, dict):
            return []
        return self.output.get("results", [])


class SemgrepClient:
    """
    Semgrep 客户端 - 支持同步和异步扫描

    支持三种扫描方式:
    1. 本地路径扫描: scan(target="/path/to/code")
    2. 单文件内容扫描: scan(content="code", filename="app.py")
    3. 多文件内容扫描: scan(target={"app.py": "code1", "utils.py": "code2"})
    """

    def __init__(self):
        """初始化客户端并加载配置"""
        if hasattr(appConfig, "semgrep"):
            self._config = appConfig.semgrep
        else:
            # 提供默认配置
            from types import SimpleNamespace

            self._config = SimpleNamespace(
                timeout=30, jobs=4, max_memory=0, debug=False
            )

    @property
    def config(self):
        """返回配置对象"""
        return self._config

    def scan(
        self,
        target: Union[str, Path, Dict[str, str], None] = None,
        content: Optional[str] = None,
        filename: str = "code.txt",
        config: Optional[str] = None,
        rules: Optional[List[str]] = None,
        json_output: bool = True,
        **kwargs,
    ) -> SemgrepResult:
        """
        同步扫描接口

        Args:
            target: 本地路径或多文件字典 {路径: 内容}
            content: 单文件字符串内容
            filename: content 对应的文件名(用于语言识别)
            config: 规则配置(如 "p/security-audit", "auto")
            rules: 额外规则列表
            json_output: 是否返回 JSON 格式
            **kwargs: 其他 semgrep 参数(如 verbose, quiet, severity 等)

        Returns:
            SemgrepResult 对象
        """
        # 参数验证
        if target is None and content is None:
            raise ValueError("必须提供 target 或 content 参数")
        if target is not None and content is not None:
            raise ValueError("target 和 content 参数不能同时提供")

        # 根据输入类型选择处理方式
        if content:
            return self._scan_content(
                content, filename, config, rules, json_output, **kwargs
            )
        elif isinstance(target, dict):
            return self._scan_files(target, config, rules, json_output, **kwargs)
        else:
            return self._scan_path(str(target), config, rules, json_output, **kwargs)

    async def ascan(
        self,
        target: Union[str, Path, Dict[str, str], None] = None,
        content: Optional[str] = None,
        filename: str = "code.txt",
        config: Optional[str] = None,
        rules: Optional[List[str]] = None,
        json_output: bool = True,
        **kwargs,
    ) -> SemgrepResult:
        """
        异步扫描接口 (参数同 scan 方法)
        """
        # 参数验证
        if target is None and content is None:
            raise ValueError("必须提供 target 或 content 参数")
        if target is not None and content is not None:
            raise ValueError("target 和 content 参数不能同时提供")

        # 根据输入类型选择处理方式
        if content:
            return await self._ascan_content(
                content, filename, config, rules, json_output, **kwargs
            )
        elif isinstance(target, dict):
            return await self._ascan_files(target, config, rules, json_output, **kwargs)
        else:
            return await self._ascan_path(
                str(target), config, rules, json_output, **kwargs
            )

    # ========================
    # 同步扫描内部方法
    # ========================

    def _scan_content(
        self, content: str, filename: str, config, rules, json_output, **kwargs
    ) -> SemgrepResult:
        """同步扫描单个字符串内容"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / filename
            tmp_path.write_text(content, encoding="utf-8")
            return self._scan_path(tmpdir, config, rules, json_output, **kwargs)

    def _scan_files(
        self, files: Dict[str, str], config, rules, json_output, **kwargs
    ) -> SemgrepResult:
        """同步扫描多个文件内容"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            for rel_path, code in files.items():
                fpath = base / rel_path
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(code, encoding="utf-8")
            return self._scan_path(tmpdir, config, rules, json_output, **kwargs)

    def _scan_path(
        self, path: str, config, rules, json_output, **kwargs
    ) -> SemgrepResult:
        """同步扫描路径"""
        args = self._build_args(path, config, rules, json_output, **kwargs)

        try:
            proc = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=False,
                timeout=getattr(self._config, "timeout", 60) + 10,
            )
            return self._parse_result(
                proc.stdout.strip(), proc.stderr.strip(), proc.returncode
            )
        except FileNotFoundError:
            return SemgrepResult(
                success=False,
                stderr="Semgrep 未安装",
                returncode=127,
                errors=["Semgrep CLI not found"],
            )
        except subprocess.TimeoutExpired:
            return SemgrepResult(
                success=False,
                stderr="执行超时",
                returncode=124,
                errors=["Execution timeout"],
            )

    # ========================
    # 异步扫描内部方法
    # ========================

    async def _ascan_content(
        self, content: str, filename: str, config, rules, json_output, **kwargs
    ) -> SemgrepResult:
        """异步扫描单个字符串内容"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / filename
            tmp_path.write_text(content, encoding="utf-8")
            return await self._ascan_path(tmpdir, config, rules, json_output, **kwargs)

    async def _ascan_files(
        self, files: Dict[str, str], config, rules, json_output, **kwargs
    ) -> SemgrepResult:
        """异步扫描多个文件内容"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            for rel_path, code in files.items():
                fpath = base / rel_path
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(code, encoding="utf-8")
            return await self._ascan_path(tmpdir, config, rules, json_output, **kwargs)

    async def _ascan_path(
        self, path: str, config, rules, json_output, **kwargs
    ) -> SemgrepResult:
        """异步扫描路径"""
        args = self._build_args(path, config, rules, json_output, **kwargs)

        try:
            proc = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=getattr(self._config, "timeout", 60) + 10,
                )
                return self._parse_result(
                    stdout.decode().strip(), stderr.decode().strip(), proc.returncode
                )
            except asyncio.TimeoutError:
                proc.kill()
                return SemgrepResult(
                    success=False,
                    stderr="执行超时",
                    returncode=124,
                    errors=["Execution timeout"],
                )
        except FileNotFoundError:
            return SemgrepResult(
                success=False,
                stderr="Semgrep 未安装",
                returncode=127,
                errors=["Semgrep CLI not found"],
            )

    # ========================
    # 工具方法
    # ========================

    def _build_args(self, path: str, config, rules, json_output, **kwargs) -> List[str]:
        """构建 semgrep 命令行参数"""
        args = ["semgrep"]

        # 添加规则配置
        if config:
            args += ["--config", config]
        if rules:
            for r in rules:
                args += ["--config", r]
        if not config and not rules:
            args += ["--config", "auto"]  # 默认使用自动配置

        # JSON 输出
        if json_output:
            args.append("--json")

        # 应用全局配置
        if getattr(self._config, "timeout", None) and "timeout" not in kwargs:
            kwargs["timeout"] = self._config.timeout
        if getattr(self._config, "jobs", None) and "jobs" not in kwargs:
            kwargs["jobs"] = self._config.jobs
        if getattr(self._config, "max_memory", 0) > 0:
            args += ["--max-memory", str(self._config.max_memory)]

        # 处理其他参数
        for k, v in kwargs.items():
            flag = f"--{k.replace('_', '-')}"
            if isinstance(v, bool):
                if v:
                    args.append(flag)
            elif isinstance(v, list):
                for item in v:
                    args += [flag, str(item)]
            else:
                args += [flag, str(v)]

        args.append(path)

        # Debug 输出
        if getattr(self._config, "debug", False):
            print(f"[SemgrepClient] Running: {' '.join(args)}")

        return args

    def _parse_result(self, stdout: str, stderr: str, returncode: int) -> SemgrepResult:
        """解析 semgrep 输出结果"""
        errors: List[str] = []
        success = returncode in (0, 1)  # 0=无问题, 1=有发现, 都是成功

        # 解析 JSON 输出
        output: Any = None
        if stdout.startswith("{"):
            try:
                parsed = json.loads(stdout)
                # 提取错误信息
                if "errors" in parsed:
                    errors.extend(
                        e.get("message", str(e)) for e in parsed.get("errors", [])
                    )
                output = parsed
            except json.JSONDecodeError as e:
                output = stdout
                errors.append(f"JSON 解析失败: {e}")
        else:
            output = stdout or None

        # 记录非成功的退出码
        if returncode >= 2:
            errors.append(f"Semgrep exited with code {returncode}")

        return SemgrepResult(
            success=success,
            output=output,
            stderr=stderr or None,
            returncode=returncode,
            errors=errors,
        )
