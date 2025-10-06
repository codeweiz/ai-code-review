from typing import Any, List, Optional

from pydantic import BaseModel, Field


class LinkItem(BaseModel):
    """Gitee 链接项模型"""

    href: str = Field(..., description="链接地址")


class Links(BaseModel):
    """Gitee 链接模型"""

    comments: LinkItem = Field(..., description="评论链接")

    commits: LinkItem = Field(..., description="提交记录链接")

    html: LinkItem = Field(..., description="网页 PR 链接")

    issue: LinkItem = Field(..., description="关联 Issue 链接")

    review_comment: LinkItem = Field(..., description="单条 Review 评论链接")

    review_comments: LinkItem = Field(..., description="Review 评论列表链接")

    self: LinkItem = Field(..., description="当前 PR API 链接")


class User(BaseModel):
    """Gitee 用户模型"""

    id: int = Field(..., description="用户 ID")

    login: str = Field(..., description="用户登录名")

    name: Optional[str] = Field(None, description="用户名称/昵称")

    type: str = Field(..., description="用户类型（User/Org/Enterprise）")

    avatar_url: str = Field(..., description="用户头像 URL")

    html_url: str = Field(..., description="用户主页地址")

    url: str = Field(..., description="用户 API 链接")

    remark: Optional[str] = Field(None, description="用户备注")

    events_url: Optional[str] = Field(None, description="用户事件 API 地址")

    followers_url: Optional[str] = Field(None, description="用户粉丝 API 地址")

    following_url: Optional[str] = Field(None, description="用户关注 API 地址")

    gists_url: Optional[str] = Field(None, description="用户 Gist API 地址")

    organizations_url: Optional[str] = Field(None, description="用户组织 API 地址")

    received_events_url: Optional[str] = Field(
        None, description="用户接收的事件 API 地址"
    )

    repos_url: Optional[str] = Field(None, description="用户仓库 API 地址")

    starred_url: Optional[str] = Field(None, description="用户 Star 仓库 API 地址")

    subscriptions_url: Optional[str] = Field(None, description="用户订阅 API 地址")


class Namespace(BaseModel):
    """Gitee 命名空间模型"""

    id: int = Field(..., description="命名空间 ID")

    path: str = Field(..., description="命名空间路径")

    name: str = Field(..., description="命名空间名称")

    type: str = Field(..., description="命名空间类型（personal/enterprise）")

    html_url: str = Field(..., description="命名空间网页地址")


class Repo(BaseModel):
    """Gitee 仓库模型"""

    id: int = Field(..., description="仓库 ID")

    name: str = Field(..., description="仓库名")

    full_name: str = Field(..., description="完整仓库名（namespace/repo）")

    human_name: str = Field(..., description="人类可读的仓库名")

    description: Optional[str] = Field(None, description="仓库描述")

    fork: bool = Field(..., description="是否为 fork 仓库")

    internal: bool = Field(..., description="是否为内部仓库")

    private: bool = Field(..., description="是否为私有仓库")

    public: bool = Field(..., description="是否为公开仓库")

    path: str = Field(..., description="仓库路径")

    html_url: str = Field(..., description="仓库网页地址")

    ssh_url: str = Field(..., description="SSH 克隆地址")

    url: str = Field(..., description="仓库 API 地址")

    owner: User = Field(..., description="仓库拥有者")

    namespace: Namespace = Field(..., description="命名空间信息")

    assigner: Optional[User] = Field(None, description="仓库分配人")


class BranchRef(BaseModel):
    """Gitee 分支模型"""

    label: str = Field(..., description="分支标签（如 main）")

    ref: str = Field(..., description="分支名")

    sha: str = Field(..., description="分支提交 SHA 值")

    repo: Repo = Field(..., description="分支所属仓库信息")

    user: User = Field(..., description="创建者信息")


class Assignee(User):
    """Gitee 指派模型"""

    accept: bool = Field(..., description="是否接受任务")

    assignee: bool = Field(..., description="是否为指派人")

    code_owner: bool = Field(..., description="是否为代码所有者")


