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
