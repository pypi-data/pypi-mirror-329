# -*- coding: utf-8 -*-
import oceanAlgorithmPrivate
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import json
import logging
import io
import boto3
import os
import matplotlib
import atexit
import warnings
import time
import psycopg2
from sklearn.preprocessing import label_binarize
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import roc_curve, auc
from botocore.exceptions import ClientError
from datetime import datetime
from sklearn.metrics import confusion_matrix
from logtos3 import upload
matplotlib.use('Agg')

DB = {}
class Dao:
    def get_secret(self, db_name, secret_name, retry_count=0):
        try:
            session = boto3.session.Session()
            client = session.client(service_name='secretsmanager', region_name="ap-northeast-2")
            self.set_db_config(client, db_name, secret_name)
        except ClientError as e:
            if retry_count > 30:
                print(f"Failed to fetch secrets after 30 retries. Error: {e}")
                raise e
            else:
                print(f"Retrying to fetch secret for {db_name}. Attempt {retry_count + 1}")
                time.sleep(2)
                self.get_secret(db_name, retry_count + 1)

    def set_db_config(self, client, db_name, secret_name):
        try:
            secret_value = client.get_secret_value(SecretId=secret_name)
            db = json.loads(secret_value['SecretString'])
            print(f"Fetched secrets for {db_name}: {secret_name}")
            
            DB["user"] = db['username']
            DB["pw"] = db['password']
            
            if "database" not in DB:
                DB["database"] = {}
                
            DB["database"][db_name] = {
                "host": db['host'],
                "port": db['port'],
                "dbname": db['dbname']
            }
        except Exception as e:
            print(f"Error setting DB configuration for {db_name}: {e}")
            raise e
        
    def db_connect(self, dbname, secret_name):
        # if self.conn is None or self.conn.closed:
        self.get_secret(dbname, secret_name)
        try:
            self.conn = psycopg2.connect(
                host=DB['database'][dbname]['host'],
                dbname=DB['database'][dbname]['dbname'],
                user=DB['user'],
                password=DB['pw'],
                port=DB['database'][dbname]['port']
            )
            print(f"Connected to the database: {dbname}")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            raise e
            
    def db_close(self):
        if self.conn and not self.conn.closed:
            try:
                self.conn.commit()
                self.conn.close()
                self.conn = None 
            except psycopg2.Error as e:
                print(f"Error closing the database connection: {e}")
                raise e
            
    def get_cursor(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor

    def select_all(self, query):
        cursor = self.get_cursor(query)
        row = cursor.fetchall()
        df = pd.DataFrame(row, columns=[desc[0]
                          for desc in cursor.description])
        cursor.close()
        return df
    
    def select_one(self, query):
        cursor = self.get_cursor(query)
        row = cursor.fetchone()
        cursor.close()
        return row

    def insert(self, query, params=None):
        cursor  = self.get_cursor(query,params)
        try:
            row_count = cursor.rowcount
            self.conn.commit()
            return row_count
        except psycopg2.Error as e:
            print(f"Error executing insert: {e}")
            raise e
        finally:
            cursor.close()

class OceanAIDao(Dao):
    def __init__(self):
        db_name = 'ocean-ai-dev'
        secret_name = f"dev/{db_name}/data/postgre"
        self.db_connect(db_name, secret_name)
    
    def get_schema_master(self, group_name):
        q = """
            select * from data.schema_master
            where group_name = '{group_name}'
            """.format(group_name=group_name)
        row = self.select_all(q)
        return row
    
    def get_node_category(self, group_name, node_name):
        q = """
            select key_name, node_name from data.node_category
            where type = '{group_name}' and node_name ='{node_name}'
            """.format(group_name=group_name, node_name=node_name)
        row = self.select_all(q)
        return row
    
class KyoboAIDao(Dao):
    def __init__(self):
        db_name = 'kyoboai'
        secret_name = f"dev/{db_name}/data/postgres"
        self.db_connect(db_name, secret_name)
        
    def get_data(self,ticker,s_date,e_date):
        ticker_lower = ticker.upper()
        condition = ""
        if s_date is not None:
            condition = f"AND '{s_date}' <= TO_CHAR(CASE \
                                WHEN oami.table_name = 'dcs.kbdcs010' THEN d10.etf_ymd \
                                WHEN oami.table_name = 'dcs.kbdcs052' THEN d52.macro_ymd \
                                WHEN oami.table_name = 'dcs.kbdcs005' THEN d05.macro_ymd \
                                WHEN oami.table_name = 'dcs.kbdcs005_ts' THEN d05_ts.macro_ymd \
                                WHEN oami.table_name = 'dcs.kbdcs105_ts' THEN d105_ts.macro_ymd \
                            END, 'YYYYMMDD')".format(s_date=s_date)
                            
        if e_date is not None:
            condition += f" AND '{e_date}' >= TO_CHAR(CASE \
                                WHEN oami.table_name = 'dcs.kbdcs010' THEN d10.etf_ymd \
                                WHEN oami.table_name = 'dcs.kbdcs052' THEN d52.macro_ymd \
                                WHEN oami.table_name = 'dcs.kbdcs005' THEN d05.macro_ymd \
                                WHEN oami.table_name = 'dcs.kbdcs005_ts' THEN d05_ts.macro_ymd \
                                WHEN oami.table_name = 'dcs.kbdcs105_ts' THEN d105_ts.macro_ymd \
                            END, 'YYYYMMDD')".format(e_date=e_date)
        query = """
                select
                    case 
                        when oami.table_name = 'dcs.kbdcs010' THEN d10.etf_ymd \
                        WHEN oami.table_name = 'dcs.kbdcs052' THEN d52.macro_ymd\
                        WHEN oami.table_name = 'dcs.kbdcs005' THEN d05.macro_ymd\
                        WHEN oami.table_name = 'dcs.kbdcs005_ts' THEN d05_ts.macro_ymd \
                        WHEN oami.table_name = 'dcs.kbdcs105_ts' THEN d105_ts.macro_ymd\
                    end as ymd,
                    oami.mnemonic as ticker,
                    CASE
                        WHEN oami.table_name = 'dcs.kbdcs010' THEN d10.instrument_ri
                        when oami.table_name = 'dcs.kbdcs052' then d52.x_value
                        when oami.table_name = 'dcs.kbdcs005' then d05.x_value
                        WHEN oami.table_name = 'dcs.kbdcs005_ts' THEN d05_ts.instrument_es
                        WHEN oami.table_name = 'dcs.kbdcs105_ts' then d105_ts.value
                        END AS value
                    from dcs.ocean_ai_meta_info oami
                    LEFT JOIN
                        dcs.kbdcs010 d10 ON oami.table_name = 'dcs.kbdcs010' AND d10.instrument = oami.instrument
                    LEFT JOIN
                        dcs.kbdcs052 d52 ON oami.table_name = 'dcs.kbdcs052' AND d52.instrument = oami.instrument
                    LEFT JOIN
                        dcs.kbdcs005 d05 ON oami.table_name = 'dcs.kbdcs005' AND d05.instrument = oami.instrument
                    LEFT JOIN
                        dcs.kbdcs105_ts d105_ts ON oami.table_name = 'dcs.kbdcs105_ts' AND d105_ts.instrument = oami.instrument
                    LEFT JOIN
                        dcs.kbdcs005_ts d05_ts ON oami.table_name = 'dcs.kbdcs005_ts' AND d05_ts.instrument = oami.instrument
                    where oami.mnemonic ='{ticker}'
                    {condition}
                    order by ymd asc
                """.format(ticker=ticker_lower,condition=condition)
        row = self.select_all(query)
        return row

class LoggerHelper:
    _shutdown_registered = False

    def __init__(self, log_level='DEBUG'):
        self.logger = self.setup_logger(log_level)
        
        if not LoggerHelper._shutdown_registered:
            atexit.register(self.log_shutdown_time)
            LoggerHelper._shutdown_registered = True

        warnings.filterwarnings("ignore")
        
    def setup_logger(self, log_level):
        logger = logging.getLogger('OceanAI_logger')
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        logger.propagate = False
        
        if not logger.hasHandlers():
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
        return logger
    
    def handle_error(self, message, exception=None):
        if exception:
            self.logger.error(f"{message}: {str(exception)}")
        else:
            self.logger.error(message)
        sys.exit(1)
    
    def log_start_time(self):
        LoggerHelper.start_time = datetime.now()
        self.logger.info(f"시작 시간: {LoggerHelper.start_time}")

    def log_shutdown_time(self):
        end_time = datetime.now()
        if hasattr(LoggerHelper, 'start_time'):
            duration = end_time - LoggerHelper.start_time
            self.logger.info(f"종료 시간: {end_time}")
            self.logger.info(f"실행 시간: {duration}")
        else:
            self.logger.info(f"종료 시간: {end_time}")
    
    def check_verbose(self, log_level):
        if log_level == 'DEBUG':
            verbose = 2
        elif log_level == 'INFO':
            verbose = 1
        return verbose
    
    def log_parameters(self, **params):
        param_lines = []
        custom_labels = {
        'dep_var': '종속 변수',
        'indep_var': '독립 변수',
        'model': '모델 파라미터 정보'
        }
        split_info_keys = {'train_size', 'test_size', 'random_state', 
                           'X_train', 'y_train', 'X_test', 'y_test'}
        
        for key, value in params.items():
            if key in split_info_keys:
                if key == 'train_size':
                    param_lines.append(f"학습-테스트 데이터 분할 정보 \ntrain_size={value}")
                elif key == 'test_size':
                    param_lines.append(f"test_size={value}")
                elif key == 'random_state':
                    param_lines.append(f"random_state={value}")
                elif key == 'X_train':
                    param_lines.append(f"학습 데이터 크기\nX_train={value.shape}")
                elif key == 'y_train':
                    param_lines.append(f"y_train={value.shape}")
                elif key == 'X_test':
                    param_lines.append(f"테스트 데이터 크기\nX_test={value.shape}")
                elif key == 'y_test':
                    param_lines.append(f"y_test={value.shape}") 
            else:       
                if isinstance(value, pd.DataFrame):
                    formatted_value = self.format_dataframe(value)
                    label = custom_labels.get(key, '데이터 프레임')
                elif isinstance(value, pd.Series):
                    formatted_value = self.format_series(value)
                    label = custom_labels.get(key, '데이터 시리즈')
                elif isinstance(value, (dict, list)):
                    formatted_value = self.format_json(value)
                    label = custom_labels.get(key, 'JSON Parameter')
                elif hasattr(value, 'get_params'):
                    formatted_value = self.format_model_params(value)
                    label = custom_labels.get(key, '모델 파라미터')
                else:
                    formatted_value = str(value)
                    label = 'General Parameter'

                param_lines.append(f"\n{label} ({key})\n{formatted_value}")
                param_message = "\n\n".join(param_lines)
        param_message = "\n".join(param_lines)
        self.logger.debug(f"데이터 정보를 출력합니다.\n{param_message}")
    
    def format_dataframe(self, df):
        df_info = f"DataFrame Shape: {df.shape} \nColumns: {', '.join(df.columns)}"
        preview = df.head(5).to_string()
        return f"{df_info}\n데이터 미리보기\n{preview}"
    
    def format_series(self, series):
        series_info = f"Series Shape: {len(series)} \nName: {series.name if series.name else '없음'}"
        preview = series.head(5).to_string()
        return f"{series_info}\n데이터 미리보기\n{preview}"
    
    def format_json(self, obj):
        return json.dumps(obj, indent=4)
    
    def format_model_params(self, model):
        if self.logger.isEnabledFor(logging.INFO):
            additional_info = []
            attributes = [
                ('Search Type', model.__class__.__name__),
                ('Estimator', getattr(model, 'estimator', None)),
                ('Cross-Validation Folds', getattr(model, 'cv', None)),
                ('Input Parameters', getattr(model, 'param_grid', None)),
                ('Best Parameters', getattr(model, 'best_params_', None)),
                ('Best Score', getattr(model, 'best_score_', None)),
                ('Classes', getattr(model.best_estimator_, 'classes_', None) if hasattr(model, 'best_estimator_') else None),
                ('Classes Count', getattr(model.best_estimator_, 'class_count_', None) if hasattr(model, 'best_estimator_') else None),
                ('Classes Prior', getattr(model.best_estimator_, 'class_prior_', None) if hasattr(model, 'best_estimator_') else None)
            ]
            for name, value in attributes:
                if value is not None:
                    additional_info.append(f"{name}: {value}")
            return '\n'.join(additional_info)
    
    def log_event(self, event_type, status=None, fold=None, total_folds=None):
        if event_type == 'training':
            if status == 'started':
                self.start_time = datetime.now()
                self.logger.debug(f"모델 학습 시작")
            elif status == 'completed':
                self.end_time = datetime.now()
                self.logger.debug(f"모델 학습 완료")
                if self.start_time and self.end_time:
                    duration = self.end_time - self.start_time
                    self.logger.debug(f"모델 학습 소요 시간: {duration}")
                    
        elif event_type == 'prediction':
            if status == 'started':
                self.logger.debug("모델 예측 시작")
            elif status == 'completed':
                self.logger.debug("모델 예측 완료")
            elif status == 'created':
                self.logger.debug("모델 예측 결과 데이터 생성 완료")
                
        elif event_type == 'scaling':
            if status == 'started':
                self.logger.debug("데이터 스케일링 시작")
            elif status == 'completed':
                self.logger.debug("데이터 스케일링 완료")
                
        elif event_type == 'cross-validation':
            if status == 'started':
                self.logger.debug(f"교차 검증 시작 ({total_folds} folds)")
            elif status == 'completed':
                self.logger.debug("교차 검증 완료")
            elif status == 'fold_started' and fold and total_folds:
                self.logger.debug(f"Fold {fold}/{total_folds} - 교차 검증 시작")
            elif status == 'fold_completed' and fold and total_folds:
                self.logger.debug(f"Fold {fold}/{total_folds} - 교차 검증 완료")


class Private(LoggerHelper):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Private, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, log_level='DEBUG'):
        if not hasattr(self, 'initialized') or not self.initialized:
            super().__init__(log_level=log_level)
            self.ocean_dao = OceanAIDao()
            self.kyobo_dao = KyoboAIDao()
            
            try:
                print(f"oceanAlgorithmPrivate version: {oceanAlgorithmPrivate.__version__}")
            except AttributeError:
                print("oceanAlgorithmPrivate does not have a __version__ attribute.")
            
            self.session = boto3.session.Session()
            self.client = self.session.client('secretsmanager', region_name='ap-northeast-2')
            self.s3 = boto3.client('s3')
            self.bucket_name = None
            self.s3_path = None
            self.base_filename = None

            self.raw_data = None
            self.schema_json = None
            
            self.features_ticker_property = None
            self.target_ticker_property = None
            self.initialized = True
            
            self.job_id = None
            self.node_name = None
            self.group_name = None
            self.target_schema = None
            
            self.performance_info = None
            self.model_info = None

    def get_secret(self, db_name):
        secret_name = 'dev/' + db_name + '/data/postgres'
        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=secret_name)
            secret_value = json.loads(get_secret_value_response['SecretString'])
            return secret_value
        except ClientError as e:
            print(f'ClientError: {e}')
            return None
    
    def upload_to_s3(self, file_name, bucket_name, s3_path):
        try:
            s3_manager = upload.S3UpAndDownManager(bucket_name=bucket_name)
            upload_result = s3_manager.upload_dataframe(
                data=file_name, 
                file_key=s3_path, 
                custom_version_id=self.job_id
            )
            print("test 업로드 결과:", upload_result)
            #self.s3.upload_file(file_name, bucket_name, s3_path)
        except Exception as e:
            self.handle_error(f"Failed to upload {file_name}")
    
    def upload_bytes_to_s3(self, byte_stream, file_name, bucket_name, s3_path):
        try:
            byte_stream.seek(0)
            #self.s3.upload_fileobj(byte_stream, bucket_name, s3_path)
            s3_manager = upload.S3UpAndDownManager(bucket_name=bucket_name)
            upload_result = s3_manager.upload_dataframe(
                data=byte_stream, 
                file_key=s3_path, 
                custom_version_id=self.job_id
            )
            print("test 업로드 결과:", upload_result)
        except Exception as e:
            self.handle_error(f"Failed to upload file-like object {file_name} to S3: {e}")
    
    def upload_file(self,files,var_names=None, target_name=None):
        if not isinstance(files, list):
            files = [files]
            
        if not isinstance(var_names, list):
            var_names = [var_names]
            
        if var_names is None:
            var_names = [None] * len(files)
        elif not isinstance(var_names, list):
            var_names = [var_names]
        elif len(var_names) != len(files):
            raise ValueError("The length of 'var_names' must match the length of 'files'.")
            
        for file_obj, var_name in zip(files, var_names):
            suffix = f"_{var_name}" if var_name else ""
            
            if target_name:
                file_name = f"{self.base_filename}_{target_name}{suffix}"
            else:
                file_name = f"{self.base_filename}{suffix}"
                
            if isinstance(file_obj, pd.DataFrame):
                file_name += ".csv"
                file_obj = self.add_dtype(file_obj)
                file_obj.to_csv(file_name, index=None, encoding='utf-8')
                self.upload_to_s3(file_name, self.bucket_name, self.s3_path + file_name)
                
            elif isinstance(file_obj, dict):
                file_name += ".json"
                self.save_to_json(file_obj, file_name)
                self.upload_to_s3(file_name, self.bucket_name, self.s3_path + file_name)
                
            elif isinstance(file_obj, plt.Figure):
                file_name += ".png"
                img_bytes = io.BytesIO()
                file_obj.savefig(img_bytes, format='png')
                img_bytes.seek(0)
                self.upload_bytes_to_s3(img_bytes, file_name, self.bucket_name, self.s3_path + file_name)

            if file_name:
                self.cleanup_files([file_name])
    
    def cleanup_files(self, file_names):
        for file_name in file_names:
            if os.path.exists(file_name):
                os.remove(file_name)

    def read_csv(self,file_path):
        raw = pd.read_csv(file_path)
        dtype_dict = {col: dtype for col, dtype in zip(raw.columns, list(raw.iloc[0]))}
        df = raw.iloc[1:]
        df = df.astype(dtype_dict)
        
        first_column_name = df.columns[0]
        df.set_index(first_column_name, inplace=True)
        df = df.dropna(how='any')
        return df, dtype_dict
    
    def read_data(self, file_path, parsed_data, schema_json=None, variable=None, params=None): # 0.0.37
        # - 파일/스키마 검증
        # - 매개변수 데이터 타입 검증
        # - 타깃 컬럼의 value에 대한 allowed_type/ 타깃 컬럼 유무 검증
        
        # 데이터 검증: 파일 읽기
        try:
            self.raw_data, dtype_dict = self.read_csv(file_path)
            self.logger.info(f"CSV 파일 '{file_path}'이 성공적으로 로드되었습니다.")
        except FileNotFoundError as e:
            self.handle_error(f"파일 '{file_path}'을 찾을 수 없습니다.")
        
        # 데이터 검증: 타깃 변수 (variable)
        if variable:
            try:
                X, y = self.validate_dataframe(self.raw_data, dtype_dict, parsed_data, variable)
                self.logger.info("데이터 유효성 검사가 완료되었습니다.")
                return X, y 
            except ValueError as e:
                self.handle_error(f"데이터 유효성 검사 실패: {str(e)}")
                  
        # 데이터 검증: 매개변수 (params)
        elif params:
            # 타깃 컬럼 데이터 유형 검증
            try:
                self.validate_target_column(self.raw_data, dtype_dict, parsed_data)
                target_var = self.validate_target_ticker(params) # 변수와 티커 맵핑 검증
                self.logger.info("데이터 유효성 검사가 완료되었습니다.")
                return self.raw_data, target_var
            except ValueError as e:
                self.handle_error(f"데이터 유효성 검사 실패: {str(e)}")
        else:
            return self.raw_data

    
    def validate_target_column(self, df, dtype_dict, parsed_data): # 0.0.37
        selected_value = {
            item['parameter_name']: {
                'allowed_data_types': item['allowed_data_types'],
                'selected_value': item.get('selected_value'),
                'ui_display_name_ko': item.get('ui_display_name_ko')
            }
            for item in parsed_data['parameters'] if item.get('allowed_data_types')}
        
        for param_name, details in selected_value.items():
            allowed_types = details['allowed_data_types']
            column_names = details['selected_value']
            display_name = details['ui_display_name_ko']
            
            # column_names의 형태를 확인하고 리스트로 변환
            if isinstance(column_names, list):
                # 리스트인 경우
                if all(isinstance(col, str) for col in column_names):
                    columns_to_check = column_names
                # 딕셔너리 리스트인 경우
                elif all(isinstance(col, dict) and 'column_name' in col for col in column_names):
                    columns_to_check = [col['column_name'] for col in column_names]
            
            # 각 열에 대해 검증 수행
            for col_name in columns_to_check:
                # 열 존재 여부 확인
                if col_name not in dtype_dict:
                    raise ValueError(f"'{col_name}' 열이 존재하지 않습니다.")

                # 데이터 유형 검증
                if not self.is_dtype_match(col_name, allowed_types, df):
                    raise ValueError(
                        f" '{display_name}'의 '{col_name}' 열의 데이터 유형이 "
                        f"허용된 유형({allowed_types})과 일치하지 않습니다.")
                    
    def validate_target_ticker(self, INPUT): # 0.0.37
        output_target = self.target_schema.iloc[0].get('output_target', None)
        target_var = INPUT[output_target]
        
        self.column_schema = {
            item['name']: {
                'ticker': item.get('ticker', None),
                'property': item.get('property', None),
            }
            for item in self.schema_json['columns']
        }
        
        if isinstance(target_var, list):
            if all(isinstance(col, str) for col in target_var):
                var_to_map = target_var
            # 딕셔너리 리스트인 경우
            elif all(isinstance(col, dict) and 'column_name' in col for col in target_var):
                var_to_map = [col['column_name'] for col in target_var]
        
        map_ticker ={}
        unique_tickers = set()  # 유니크 티커를 추적하기 위한 집합
        for key, value in self.column_schema.items():
            if key in var_to_map:
                ticker = value.get('ticker')
                if ticker in unique_tickers:
                    raise ValueError(f"중복 티커가 발견되었습니다: {ticker}. 고유한 티커 열을 선택해 주세요.")
                unique_tickers.add(ticker)
                map_ticker[key] = value
        
        return map_ticker
    

    def validate_dataframe(self, df, dtype_dict, parsed_data, variable):
        column_schema = {
            item['name']: {
                'ticker': item.get('ticker', None),
                'property': item.get('property', None),
                'description': item.get('description', None),
            }
            for item in self.schema_json['columns']
        }
        target_columns = variable.get('dep_var', [])
        if not isinstance(target_columns, list): # 종속변수 확인
            target_columns = [target_columns]
        
        # 데이터 타입 검증
        self.validate_selected_column(df, dtype_dict, parsed_data, variable)
        # 스케일링 피처 검증
        features_columns_scaled = self.validate_scaling_columns(column_schema, variable)
        X, y = self.validate_common_columns(df, column_schema, features_columns_scaled, target_columns)
        return X, y

    
    def map_ticker_properties(self, columns, column_schema):
        # 티커별 속성 매핑
        ticker_property_map = {}
        for column in columns:
            column_info = column_schema[column]
            ticker = column_info['ticker']
            property_name = column_info['property']
            
            if ticker not in ticker_property_map:
                ticker_property_map[ticker] = set()
            ticker_property_map[ticker].add(property_name)
        return ticker_property_map
    
    def validate_common_columns(self, df, column_schema, features_columns, target_columns):
        self.features_ticker_property = self.map_ticker_properties(features_columns, column_schema) # indep_var
        self.target_ticker_property = self.map_ticker_properties(target_columns, column_schema) # dep_var
        
        # 종속변수 갯수 확인
        num_target_column = len(target_columns)
        num_target_ticker = len(self.target_ticker_property)
        
        # 1. 종속변수 == 1개 -> 그대로 학습함
        if num_target_column == 1:
            X = df[features_columns]
            y = df[target_columns]
            return X, y
        
        if num_target_column > 1 and num_target_ticker > 1:
            # 공통 티커와 속성 찾기
            common_properties_features = set.intersection(*self.features_ticker_property.values()) # 피처 공통 속성(indep_var)
            common_properties_target = set.intersection(*self.target_ticker_property.values()) # 타겟 공통 속성(dep_var)
            
            # 종속변수 속성이 1개인지 확인
            if len(common_properties_target) != 1:
                raise ValueError("종속변수의 공통 속성이 1개가 아닙니다.")
                
            # 종속변수와 독립변수의 공통티커 확인
            if set(self.features_ticker_property.keys()) != set(self.target_ticker_property.keys()):
                error_message = (f"종속변수와 독립변수가 동일 티커에 대한 값을 포함하고 있지 않습니다."
                         f"종속변수 티커: {', '.join(self.target_ticker_property.keys())}, "
                         f"독립변수 티커: {', '.join(self.features_ticker_property.keys())}")
                raise ValueError(error_message)
            
            # 피처 중에서 공통 속성 확인
            final_features_columns = []
            for feature in features_columns:
                if feature in column_schema:
                    feature_info = column_schema[feature]
                    feature_property = feature_info['property']
                    
                    if (feature_property in common_properties_features):
                        final_features_columns.append(feature)
            
            # 선택된 독립변수와 종속변수 반환
            X = df[final_features_columns]
            y = df[target_columns]
            return X, y
    
    def reshape_for_model(self, X_train, y_train, X_test=None, y_test=None):
        feature = X_train.columns
        target = y_train.columns
        
        if X_test is None and y_test is None:
            if len(target) == 1:
                return X_train, y_train.squeeze()
            train_data = pd.concat([X_train, y_train], axis=1)
            X_train_data, y_train_data = self.reshape_frame(train_data, feature, target)
            return X_train_data, y_train_data
        
        else:
            if len(target) == 1:
                return X_train, y_train.squeeze(), X_test, y_test.squeeze()
            train_data = pd.concat([X_train, y_train], axis=1)
            test_data = pd.concat([X_test, y_test], axis=1)
        
            # reshape -> model에 입력되는 형태로 재가공
            X_train_data, y_train_data = self.reshape_frame(train_data, feature, target)
            X_test_data, y_test_data = self.reshape_frame(test_data, feature, target)
        
            return X_train_data, y_train_data, X_test_data, y_test_data
    
    def validate_scaling_columns(self, column_schema, variable):
        features = variable['indep_var']
        excluded_scaling_columns = []
        selected_columns = []

        # 피처 컬럼에서 스케일링된 컬럼 제외
        for column in features:
            column_info = column_schema[column]
            if 'scaling' in column_info['description'].lower():
                excluded_scaling_columns.append(column)
            else:
                selected_columns.append(column) # 스케일링 컬럼 제외한 타겟 컬럼
        # validation
        if not selected_columns:
            raise ValueError("선택된 독립변수는 스케일링이 적용된 데이터이므로 데이터 리키지를 방지하기 위해 학습을 중단합니다.")
        else:
            if excluded_scaling_columns:
                warning_message =f"주의: 이미 스케일링이 적용된 컬럼은 학습 대상에서 제외됩니다: {', '.join(excluded_scaling_columns)}"
                self.logger.warning(warning_message)
        return selected_columns

    def select_scaler(self, scaler_option):
        if scaler_option == 'minmax':
            scaler = MinMaxScaler()
        elif scaler_option == 'standard':
            scaler = StandardScaler()
        else:
            scaler = None  # No scaling
        return scaler
    
    def scale_data(self, scaler, train_set, test_set=None):
        if scaler is None:
            if test_set is None:
                return train_set
            else:
                return train_set, test_set
        else:
            if test_set is None:
                train_scaled = pd.DataFrame(scaler.fit_transform(train_set), index=train_set.index, columns=train_set.columns)
                return train_scaled
            else:
                train_scaled = pd.DataFrame(scaler.fit_transform(train_set), index=train_set.index, columns=train_set.columns)
                test_scaled = pd.DataFrame(scaler.transform(test_set), index=test_set.index, columns=test_set.columns)
                return train_scaled, test_scaled

    def reshape_frame(self, df, indep_vars, dep_vars):
        var_info = self.raw_info
        dep_var_info, indep_var_info = [], []

        for label_col in dep_vars:
            for column in var_info['columns']:
                if column['name'] == label_col:
                    dep_var_info.append(column)
        
        for label_col in indep_vars:
            for column in var_info['columns']:
                if column['name'] == label_col:
                    indep_var_info.append(column)        

        dep_tickers = set(info['ticker'] for info in dep_var_info)
        indep_tickers = set(info['ticker'] for info in indep_var_info)
        
        dep_df = self.build_rows(df, dep_tickers, dep_var_info).squeeze()
        indep_df = self.build_rows(df, indep_tickers, indep_var_info)
        return indep_df, dep_df
    
    def build_rows(self, df, tickers, target_var_info):
        # var_info에서 ticker와 property 정보를 기반으로 재구성
        rows = []
        index_name = df.index.name
        for date in df.index:
            for ticker in tickers:
                row = {'ticker': ticker, index_name: date}
                for info in target_var_info:
                    if info['ticker'] == ticker:
                        col_name = info['name']
                        prop_name = info['property']
                        
                        row[prop_name] = df.at[date, col_name]
                rows.append(row)
                
        result_df = pd.DataFrame(rows).set_index([df.index.name, 'ticker']).sort_index()
        return result_df

    
    def merge_result(self, X_test, df_result): # input 수정
        original_df = self.raw_data.copy()
        df_result = pd.concat([X_test, df_result], axis=1)
        
        column_properties = ['y_true', 'y_pred']
        if 'y_prob' in df_result.columns:
            column_properties.append('y_prob') # 분류 모델일 경우 확률 값 추가
            
        if len(self.target_ticker_property.keys()) == 1:
            target_ticker = next(iter(self.target_ticker_property.keys()))
            
            rename_mapping = {}
            for prop in column_properties:
                if prop in df_result.columns:
                    # 각 속성에 target_ticker를 추가하여 새 이름을 생성
                    new_column_name = f"{target_ticker}_{prop}"
                    rename_mapping[prop] = new_column_name
            df_result = df_result.rename(columns=rename_mapping)
            return df_result
        
        df_result = df_result.reset_index().set_index(original_df.index.name)
        
        if 'ticker' in df_result.columns: # ticker 컬럼 여부 확인
            unique_tickers = df_result['ticker'].unique()
            for ticker in unique_tickers:
                df_ticker = df_result[df_result['ticker'] == ticker]
                for base_col_name in column_properties:
                    col_name = f'{ticker}_{base_col_name}'
                    original_df.loc[df_ticker.index, col_name] = df_ticker[base_col_name].values
        else:
            for base_col_name in column_properties:
                original_df[base_col_name] = df_result[base_col_name].values

        original_df = original_df.loc[original_df.index.isin(df_result.index)]
        return original_df
    
    
    def merge_result_pca(self, input_data, output_data):
        original_df = self.raw_data.copy()
        
        df_result = pd.concat([input_data, output_data], axis=1)
        df_result = df_result.reset_index().set_index(original_df.index.name)
        
        column_properties = output_data.columns
        for base_col_name in column_properties:
            original_df[base_col_name] = df_result[base_col_name].values

        original_df = original_df.loc[original_df.index.isin(df_result.index)]
        return original_df
    
        
    def save_results(self, variable, report=None, fig=None):
        target_name = variable['dep_var']
        uploaded_files = []  # 업로드된 파일들을 추적하기 위한 리스트
        var_names = []  # 업로드 파일의 변수 이름
       
        # eval_report 업로드
        if report is not None:
            uploaded_files.append(report)
            var_names.append('report')
 
        # fig 업로드
        if fig is not None:
            uploaded_files.append(fig)
            var_names.append('fig')
       
        # 업로드 파일이 있는 경우에만 파일 업로드
        if uploaded_files:
            self.upload_file(uploaded_files, var_names=var_names, target_name=target_name)
           
        if fig is not None:
            print(f"{self.base_filename}_{target_name}_fig.png")
 
        self.log_event('prediction', status='created')

    
    def handle_target_schema(self, params, target_schema): # 0.0.37
        filtered_df = target_schema.copy()
        pred_type = params.get('pred_type', '')
        
        if 'class' in pred_type:
            filtered_df = filtered_df[filtered_df['key_name'].str.contains('class', na=False)]
        if 'reg' in pred_type:
            filtered_df = filtered_df[filtered_df['key_name'].str.contains('reg', na=False) ]  
        return filtered_df
    
    def handle_target_var(self, params, output_target): # 0.0.39
        output_target_values = params.get(output_target, []) # 퀀트
        
        if all(isinstance(item, str) for item in output_target_values):
            return output_target_values
        
        target_vars = []
        for item in output_target_values:
            if isinstance(item, dict) and 'column_name' in item: # 비중배분 딕셔너리
                target_vars.append(item['column_name'])
            elif isinstance(item, dict) and 'dep_var' in item:
                target_vars.append(item['dep_var'])
        return target_vars

    def get_column_value(self, schema_json, column_name, property_): # 0.0.41
        for column in schema_json.get('columns', []):
            if column['name'] == column_name:
                if property_.upper() in ['TRUE_VALUE', 'PROBABILITY', 'PREDICTED_VALUE']:
                    name = column.get('ticker', "") # 알고리즘 아웃풋은 컬럼명을 티커명으로 하기 위함
                else: 
                    name = column.get('name', "")
                ticker = column.get('ticker', "")
                ticker_type = column.get('ticker_type', "")
                parent_property = column.get('parent_property', "") # Parent property 추가
                return name, ticker, ticker_type, parent_property
            
        self.logger.warning(f"Column '{column_name}' not found in the schema JSON.")
        return None, None, None, None
    
    def generate_schema_json(self, params, schema_json):  # 0.0.40
        # 1. PROPERTY는 액션, 노드를 거치면 항상 바뀐다. -> 공통이다.
        # 2. DESCRIPTION은 타겟 컬럼에 대해 모두 알고리즘(동일함), Progress(동일함), 데이터처리(동일함) -> 공통이다.
        # 3. OUTPUT COLUMN의 prefix, suffix 공통으로 적용한다
        # 4. TICKER/TICKER TYPE은 타겟 컬럼에 대해 다르다.
        group_name = self.group_name
        node_name = self.node_name

        node_category = self.ocean_dao.get_node_category(group_name, node_name)
        schema_master = self.ocean_dao.get_schema_master(group_name)
        target_schema = schema_master.merge(node_category, on="key_name", how="inner") # key_name 기준으로 조인
        
        # 타깃 스키마 테이블 조회
        self.target_schema = self.handle_target_schema(params, target_schema)
        existing_columns = {col['name'] for col in schema_json.get('columns', [])}

        for _, entry in self.target_schema.iterrows():
            output_target = entry.get('output_target', None)
            output_prefix = entry.get('output_prefix', None)
            output_suffix = entry.get('output_suffix', None)
            output_suffix_target = entry.get('output_suffix_target', None)

            description_prefix = entry.get('description_prefix', None)
            description_suffix = entry.get('description_suffix', None)
            description_suffix_target = entry.get('description_suffix_target', None)
            
            property_ = entry.get('property', None)
            data_type = entry.get('data_type', None)

            # Dynamic description -> Description은 1개 공통
            description_suffix_target_value = params.get(description_suffix_target, None)
            description_parts = [description_prefix]
            
            if description_suffix:
                if description_suffix_target_value:
                    description_parts.append(f"{description_suffix}{description_suffix_target_value}")
                else:
                    description_parts.append(description_suffix)

            if description_suffix_target_value:
                description_parts.append(description_suffix_target_value)
            updated_description = "_".join(description_parts)
            
            # Dynamic output_column_target value -> output column은 여러개일 수 있음
            output_suffix_target_value = params.get(output_suffix_target, None)
            
            # Target var 찾기
            output_target_values = self.handle_target_var(params, output_target)

            for output_target_value in output_target_values:
                output_column_target_value, ticker, ticker_type, parent_property = self.get_column_value(schema_json, output_target_value, property_)
                
                if (output_column_target_value is not None):
                    updated_output_column_name = "_".join(
                        filter(None,
                            [output_column_target_value, output_prefix, 
                                f"{output_suffix}{output_suffix_target_value}" 
                                if output_suffix or output_suffix_target_value else "",
                            ]
                        )
                    )
                    if updated_output_column_name not in existing_columns:
                        schema_json['columns'].append({
                        "name": updated_output_column_name,
                        "ticker": ticker or "",
                        "ticker_type": ticker_type or "",
                        "property": property_,
                        "parent_property": parent_property or "",
                        "description": updated_description,
                        "data_type": data_type,
                        "created_by": node_name,
                    })
        
        self.upload_file(schema_json)
        self.schema_json = schema_json.copy()
        return schema_json


    def add_dtype(self,df):
        if type(df.index) == pd.core.indexes.range.RangeIndex:
            pass
        else:
            df = df.reset_index()
        column_and_type = [(col, df[col].dtype) for col in df.columns]
        df.columns = pd.MultiIndex.from_tuples(column_and_type)
        return df
    
    def parse_json(self,json_string: str) -> dict:
        try:
            data_dict = json.loads(json_string)
            return data_dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {}
    
    def read_json(self, file_path):
        if not os.path.exists(file_path):
            self.handle_error(f"데이터 속성 파일 '{file_path}'이 존재하지 않습니다.")
        try:
            with open(file_path, 'r') as file:
                params = json.load(file)
                self.logger.info(f"데이터 속성 파일 '{file_path}'이 로드되었습니다.")
                return params
        except json.JSONDecodeError as e:
            self.handle_error(f"데이터 속성 파일 '{file_path}'을 파싱하는 동안 오류가 발생했습니다: {e}")
        except Exception as e:
            self.handle_error(f"데이터 속성 파일 '{file_path}'을 읽는 동안 예상치 못한 오류가 발생했습니다: {e}")
    
    def create_report_parameter(self, name, display_name, display_name_ko, value, value_type):
        result = {
            "parameter_name": name,
            "selected_value": value,
            "ui_display_name": display_name,
            "ui_display_name_ko": display_name_ko,
            "ui_help_text": "",
            "value_type": value_type
        }
        return result
    
    def generate_model_report(self, model=None, label_name=None, **dataset_info): # name, display_name, display_name_ko
        if self.model_info is None:
            self.model_info = []

        if model:
            existing_algorithm_info = self.get_existing_parameter(self.model_info, "algorithm_information", "algorithm_details")
            existing_algorithm_info[label_name] = model.get_params()
            
            for entry in self.model_info:
                if entry["category"] == "algorithm_information":
                    entry["parameters"][0]["selected_value"] = existing_algorithm_info
                    break
            else:
                self.model_info.append({
                    "category": "algorithm_information",
                    "parameters": [
                        self.create_report_parameter(
                            "algorithm_details",
                            "Algorithm Details",
                            "알고리즘 세부 정보",
                            existing_algorithm_info,
                            "value_map"
                        )
                    ]
                })
        
        if dataset_info:
            existing_training_info = self.get_existing_parameter(self.model_info, "training_information", "training_details")
            split_info_keys = {'train_size', 'random_state'}
            dataset_details = {
                key: (str(value.shape) if hasattr(value, 'shape') else str(value))
                for key, value in dataset_info.items()
                if key in split_info_keys and value is not None  # Skip missing data
            }
            
            if 'train_size' in dataset_info:
                dataset_details["policy"] = 'split'
                
            if "X_train" in dataset_info and hasattr(dataset_info["X_train"], "shape"):
                dataset_details["train_set_rows"] = str(dataset_info["X_train"].shape[0])
                dataset_details["columns"] = str(dataset_info["X_train"].shape[1])

            if "X_test" in dataset_info and hasattr(dataset_info["X_test"], "shape"):
                dataset_details["test_set_rows"] = str(dataset_info["X_test"].shape[0])
            
            if not existing_training_info:
                self.model_info.append({
                    "category": "training_information",
                    "parameters": [
                        self.create_report_parameter(
                            "training_details",
                            "Training Details",
                            "훈련 세부 정보",
                            dataset_details,
                            "value_map"
                        )
                    ]
                })
        return self.model_info
    
    def get_existing_parameter(self, info, category_name, param_name):
        for category in info:
            if category["category"] == category_name:
                for param in category["parameters"]:
                    if param["parameter_name"] == param_name:
                        return param.setdefault("selected_value", {})
        return {}
    
    def generate_evaluation_report(self, type=None, report=None, matrix=None, auc_score=None, mse=None, rmse=None, mae=None, r2=None, label_name=None): # 0.0.44
        """
        개별 레이블(label)별로 JSON을 생성하고 기존 JSON과 누적하여 저장하는 방식으로 수정
        """
        
        if self.performance_info is None:
            self.performance_info = []
        
        if type =='class':
            # 기존 데이터 가져오기 (없으면 초기화)
            accuracy_matrix = self.get_existing_parameter(self.performance_info, "confusion_matrix", "accuracy_matrix")
            confusion_matrix = self.get_existing_parameter(self.performance_info, "confusion_matrix", "confusion_matrix")
            accuracy_score = self.get_existing_parameter(self.performance_info, "confusion_matrix", "accuracy_score")
            auc_score_value = self.get_existing_parameter(self.performance_info, "roc_curve", "roc_curve_value")
            roc_chart = self.get_existing_parameter(self.performance_info, "roc_curve", "roc_curve_chart")
            
            # Accuracy Score
            accuracy_score[label_name] = {"accuracy_score": report['accuracy']}
            
            # Accuracy Matrix
            accuracy_matrix[label_name] = {
                "columns": [f'Predicted_{i}' for i in range(matrix.shape[1])],
                "rows": [
                    {"label": index_label, "values": [f"{val:.2f}" for val in matrix.iloc[idx].values]}
                    for idx, index_label in enumerate(matrix.index)
                ]
            }
            
            # Confusion Matrix
            confusion_matrix[label_name] = {
                "columns": ["Precision", "Recall", "F1-Score", "Support"],
                "rows": [
                    {
                        "label": f"Class_{cls}",
                        "values": [
                            f"{report[str(cls)]['precision']:.2f}",
                            f"{report[str(cls)]['recall']:.2f}",
                            f"{report[str(cls)]['f1-score']:.2f}",
                            f"{int(report[str(cls)]['support'])}"
                        ]
                    } for cls in report.keys() if cls not in ["accuracy", "macro avg", "weighted avg"]
                ]
            }

            # AUC Score
            auc_score_value[label_name] = {"auc_value": auc_score}
            s3_base_url = 'https://s3-ocean-ai-temp.s3.ap-northeast-2.amazonaws.com'
            roc_chart[label_name] = f"{s3_base_url}/{self.s3_path}{self.base_filename}_{label_name}_fig.png"
            
            # Confusion Matrix & Accuracy Matrix 업데이트 (중복 방지)
            for entry in self.performance_info:
                if entry["category"] == "confusion_matrix":
                    entry["parameters"][0]["selected_value"] = confusion_matrix
                    entry["parameters"][1]["selected_value"] = accuracy_matrix
                    break
            
            else:
                self.performance_info.append({
                    "category": "confusion_matrix",
                    "parameters": [
                        self.create_report_parameter('confusion_matrix', 'Confusion Matrix', '혼동 행렬', confusion_matrix, 'table'),
                        self.create_report_parameter('accuracy_matrix', 'Accuracy Matrix', '정확도 행렬', accuracy_matrix, 'table'),
                        self.create_report_parameter('accuracy_score', 'Accuracy', 'Accuracy', accuracy_score, 'value_map')
                    ]
                })
            
            # ROC Curve 업데이트 (중복 방지)
            for entry in self.performance_info:
                if entry["category"] == "roc_curve":
                    entry["parameters"][0]["selected_value"] = auc_score_value
                    break

            else:
                self.performance_info.append({
                    "category": "roc_curve",
                    "parameters": [
                        self.create_report_parameter('roc_curve_value', 'AUC Value', 'ROC AUC', auc_score_value, 'value_map'),
                        self.create_report_parameter('roc_curve_chart', 'ROC Curve', 'ROC Curve', roc_chart, 'image')
                    ]
                })
        
        if type == 'reg':
            mse_value = self.get_existing_parameter(self.performance_info, "regression_metrics", "mse")
            rmse_value = self.get_existing_parameter(self.performance_info, "regression_metrics", "rmse")
            mae_value = self.get_existing_parameter(self.performance_info, "regression_metrics", "mae")
            r2_value = self.get_existing_parameter(self.performance_info, "regression_metrics", "r2_score")

            # MSE, RMSE, MAE, R^2 Score 저장
            mse_value[label_name] = {"mse": round(mse, 4)}
            rmse_value[label_name] = {"rmse": round(rmse, 4)}
            mae_value[label_name] = {"mae": round(mae, 4)}
            r2_value[label_name] = {"r2_score": round(r2, 4)}

            # 회귀 평가 결과 업데이트 (중복 방지)
            for entry in self.performance_info:
                if entry["category"] == "regression_metrics":
                    entry["parameters"][0]["selected_value"] = mse_value
                    entry["parameters"][1]["selected_value"] = rmse_value
                    entry["parameters"][2]["selected_value"] = mae_value
                    entry["parameters"][3]["selected_value"] = r2_value
                    break
            else:
                self.performance_info.append({
                    "category": "regression_metrics",
                    "parameters": [
                        self.create_report_parameter('mse', 'MSE', '평균 제곱 오차', mse_value, 'value_map'),
                        self.create_report_parameter('rmse', 'RMSE', '제곱근 평균 제곱 오차', rmse_value, 'value_map'),
                        self.create_report_parameter('mae', 'MAE', '평균 절대 오차', mae_value, 'value_map'),
                        self.create_report_parameter('r2_score', 'R² Score', '결정 계수', r2_value, 'value_map')
                    ]
                })

        self.log_event('evaluation', status='completed')
        return self.performance_info
    

    def generate_report_json(self, INPUT=None):
        """
        최종적으로 누적된 성능 정보를 JSON에 반영
        """
        report_json = {
            "node_information": INPUT.get("node_info"),
            "node_results": [
                {
                    "area": "model_information",
                    "categories": self.model_info
                },
                {
                    "area": "performance",
                    "categories": self.performance_info  # 누적된 성능 정보 반영
                }
            ]
        }
        self.upload_file([report_json], 'report')
        return report_json
    

    def generate_report(self, INPUT=None, accuracy=None, report=None, matrix=None, auc_score=None, mse=None, rmse=None, mae=None, r2=None):
        pred_type = INPUT.get('pred_type', None)
        if pred_type != 'reg': # 로지스틱의 경우 pred_type이 없음
            # Classification Report Generation
            report_df = pd.DataFrame(report).transpose().reset_index().rename(columns={'index': 'Class'})
            class_labels = report_df['Class'][:len(matrix)].tolist()
            num_classes = matrix.shape[1]
            column_names = [f'Predicted {i}' for i in range(num_classes)]

            matrix_df = pd.DataFrame(matrix, columns=column_names)
            matrix_df['Class'] = class_labels
            matrix_df = matrix_df[['Class'] + column_names]

            combined_df = pd.merge(report_df, matrix_df, on='Class', how='left')

            metrics_df = pd.DataFrame({
                'Class': ['Accuracy', 'AUC Score'],
                'Score': [accuracy, auc_score],
                'precision': [None, None],
                'recall': [None, None],
                'f1-score': [None, None],
                'support': [None, None],
                'Predicted 0': [None, None],
                'Predicted 1': [None, None]
            })

            for col in column_names:
                metrics_df[col] = [None, None]

            final_df = pd.concat([metrics_df, combined_df], ignore_index=True)
            final_df = final_df.set_index('Class')

        else:
            # Regression Report Generation
            final_df = pd.DataFrame({
                'Metric': ['Mean Squared Error (MSE)', 'Root Mean Squared Error (RMSE)', 
                        'Mean Absolute Error (MAE)', 'R2 Score'],
                'Score': [mse, rmse, mae, r2]
            })

        final_df = final_df.fillna(' ')
        self.log_event('evaluation', status='completed')
        self.log_parameters(evaluation_report=final_df)
        return final_df
    
    def generate_report_pca(self, optimal_pc_count, eigen_val, eigen_vec, colnames):    
        n_dim = eigen_vec.shape[0]
        pc_result_title = pd.DataFrame([['Result summary ---'] + [''] * (n_dim - 1)])
        # result summary dataframe
        metric_name = ['Optimal PC Count']
        metric_value = [str(optimal_pc_count)]
        if len(metric_name) < n_dim:
            metric_name.extend([' '] * (n_dim - len(metric_name)))
            metric_value.extend([' '] * (n_dim - len(metric_value)))
        
        result_summary = pd.DataFrame({
            ' ': metric_name,
            ' ': metric_value
        })
        btw_line = pd.DataFrame([[' '] * n_dim])
        pcs = pd.DataFrame([f"pc_{i + 1}" for i in range(n_dim)])
        eigen_val_title = pd.DataFrame([['Eigenvalues ---'] + [''] * (n_dim - 1)])
        eigenvalue_df = pd.DataFrame([eigen_val])
        eigen_vec_title = pd.DataFrame([['Eigenvectors ---'] + [''] * (n_dim - 1)])
        eigenvector_df = pd.DataFrame(eigen_vec.T, index=colnames)

        report_df = pd.concat([pc_result_title, result_summary, 
                               btw_line, pcs, eigen_val_title, eigenvalue_df, 
                               btw_line, pcs, eigen_vec_title, eigenvector_df])
        return report_df
    
    def save_to_json(self, data, file_path):
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    def confusion_matrix(self,y, y_pred):
        classes = sorted(y.unique())
        matrix = confusion_matrix(y, y_pred, labels=classes)
        df = pd.DataFrame(matrix, columns=[f'Predicted {cls}' for cls in classes], index=[f'Actual {cls}' for cls in classes])
        return df
    
    def roc_curve(self, y, probabilities):
        classes = sorted(list(set(y)))
        n_classes = len(classes)
        plt.figure(figsize=(8, 6))
        
        if n_classes > 2:
            y_bin = label_binarize(y, classes=classes)
        
            for i, class_name in enumerate(classes):
                y_prob = probabilities[:, i]
                fpr, tpr, _ = roc_curve(y_bin[:, i], y_prob) # ROC 곡선 계산
                auc_score = auc(fpr, tpr) # AUC 값 계산
                plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'{class_name} (AUC = {auc_score:.2f})')
                
        else:  # Binary case
            y_prob = probabilities[:, 1]
            fpr, tpr, _ = roc_curve(y, y_prob)
            auc_score = auc(fpr, tpr)
            class_name = classes[1]
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'{class_name} (AUC = {auc_score:.2f})')
                
            plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title(f'ROC Curve for {y.name}')
            plt.legend(loc="lower right")

        fig = plt.gcf()
        plt.close()  
        return fig, auc_score
    
    def get_parameters(self, json_data): #0.0.37
        """
        JSON 데이터를 파싱하여 파라미터를 구성하는 함수.
        """
        parameters = {
            'model_par': {},
            's3_info':{},
            'node_info':{}
            }
        
        s3_storage = json_data['s3_storage']
        node_information = json_data['node_information']
        
        parameters['s3_info']['s3_repository'] = s3_storage.get('s3_repository', None)
        parameters['s3_info']['s3_write_path'] = s3_storage.get('s3_write_path', None)
        parameters['s3_info']['filename'] = node_information.get('user_defined_name', None)
        parameters['node_info'] = node_information
        
        for parameter in json_data.get('parameters', []):
            area = parameter['area']
            options = parameter.get('options')
            parameter_name = parameter['parameter_name']
            selected_value = parameter.get('selected_value')
            value_type = parameter.get('value_type')
                
            parameter_value = None
                     
            if options and area =='hyperparameter':
                if isinstance(options, list) and len(options) == 1:
                    options = options[0]
                
                if isinstance(selected_value, list) and len(selected_value) == 1:
                    selected_value = selected_value[0]
					
                # Match the selected value with options
                matching_option = next((opt for opt in options if opt.get('value') == selected_value), None)
                
                if matching_option:
                    if 'members' in matching_option:
                        parameter_value = {
                        'min': next((member['selected_value'] for member in matching_option['members'] if member['name'] == 'min'), None),
                        'max': next((member['selected_value'] for member in matching_option['members'] if member['name'] == 'max'), None),
                        'value': matching_option['value']
                    }
    
                if selected_value in ['values', 'range']:
                    if selected_value == 'values':
                        values_option = next((opt for opt in options if opt.get('value') == 'values'), None)
                        if values_option:
                            parameter_value  = [member['selected_value'] for member in values_option['members']]
                            if len(parameter_value) == 1:
                                parameter_value = parameter_value[0]
                                
                    elif selected_value == 'range':
                        range_option = next((opt for opt in options if opt.get('value') == 'range'), None)
                        if range_option:
                            range_members = range_option.get('members', [])
                            range_values = {member['name']: member['selected_value'] for member in range_members}
                            value_types = {member['name']: member['value_type'] for member in range_members}

                            min_val = range_values['min']
                            max_val = range_values['max']
                            count = range_values['count']
                            dist = range_values['dist']
                            
                            # Generate range values based on distribution type
                            if dist == 'uniform':
                                if value_types['min'] == 'integer' and value_types['max'] == 'integer':
                                    parameter_value = np.linspace(min_val, max_val, count).astype(int).tolist()
                                else:
                                    parameter_value = np.linspace(min_val, max_val, count).tolist()
                            elif dist == 'log_uniform':
                                parameter_value = np.logspace(np.log10(float(min_val)), np.log10(float(max_val)), count).tolist()
                    
                parameters[parameter_name] = selected_value

            elif value_type == "dict":
                if isinstance(selected_value, list) and all(isinstance(item, dict) for item in selected_value):
                    parameter_value = [
                        {'dep_var': item.get('dep_var'), 'indep_var': item.get('indep_var')}
                        for item in selected_value
                    ]
                else:
                    parameter_value = selected_value
            
            else:
                if isinstance(selected_value, list) and len(selected_value) == 1:
                    parameter_value = selected_value[0]
                else:
                    parameter_value = selected_value
					
            # Value 저장
            if area =='hyperparameter':
                parameters['model_par'][parameter_name] = parameter_value if parameter_value is not None else selected_value
            else:
                parameters[parameter_name] = selected_value

        return parameters


    def set_node_info(self, json_data): # 0.0.37
        self.s3_info = json_data['s3_storage']
        self.node_info = json_data['node_information']

        self.s3_path = self.s3_info['s3_write_path']
        self.bucket_name = self.s3_info['s3_repository']
        self.job_id = self.node_info.get('job_id', None)
        
        self.base_filename = self.node_info['user_defined_name']
        self.group_name = self.node_info.get('type', None)
        self.node_name = self.node_info.get('name', None)
        

    def validate_data(self, parsed_data): # 0.0.37
        self.set_node_info(parsed_data)
        # 매개변수 유효성(타입/값 형태) 검증
        try:
            self.validate_selected_value(parsed_data)
            self.logger.info("매개변수 유효성 검사가 완료되었습니다.")
        except ValueError as e:
            self.handle_error(f"매개변수 유효성 검사 실패: {str(e)}")

            
    def get_pred_type(self, json_data):
        for item in json_data['parameters']:
            if item.get('parameter_name') == 'pred_type':
                return item.get('selected_value')
        return None
    
    def is_dtype_match(self, column, allowed_types, df):
        if 'int' in allowed_types and pd.api.types.is_integer_dtype(df[column]):
            return True
        if 'float' in allowed_types and pd.api.types.is_float_dtype(df[column]):
            return True
        if 'string' in allowed_types and pd.api.types.is_string_dtype(df[column]):
            return True
        if 'datetime' in allowed_types and pd.api.types.is_datetime64_any_dtype(df[column]):
            return True
        return False
    
    def validate_selected_column(self, df, dtype_dict, parsed_data, variable):
        variables_param = None
        pred_type = self.get_pred_type(parsed_data)
        pred_type_display_map = {"reg": "회귀", "class_binary": "이진분류", 'class_multi': '다중분류'}

        for param in parsed_data['parameters']:
            if param.get('parameter_name') == 'variables':
                variables_param = param
                break
            
        for item in variables_param['members']:
            param_name = item['name']
            allowed_types = item.get('allowed_data_types', [])
            columns_to_check = variable[param_name]
            display_name = item.get('ui_display_name_ko', param_name)
            unique_value_constraints = [
                constraint for constraint in item.get('n_unique_value', [])
                if constraint.get('pred_type') == pred_type
            ]
            
            columns_to_check = columns_to_check if isinstance(columns_to_check, list) else [columns_to_check]
            
            for col_name in columns_to_check:
                # 컬럼 존재 여부 확인
                if col_name not in dtype_dict:
                    raise ValueError(f"데이터 프레임에 '{col_name}' 열이 존재하지 않습니다.")
                
                if not self.is_dtype_match(col_name, allowed_types, df):
                    raise ValueError(f"'{display_name}'의 '{col_name}'열의 데이터 유형이 허용된 유형({allowed_types})과 일치하지 않습니다.")
                    
                # pred_type의 unique_value 조건 조회
                unique_count = df[col_name].nunique()
                for constraint in unique_value_constraints:
                    min_val, max_val = constraint['min'], constraint['max']
                    pred_type_display = pred_type_display_map.get(pred_type, pred_type)
                    
                    if max_val == 'inf': # 회귀
                        if unique_count < min_val:
                            if pred_type_display:
                                raise ValueError(f"'{display_name}'의 '{col_name}'열의 고유값 개수({unique_count})가 '{pred_type_display}'에 대한 최소 허용값({min_val})을 벗어납니다.")
                            else:
                                raise ValueError(f"'{display_name}'의 '{col_name}'열의 고유값 개수({unique_count})가 최소 허용값({min_val})을 벗어납니다.")
                    else:
                        if not (min_val <= unique_count <= max_val):
                            if pred_type_display:
                                raise ValueError(f"'{display_name}'의 '{col_name}'열의 고유값 개수({unique_count})가 '{pred_type_display}'에 대한 허용 범위(최소값:{min_val}, 최대값:{max_val})를 벗어납니다.")
                            else:
                                raise ValueError(f"'{display_name}'의 '{col_name}'열의 고유값 개수({unique_count})가 허용 범위(최소값:{min_val}, 최대값:{max_val})를 벗어납니다.")


    def handle_type_error(self, ui_display_name, expected_type):
        self.handle_error(f"'{ui_display_name}'의 값이 {expected_type} 타입이 아닙니다. {expected_type}형 값을 입력해 주세요.")

    def handle_list_error(self, ui_display_name, element_type):
        self.handle_error(f"'{ui_display_name}'의 리스트 내 요소가 {element_type} 타입이 아닙니다. 모든 요소가 {element_type}형인지 확인해 주세요.")

    def validate_selected_value(self, parsed_data):
        type_mapping = {
            "float_array": (float, "실수"),
            "integer_array": (int, "정수"),
            "string_array": (str, "문자열"),
            }
        for data in parsed_data['parameters']:
            value_type = data.get("value_type")
            selected_value = data.get("selected_value")
            ui_display_name = data.get("ui_display_name_ko")
            value_range = data.get("value_range")
            
            if value_type == "float":
                if not isinstance(selected_value, float):
                    self.handle_type_error(ui_display_name, "실수")
            elif value_type == "integer":
                if not isinstance(selected_value, int):
                    self.handle_type_error(ui_display_name, "정수")
            elif value_type == "string":
                if not isinstance(selected_value, str):
                    self.handle_type_error(ui_display_name, "문자열")
            elif value_type in type_mapping:
                if not isinstance(selected_value, list):
                    self.handle_type_error(ui_display_name, "리스트")
                expected_type, element_type = type_mapping.get(value_type)
                
                if not all(isinstance(item, expected_type) for item in selected_value):
                    self.handle_list_error(ui_display_name, element_type)
        
            elif value_type == 'dict':
                if not isinstance(selected_value, list) or not all(isinstance(item, dict) for item in selected_value):
                    self.handle_type_error(ui_display_name, "딕셔너리 리스트")
                for item in selected_value:
                    if 'dep_var' not in item or 'indep_var' not in item:
                        self.handle_error(f"'{ui_display_name}' 항목에 '종속변수' 또는 '독립변수'가 누락되었습니다.")
            else:
                self.handle_error(f"'{ui_display_name}'의 데이터 타입('{value_type}')은 지원되지 않는 유형입니다. 올바른 유형인지 확인해 주세요.")

            # Range validation
            if value_range:
                min_value = value_range.get("min")
                max_value = value_range.get("max")
                if min_value is None or max_value is None:
                    self.handle_error(f"'{ui_display_name}'에 최소값 또는 최대값이 누락되었습니다.")
        
                if isinstance(selected_value, list):
                    if not all(min_value <= item <= max_value for item in selected_value):
                        self.handle_error(f"'{ui_display_name}'의 한 개 이상의 요소가 범위 [최소값:{min_value}, 최대값:{max_value}]를 벗어납니다.")

                else:
                    if not (min_value <= selected_value <= max_value):
                        self.handle_error(f"'{ui_display_name}'의 값이({selected_value}) 범위 [최소값:{min_value}, 최대값:{max_value}]을 벗어납니다.")

    
    def residual_diag_plot(self, fitted, residual):
        plt.figure(figsize=(8, 6))
       
        plt.scatter(fitted, residual)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Fitted Values (Predicted)')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
       
        fig = plt.gcf()
        plt.close()
        return fig
    
    def plot_explained_variance(self, exp_var, opt_pc_count):
        opt_pc_count = np.argmax(exp_var > 0.95) + 1
        
        plt.figure(figsize=(8, 5))
        plt.plot(np.arange(1, len(exp_var) + 1), exp_var, marker='o', linestyle='--', color='b')
        plt.title('Explained Variance Ratio by Principal Components')
        plt.xlabel('Number of Principal Components')
        plt.ylabel('Cumulative Explained Variance')
        plt.axhline(y=0.95, color='r', linestyle='-')
        plt.axvline(x=opt_pc_count, color='r', linestyle='-')
        plt.show()
        
        fig = plt.gcf()
        plt.close()
        return fig
    
    def get_date(self, df, input_param): # 0.0.42
        s_date = input_param['model_par'].get('start_date', None)
        e_date = input_param['model_par'].get('end_date', None)
        rebal_date = pd.DatetimeIndex(sorted(df.index.tolist()))
        # 시작점은 리밸런싱 시작점 -> 데이터 시작일 조회해서 벤치마크랑 맞춰야함
        if s_date in [None, '']:
            s_date = rebal_date[0].strftime('%Y%m%d')
            self.logger.info(f"시작일이 제공되지 않았습니다. 데이터 시작일로 기본 설정됩니다: {s_date}")
        else:
            df = df[(df.index >= s_date)]
            if df.empty:
                self.handle_error(f"입력한 시작일 ({s_date})이 데이터의 시작일({rebal_date[0].strftime('%Y-%m-%d')})보다 늦습니다.")
            rebal_date = pd.DatetimeIndex(sorted(df.index.tolist()))
            s_date = rebal_date[0].strftime('%Y%m%d')
            
        if e_date in [None, '']:
            e_date = rebal_date[-1].strftime('%Y%m%d')
            self.logger.info(f"종료일이 제공되지 않았습니다. 데이터의 마지막 날짜로 기본 설정됩니다: {e_date}")
        else:
            e_date = datetime.strptime(e_date, '%Y-%m-%d')
            e_date = e_date.strftime('%Y%m%d')
        return df, s_date, e_date
    
    def get_close_data(self, s_date, e_date, target_period, target_var):
        period_value = int(target_period[:-1])
        period_type = target_period[-1].upper()
        
        if period_type == 'M': # '기간_값'을 기준으로 '최소_일'을 계산
            min_days =  (30 * period_value) + 21
        elif period_type == 'Y':
            min_days =  (30 * 12 * period_value) + 21
        
        extended_s_date = pd.to_datetime(s_date) - pd.Timedelta(days=min_days)
        
        if isinstance (target_var, dict):
            ticker_list = [value['ticker'] for value in target_var.values()]
        elif isinstance(target_var, str):
            ticker_list = [target_var]
            
        dfs = []
        for ticker in ticker_list:
            close_data = self.kyobo_dao.get_data(ticker, extended_s_date, e_date)
            duplicates = close_data[close_data.duplicated(subset=['ymd', 'ticker'], keep=False)]
            close_data = close_data.drop_duplicates(subset=['ymd', 'ticker'])
            close_data.fillna(method='ffill', inplace=True)
            dfs.append(close_data)
            
        close_data = pd.concat(dfs, axis=0)
        close_data = close_data.pivot(index='ymd', columns='ticker', values='value')
        close_data.index = pd.to_datetime(close_data.index)
        
        all_days = pd.date_range(start=extended_s_date, end=e_date, freq='D') # 캘린더데이
        close_data = close_data.reindex(all_days)
        
        close_data = close_data.applymap(lambda x: None if pd.isna(x) or x is None else x)
        close_data = close_data.fillna(method='ffill')
        close_data.dropna(inplace=True)
        close_data = close_data.loc[s_date:e_date]
        return close_data