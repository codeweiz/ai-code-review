from typing import List, Optional

from pydantic import BaseModel, Field


class Permissions(BaseModel):
    """Gitea 权限模型"""

    admin: bool = Field(..., description="是否具有管理权限")

    push: bool = Field(..., description="是否可以推送代码")

    pull: bool = Field(..., description="是否可以拉取代码")


class InternalTracker(BaseModel):
    """Gitea 工时跟踪模型"""

    enable_time_tracker: bool = Field(..., description="是否启用工时跟踪")

    allow_only_contributors_to_track_time: bool = Field(
        ..., description="是否只允许贡献者记录工时"
    )

    enable_issue_dependencies: bool = Field(..., description="是否启用任务依赖关系")


class User(BaseModel):
    """Gitea 用户模型"""

    id: int = Field(..., description="用户ID")

    login: str = Field(..., description="登录名")

    login_name: str = Field(..., description="登录名（完整）")

    source_id: int = Field(..., description="来源ID")

    full_name: str = Field(..., description="用户全名")

    email: str = Field(..., description="邮箱")

    avatar_url: str = Field(..., description="头像URL")

    html_url: str = Field(..., description="用户主页URL")

    language: str = Field(..., description="语言偏好")

    is_admin: bool = Field(..., description="是否管理员")

    last_login: str = Field(..., description="最后登录时间")

    created: str = Field(..., description="账户创建时间")

    restricted: bool = Field(..., description="是否受限")

    active: bool = Field(..., description="是否激活")

    prohibit_login: bool = Field(..., description="是否禁止登录")

    location: str = Field(..., description="所在地")

    website: str = Field(..., description="个人网站")

    description: str = Field(..., description="用户描述")

    visibility: str = Field(..., description="可见性")

    followers_count: int = Field(..., description="粉丝数量")

    following_count: int = Field(..., description="关注数量")

    starred_repos_count: int = Field(..., description="收藏的仓库数量")

    username: str = Field(..., description="用户名")


class RepoOwner(User):
    """Gitea 仓库拥有者，继承用户模型"""

    pass


class Repository(BaseModel):
    """Gitea 仓库模型"""

    id: int = Field(..., description="仓库ID")

    owner: RepoOwner = Field(..., description="仓库拥有者信息")

    name: str = Field(..., description="仓库名称")

    full_name: str = Field(..., description="仓库全名（含组织）")

    description: str = Field(..., description="仓库描述")

    empty: bool = Field(..., description="是否为空仓库")

    private: bool = Field(..., description="是否私有仓库")

    fork: bool = Field(..., description="是否为 fork")

    template: bool = Field(..., description="是否为模板仓库")

    mirror: bool = Field(..., description="是否为镜像仓库")

    size: int = Field(..., description="仓库大小")

    html_url: str = Field(..., description="仓库主页URL")

    url: str = Field(..., description="仓库 API 地址")

    ssh_url: str = Field(..., description="仓库 SSH 地址")

    clone_url: str = Field(..., description="仓库 HTTP 克隆地址")

    original_url: str = Field(..., description="仓库原始URL")

    website: str = Field(..., description="仓库网站")

    stars_count: int = Field(..., description="Star 数量")

    forks_count: int = Field(..., description="Fork 数量")

    watchers_count: int = Field(..., description="Watcher 数量")

    open_issues_count: int = Field(..., description="开启的 Issue 数量")

    open_pr_counter: int = Field(..., description="开启的 PR 数量")

    release_counter: int = Field(..., description="发布数量")

    default_branch: str = Field(..., description="默认分支")

    archived: bool = Field(..., description="是否已归档")

    created_at: str = Field(..., description="仓库创建时间")

    updated_at: str = Field(..., description="仓库更新时间")

    permissions: Permissions = Field(..., description="权限信息")

    has_issues: bool = Field(..., description="是否启用 Issue")

    internal_tracker: InternalTracker = Field(..., description="内部跟踪器配置")


class Branch(BaseModel):
    """Gitea 分支模型"""

    label: str = Field(..., description="分支标签")

    ref: str = Field(..., description="分支引用")

    sha: str = Field(..., description="提交哈希")

    repo_id: int = Field(..., description="仓库ID")

    repo: Repository = Field(..., description="分支所属仓库")


