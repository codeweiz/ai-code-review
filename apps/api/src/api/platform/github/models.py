from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    """GitHub 用户模型"""

    id: int = Field(..., description="用户唯一ID")

    login: str = Field(..., description="用户登录名（GitHub 用户名）")

    node_id: str = Field(..., description="节点 ID（GitHub 内部使用）")

    avatar_url: str = Field(..., description="用户头像 URL")

    gravatar_id: str = Field(..., description="Gravatar ID，如果没有则为空")

    url: str = Field(..., description="用户 API 地址")

    html_url: str = Field(..., description="用户 GitHub 主页地址")

    followers_url: str = Field(..., description="获取粉丝的 API 地址")

    following_url: str = Field(..., description="获取关注的 API 地址")

    gists_url: str = Field(..., description="获取 Gist 的 API 地址")

    starred_url: str = Field(..., description="获取 Star 的 API 地址")

    subscriptions_url: str = Field(..., description="获取订阅的 API 地址")

    organizations_url: str = Field(..., description="获取组织的 API 地址")

    repos_url: str = Field(..., description="获取仓库的 API 地址")

    events_url: str = Field(..., description="获取事件的 API 地址")

    received_events_url: str = Field(..., description="接收事件的 API 地址")

    type: str = Field(..., description="用户类型（如 User、Bot 等）")

    user_view_type: str = Field(..., description="用户可见类型")

    site_admin: bool = Field(..., description="是否为 GitHub 管理员")


class Repo(BaseModel):
    """GitHub 仓库模型"""

    id: int = Field(..., description="仓库唯一 ID")

    node_id: str = Field(..., description="节点 ID")

    name: str = Field(..., description="仓库名")

    full_name: str = Field(..., description="仓库全名（包含用户名/组织名）")

    private: bool = Field(..., description="是否为私有仓库")

    owner: User = Field(..., description="仓库所有者信息")

    html_url: str = Field(..., description="仓库主页地址")

    description: Optional[str] = Field(None, description="仓库描述")

    fork: bool = Field(..., description="是否为 fork 仓库")

    url: str = Field(..., description="仓库 API 地址")

    created_at: str = Field(..., description="仓库创建时间")

    updated_at: str = Field(..., description="仓库更新时间")

    pushed_at: str = Field(..., description="最近推送时间")

    git_url: str = Field(..., description="Git 协议克隆地址")

    ssh_url: str = Field(..., description="SSH 协议克隆地址")

    clone_url: str = Field(..., description="HTTPS 克隆地址")

    svn_url: str = Field(..., description="SVN 地址")

    homepage: Optional[str] = Field(None, description="仓库主页/网站")

    size: int = Field(..., description="仓库大小（KB）")

    stargazers_count: int = Field(..., description="Star 数量")

    watchers_count: int = Field(..., description="Watch 数量")

    language: Optional[str] = Field(None, description="主要编程语言")

    has_issues: bool = Field(..., description="是否启用 Issues")

    has_projects: bool = Field(..., description="是否启用 Projects")

    has_downloads: bool = Field(..., description="是否启用下载")

    has_wiki: bool = Field(..., description="是否启用 Wiki")

    has_pages: bool = Field(..., description="是否启用 GitHub Pages")

    forks_count: int = Field(..., description="Fork 数量")

    archived: bool = Field(..., description="是否已归档")

    disabled: bool = Field(..., description="是否禁用")

    open_issues_count: int = Field(..., description="打开的 Issue 数量")

    visibility: str = Field(..., description="仓库可见性（public/private）")

    default_branch: str = Field(..., description="默认分支")


class BranchRef(BaseModel):
    """GitHub 分支模型"""

    label: str = Field(..., description="分支标签（例如 'user:branch'）")

    ref: str = Field(..., description="分支名")

    sha: str = Field(..., description="分支对应的 commit SHA")

    user: User = Field(..., description="分支所属的用户")

    repo: Repo = Field(..., description="分支所属的仓库")


class CommitUserInfo(BaseModel):
    """GitHub 提交者/作者信息模型"""

    name: str = Field(..., description="提交者/作者姓名")
    email: str = Field(..., description="提交者/作者邮箱")
    date: str = Field(..., description="提交时间/作者时间")


