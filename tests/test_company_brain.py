"""Integration checks: explicit disposable KB_TEST_DATABASE_URL, no paid model calls.
Run: KB_TEST_DATABASE_URL=postgresql://.../kb_test CRM_TOKEN=dev python -m unittest discover -s tests -p test_company_brain.py -v
"""
import asyncio
import io
import json
import os
import unittest
import zipfile
from datetime import datetime, timedelta
from unittest.mock import patch

import httpx

from app import config, db, store
from app.agent import kb, read, run
from app.agent.tools import RunState, execute_tool
from app.errors import ApiError
from app.main import app
from app.migrate import setup
from app.migrate.run import run as migrate

URL = os.environ.get('KB_TEST_DATABASE_URL', '')
NOW = datetime.fromisoformat('2026-12-02T10:00:00+01:00')


def call(name, **arguments):
    return {'content': None, 'tool_calls': [{'id': name, 'type': 'function', 'function': {
        'name': name, 'arguments': json.dumps(arguments)}}]}


@unittest.skipUnless(URL and 'kb_test' in URL.rsplit('/', 1)[-1], 'requires an explicitly disposable kb_test database')
class CompanyBrain(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.env = patch.object(config, 'DATABASE_URL', URL)
        self.env.start()
        await db.connect()
        await db.reset()
        async with db.pool.acquire() as conn:
            await setup.ensure(conn)
            await store.replace_agent_users(conn, [
                {'id_utente': 'U01', 'nome': 'Anna', 'cognome': 'Sala', 'email': 'anna@acme.it', 'attivo': 'S'},
                {'id_utente': 'U02', 'nome': 'Ex', 'cognome': 'Employee', 'email': 'ex@acme.it', 'attivo': 'N'}])
        self.state = RunState('anna@acme.it', NOW, 'Aggiorna il record', allow_writes=True)

    async def asyncTearDown(self):
        await db.close()
        self.env.stop()

    async def company(self, name='Acme', **properties):
        async with db.pool.acquire() as conn:
            return await store.create(conn, 'companies', {'name': name, **properties})

    async def publish(self, doc_id, content='La garanzia dura 24 mesi.', links=None):
        async with db.pool.acquire() as conn:
            revision = await conn.fetchval('SELECT revision FROM kb_documents WHERE doc_id=$1', doc_id) or 0
            return await store.publish_kb_document(conn, {'doc_id': doc_id, 'title': 'Garanzia speciale',
                'category': 'policy', 'content': content, 'source': 'reviewed test fixture',
                'metadata': {'aliases': ['garanzia'], 'object_types': ['companies'], 'skus': ['BF-00001']},
                'links': links or []}, expected_revision=revision)

    async def scripted_reply(self, messages, body):
        script = iter(messages)
        async def complete(*args):
            return next(script)
        with patch.object(config, 'OPENROUTER_API_KEY', 'mock-not-a-key'), patch.object(run, '_complete', complete):
            return await run.reply(body)

    def body(self, text):
        return {'context': {'now': NOW.isoformat(), 'user': 'anna@acme.it'}, 'messages': [{'role': 'user', 'content': text}]}

    async def test_document_publication_live_revision_and_seed_preservation(self):
        first = await self.publish('KB-LIVE')
        async with db.pool.acquire() as conn:
            self.assertIn('24 mesi', (await kb.get_document(conn, 'KB-LIVE'))['content'])
        second = await self.publish('KB-LIVE', 'La garanzia dura 36 mesi.')
        self.assertEqual(second['revision'], first['revision'] + 1)
        async with db.pool.acquire() as conn:
            self.assertIn('36 mesi', (await kb.search_documents(conn, 'garanzia'))[0]['content'])
            self.assertIn('24 mesi', (await kb.get_document(conn, 'KB-LIVE', first['revision']))['content'])
            await store.publish_kb_document(conn, {'doc_id': 'KB-LIVE', 'title': 'Ignored seed', 'category': 'policy',
                'content': 'Old content', 'source': 'seed'}, only_if_missing=True)
        await db.close()
        await db.connect()
        async with db.pool.acquire() as conn:
            self.assertIn('36 mesi', (await kb.get_document(conn, 'KB-LIVE'))['content'])

    async def test_revision_conflicts_noop_and_archive(self):
        row = await self.publish('KB-CONFLICT')
        async with db.pool.acquire() as conn:
            doc = await kb.get_document(conn, row['doc_id'])
            again = await store.publish_kb_document(conn, doc, expected_revision=row['revision'])
            self.assertEqual(again['revision'], row['revision'])
            with self.assertRaises(ApiError) as failure:
                await store.publish_kb_document(conn, doc, expected_revision=0)
            self.assertEqual(failure.exception.status, 409)
            await store.change_kb_document(conn, row['doc_id'], expected_revision=row['revision'], archived=True)
            with self.assertRaises(ApiError):
                await kb.get_document(conn, row['doc_id'])

    async def test_exact_retrieval_italian_and_no_match(self):
        await self.publish('KB-SKU')
        async with db.pool.acquire() as conn:
            self.assertEqual((await kb.search_documents(conn, 'R11'))[0]['doc_id'], 'BKB-R11')
            self.assertIn('BKB-R11', [r['doc_id'] for r in await kb.search_documents(conn, 'trattativa perso')])
            self.assertTrue(await kb.search_documents(conn, 'BF-00001'))
            self.assertEqual(await kb.search_documents(conn, 'BF-99999'), [])
            self.assertEqual(await kb.search_documents(conn, 'zzzznotawordqqq'), [])

    async def test_graph_api_updates_and_reset_clear_links(self):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url='http://test', headers={'Authorization': 'Bearer dev'}) as client:
            response = await client.post('/crm/objects/2026-09/companies', json={'properties': {'name': 'Live company', 'domain': 'live.it'}})
            self.assertEqual(response.status_code, 201, response.text)
            identifier = response.json()['id']
            await client.patch('/crm/objects/2026-09/companies/' + identifier, json={'properties': {'city': 'Roma'}})
        doc = await self.publish('KB-LINK', links=[{'object_id': identifier, 'relation': 'applies_to'}])
        async with db.pool.acquire() as conn:
            graph = await kb.related_knowledge(conn, 'companies', int(identifier))
            self.assertEqual(graph['records'][0]['properties']['city'], 'Roma')
            self.assertIn('KB-LINK', [d['doc_id'] for d in graph['documents']])
        answer = await self.scripted_reply([call('get_record', object_type='companies', id=identifier), {'content': 'La sede è Roma.'}], self.body('Dove si trova la company ' + identifier + '?'))
        self.assertIn('Roma', answer)
        self.assertIn('companies:' + identifier, answer)
        await db.reset()
        async with db.pool.acquire() as conn:
            self.assertEqual(await conn.fetchval('SELECT count(*) FROM kb_document_links'), 0)
            self.assertEqual(await conn.fetchval('SELECT count(*) FROM agent_users'), 0)
            self.assertEqual((await kb.get_document(conn, doc['doc_id']))['revision'], doc['revision'])
        replacement = await self.company('Different company')
        self.assertEqual(str(replacement['id']), identifier)
        async with db.pool.acquire() as conn:
            self.assertEqual(await conn.fetchval('SELECT count(*) FROM kb_document_links WHERE object_id=$1', replacement['id']), 0)

    async def test_won_sample_readback_and_once_only(self):
        company = await self.company('Nuova Serramenti Mazza')
        async with db.pool.acquire() as conn:
            deal = await store.create(conn, 'deals', {'dealname': 'Fornitura Mazza', 'dealstage': 'qualifiedtobuy', 'commerciale': 'anna@acme.it'}, [('companies', company['id'], None)])
        answer = await self.scripted_reply([
            call('search_records', object_type='companies', query='Nuova Serramenti Mazza'),
            call('search_records', object_type='deals', related_to={'object_type': 'companies', 'id': str(company['id'])}),
            call('update_record', object_type='deals', id=str(deal['id']), properties={'dealstage': 'closedwon'}),
            {'content': 'Ho aggiornato la trattativa a Vinta.'}], self.body("Segna come vinta la trattativa di Nuova Serramenti Mazza, è arrivato l'ordine firmato."))
        self.assertIn('Modifiche verificate', answer)
        async with db.pool.acquire() as conn:
            self.assertEqual((await store.get(conn, 'deals', deal['id']))['properties']['dealstage'], 'closedwon')
            await store.update(conn, 'deals', deal['id'], {'dealstage': 'closedwon'})
            related = await read.related_records(conn, 'deals', deal['id'], 'tickets')
            self.assertEqual(related['total'], 1)
            self.assertEqual(related['records'][0]['properties']['assegnatario'], 'anna@acme.it')

    async def test_revenue_sample(self):
        company = await self.company('Nuova Tessile Spinelli', fatturato_2025='12345.67', classe_cliente='B')
        answer = await self.scripted_reply([call('search_records', object_type='companies', query='Nuova Tessile Spinelli'), {'content': 'Il fatturato 2025 è 12.345,67 euro.'}], self.body('Quanto abbiamo fatturato con Nuova Tessile Spinelli nel 2025?'))
        self.assertIn('12.345,67', answer)
        self.assertIn('companies:' + str(company['id']), answer)

    async def test_lost_context_clock_r12_and_inactive_assignment(self):
        company = await self.company('Acme', domain='acme.it')
        async with db.pool.acquire() as conn:
            deal = await store.create(conn, 'deals', {'dealname': 'Lost', 'dealstage': 'qualifiedtobuy'})
        await execute_tool('get_record', {'object_type': 'deals', 'id': str(deal['id'])}, self.state)
        result = await execute_tool('update_record', {'object_type': 'deals', 'id': str(deal['id']), 'properties': {'dealstage': 'Persa'}}, self.state)
        due = result['automation_records'][0]['properties']['hs_timestamp']
        self.assertEqual(datetime.fromisoformat(due.replace('Z', '+00:00')), NOW + timedelta(days=180))
        result = await execute_tool('create_record', {'object_type': 'contacts', 'properties': {'email': 'NEW@ACME.IT'}}, self.state)
        self.assertIn(company['id'], [r['to_id'] for r in result['record']['associations']])
        with self.assertRaises(ApiError):
            await execute_tool('update_record', {'object_type': 'deals', 'id': str(deal['id']), 'properties': {'commerciale': 'ex@acme.it'}}, self.state)

    async def test_ambiguity_vat_and_read_only_guards(self):
        await self.company('Same', partita_iva='12345678901')
        await self.company('Same')
        matches = await execute_tool('search_records', {'object_type': 'companies', 'query': 'Same'}, self.state)
        with self.assertRaises(ApiError):
            await execute_tool('update_record', {'object_type': 'companies', 'id': matches['records'][0]['id'], 'properties': {'city': 'Roma'}}, self.state)
        with self.assertRaises(ApiError) as error:
            await execute_tool('create_record', {'object_type': 'companies', 'properties': {'name': 'Duplicate', 'partita_iva': '12345678901'}}, self.state)
        self.assertEqual(error.exception.status, 409)
        self.state.allow_writes = False
        with self.assertRaises(ApiError):
            await execute_tool('create_record', {'object_type': 'companies', 'properties': {'name': 'Unrequested'}}, self.state)

    async def test_exact_aggregate_over_multiple_pages_and_currencies(self):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                for i in range(205):
                    await store.create(conn, 'deals', {'dealname': str(i), 'amount': '0.1', 'deal_currency_code': 'EUR'})
                await store.create(conn, 'deals', {'dealname': 'USD', 'amount': '3', 'deal_currency_code': 'USD'})
            result = await read.aggregate_records(conn, 'deals', {'operation': 'sum', 'field': 'amount'}, self.state.user)
        self.assertEqual(result['count'], 206)
        self.assertEqual({g['currency']: g['sum'] for g in result['groups']}, {'EUR': '20.5', 'USD': '3'})

    async def test_csv_partial_failure_rolls_back(self):
        self.state.attachments = [{'name': 'products.csv', 'content_type': 'text/csv', 'content': 'codice_articolo;descrizione;prezzo_listino\nBF00001;Valid;12,50\nBF00002;Invalid;bad\n'}]
        with self.assertRaises(ApiError):
            await execute_tool('apply_csv', {'attachment_index': 0, 'object_type': 'products', 'mode': 'create', 'id_property': 'hs_sku'}, self.state)
        self.assertEqual(self.state.actions, [])
        async with db.pool.acquire() as conn:
            self.assertEqual(await conn.fetchval("SELECT count(*) FROM objects WHERE object_type='products'"), 0)

    async def test_concurrent_conversations_have_separate_evidence(self):
        companies = [await self.company('Customer ' + str(i)) for i in range(4)]
        async def complete(client, messages, deadline, final):
            tools = [m for m in messages if m['role'] == 'tool']
            if tools:
                data = json.loads(tools[-1]['content'])
                return {'content': data['properties']['name']}
            text = next(m['content'] for m in reversed(messages) if m['role'] == 'user')
            await asyncio.sleep(0.01)
            return call('get_record', object_type='companies', id=text.split()[-1])
        with patch.object(config, 'OPENROUTER_API_KEY', 'mock'), patch.object(run, '_complete', complete):
            answers = await asyncio.gather(*[run.reply(self.body('Leggi company ' + str(c['id']))) for c in companies])
        for i, answer in enumerate(answers):
            self.assertIn('Customer ' + str(i), answer)
            for j, company in enumerate(companies):
                self.assertEqual('companies:' + str(company['id']) in answer, i == j)

    async def test_provider_failure_after_commit_is_truthful(self):
        company = await self.company()
        script = [call('get_record', object_type='companies', id=str(company['id'])),
                  call('update_record', object_type='companies', id=str(company['id']), properties={'city': 'Roma'}),
                  httpx.ReadTimeout('mock outage')]
        async def complete(*args):
            value = script.pop(0)
            if isinstance(value, Exception):
                raise value
            return value
        with patch.object(config, 'OPENROUTER_API_KEY', 'mock'), patch.object(run, '_complete', complete):
            answer = await run.reply(self.body('Aggiorna company ' + str(company['id']) + ' a Roma'))
        self.assertIn('city=Roma', answer)
        self.assertIn('completate e verificate', answer)

    async def test_timeout_and_tool_cap(self):
        async def slow(*args):
            await asyncio.sleep(1)
        with patch.object(config, 'OPENROUTER_API_KEY', 'mock'), patch.object(run, '_complete', slow), patch.object(run, 'TURN_TIMEOUT', 0.03):
            answer = await run.reply(self.body('Leggi il CRM'))
        self.assertIn('Non ho effettuato modifiche', answer)
        calls = []
        async def repetitive(client, messages, deadline, final):
            calls.append(final)
            return {'content': 'Fine.'} if final else call('list_kb_documents')
        with patch.object(config, 'OPENROUTER_API_KEY', 'mock'), patch.object(run, '_complete', repetitive):
            await run.reply(self.body('Leggi il CRM'))
        self.assertEqual(calls, [False] * 8 + [True])

    async def test_migration_persists_roster(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as archive:
            archive.writestr('utenti.csv', 'id_utente;nome;cognome;email;attivo\nU33;Elena;Silvestri;elena@brambilla.it;S\n')
            archive.writestr('aziende.csv', 'id_azienda;ragione_sociale;sito_web\n100;Migrated;new.it\n')
        await migrate(db.pool, data.getvalue())
        async with db.pool.acquire() as conn:
            users = await read.list_users(conn, 'Elena')
            self.assertEqual(users[0]['email'], 'elena@brambilla.it')
            self.assertTrue(users[0]['active'])
            self.assertEqual((await read.search_records(conn, 'companies', {'query': 'Migrated'}, users[0]['email']))['total'], 1)


if __name__ == '__main__':
    unittest.main()
