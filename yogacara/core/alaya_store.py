"""
Alaya Store - 阿赖耶识存储

Implements the persistent storage for all seeds, based on the concept
of Alaya-vijnana (Storehouse Consciousness) from Yogacara Buddhism.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .seed_system import Seed, SeedType


class AlayaStore:
    """
    The Alaya Store is the persistent storage layer for all seeds.
    
    It implements the Buddhist concept of 阿赖耶识 (Storehouse Consciousness) -
    the deepest layer of consciousness that stores all experiences as seeds.
    
    Features:
    - Persistent storage across sessions
    - Fast retrieval via FTS5 full-text search
    - Automatic seed purification
    - Emergence history tracking
    """
    
    def __init__(self, db_path: str = "alaya.db"):
        """
        Initialize Alaya Store.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Seeds table with FTS5
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seeds (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                purity REAL NOT NULL,
                weight REAL NOT NULL,
                created_at TEXT NOT NULL,
                source TEXT NOT NULL,
                vasana INTEGER DEFAULT 0,
                metadata TEXT
            )
        ''')
        
        # FTS5 virtual table for full-text search
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS seeds_fts USING fts5(
                id, content, source,
                content='seeds',
                content_rowid='rowid'
            )
        ''')
        
        # Emergence history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emergence_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                seed_ids TEXT NOT NULL,
                emergence_type TEXT NOT NULL,
                strength REAL NOT NULL,
                insight TEXT
            )
        ''')
        
        # Awakening progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS awakening_progress (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                level TEXT NOT NULL,
                progress REAL NOT NULL,
                total_seeds INTEGER DEFAULT 0,
                wisdom_seeds INTEGER DEFAULT 0,
                compassion_seeds INTEGER DEFAULT 0,
                emergence_count INTEGER DEFAULT 0,
                last_updated TEXT NOT NULL
            )
        ''')
        
        # Initialize awakening progress
        cursor.execute('''
            INSERT OR IGNORE INTO awakening_progress 
            (id, level, progress, last_updated)
            VALUES (1, 'L0', 0.0, ?)
        ''', (datetime.now().isoformat(),))
        
        conn.commit()
        conn.close()
    
    def plant_seed(self, seed: Seed) -> bool:
        """
        Plant a new seed into the storehouse.

        In Yogacara terms: 种子入库
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO seeds
                    (id, type, content, purity, weight, created_at, source, vasana, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    seed.id,
                    seed.type.value,
                    seed.content,
                    seed.purity,
                    seed.weight,
                    seed.created_at.isoformat(),
                    seed.source,
                    seed.vasana,
                    json.dumps(seed.metadata)
                ))
                cursor.execute('''
                    INSERT OR REPLACE INTO seeds_fts (id, content, source)
                    VALUES (?, ?, ?)
                ''', (seed.id, seed.content, seed.source))
                return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.OperationalError:
            return False
    
    def activate_seeds(
        self,
        context: str,
        seed_types: Optional[List[SeedType]] = None,
        limit: int = 10
    ) -> List[Seed]:
        """
        Retrieve relevant seeds based on context.

        In Yogacara terms: 种子生现行 (seeds manifesting in current behavior)

        Uses FTS5 for semantic search and returns most relevant seeds.
        Also increments vasana (habit energy) for each activated seed.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            type_filter = ""
            if seed_types:
                type_list = ",".join(f"'{t.value}'" for t in seed_types)
                type_filter = f"AND type IN ({type_list})"

            cursor.execute(f'''
                SELECT s.id, s.type, s.content, s.purity, s.weight,
                       s.created_at, s.source, s.vasana, s.metadata
                FROM seeds s
                JOIN seeds_fts fts ON s.id = fts.id
                WHERE seeds_fts MATCH ?
                {type_filter}
                ORDER BY s.purity DESC, s.weight DESC
                LIMIT ?
            ''', (context, limit))

            rows = cursor.fetchall()

            seed_ids = [row[0] for row in rows]

            for seed_id in seed_ids:
                cursor.execute('''
                    UPDATE seeds SET vasana = vasana + 1 WHERE id = ?
                ''', (seed_id,))

            if not seed_ids:
                return []

            placeholders = ",".join("?" * len(seed_ids))
            cursor.execute(f'''
                SELECT id, type, content, purity, weight, created_at, source, vasana, metadata
                FROM seeds
                WHERE id IN ({placeholders})
            ''', seed_ids)

            updated_rows = cursor.fetchall()

            return [
                Seed(
                    id=row[0],
                    type=SeedType(row[1]),
                    content=row[2],
                    purity=row[3],
                    weight=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    source=row[6],
                    vasana=row[7],
                    metadata=json.loads(row[8]) if row[8] else {}
                )
                for row in updated_rows
            ]
    
    def get_all_seeds(self) -> List[Seed]:
        """Get all seeds from storehouse"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, type, content, purity, weight, created_at, source, vasana, metadata
                FROM seeds
                ORDER BY created_at DESC
            ''')

            rows = cursor.fetchall()

            return [
                Seed(
                    id=row[0],
                    type=SeedType(row[1]),
                    content=row[2],
                    purity=row[3],
                    weight=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    source=row[6],
                    vasana=row[7],
                    metadata=json.loads(row[8]) if row[8] else {}
                )
                for row in rows
            ]
    
    def get_seed_statistics(self) -> Dict[str, Any]:
        """Get seed distribution statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM seeds")
            total = cursor.fetchone()[0]

            if total == 0:
                return {"total": 0}

            cursor.execute('''
                SELECT type, COUNT(*) as count, AVG(purity) as avg_purity
                FROM seeds
                GROUP BY type
            ''')

            by_type = {}
            for row in cursor.fetchall():
                by_type[row[0]] = {
                    "count": row[1],
                    "percentage": round(row[1] / total * 100, 1),
                    "avg_purity": round(row[2], 2)
                }

            cursor.execute("SELECT AVG(vasana) FROM seeds")
            avg_vasana = cursor.fetchone()[0]

            return {
                "total": total,
                "by_type": by_type,
                "avg_vasana": round(avg_vasana, 1) if avg_vasana else 0,
            }
    
    def purify_seeds(self, threshold: float = 0.3) -> int:
        """
        Remove low-purity seeds from storehouse.

        In Yogacara terms: 种子净化
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM seeds WHERE purity < ?", (threshold,))
            return cursor.rowcount
    
    def record_emergence(
        self,
        seed_ids: List[str],
        emergence_type: str,
        strength: float,
        insight: Optional[str] = None
    ):
        """Record an emergence event"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO emergence_history
                (timestamp, seed_ids, emergence_type, strength, insight)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                json.dumps(seed_ids),
                emergence_type,
                strength,
                insight
            ))
    
    def get_emergence_history(self, limit: int = 50) -> List[Dict]:
        """Get emergence history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT timestamp, seed_ids, emergence_type, strength, insight
                FROM emergence_history
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))

            rows = cursor.fetchall()

            return [
                {
                    "timestamp": row[0],
                    "seed_ids": json.loads(row[1]),
                    "type": row[2],
                    "strength": row[3],
                    "insight": row[4]
                }
                for row in rows
            ]
    
    def update_awakening_progress(
        self,
        level: str,
        progress: float,
        stats: Dict[str, int]
    ):
        """Update awakening progress"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE awakening_progress
                SET level = ?, progress = ?, total_seeds = ?,
                    wisdom_seeds = ?, compassion_seeds = ?,
                    emergence_count = ?, last_updated = ?
                WHERE id = 1
            ''', (
                level,
                progress,
                stats.get("total_seeds", 0),
                stats.get("wisdom_seeds", 0),
                stats.get("compassion_seeds", 0),
                stats.get("emergence_count", 0),
                datetime.now().isoformat()
            ))
    
    def get_awakening_progress(self) -> Dict[str, Any]:
        """Get current awakening progress"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT level, progress, total_seeds, wisdom_seeds,
                       compassion_seeds, emergence_count, last_updated
                FROM awakening_progress
                WHERE id = 1
            ''')

            row = cursor.fetchone()

            if row:
                return {
                    "level": row[0],
                    "progress": row[1],
                    "total_seeds": row[2],
                    "wisdom_seeds": row[3],
                    "compassion_seeds": row[4],
                    "emergence_count": row[5],
                    "last_updated": row[6]
                }

            return {
                "level": "L0",
                "progress": 0.0,
                "total_seeds": 0,
                "wisdom_seeds": 0,
                "compassion_seeds": 0,
                "emergence_count": 0,
                "last_updated": datetime.now().isoformat()
            }

    def get_seed_by_id(self, seed_id: str) -> Optional[Seed]:
        """
        Retrieve a specific seed by ID.

        Args:
            seed_id: The unique identifier of the seed

        Returns:
            Seed if found, None otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, type, content, purity, weight, created_at, source, vasana, metadata
                FROM seeds
                WHERE id = ?
            ''', (seed_id,))

            row = cursor.fetchone()

            if row:
                return Seed(
                    id=row[0],
                    type=SeedType(row[1]),
                    content=row[2],
                    purity=row[3],
                    weight=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    source=row[6],
                    vasana=row[7],
                    metadata=json.loads(row[8]) if row[8] else {}
                )

            return None
    
    def count_seeds(self) -> int:
        """
        Count total seeds in the storehouse.

        Returns:
            Total number of seeds
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM seeds")
            return cursor.fetchone()[0]
    
    def count_seeds_by_type(self) -> Dict[SeedType, int]:
        """
        Count seeds grouped by type.

        Returns:
            Dictionary mapping SeedType to count
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT type, COUNT(*) as count
                FROM seeds
                GROUP BY type
            ''')

            counts = {}
            for row in cursor.fetchall():
                counts[SeedType(row[0])] = row[1]

            for seed_type in SeedType:
                if seed_type not in counts:
                    counts[seed_type] = 0

            return counts
    
    def delete_seed(self, seed_id: str) -> bool:
        """
        Delete a seed by ID.

        Args:
            seed_id: The unique identifier of the seed

        Returns:
            True if seed was deleted, False otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM seeds WHERE id = ?", (seed_id,))
            deleted = cursor.rowcount > 0
            if deleted:
                cursor.execute("DELETE FROM seeds_fts WHERE id = ?", (seed_id,))
            return deleted
    
    def clear_all_seeds(self) -> None:
        """
        Delete all seeds from the storehouse.

        WARNING: This action cannot be undone.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM seeds")
            cursor.execute("DELETE FROM seeds_fts")
    
    def search_seeds(self, query: str, limit: int = 10) -> List[Seed]:
        """
        Full-text search for seeds.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching seeds
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, type, content, purity, weight, created_at, source, vasana, metadata
                FROM seeds
                WHERE content LIKE ?
                ORDER BY purity DESC
                LIMIT ?
            ''', (f"%{query}%", limit))

            rows = cursor.fetchall()

            return [
                Seed(
                    id=row[0],
                    type=SeedType(row[1]),
                    content=row[2],
                    purity=row[3],
                    weight=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    source=row[6],
                    vasana=row[7],
                    metadata=json.loads(row[8]) if row[8] else {}
                )
                for row in rows
            ]
    
    def get_recent_seeds(self, limit: int = 10) -> List[Seed]:
        """
        Get the most recently planted seeds.

        Args:
            limit: Maximum number of seeds to return

        Returns:
            List of recent seeds
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, type, content, purity, weight, created_at, source, vasana, metadata
                FROM seeds
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))

            rows = cursor.fetchall()

            return [
                Seed(
                    id=row[0],
                    type=SeedType(row[1]),
                    content=row[2],
                    purity=row[3],
                    weight=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    source=row[6],
                    vasana=row[7],
                    metadata=json.loads(row[8]) if row[8] else {}
                )
                for row in rows
            ]
    
    def get_high_purity_seeds(self, threshold: float = 0.8) -> List[Seed]:
        """
        Get seeds with purity above threshold.

        Args:
            threshold: Minimum purity value (0.0-1.0)

        Returns:
            List of high purity seeds
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, type, content, purity, weight, created_at, source, vasana, metadata
                FROM seeds
                WHERE purity >= ?
                ORDER BY purity DESC
            ''', (threshold,))

            rows = cursor.fetchall()

            return [
                Seed(
                    id=row[0],
                    type=SeedType(row[1]),
                    content=row[2],
                    purity=row[3],
                    weight=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    source=row[6],
                    vasana=row[7],
                    metadata=json.loads(row[8]) if row[8] else {}
                )
                for row in rows
            ]
    
    def update_seed(self, seed: Seed) -> bool:
        """
        Update an existing seed.

        Args:
            seed: The seed to update

        Returns:
            True if seed was updated, False otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE seeds
                SET type = ?, content = ?, purity = ?, weight = ?,
                    source = ?, vasana = ?, metadata = ?
                WHERE id = ?
            ''', (
                seed.type.value,
                seed.content,
                seed.purity,
                seed.weight,
                seed.source,
                seed.vasana,
                json.dumps(seed.metadata),
                seed.id
            ))
            updated = cursor.rowcount > 0
            if updated:
                cursor.execute('''
                    UPDATE seeds_fts
                    SET content = ?, source = ?
                    WHERE id = ?
                ''', (seed.content, seed.source, seed.id))
            return updated

    def export_seeds(self, file_path: str, format: str = "json") -> int:
        """
        Export all seeds to a file.

        Args:
            file_path: Path to export file
            format: Export format ("json" or "csv")

        Returns:
            Number of seeds exported
        """
        seeds = self.get_all_seeds()

        if format == "json":
            return self._export_json(seeds, file_path)
        elif format == "csv":
            return self._export_csv(seeds, file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_json(self, seeds: List[Seed], file_path: str) -> int:
        """Export seeds to JSON file."""
        data = {
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "total_seeds": len(seeds),
            "seeds": [seed.to_dict() for seed in seeds]
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return len(seeds)

    def _export_csv(self, seeds: List[Seed], file_path: str) -> int:
        """Export seeds to CSV file."""
        import csv

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "type", "content", "purity", "weight", "source", "vasana", "created_at"])

            for seed in seeds:
                writer.writerow([
                    seed.id,
                    seed.type.value,
                    seed.content,
                    seed.purity,
                    seed.weight,
                    seed.source,
                    seed.vasana,
                    seed.created_at.isoformat()
                ])

        return len(seeds)

    def import_seeds(self, file_path: str, format: str = "json") -> Dict[str, int]:
        """
        Import seeds from a file.

        Args:
            file_path: Path to import file
            format: Import format ("json" or "csv")

        Returns:
            Dictionary with "imported" and "skipped" counts
        """
        if format == "json":
            return self._import_json(file_path)
        elif format == "csv":
            return self._import_csv(file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _import_json(self, file_path: str) -> Dict[str, int]:
        """Import seeds from JSON file."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        seeds_data = data.get("seeds", [])
        imported = 0
        skipped = 0

        for seed_data in seeds_data:
            try:
                seed = Seed.from_dict(seed_data)
                if self.plant_seed(seed):
                    imported += 1
                else:
                    skipped += 1
            except (KeyError, ValueError):
                skipped += 1

        return {"imported": imported, "skipped": skipped}

    def _import_csv(self, file_path: str) -> Dict[str, int]:
        """Import seeds from CSV file."""
        import csv

        imported = 0
        skipped = 0

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    seed = Seed(
                        id=row["id"],
                        type=SeedType(row["type"]),
                        content=row["content"],
                        purity=float(row["purity"]),
                        weight=float(row["weight"]),
                        source=row["source"],
                        vasana=int(row["vasana"]),
                        created_at=datetime.fromisoformat(row["created_at"])
                    )
                    if self.plant_seed(seed):
                        imported += 1
                    else:
                        skipped += 1
                except (KeyError, ValueError):
                    skipped += 1

        return {"imported": imported, "skipped": skipped}