class CommitTree(BaseModel):
    """GitHub 提交记录树模型"""

    url: str = Field(..., description="对应树对象的 API 地址")

    sha: str = Field(..., description="树对象的 SHA 值")


class CommitVerification(BaseModel):
    """GitHub 提交验证模型"""

    verified: bool = Field(..., description="是否已验证签名")

    reason: str = Field(..., description="未验证原因或验证说明")

    signature: Optional[str] = Field(None, description="签名内容，如果有的话")

    payload: Optional[str] = Field(None, description="签名原始数据，如果有的话")

    verified_at: Optional[str] = Field(None, description="验证的时间戳")


class CommitDetail(BaseModel):
    """GitHub 提交详情模型"""

    url: str = Field(..., description="Commit 的 API 地址")

    author: CommitUserInfo = Field(..., description="作者信息（来自提交内容）")

    committer: CommitUserInfo = Field(..., description="提交者信息（来自提交内容）")

    message: str = Field(..., description="提交信息")

    tree: CommitTree = Field(..., description="commit 对应的树对象")

    comment_count: int = Field(..., description="评论数量")

    verification: CommitVerification = Field(..., description="验证信息")


class CommitItem(BaseModel):
    """GitHub 提交记录模型"""

    url: str = Field(..., description="commit 的 API 地址")

    sha: str = Field(..., description="commit 的 SHA 值")

    node_id: str = Field(..., description="commit 的节点 ID")

    html_url: str = Field(..., description="commit 的网页链接")

    comments_url: str = Field(..., description="commit 的评论 API 链接")

    commit: CommitDetail = Field(..., description="commit 的详细信息块")

    author: Optional[User] = Field(None, description="作者用户信息（关联 GitHub 账户）")

    committer: Optional[User] = Field(
        None, description="提交用户信息（关联 GitHub 账户）"
    )

    parents: List[CommitTree] = Field(..., description="父提交列表")


class FileLinks(BaseModel):
    """GitHub 文件链接模型"""

    git: str = Field(..., description="指向 Git Blob API 的链接")

    self: str = Field(..., description="指向当前文件内容 API 的链接")

    html: str = Field(..., description="指向 GitHub 网页的链接")


class FileContent(BaseModel):
    """GitHub 文件内容模型"""

    type: str = Field(..., description="条目的类型，例如 'file' 或 'dir'")

    encoding: Optional[str] = Field(
        None, description="文件内容的编码方式（通常为 base64）"
    )

    size: int = Field(..., description="文件大小，单位为字节")

    name: str = Field(..., description="文件名")

    path: str = Field(..., description="文件在仓库中的路径")

    content: Optional[str] = Field(None, description="文件内容（Base64 编码）")

    sha: str = Field(..., description="文件 SHA 值")

    url: str = Field(..., description="当前文件内容的 GitHub API URL")

    git_url: str = Field(..., description="Git Blob API 的 URL")

    html_url: str = Field(..., description="GitHub 页面 URL")

    download_url: Optional[str] = Field(None, description="文件下载的原始地址 URL")

    links: FileLinks = Field(..., alias="_links", description="相关链接集合")


class Links(BaseModel):
    """GitHub 链接模型"""

    self: Dict[str, str] = Field(..., description="PR 自身的 API 链接")

    html: Dict[str, str] = Field(..., description="PR 网页链接")

    issue: Dict[str, str] = Field(..., description="相关 Issue 链接")

    comments: Dict[str, str] = Field(..., description="评论链接")

    review_comments: Dict[str, str] = Field(..., description="代码 Review 评论链接")

    review_comment: Dict[str, str] = Field(..., description="单个 Review 评论链接")

    commits: Dict[str, str] = Field(..., description="提交记录链接")

    statuses: Dict[str, str] = Field(..., description="PR 状态检查链接")


