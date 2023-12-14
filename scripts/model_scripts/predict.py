import joblib
import pandas as pd
import os
import yaml
import pickle

import scripts.data_scripts.create_features as cf
from scripts.data_scripts.data_prepare import prepare_dataset
from scripts.data_scripts.fill_na import fill_na_in_dataset
from scripts.data_scripts.fix_errors import fix_errors_in_dataset
import scripts.data_scripts.feature_prepare as fp


def predict(client):
    """
    Предсказание ообрения банками данного клиента
    :param client: данные в клиента
    """

    # %% Задание каталогов
    project_path = os.getcwd()
    model_dir = os.path.join(project_path, "models")

    # Загрузка параметров расчета
    params = yaml.safe_load(open(os.path.join(project_path, "params.yaml")))
    train_method = params["general"]["train_method"]
    num_columns = ['Ежемесячный_доход', 'Ежемесячный_расход', 'Сумма_заказа', 'Кредитная_нагрузка']

    client_df = convert_data_format(client)
    client_df = fill_na_in_dataset(client_df)
    client_df = prepare_dataset(client_df)
    client_df = fix_errors_in_dataset(client_df)
    client_df = cf.replace_features(client_df)

    bank_ids=['A', 'B', 'C', 'D', 'E']
    preds=[]
    for bank_id in bank_ids:
        scaler_filename = f'scaler_{bank_id}.pkl'
        scaler_full_filename = os.path.join(model_dir, scaler_filename)
        standard_scaler = joblib.load(scaler_full_filename)

        filename_model = os.path.join(model_dir, 'models', f'model_{train_method}_{bank_id}.pkl')
        df = fp.feature_prepare_for_bank (client_df, bank_id,standard_scaler, num_columns)

        with open(filename_model, "rb") as fd:
            clf = pickle.load(fd)
            pred = clf.predict(client_df)
            preds.append(pred)

    predictions = {
        'BankA_decision': 1,
        'BankB_decision': 1,
        'BankC_decision': 1,
        'BankD_decision': 1,
        'BankE_decision': 1,
    }

    return preds


def convert_data_format(raw_data):
    """
    Конвертация данных из формата для API-контракта во внутренний формат
    :param raw_data: данные в исходном формате
    """
    data = {
        "SkillFactory_Id": raw_data.skillfactory_id,
        "BirthDate": raw_data.birth_date,
        "education": raw_data.education,
        "employment status": raw_data.employment_status,
        "Value": raw_data.value,
        "JobStartDate": raw_data.job_start_date,
        "Position": raw_data.position,
        "MonthProfit": raw_data.month_profit,
        "MonthExpense": raw_data.month_expense,
        "Gender": raw_data.gender,
        "Family status": raw_data.family_status,
        "ChildCount": raw_data.child_count,
        "SNILS": raw_data.snils,
        "Loan_amount": raw_data.loan_amount,
        "Loan_term": raw_data.loan_term,
        "Goods_category": raw_data.goods_category,
        "Merch_code": raw_data.merch_code
    }

    return pd.DataFrame(data=data, index=[0])
