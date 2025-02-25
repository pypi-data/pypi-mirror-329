import nichey as wiki
import sqlite3
from .utils import get_tmp_path
import os


def test_migration():
    tmp_path = get_tmp_path()
    mywiki = wiki.Wiki(topic="", path=tmp_path)
    try:
        title = "My First Entity"
        ent = mywiki.add_entity(
            title=title,
            desc="My Desc"
        )
        src = mywiki.add_source(
            title="My First Source",
            text=""
        )

        new_conn = sqlite3.connect(mywiki.path)
        cur = new_conn.cursor()
        cur.execute("DROP TABLE sources")
        cur.execute("ALTER TABLE entities DROP COLUMN desc")
        cur.execute("PRAGMA user_version = 0")
        cur.close()
        new_conn.close()
        
        mywiki._migrate_db()
        retrieved_entity = mywiki.get_entity_by_slug(ent.slug)
        assert(retrieved_entity is not None)
        assert(retrieved_entity.title == title)
        assert(retrieved_entity.desc is None)

        retrieved_source = mywiki.get_source_by_id(src.id)
        assert(retrieved_source is None)

        new_source = mywiki.add_source(
            title="My Second Source",
            text=""
        )
        new_retrieved_source = mywiki.get_source_by_id(new_source.id)
        assert(new_retrieved_source is not None)
    
    finally:
        os.remove(mywiki.path)


def test_integrity():
    tmp_path = get_tmp_path()
    mywiki = wiki.Wiki(topic="", path=tmp_path)
    try:
        new_ent: wiki.Entity = mywiki.add_entity(title="My Entity")
        new_src: wiki.Source = mywiki.add_source(title="My Source", text="")
        ref = mywiki.add_reference(entity_id=new_ent.id, source_id=new_src.id)
        assert(ref)
        lst = mywiki.get_referenced_sources(entity_id=new_ent.id)
        assert(len(lst))
        mywiki.delete_source_by_id(new_src.id)
        lst = mywiki.get_referenced_sources(entity_id=new_ent.id)
        assert(not len(lst))
        ent = mywiki.get_entity_by_slug(new_ent.slug)
        assert(ent)

    finally:
        os.remove(mywiki.path)
