"""Local durability bench: concurrency, R7 under load, 20-client reads, COPY speed. RESETS DATA.
    BASE_URL=http://localhost:8000 CRM_TOKEN=dev DATABASE_URL=... python tests/bench.py"""
import asyncio, time, httpx, os, sys
sys.path.insert(0, '.')
B=os.environ.get("BASE_URL","http://localhost:8000"); H={"Authorization":"Bearer "+os.environ.get("CRM_TOKEN","dev")}; V="/crm/objects/2026-09"
async def main():
    async with httpx.AsyncClient(base_url=B, headers=H, timeout=30) as c:
        await c.post("/__reset")
        r = await c.post(V+"/contacts", json={"properties":{"email":"x@y.it"}}); cid=r.json()["id"]
        props=["firstname","lastname","phone","city","state","jobtitle","website","zip","country","address"]
        rs = await asyncio.gather(*[c.patch(f"{V}/contacts/{cid}", json={"properties":{p: f"v{i}"}}) for i,p in enumerate(props)])
        got = (await c.get(f"{V}/contacts/{cid}", params={"properties":",".join(props)})).json()["properties"]
        print("parallel patches, none lost:", all(got[p]==f"v{i}" for i,p in enumerate(props)), {r.status_code for r in rs})
        rs = await asyncio.gather(*[c.post(V+"/contacts", json={"properties":{"email":"dup@y.it","firstname":str(i)}}) for i in range(20)])
        print("parallel same-email creates:", sorted(r.status_code for r in rs).count(201), "created,", sum(r.status_code==409 for r in rs), "409")
    # R7 via direct property def (POST /properties is Lane A)
    import asyncpg
    conn = await asyncpg.connect(os.environ["DATABASE_URL"])
    await conn.execute("INSERT INTO property_defs(object_type,name,label,has_unique_value) VALUES('companies','partita_iva','Partita IVA',true) ON CONFLICT DO NOTHING")
    await conn.close()
    async with httpx.AsyncClient(base_url=B, headers=H, timeout=30) as c:
        a = await c.post(V+"/companies", json={"properties":{"name":"A","partita_iva":"IT 12345678901"}})
        b = await c.post(V+"/companies", json={"properties":{"name":"B","partita_iva":"12345678901"}})
        print("R7:", a.status_code, a.json()["properties"].get("partita_iva"), "->", b.status_code, b.json().get("category"))
        rs = await asyncio.gather(*[c.post(V+"/companies", json={"properties":{"name":f"C{i}","partita_iva":"99999999999"}}) for i in range(10)])
        print("R7 parallel:", sorted(r.status_code for r in rs))
        # read latency under 20 clients
        lat=[]
        async def one():
            for _ in range(25):
                t=time.monotonic(); await c.get(f"{V}/contacts/{cid}"); lat.append(time.monotonic()-t)
        await asyncio.gather(*[one() for _ in range(20)])
        lat.sort(); print(f"20 clients x25 GET: p95 {lat[int(len(lat)*.95)]*1000:.0f} ms, max {lat[-1]*1000:.0f} ms")
    # COPY benchmark at migration scale
    from app import db, store
    await db.connect()
    async with db.pool.acquire() as conn:
        n=600_000
        t=time.monotonic()
        ids = await store.reserve_ids(conn, n)
        now = store.utcnow()
        recs=[(i,"notes",{"hs_note_body":"Promemoria su Valentina per campionatura. Inviato listino 2024","hs_timestamp":"2018-01-13T16:02:00.000Z","id_legacy":str(i),"autore":"u@b.it"},now,now) for i in ids]
        t1=time.monotonic()
        async with conn.transaction():
            await conn.copy_records_to_table("objects", records=recs, columns=["id","object_type","properties","created_at","updated_at"])
        t2=time.monotonic()
        arecs=[("notes",i,"contacts",1,"HUBSPOT_DEFINED",202) for i in ids]
        async with conn.transaction():
            await conn.copy_records_to_table("associations", records=arecs, columns=["from_type","from_id","to_type","to_id","category","type_id"])
        t3=time.monotonic()
        print(f"COPY {n} objects: build {t1-t:.1f}s copy {t2-t1:.1f}s; {n} assoc rows {t3-t2:.1f}s")
        t=time.monotonic(); await db.reset(); print(f"reset after 600k rows: {(time.monotonic()-t)*1000:.0f} ms")
    await db.close()
asyncio.run(main())