class PullRequest(BaseModel):
    """Gitea Pull Request 模型"""

    id: int = Field(..., description="PR ID")

    url: str = Field(..., description="PR API 地址")

    number: int = Field(..., description="PR 编号")

    user: User = Field(..., description="创建PR的用户")

    title: str = Field(..., description="PR 标题")

    body: str = Field(..., description="PR 描述内容")

    state: str = Field(..., description="PR 状态")

    draft: bool = Field(..., description="是否为草稿")

    comments: int = Field(..., description="评论数")

    review_comments: int = Field(..., description="代码评审评论数")

    additions: int = Field(..., description="新增行数")

    deletions: int = Field(..., description="删除行数")

    changed_files: int = Field(..., description="修改文件数量")

    html_url: str = Field(..., description="PR 页面URL")

    diff_url: str = Field(..., description="Diff 文件URL")

    patch_url: str = Field(..., description="Patch 文件URL")

    mergeable: bool = Field(..., description="是否可合并")

    merged: bool = Field(..., description="是否已合并")

    merged_at: Optional[str] = Field(None, description="合并时间")

    closed_at: Optional[str] = Field(None, description="关闭时间")

    base: Branch = Field(..., description="目标分支")

    head: Branch = Field(..., description="源分支")

    merge_base: str = Field(..., description="合并基点 commit")

    created_at: str = Field(..., description="创建时间")

    updated_at: str = Field(..., description="更新时间")

    due_date: Optional[str] = Field(None, description="截止时间")


class PullRequestFile(BaseModel):
    """Gitea Pull Request 文件模型"""

    filename: str = Field(..., description="文件路径")

    status: str = Field(
        ..., description="文件变更状态（added/changed/removed/renamed 等）"
    )

    additions: int = Field(..., description="新增行数")

    deletions: int = Field(..., description="删除行数")

    changes: int = Field(..., description="总的变更行数")

    html_url: str = Field(..., description="仓库中该文件的 HTML 地址")

    contents_url: str = Field(..., description="仓库 API 获取文件内容的地址")

    raw_url: str = Field(..., description="文件原始内容的下载地址")


class CommitPerson(BaseModel):
    """Gitea 提交人模型"""

    name: str = Field(..., description="提交人或作者姓名")

    email: str = Field(..., description="提交人或作者邮箱")

    date: str = Field(..., description="提交时间")


class CommitTree(BaseModel):
    """Gitea 提交树模型"""

    url: str = Field(..., description="树对象 API 地址")

    sha: str = Field(..., description="树对象 SHA 值")

    created: str = Field(..., description="创建时间")


class CommitVerification(BaseModel):
    """Gitea 提交验证模型"""

    verified: bool = Field(..., description="提交是否经过验证")

    reason: str = Field(..., description="验证结果原因")

    signature: str = Field(..., description="签名内容")

    signer: Optional[str] = Field(None, description="签名者")

    payload: str = Field(..., description="签名载荷")


class CommitDetail(BaseModel):
    """Gitea 提交详情模型"""

    url: str = Field(..., description="Commit API 地址")

    author: CommitPerson = Field(..., description="作者信息")

    committer: CommitPerson = Field(..., description="提交者信息")

    message: str = Field(..., description="提交信息")

    tree: CommitTree = Field(..., description="代码树信息")

    verification: CommitVerification = Field(..., description="验证信息")


class CommitUser(BaseModel):
    """Gitea 提交用户模型"""

    id: int = Field(..., description="用户ID")

    login: str = Field(..., description="登录名")

    login_name: str = Field(..., description="完整登录名")

    source_id: int = Field(..., description="来源ID")

    full_name: str = Field(..., description="用户全名")

    email: str = Field(..., description="用户邮箱")

    avatar_url: str = Field(..., description="头像URL")

    html_url: str = Field(..., description="主页URL")

    language: str = Field(..., description="语言")

    is_admin: bool = Field(..., description="是否管理员")

    last_login: str = Field(..., description="最后登录时间")

    created: str = Field(..., description="创建时间")

    restricted: bool = Field(..., description="是否受限")

    active: bool = Field(..., description="是否激活")

    prohibit_login: bool = Field(..., description="是否禁止登录")

    location: str = Field(..., description="所在地")

    website: str = Field(..., description="个人网站")

    description: str = Field(..., description="描述")

    visibility: str = Field(..., description="可见性")

    followers_count: int = Field(..., description="粉丝数量")

    following_count: int = Field(..., description="关注数量")

    starred_repos_count: int = Field(..., description="收藏数")

    username: str = Field(..., description="用户名")


