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