class PullRequest(BaseModel):
    """Gitee Pull Request 模型"""

    id: int = Field(..., description="PR 唯一标识 ID")

    number: int = Field(..., description="PR 编号")

    title: str = Field(..., description="PR 标题")

    body: Optional[str] = Field(None, description="PR 内容/描述")

    state: str = Field(..., description="PR 状态（open/closed/merged）")

    html_url: str = Field(..., description="PR 页面 URL")

    url: str = Field(..., description="PR API 地址")

    issue_url: Optional[str] = Field(None, description="关联 Issue API 地址")

    diff_url: Optional[str] = Field(None, description="Diff 文件下载地址")

    patch_url: Optional[str] = Field(None, description="Patch 文件下载地址")

    comments_url: str = Field(..., description="评论链接")

    commits_url: str = Field(..., description="提交记录 API 地址")

    review_comment_url: str = Field(..., description="单条评论 API 地址")

    review_comments_url: str = Field(..., description="评论列表 API 地址")

    created_at: str = Field(..., description="PR 创建时间")

    updated_at: str = Field(..., description="PR 更新时间")

    closed_at: Optional[str] = Field(None, description="PR 关闭时间")

    merged_at: Optional[str] = Field(None, description="PR 合并时间")

    user: User = Field(..., description="提交 PR 的用户信息")

    base: BranchRef = Field(..., description="目标分支（base branch）")

    head: BranchRef = Field(..., description="源分支（head branch）")

    assignees: List[Assignee] = Field(
        default_factory=list, description="指派处理人列表"
    )

    assignees_number: int = Field(..., description="指派人数")

    testers: List[Assignee] = Field(default_factory=list, description="测试人员列表")

    testers_number: int = Field(..., description="测试人数")

    can_merge_check: bool = Field(..., description="是否可通过合并检查")

    mergeable: bool = Field(..., description="是否可直接合并")

    draft: bool = Field(..., description="是否为草稿 PR")

    locked: bool = Field(..., description="是否锁定")

    prune_branch: bool = Field(..., description="合并后是否删除分支")

    labels: List[Any] = Field(default_factory=list, description="标签列表")

    milestone: Optional[Any] = Field(None, description="里程碑信息")

    ref_pull_requests: List[Any] = Field(
        default_factory=list, description="关联的其他 PR 列表"
    )

    close_related_issue: Optional[int] = Field(
        None, description="是否自动关闭关联的 issue"
    )

    links: Links = Field(..., alias="_links", description="PR 链接资源集合")


class FilePatch(BaseModel):
    """Gitee 文件补丁信息模型"""

    diff: Optional[str] = Field(None, description="diff 差异内容")

    new_path: Optional[str] = Field(None, description="新文件路径")

    old_path: Optional[str] = Field(None, description="旧文件路径")

    a_mode: Optional[str] = Field(None, description="旧文件权限模式")

    b_mode: Optional[str] = Field(None, description="新文件权限模式")

    new_file: bool = Field(..., description="是否为新文件")

    renamed_file: bool = Field(..., description="是否为重命名文件")

    deleted_file: bool = Field(..., description="是否为删除文件")

    too_large: bool = Field(..., description="补丁是否过大无法显示")


class PullRequestFile(BaseModel):
    """Gitee PR 文件变更项模型"""

    sha: str = Field(..., description="文件对应的 commit sha 值")

    filename: str = Field(..., description="文件全路径名")

    status: Optional[str] = Field(
        None, description="文件状态 (added/modified/deleted 等)"
    )

    additions: str = Field(..., description="新增行数")

    deletions: str = Field(..., description="删除行数")

    blob_url: str = Field(..., description="文件在代码托管平台中的浏览地址")

    raw_url: str = Field(..., description="文件原始内容下载地址")

    patch: Optional[FilePatch] = Field(None, description="文件 diff 补丁信息")


class CommitUserInfo(BaseModel):
    """Gitee 提交人或提交者在 commit 对象里的信息模型"""

    name: str = Field(..., description="用户名称")

    email: str = Field(..., description="用户邮箱")

    date: str = Field(..., description="提交时间")


class CommitDetail(BaseModel):
    """Gitee Commit 内部提交详情模型"""

    url: str = Field(..., description="commit API 地址")

    author: CommitUserInfo = Field(..., description="提交作者信息")

    committer: CommitUserInfo = Field(..., description="提交者信息")

    message: str = Field(..., description="提交信息")

    comment_count: int = Field(..., description="评论数")


