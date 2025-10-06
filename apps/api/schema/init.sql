-- 如果数据库已存在则删除
DROP DATABASE IF EXISTS `ai_code_review`;

-- 创建数据库
CREATE DATABASE `ai_code_review`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

-- 切换到该数据库
USE `ai_code_review`;

-- 如果表已存在则删除
DROP TABLE IF EXISTS `cs_pr_repository`;

-- 创建表
CREATE TABLE `cs_pr_repository` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',

    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `created_by` VARCHAR(255) NULL COMMENT '创建人',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `updated_by` VARCHAR(255) NULL COMMENT '更新人',

    `repo_id` VARCHAR(255) NOT NULL COMMENT '仓库 ID',
    `full_name` VARCHAR(255) NOT NULL COMMENT '仓库全名：owner/repo',
    `name` VARCHAR(255) NOT NULL COMMENT '名称：XX仓库',
    `default_branch` VARCHAR(100) NOT NULL DEFAULT 'master' COMMENT '默认分支：master',

    `enable_status` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '启用状态',
    `delete_flag` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '删除状态',

    INDEX `idx_cs_pr_repository_id` (`id`),
    INDEX `idx_cs_pr_repository_repo_id` (`repo_id`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci
  COMMENT='仓库表';

-- 删除旧表
DROP TABLE IF EXISTS `cs_pr_pull_request`;

-- 创建 PullRequest 表
CREATE TABLE `cs_pr_pull_request` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',

    -- 审计字段
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `created_by` VARCHAR(255) NULL COMMENT '创建人',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `updated_by` VARCHAR(255) NULL COMMENT '更新人',

    -- Git 信息
    `repository_id` VARCHAR(255) NOT NULL COMMENT '仓库 ID',
    `pr_id` VARCHAR(255) NOT NULL COMMENT 'Pull Request ID',
    `pr_number` INT NOT NULL COMMENT 'PR 编号',

    -- PR 基础信息
    `title` TEXT NOT NULL COMMENT 'PR 标题',
    `description` TEXT NULL COMMENT 'PR 描述',
    `source_branch` VARCHAR(255) NOT NULL COMMENT '源分支',
    `target_branch` VARCHAR(255) NOT NULL COMMENT '目标分支',
    `author` VARCHAR(255) NOT NULL COMMENT '作者',
    `author_email` VARCHAR(255) NULL COMMENT '作者邮箱',

    -- PR 状态
    `status` VARCHAR(50) NOT NULL DEFAULT 'open' COMMENT 'PR 状态：open、merged、closed、draft',
    `is_draft` BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否为草稿',

    -- 代码统计
    `files_changed` INT NOT NULL DEFAULT 0 COMMENT '文件改动数量',
    `lines_added` INT NOT NULL DEFAULT 0 COMMENT '新增行数',
    `lines_deleted` INT NOT NULL DEFAULT 0 COMMENT '删除行数',
    `commits_count` INT NOT NULL DEFAULT 0 COMMENT '提交数量',

    -- 审查信息
    `review_status` VARCHAR(50) NOT NULL DEFAULT 'pending' COMMENT '审查状态：pending、in_progress、completed、failed',
    `last_review_at` DATETIME NULL COMMENT '上次审查时间',
    `review_triggered_by` VARCHAR(50) NULL COMMENT '审查触发方式：webhook、manual、scheduled',

    -- 索引
    INDEX `idx_cs_pr_pull_request_id` (`id`),
    INDEX `idx_cs_pr_pull_request_repo` (`repository_id`),
    INDEX `idx_cs_pr_pull_request_pr_id` (`pr_id`),
    INDEX `idx_cs_pr_pull_request_pr_number` (`pr_number`),
    INDEX `idx_cs_pr_pull_request_status` (`status`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci
  COMMENT='Pull Request 表';

-- 删除旧表
DROP TABLE IF EXISTS `cs_pr_pull_request_review`;

-- 创建表
CREATE TABLE `cs_pr_pull_request_review` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',

    -- 审计字段
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `created_by` VARCHAR(255) NULL COMMENT '创建人',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `updated_by` VARCHAR(255) NULL COMMENT '更新人',

    -- 关联信息
    `pull_request_id` INT NOT NULL COMMENT '关联的 Pull Request ID',
    `review_number` INT NOT NULL DEFAULT 0 COMMENT '评审轮次编号（第几次评审）',
    `git_commit_sha` VARCHAR(64) NOT NULL COMMENT '关联的提交哈希（Commit SHA）',

    -- 评分信息
    `total_score` INT NULL DEFAULT 0 COMMENT '总分',
    `secure_score` INT NULL DEFAULT 0 COMMENT '安全评分',
    `design_score` INT NULL DEFAULT 0 COMMENT '架构评分',
    `quality_score` INT NULL DEFAULT 0 COMMENT '质量评分',
    `practice_score` INT NULL DEFAULT 0 COMMENT '实践评分',
    `performance_score` INT NULL DEFAULT 0 COMMENT '性能评分',

    -- 状态信息
    `status` VARCHAR(50) NOT NULL DEFAULT 'running' COMMENT '处理状态：running、completed、failed、canceled',
    `error_message` TEXT NULL COMMENT '错误信息',

    -- 索引
    INDEX `idx_cs_pr_review_id` (`id`),
    INDEX `idx_cs_pr_review_pull_request` (`pull_request_id`),
    INDEX `idx_cs_pr_review_status` (`status`),
    INDEX `idx_cs_pr_review_commit_sha` (`git_commit_sha`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci
  COMMENT='Pull Request Review 表（评审记录）';

-- 删除旧表
DROP TABLE IF EXISTS `cs_pr_issue`;

-- 创建 Issue 表
CREATE TABLE `cs_pr_issue` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',

    -- 审计字段
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `created_by` VARCHAR(255) NULL COMMENT '创建人',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `updated_by` VARCHAR(255) NULL COMMENT '更新人',

    -- 关联信息
    `pull_request_review_id` INT NOT NULL COMMENT '关联的 Pull Request Review ID',

    -- 来源与规则
    `source` VARCHAR(50) NOT NULL COMMENT '问题来源：semgrep、llm、eslint、sonarqube 等',
    `rule_id` VARCHAR(255) NULL COMMENT '静态检查规则 ID',
    `type` VARCHAR(50) NULL COMMENT '问题类型：security、design、quality、practice、performance、bug',
    `severity` VARCHAR(20) NULL COMMENT '严重程度：critical、high、medium、low',
    `category` VARCHAR(100) NULL COMMENT '分类：如 sql_injection、null_pointer',

    -- 问题描述信息
    `title` TEXT NOT NULL COMMENT '问题标题',
    `description` TEXT NULL COMMENT '详细描述',
    `impact` TEXT NULL COMMENT '影响说明',
    `suggestion` TEXT NULL COMMENT '修复建议',

    -- 状态信息
    `status` VARCHAR(50) NOT NULL DEFAULT 'active' COMMENT '状态：active、fixed、exempted、ignored',

    -- 索引
    INDEX `idx_cs_pr_issue_id` (`id`),
    INDEX `idx_cs_pr_issue_review` (`pull_request_review_id`),
    INDEX `idx_cs_pr_issue_source` (`source`),
    INDEX `idx_cs_pr_issue_status` (`status`),
    INDEX `idx_cs_pr_issue_type` (`type`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci
  COMMENT='Issue 表（代码问题记录）';
