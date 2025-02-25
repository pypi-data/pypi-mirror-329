import collections
import uuid

from common.service.medical_text import extract_all_relation_key, extract_medical_text, sentence_count, \
    random_pick_relation_key
from common.util.csv_util import write_csv
from common.util.database_connection_util import get_connection_by_schema
from common.util.date_util import current_time
from common.util.sql_util import store_by_batch
from common.util.string_util import cut_by_time


class TestSqlUtil:
    def test_extract_all_relation_key(self):
        pass
        # conn = get_tumour_stage_connection(b'')
        # cursor = conn.cursor()
        # relation_key_list = extract_all_relation_key(cursor)
        # for relation_key in relation_key_list:
        #     print(relation_key)

    def test_extract_medical_text(self):
        present_dict = {
            "nc_admission_record": ["nc_present_illness_history"]
        }
        conn = get_connection_by_schema(b'', 'ncpcs_all', 'prod_test')
        nlp_conn = get_connection_by_schema(b'', 'ncpcs_nlp')
        corpus_conn = get_connection_by_schema(b'', 'nlp_corpus')

        cursor = conn.cursor()
        entity_data_list = []
        entity_list = []
        admission_record_list = []
        # relation_key_list = extract_all_relation_key(cursor)[1000:1500]
        relation_key_list = extract_all_relation_key(cursor)
        for relation_key in relation_key_list:
            medical_text_list = extract_medical_text(cursor, relation_key, column_dict=present_dict, split_method=cut_by_time)
            if not medical_text_list:
                continue
            medical_text = medical_text_list[0]
            if not medical_text['文本列表']:
                continue

            entity_data_list.append({
                'nc_key': str(relation_key),
                'nc_medical_institution_code': relation_key.medical_institution_code,
                'nc_medical_record_no': relation_key.medical_record_no,
                'nc_discharge_time': relation_key.discharge_time,
                'nc_valid_flag': 1
            })

            admission_record_list.append({
                'nc_rid': str(uuid.uuid4()),
                'nc_medical_institution_code': relation_key.medical_institution_code,
                'nc_medical_record_no': relation_key.medical_record_no,
                'nc_discharge_time': relation_key.discharge_time,
                'nc_present_illness_history': medical_text['原文'],
                'nc_backup_time': current_time(),
            })
            for timeline, _ in medical_text['文本列表']:
                if not timeline:
                    continue
                entity_list.append({
                    'nc_key': str(relation_key),
                    'nc_medical_institution_code': relation_key.medical_institution_code,
                    'nc_medical_record_no': relation_key.medical_record_no,
                    'nc_discharge_time': relation_key.discharge_time,
                    'nc_entity_name': timeline.base_time,
                    'nc_entity_name_convert': timeline.base_time_convert,
                    'nc_content': timeline.content,
                    # 'nc_entity_classification': timeline.base_time_convert,
                    'nc_entity_classification': '时间',
                    'nc_table_name': medical_text['表名'],
                    'nc_column_name': medical_text['字段名'],
                    'nc_source': medical_text['表名'] + '-' + medical_text['字段名'],
                    'nc_start_index': timeline.start_index,
                    'nc_end_index': timeline.end_index,
                    'nc_page': medical_text['页码'],
                    'nc_page_uuid': medical_text['组号']
                })
        store_by_batch('nc_entity_data', entity_data_list, nlp_conn)
        store_by_batch('nc_entity', entity_list, nlp_conn)
        store_by_batch('nc_admission_record', admission_record_list, corpus_conn)

    def test_sentence_count(self):
        sentence_list = ["测试", "测试", "四大皆空", "第三方i哦", "第三方i哦", "第三方i哦"]
        sentence_count(sentence_list)

    def test_random_pick_relation_key(self):
        conn = get_connection_by_schema(b'')
        cursor = conn.cursor()
        all_relation_key_list = extract_all_relation_key(cursor)
        relation_key_dict = collections.defaultdict(list)
        for relation_key in all_relation_key_list:
            relation_key_dict[relation_key.medical_institution_code].append(relation_key)
        assert len(random_pick_relation_key(relation_key_dict, 500)) == 500
        assert len(random_pick_relation_key(relation_key_dict, 37)) == 37