class CommitParent(BaseModel):
    """Gitea 父提交模型"""

    url: str = Field(..., description="父提交 API 地址")

    sha: str = Field(..., description="父提交 SHA 值")

    created: str = Field(..., description="父提交时间")


class CommitFile(BaseModel):
    """Gitea 提交文件模型"""

    filename: str = Field(..., description="文件名")

    status: str = Field(..., description="文件修改状态（added/modified/removed 等）")


class CommitStats(BaseModel):
    """Gitea 提交状态模型"""

    total: int = Field(..., description="总变更行数")

    additions: int = Field(..., description="新增行数")

    deletions: int = Field(..., description="删除行数")


class CommitItem(BaseModel):
    """Gitea 提交项模型"""

    url: str = Field(..., description="Commit API 地址")

    sha: str = Field(..., description="Commit 哈希")

    created: str = Field(..., description="Commit 创建时间")

    html_url: str = Field(..., description="Commit 页面 URL")

    commit: CommitDetail = Field(..., description="Commit 详细信息")

    author: Optional[CommitUser] = Field(None, description="作者用户信息（平台账户）")

    committer: Optional[CommitUser] = Field(
        None, description="提交者用户信息（平台账户）"
    )

    parents: List[CommitParent] = Field(..., description="父提交列表")

    files: List[CommitFile] = Field(..., description="修改的文件列表")

    stats: CommitStats = Field(..., description="统计信息")


class FileLinks(BaseModel):
    """Gitea 文件关联链接模型"""

    self: str = Field(..., description="自引用 API 地址")

    git: str = Field(..., description="Git 对象 API 地址")

    html: str = Field(..., description="文件的 HTML 页面地址")


class FileContent(BaseModel):
    """Gitea 文件内容模型"""

    name: str = Field(..., description="文件名")

    path: str = Field(..., description="文件路径")

    sha: str = Field(..., description="文件 SHA 值")

    last_commit_sha: str = Field(..., description="最后一次提交的 SHA 值")

    type: str = Field(..., description="对象类型（文件/目录/子模块等）")

    size: int = Field(..., description="文件大小（字节数）")

    encoding: Optional[str] = Field(None, description="文本内容的编码方式，例如 base64")

    content: Optional[str] = Field(None, description="文件内容（一般是 base64 编码）")

    target: Optional[str] = Field(None, description="若是子模块，指向的目标地址")

    url: str = Field(..., description="文件 API 地址")

    html_url: str = Field(..., description="文件 HTML 页面地址")

    git_url: str = Field(..., description="Git 对象 API 地址")

    download_url: str = Field(..., description="文件原始内容下载地址")

    submodule_git_url: Optional[str] = Field(
        None, description="子模块 Git 地址（如适用）"
    )

    links: FileLinks = Field(..., alias="_links", description="相关链接集合")


class WebhookConfig(BaseModel):
    """Gitea webhook 配置模型"""

    content_type: str = Field(..., description="内容类型（json/form 等）")

    url: str = Field(..., description="Webhook 回调地址")


class Webhook(BaseModel):
    """Gitea webhook 模型"""

    id: int = Field(..., description="Webhook ID")

    type: str = Field(..., description="Webhook 类型，例如 gitea/slack 等")

    branch_filter: str = Field(..., description="分支过滤规则")

    config: WebhookConfig = Field(..., description="Webhook 配置信息")

    events: List[str] = Field(..., description="触发事件列表")

    authorization_header: Optional[str] = Field(None, description="自定义认证请求头")

    active: bool = Field(..., description="是否启用 Webhook")

    updated_at: str = Field(..., description="最后更新时间")

    created_at: str = Field(..., description="创建时间")
