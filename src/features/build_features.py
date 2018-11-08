'''
Transformations, feature engineering and extraction
'''

import pandas as pd
import numpy as np

# join student registration to student info
def _join_reg(df1, df2):
    '''
    Joins the student registrations table to the student info (master)table on three columns: code_module, code_presentation, id_student. Records without a value for 'date unregistration' are set to zero
    '''
    return pd.merge(df1, df2, how='outer', on=['code_module', 'code_presentation', 'id_student']).fillna(value = 0)

# join vle to student vle
# join vle to student info
def _join_vle(df1, df2):
    '''
    input {vle, studentvle dataframes}
    output {joined dataframe}
    '''
    return pd.merge(st_vle_df, vle_df, how='outer', on = ['code_module', 'code_presentation', 'id_site'])

# create features from vle


# join assessments to student assessments
def _join_asssessments(df1, df2):
    '''
    Joins the assessments table to the student assessment table on id_assessment; drop rows with null values (about 1.5%); relabel 'date' as 'due_date'.
    '''
    df3 = pd.merge(df1, df2, how='outer', on=['id_assessment']).dropna()
    df3['id_student'] = df3['id_student'].astype('int64')
    df3['days_submitted_early'] = df3['date'] - df3['date_submitted']
    return df3

# create features from assessments
# average score and days submitted early per student/module/presentation
def _averages_from_assessments(df):
    '''
    Returns per student/module/presentation averages of assessment score, days submitted early, and estimated final score

    Parameters:
    ----------
    input {dataframes}: studentAssessment, assessment
    output {dataframe}: df['avg_score', 'avg_days_submitted_early', 'est_final_score']
    '''
    # add weighted score for each assessment
    df['weighted_score'] = df['score'] * df['weight'] / 100

    # caluculate mean scores, days submitted early
    av_df = df.groupby(by=['id_student', 'code_module', 'code_presentation']).mean()[['score', 'days_submitted_early']]

    # calculate estimated final score
    f_df = df.groupby(by=['id_student', 'code_module', 'code_presentation']).sum()[['weighted_score']]

    # merge and rename columns
    merged = pd.merge(av_df, f_df, how='outer', on = ['code_module', 'code_presentation', 'id_student'])

    merged.rename({'score':'avg_score', 'days_submitted_early':  'avg_days_sub_early', 'weighted_score': 'est_final_score'}, axis = 'columns', inplace=True)

    return merged
    
# drop null values (about 3.5% of rows)
def drop_nulls(dataframe):
    '''
    Drops rows with null values from dataframe
    '''
    return dataframe.dropna(axis = 0)

# make dummmies
def one_hot(dataframe, columns):
    '''
    Concatenates dummy variable (one-hot encoded) columns onto original dataframe for specified columns. Original columns are dropped.

    Parameters:
    ----------
    input {dataframe, list}: original dataframe, list of columns to be one-hot encoded and dropped
    output {dataframe}: resulting modified dataframe
    '''
    dumms = pd.get_dummies(dataframe[columns], dummy_na=True, drop_first=True)
    full_df = pd.concat([dataframe, dumms], axis = 1)
    return full_df.drop(columns, axis = 1)


# encode some columns as string? student_id?


# encode target: pass/fail
# three potential targets: pass/fail, type of result, final score
def _encode_target(dataframe):
    '''
    Encodes target column 'final_result' into two categories from four.
    Retains original target column
    '''
    dataframe['module_not_completed'] = (dataframe['final_result'] == 'Fail') | (dataframe['final_result'] == 'Withdrawn')
    return dataframe


if __name__ == "__main__":

    _cols_to_onehot = ['code_module', 'code_presentation', 'gender',    'region', 'highest_education', 'imd_band', 'age_band', 'disability']


    # import the dataframes
    main_df = pd.read_csv('../data/raw/studentInfo.csv')
    reg_df = pd.read_csv('../data/raw/studentRegistration.csv')
    st_asmt_df = pd.read_csv('../data/raw/studentAssessment.csv')
    asmt_df = pd.read_csv('../data/raw/assessments.csv')
    st_vle_df = pd.read_csv('../data/raw/studentVle.csv')
    vle_df = pd.read_csv('../data/raw/vle.csv')

    # perfom transformations / feature engineering


    # join dataframes to main_df
    
    pd.merge(main_df, reg_df, how='outer', on=['code_module', 'code_presentation', 'id_student']).fillna(value = 0)    
    
    pd.merge(main_df, f_df, how='outer', on = ['code_module', 'code_presentation', 'id_student'])

    pd.merge(std_asmt_df, asmt_df, how='outer', on='id_assessment')