#!/usr/bin/env python3
"""
记忆保护机制
防止记忆被意外删除，提供自动备份和恢复功能
"""

import json
import shutil
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Optional

class MemoryProtector:
    """记忆保护器"""
    
    def __init__(self, database_path: str = "memory/database"):
        self.database_path = Path(database_path)
        self.backup_path = self.database_path / "backups"
        self.backup_path.mkdir(exist_ok=True)
        
        # 配置
        self.config = {
            "enabled": True,
            "auto_backup": True,
            "retention_days": 365,
            "prevent_deletion": True,
            "backup_schedule": "daily",  # daily, weekly, monthly
            "max_backups": 30,
            "integrity_check": True
        }
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.database_path / "protection.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("MemoryProtector")
    
    def protect_memory(self, memory_id: str, memory_type: str) -> bool:
        """
        保护特定记忆
        
        Args:
            memory_id: 记忆ID
            memory_type: 记忆类型
            
        Returns:
            是否保护成功
        """
        if not self.config["enabled"]:
            return True
        
        try:
            # 获取记忆文件路径
            mem_file = self.database_path / memory_type / f"{memory_id}.json"
            if not mem_file.exists():
                self.logger.warning(f"记忆文件不存在: {mem_file}")
                return False
            
            # 计算文件哈希值
            file_hash = self._calculate_hash(mem_file)
            
            # 创建保护记录
            protection_record = {
                "memory_id": memory_id,
                "memory_type": memory_type,
                "protected_at": datetime.now().isoformat(),
                "file_hash": file_hash,
                "file_size": mem_file.stat().st_size,
                "protection_level": "critical" if memory_type == "decision" else "normal",
                "backup_created": False
            }
            
            # 保存保护记录
            protection_file = self.database_path / "protection" / f"{memory_id}.json"
            protection_file.parent.mkdir(exist_ok=True)
            
            with open(protection_file, 'w', encoding='utf-8') as f:
                json.dump(protection_record, f, ensure_ascii=False, indent=2)
            
            # 自动备份
            if self.config["auto_backup"]:
                backup_success = self._create_backup(memory_id, memory_type, file_hash)
                protection_record["backup_created"] = backup_success
            
            self.logger.info(f"记忆保护成功: {memory_id} ({memory_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"记忆保护失败: {memory_id}, 错误: {str(e)}")
            return False
    
    def _calculate_hash(self, file_path: Path) -> str:
        """计算文件哈希值"""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def _create_backup(self, memory_id: str, memory_type: str, original_hash: str) -> bool:
        """
        创建记忆备份
        
        Args:
            memory_id: 记忆ID
            memory_type: 记忆类型
            original_hash: 原始文件哈希
            
        Returns:
            是否备份成功
        """
        try:
            # 源文件路径
            source_file = self.database_path / memory_type / f"{memory_id}.json"
            
            # 备份文件路径
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_path / f"{memory_id}_{timestamp}.json"
            
            # 复制文件
            shutil.copy2(source_file, backup_file)
            
            # 验证备份
            backup_hash = self._calculate_hash(backup_file)
            if backup_hash != original_hash:
                self.logger.error(f"备份验证失败: {memory_id}")
                backup_file.unlink()
                return False
            
            # 记录备份信息
            backup_info = {
                "memory_id": memory_id,
                "memory_type": memory_type,
                "backup_time": timestamp,
                "backup_path": str(backup_file),
                "file_hash": backup_hash,
                "verified": True
            }
            
            backup_info_file = self.backup_path / f"{memory_id}_{timestamp}_info.json"
            with open(backup_info_file, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, ensure_ascii=False, indent=2)
            
            # 清理旧备份
            self._cleanup_old_backups(memory_id)
            
            self.logger.info(f"记忆备份成功: {memory_id} -> {backup_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"记忆备份失败: {memory_id}, 错误: {str(e)}")
            return False
    
    def _cleanup_old_backups(self, memory_id: str):
        """清理旧的备份文件"""
        try:
            # 查找该记忆的所有备份
            backup_files = list(self.backup_path.glob(f"{memory_id}_*.json"))
            info_files = list(self.backup_path.glob(f"{memory_id}_*_info.json"))
            
            # 只保留信息文件对应的备份文件
            valid_backups = []
            for info_file in info_files:
                with open(info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    if "backup_path" in info:
                        backup_file = Path(info["backup_path"])
                        if backup_file.exists():
                            valid_backups.append((info_file, backup_file))
            
            # 按时间排序
            valid_backups.sort(key=lambda x: x[0].stem.split('_')[-1], reverse=True)
            
            # 删除超出数量限制的旧备份
            max_backups = self.config["max_backups"]
            if len(valid_backups) > max_backups:
                for info_file, backup_file in valid_backups[max_backups:]:
                    try:
                        info_file.unlink()
                        backup_file.unlink()
                        self.logger.info(f"清理旧备份: {backup_file.name}")
                    except Exception as e:
                        self.logger.warning(f"清理备份失败: {backup_file.name}, 错误: {str(e)}")
            
        except Exception as e:
            self.logger.error(f"清理备份失败: {memory_id}, 错误: {str(e)}")
    
    def check_integrity(self, memory_id: str = None) -> Dict:
        """
        检查记忆完整性
        
        Args:
            memory_id: 可选，特定记忆ID，None表示检查所有
            
        Returns:
            完整性检查结果
        """
        if not self.config["integrity_check"]:
            return {"status": "disabled", "checked": 0, "errors": []}
        
        try:
            errors = []
            checked_count = 0
            
            # 加载保护记录
            protection_dir = self.database_path / "protection"
            if not protection_dir.exists():
                return {"status": "no_protection", "checked": 0, "errors": []}
            
            # 确定要检查的记忆
            if memory_id:
                protection_files = [protection_dir / f"{memory_id}.json"]
            else:
                protection_files = list(protection_dir.glob("*.json"))
            
            for protection_file in protection_files:
                if not protection_file.exists():
                    continue
                
                try:
                    with open(protection_file, 'r', encoding='utf-8') as f:
                        protection_record = json.load(f)
                    
                    mem_id = protection_record["memory_id"]
                    mem_type = protection_record["memory_type"]
                    expected_hash = protection_record["file_hash"]
                    
                    # 检查记忆文件是否存在
                    mem_file = self.database_path / mem_type / f"{mem_id}.json"
                    if not mem_file.exists():
                        errors.append({
                            "memory_id": mem_id,
                            "error": "记忆文件丢失",
                            "type": "missing_file"
                        })
                        continue
                    
                    # 检查文件哈希
                    current_hash = self._calculate_hash(mem_file)
                    if current_hash != expected_hash:
                        errors.append({
                            "memory_id": mem_id,
                            "error": "文件哈希不匹配",
                            "type": "hash_mismatch",
                            "expected": expected_hash,
                            "actual": current_hash
                        })
                    
                    checked_count += 1
                    
                except Exception as e:
                    errors.append({
                        "memory_id": protection_file.stem,
                        "error": f"保护记录读取失败: {str(e)}",
                        "type": "record_error"
                    })
            
            status = "healthy" if not errors else "errors_found"
            
            result = {
                "status": status,
                "checked": checked_count,
                "errors": errors,
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"完整性检查完成: 检查{checked_count}个记忆，发现{len(errors)}个错误")
            return result
            
        except Exception as e:
            self.logger.error(f"完整性检查失败: {str(e)}")
            return {
                "status": "check_failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def restore_memory(self, memory_id: str, backup_timestamp: str = None) -> bool:
        """
        从备份恢复记忆
        
        Args:
            memory_id: 记忆ID
            backup_timestamp: 备份时间戳，None表示使用最新备份
            
        Returns:
            是否恢复成功
        """
        try:
            # 查找备份
            if backup_timestamp:
                info_file = self.backup_path / f"{memory_id}_{backup_timestamp}_info.json"
            else:
                # 查找最新备份
                info_files = list(self.backup_path.glob(f"{memory_id}_*_info.json"))
                if not info_files:
                    self.logger.error(f"找不到备份: {memory_id}")
                    return False
                
                # 按时间戳排序，取最新的
                info_files.sort(key=lambda x: x.stem.split('_')[-2], reverse=True)
                info_file = info_files[0]
            
            if not info_file.exists():
                self.logger.error(f"备份信息文件不存在: {info_file}")
                return False
            
            # 读取备份信息
            with open(info_file, 'r', encoding='utf-8') as f:
                backup_info = json.load(f)
            
            backup_file = Path(backup_info["backup_path"])
            if not backup_file.exists():
                self.logger.error(f"备份文件不存在: {backup_file}")
                return False
            
            # 确定目标路径
            memory_type = backup_info["memory_type"]
            target_dir = self.database_path / memory_type
            target_dir.mkdir(exist_ok=True)
            
            target_file = target_dir / f"{memory_id}.json"
            
            # 恢复文件
            shutil.copy2(backup_file, target_file)
            
            # 验证恢复
            restored_hash = self._calculate_hash(target_file)
            if restored_hash != backup_info["file_hash"]:
                self.logger.error(f"恢复验证失败: {memory_id}")
                target_file.unlink()
                return False
            
            # 更新保护记录
            protection_record = {
                "memory_id": memory_id,
                "memory_type": memory_type,
                "restored_at": datetime.now().isoformat(),
                "restored_from": backup_info["backup_time"],
                "file_hash": restored_hash,
                "file_size": target_file.stat().st_size,
                "protection_level": "critical" if memory_type == "decision" else "normal"
            }
            
            protection_file = self.database_path / "protection" / f"{memory_id}.json"
            with open(protection_file, 'w', encoding='utf-8') as f:
                json.dump(protection_record, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"记忆恢复成功: {memory_id} 从备份 {backup_info['backup_time']}")
            return True
            
        except Exception as e:
            self.logger.error(f"记忆恢复失败: {memory_id}, 错误: {str(e)}")
            return False
    
    def schedule_backup(self):
        """执行计划备份"""
        if not self.config["auto_backup"]:
            return
        
        try:
            # 加载索引，获取所有记忆
            index_file = self.database_path / "index.json"
            if not index_file.exists():
                return
            
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            # 备份所有关键记忆
            critical_memories = index.get("by_importance", {}).get("critical", [])
            
            backup_count = 0
            for mem_id in critical_memories:
                mem_info = index["by_id"].get(mem_id)
                if mem_info:
                    success = self.protect_memory(mem_id, mem_info["type"])
                    if success:
                        backup_count += 1
            
            self.logger.info(f"计划备份完成: 备份了{backup_count}个关键记忆")
            
        except Exception as e:
            self.logger.error(f"计划备份失败: {str(e)}")

def main():
    """测试记忆保护机制"""
    protector = MemoryProtector()
    
    print("测试记忆保护机制:")
    print("=" * 50)
    
    # 测试保护记忆
    test_memory_id = "mem_20260211T045000PST"
    test_memory_type = "conversation"
    
    print(f"\n1. 保护记忆: {test_memory_id}")
    success = protector.protect_memory(test_memory_id, test_memory_type)
    print(f"保护结果: {'成功' if success else '失败'}")
    
    # 测试完整性检查
    print(f"\n2. 完整性检查:")
    integrity_result = protector.check_integrity(test_memory_id)
    print(f"检查状态: {integrity_result['status']}")
    print(f"检查数量: {integrity_result['checked']}")
    if integrity_result['errors']:
        print(f"发现错误: {len(integrity_result['errors'])}个")
    
    # 测试计划备份
    print(f"\n3. 执行计划备份:")
    protector.schedule_backup()
    print("计划备份执行完成")
    
    print("\n" + "=" * 50)
    print("记忆保护机制测试完成!")

if __name__ == "__main__":
    main()