class PullRequest(BaseModel):
    """GitHub Pull Request 模型"""

    id: int = Field(..., description="PR 唯一 ID")

    url: str = Field(..., description="PR 的 API 地址")

    node_id: str = Field(..., description="PR 节点 ID")

    html_url: str = Field(..., description="PR 网页链接")

    diff_url: str = Field(..., description="PR diff 文件链接")

    patch_url: str = Field(..., description="PR patch 文件链接")

    issue_url: str = Field(..., description="关联 Issue 的 API 地址")

    number: int = Field(..., description="PR 编号")

    state: str = Field(..., description="PR 状态（open/closed）")

    locked: bool = Field(..., description="是否被锁定")

    title: str = Field(..., description="PR 标题")

    user: User = Field(..., description="提交 PR 的用户")

    body: str = Field(..., description="PR 内容正文")

    created_at: str = Field(..., description="创建时间")

    updated_at: str = Field(..., description="最后更新时间")

    closed_at: Optional[str] = Field(None, description="关闭时间")

    merged_at: Optional[str] = Field(None, description="合并时间（如已合并）")

    merge_commit_sha: Optional[str] = Field(None, description="合并时的 commit SHA")

    draft: bool = Field(..., description="是否是草稿 PR")

    commits_url: str = Field(..., description="commits 列表 API 地址")

    review_comments_url: str = Field(..., description="review 评论 API 地址")

    comments_url: str = Field(..., description="普通评论 API 地址")

    statuses_url: str = Field(..., description="状态 API 地址")

    head: BranchRef = Field(..., description="PR 的 head 分支信息")

    base: BranchRef = Field(..., description="PR 的 base 分支信息")

    links: Links = Field(..., alias="_links", description="相关链接集合")

    comments: int = Field(..., description="评论数量")

    review_comments: int = Field(..., description="评审评论数量")

    commits: int = Field(..., description="提交数量")

    additions: int = Field(..., description="新增行数")

    deletions: int = Field(..., description="删除行数")

    changed_files: int = Field(..., description="修改的文件数")


class PullRequestFile(BaseModel):
    """GitHub Pull Request 文件模型"""

    sha: str = Field(..., description="文件的 Git blob SHA 值")

    filename: str = Field(..., description="文件路径")

    status: str = Field(..., description="文件状态（added/modified/removed 等）")

    additions: int = Field(..., description="增加的行数")

    deletions: int = Field(..., description="删除的行数")

    changes: int = Field(..., description="总共修改的行数（additions + deletions）")

    blob_url: str = Field(..., description="文件在 GitHub Web 界面的 blob URL")

    raw_url: str = Field(..., description="文件原始内容的 URL")

    contents_url: str = Field(..., description="文件内容的 API URL")

    patch: Optional[str] = Field(None, description="diff patch 片段（可能为空）")


class WebhookConfig(BaseModel):
    """GitHub webhook 配置模型"""

    content_type: Optional[str] = Field(
        None, description="Webhook 请求的内容类型 (如 json, form)"
    )

    insecure_ssl: Optional[str] = Field(
        None, description="是否允许不安全的 SSL：'0'=false, '1'=true"
    )

    url: Optional[str] = Field(None, description="Webhook 的回调 URL")


class WebhookLastResponse(BaseModel):
    """GitHub webhook 最近一次响应模型"""

    code: Optional[int] = Field(None, description="最近一次请求的 HTTP 状态码")

    status: str = Field(..., description="最近一次请求的状态，例如 'unused'")

    message: Optional[str] = Field(None, description="错误信息或提示内容")


class Webhook(BaseModel):
    """GitHub webhook 模型"""

    id: int = Field(..., description="Webhook 唯一 ID")

    type: str = Field(..., description="Webhook 类型（例如 Repository）")

    name: str = Field(..., description="Webhook 名称")

    active: bool = Field(..., description="是否处于激活状态")

    events: List[str] = Field(
        ..., description="监听的事件列表（如 push, pull_request 等）"
    )

    config: WebhookConfig = Field(..., description="Webhook 配置信息")

    updated_at: str = Field(..., description="Webhook 最后更新时间")

    created_at: str = Field(..., description="Webhook 创建时间")

    url: str = Field(..., description="该 Webhook 的 API 地址")

    test_url: str = Field(..., description="Webhook 测试触发的 API 地址")

    ping_url: str = Field(..., description="Webhook ping 测试 API 地址")

    deliveries_url: str = Field(..., description="Webhook 投递记录 API 地址")

    last_response: WebhookLastResponse = Field(
        ..., description="最近一次请求的响应信息"
    )
