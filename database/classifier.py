#!/usr/bin/env python3
"""
记忆分类系统
自动对记忆进行分类、重要性评估和标签生成
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Tuple, Optional

class MemoryClassifier:
    """记忆分类器"""
    
    def __init__(self, database_path: str = "memory/database"):
        self.database_path = Path(database_path)
        self.database_path.mkdir(exist_ok=True)
        
        # 分类规则定义
        self.classification_rules = {
            "conversation": {
                "keywords": ["说", "问", "回答", "聊天", "对话", "消息"],
                "patterns": [r"^[\"'].*[\"']$", r".*[？?].*"],
                "channels": ["whatsapp", "telegram", "webchat"]
            },
            "decision": {
                "keywords": ["决定", "选择", "策略", "政策", "规则", "标准"],
                "patterns": [r".*决策.*", r".*策略.*", r".*标准.*"],
                "importance_boost": 2.0
            },
            "preference": {
                "keywords": ["喜欢", "偏好", "习惯", "风格", "方式", "模式"],
                "patterns": [r".*偏好.*", r".*喜欢.*", r".*习惯.*"]
            },
            "project": {
                "keywords": ["项目", "任务", "工作", "计划", "进展", "系统"],
                "patterns": [r".*项目.*", r".*系统.*", r".*任务.*"]
            },
            "skill": {
                "keywords": ["技能", "工具", "功能", "插件", "扩展"],
                "patterns": [r".*技能.*", r".*工具.*", r".*插件.*"]
            },
            "system": {
                "keywords": ["配置", "设置", "初始化", "升级", "维护"],
                "patterns": [r".*配置.*", r".*设置.*", r".*初始化.*"]
            }
        }
        
        # 重要性评估规则
        self.importance_rules = {
            "critical": {
                "keywords": ["安全", "密码", "密钥", "隐私", "关键", "必须", "禁止"],
                "patterns": [r".*安全.*", r".*关键.*", r".*禁止.*"],
                "min_score": 8.0
            },
            "important": {
                "keywords": ["重要", "优先", "主要", "核心", "基础"],
                "patterns": [r".*重要.*", r".*优先.*", r".*核心.*"],
                "min_score": 5.0
            },
            "normal": {
                "keywords": ["一般", "普通", "日常", "常规"],
                "min_score": 2.0
            },
            "temporary": {
                "keywords": ["临时", "测试", "调试", "示例"],
                "max_score": 2.0
            }
        }
        
        # 标签生成规则
        self.tag_rules = {
            "技术": ["代码", "编程", "开发", "技术", "算法", "系统"],
            "安全": ["安全", "防护", "加密", "权限", "验证"],
            "沟通": ["聊天", "对话", "消息", "回复", "交流"],
            "项目": ["项目", "任务", "计划", "进度", "目标"],
            "个人": ["偏好", "习惯", "风格", "个性", "兴趣"],
            "系统": ["配置", "设置", "初始化", "维护", "升级"]
        }
    
    def classify_memory(self, content: str, metadata: Dict = None) -> Dict:
        """
        对记忆进行分类
        
        Args:
            content: 记忆内容
            metadata: 元数据（时间、渠道等）
            
        Returns:
            分类结果字典
        """
        if metadata is None:
            metadata = {}
        
        # 初始化结果
        result = {
            "type": "conversation",  # 默认类型
            "importance": "normal",   # 默认重要性
            "tags": [],               # 标签列表
            "confidence": 0.0,        # 分类置信度
            "scores": {}              # 各类型得分
        }
        
        # 计算各类型得分
        type_scores = {}
        for mem_type, rules in self.classification_rules.items():
            score = 0.0
            
            # 关键词匹配
            for keyword in rules.get("keywords", []):
                if keyword in content:
                    score += 1.0
            
            # 正则匹配
            for pattern in rules.get("patterns", []):
                if re.search(pattern, content):
                    score += 2.0
            
            # 渠道匹配
            channel = metadata.get("channel", "")
            if channel in rules.get("channels", []):
                score += 1.0
            
            # 重要性提升
            score *= rules.get("importance_boost", 1.0)
            
            type_scores[mem_type] = score
        
        # 选择得分最高的类型
        if type_scores:
            result["type"] = max(type_scores, key=type_scores.get)
            max_score = max(type_scores.values())
            total_score = sum(type_scores.values())
            result["confidence"] = max_score / total_score if total_score > 0 else 0.0
            result["scores"] = type_scores
        
        # 评估重要性
        importance_score = 0.0
        
        # 基于类型的基础分
        type_base_scores = {
            "decision": 3.0,
            "preference": 2.0,
            "system": 2.0,
            "project": 1.5,
            "skill": 1.5,
            "conversation": 1.0
        }
        importance_score += type_base_scores.get(result["type"], 1.0)
        
        # 关键词匹配加分
        for imp_level, rules in self.importance_rules.items():
            for keyword in rules.get("keywords", []):
                if keyword in content:
                    if imp_level == "critical":
                        importance_score += 3.0
                    elif imp_level == "important":
                        importance_score += 2.0
                    elif imp_level == "normal":
                        importance_score += 1.0
        
        # 确定重要性等级
        if importance_score >= self.importance_rules["critical"]["min_score"]:
            result["importance"] = "critical"
        elif importance_score >= self.importance_rules["important"]["min_score"]:
            result["importance"] = "important"
        elif importance_score >= self.importance_rules["normal"]["min_score"]:
            result["importance"] = "normal"
        else:
            result["importance"] = "temporary"
        
        # 生成标签
        tags = set()
        for tag, keywords in self.tag_rules.items():
            for keyword in keywords:
                if keyword in content:
                    tags.add(tag)
        
        # 添加类型标签
        tags.add(result["type"])
        
        # 添加重要性标签
        tags.add(f"importance_{result['importance']}")
        
        result["tags"] = list(tags)
        result["importance_score"] = importance_score
        
        return result
    
    def create_memory_record(self, content: str, metadata: Dict = None) -> Dict:
        """
        创建完整的记忆记录
        
        Args:
            content: 记忆内容
            metadata: 元数据
            
        Returns:
            完整的记忆记录
        """
        if metadata is None:
            metadata = {}
        
        # 生成唯一ID
        timestamp = metadata.get("timestamp", datetime.now().isoformat())
        mem_id = f"mem_{timestamp.replace(':', '').replace('-', '').replace('.', '_')}"
        
        # 分类记忆
        classification = self.classify_memory(content, metadata)
        
        # 构建完整记录
        record = {
            "id": mem_id,
            "timestamp": timestamp,
            "content": content,
            "metadata": metadata,
            "classification": classification,
            "storage_info": {
                "path": f"{classification['type']}/{mem_id}.json",
                "archived": False,
                "backup_count": 0
            }
        }
        
        return record
    
    def save_memory(self, record: Dict) -> str:
        """
        保存记忆记录到数据库
        
        Args:
            record: 记忆记录
            
        Returns:
            保存路径
        """
        mem_type = record["classification"]["type"]
        mem_id = record["id"]
        
        # 创建类型目录
        type_dir = self.database_path / mem_type
        type_dir.mkdir(exist_ok=True)
        
        # 保存文件
        file_path = type_dir / f"{mem_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        
        # 更新索引
        self._update_index(record)
        
        return str(file_path)
    
    def _update_index(self, record: Dict):
        """更新记忆索引"""
        index_file = self.database_path / "index.json"
        
        # 加载现有索引
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {
                "by_id": {},
                "by_type": {},
                "by_importance": {},
                "by_tag": {},
                "by_time": {}
            }
        
        mem_id = record["id"]
        classification = record["classification"]
        
        # 更新ID索引
        index["by_id"][mem_id] = {
            "type": classification["type"],
            "importance": classification["importance"],
            "timestamp": record["timestamp"],
            "path": record["storage_info"]["path"]
        }
        
        # 更新类型索引
        mem_type = classification["type"]
        if mem_type not in index["by_type"]:
            index["by_type"][mem_type] = []
        index["by_type"][mem_type].append(mem_id)
        
        # 更新重要性索引
        importance = classification["importance"]
        if importance not in index["by_importance"]:
            index["by_importance"][importance] = []
        index["by_importance"][importance].append(mem_id)
        
        # 更新标签索引
        for tag in classification["tags"]:
            if tag not in index["by_tag"]:
                index["by_tag"][tag] = []
            index["by_tag"][tag].append(mem_id)
        
        # 更新时间索引
        timestamp = record["timestamp"]
        date_key = timestamp[:10]  # YYYY-MM-DD
        if date_key not in index["by_time"]:
            index["by_time"][date_key] = []
        index["by_time"][date_key].append(mem_id)
        
        # 保存索引
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def search_memories(self, query: str, limit: int = 10) -> List[Dict]:
        """
        搜索记忆
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            
        Returns:
            匹配的记忆记录列表
        """
        # 加载索引
        index_file = self.database_path / "index.json"
        if not index_file.exists():
            return []
        
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        results = []
        
        # 简单关键词搜索（实际应该用更复杂的语义搜索）
        for mem_id, info in index["by_id"].items():
            # 加载记忆内容
            mem_path = self.database_path / info["path"]
            if mem_path.exists():
                with open(mem_path, 'r', encoding='utf-8') as f:
                    record = json.load(f)
                
                # 检查是否匹配
                content = record["content"].lower()
                if query.lower() in content:
                    # 计算简单相关性分数
                    score = content.count(query.lower()) * 0.5
                    score += 1.0 if info["importance"] == "critical" else 0.0
                    
                    results.append({
                        "record": record,
                        "score": score,
                        "relevance": min(score / 5.0, 1.0)
                    })
        
        # 按分数排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:limit]

def main():
    """测试分类系统"""
    classifier = MemoryClassifier()
    
    # 测试记忆
    test_memories = [
        {
            "content": "记住现在这个命令，以后在安装skills的时候要检查一下安全",
            "metadata": {
                "timestamp": "2026-02-11T04:50:00PST",
                "channel": "whatsapp",
                "sender": "用户"
            }
        },
        {
            "content": "OK继续初始化",
            "metadata": {
                "timestamp": "2026-02-11T04:50:00PST",
                "channel": "whatsapp",
                "sender": "用户"
            }
        },
        {
            "content": "爆款素材积累系统已完成10个频道的视频数据抓取",
            "metadata": {
                "timestamp": "2026-02-11T04:45:00PST",
                "channel": "system",
                "sender": "小玉"
            }
        }
    ]
    
    print("测试记忆分类系统:")
    print("=" * 50)
    
    for i, test in enumerate(test_memories, 1):
        print(f"\n测试记忆 #{i}:")
        print(f"内容: {test['content']}")
        
        # 分类
        classification = classifier.classify_memory(test["content"], test["metadata"])
        print(f"分类结果: {classification}")
        
        # 创建完整记录
        record = classifier.create_memory_record(test["content"], test["metadata"])
        print(f"记忆ID: {record['id']}")
        
        # 保存
        saved_path = classifier.save_memory(record)
        print(f"保存路径: {saved_path}")
    
    print("\n" + "=" * 50)
    print("分类系统测试完成!")

if __name__ == "__main__":
    main()