class CommitAuthor(BaseModel):
    """Gitee 提交关联的用户模型"""

    id: int = Field(..., description="用户 ID")

    login: str = Field(..., description="用户登录名")

    name: Optional[str] = Field(None, description="用户姓名")

    avatar_url: str = Field(..., description="用户头像 URL")

    url: str = Field(..., description="用户 API 地址")

    html_url: str = Field(..., description="用户主页地址")

    type: str = Field(..., description="用户类型")

    remark: Optional[str] = Field(None, description="备注")

    followers_url: Optional[str] = Field(None, description="粉丝 API 地址")

    following_url: Optional[str] = Field(None, description="关注 API 地址")

    gists_url: Optional[str] = Field(None, description="Gist API 地址")

    starred_url: Optional[str] = Field(None, description="Star API 地址")

    subscriptions_url: Optional[str] = Field(None, description="订阅 API 地址")

    organizations_url: Optional[str] = Field(None, description="组织 API 地址")

    repos_url: Optional[str] = Field(None, description="仓库 API 地址")

    events_url: Optional[str] = Field(None, description="事件 API 地址")

    received_events_url: Optional[str] = Field(None, description="接收事件 API 地址")


class ParentCommit(BaseModel):
    """Gitee 父提交信息模型"""

    url: str = Field(..., description="父提交 API 地址")

    sha: str = Field(..., description="父提交 SHA")

    shas: List[str] = Field(..., description="父提交 SHA 列表")


class CommitItem(BaseModel):
    """Gitee PR Commit 模型"""

    url: str = Field(..., description="commit API 地址")

    sha: str = Field(..., description="commit SHA 值")

    html_url: str = Field(..., description="commit 网页地址")

    comments_url: str = Field(..., description="评论 API 地址")

    commit: CommitDetail = Field(..., description="提交详情")

    author: Optional[CommitAuthor] = Field(None, description="提交作者用户信息")

    committer: Optional[CommitAuthor] = Field(None, description="提交者用户信息")

    parents: ParentCommit = Field(..., description="父提交信息")


class FileLinks(BaseModel):
    """Gitee 文件关联链接模型"""

    self: str = Field(..., description="文件 API 地址")

    html: str = Field(..., description="文件网页 URL")


class FileContent(BaseModel):
    """Gitee 文件内容模型"""

    type: str = Field(..., description="对象类型（file/dir/submodule/symlink）")

    encoding: Optional[str] = Field(None, description="内容编码方式（如 base64）")

    size: int = Field(..., description="文件大小（字节数）")

    name: str = Field(..., description="文件名")

    path: str = Field(..., description="文件路径")

    content: Optional[str] = Field(
        None, description="文件内容（通常为 base64 编码，需要解码）"
    )

    sha: str = Field(..., description="文件对应的 SHA 值")

    url: str = Field(..., description="文件 API 地址")

    html_url: str = Field(..., description="文件 web 地址")

    download_url: Optional[str] = Field(None, description="文件原始下载地址")

    links: FileLinks = Field(..., alias="_links", description="关联链接集合")


class Webhook(BaseModel):
    """Gitee Webhook 配置信息模型"""

    id: int = Field(..., description="Webhook 唯一标识 ID")

    url: str = Field(..., description="Webhook 回调地址")

    password: Optional[str] = Field(None, description="Webhook 密码/secret")

    result: Optional[str] = Field(None, description="上次请求返回的结果内容")

    result_code: Optional[int] = Field(None, description="上次请求返回的 HTTP 状态码")

    project_id: int = Field(..., description="Webhook 绑定的项目 ID")

    created_at: str = Field(..., description="Webhook 创建时间")

    push_events: bool = Field(..., description="是否触发 push 事件")

    tag_push_events: bool = Field(..., description="是否触发 tag push 事件")

    issues_events: bool = Field(..., description="是否触发 issue 事件")

    note_events: bool = Field(..., description="是否触发 note 评论 事件")

    merge_requests_events: bool = Field(..., description="是否触发 merge request 事件")
