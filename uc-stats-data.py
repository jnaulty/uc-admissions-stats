
# coding: utf-8

# # Fort Bragg Admissions to UC Stats
# 
# By: John Naulty Jr
# 
# Date: March 27, 2018
# 
# Data from [UC Admissions Infocenter](https://www.universityofcalifornia.edu/infocenter/admissions-source-school)
# 

# In[1]:


import pandas as pd

# Downloaded from: https://www.universityofcalifornia.edu/infocenter/admissions-source-school
FALL_FRESH_BY_HIGH_SCHOOL="HS_by_Year_data_fort_bragg_ca.csv"
HS_YEAR_PD = pd.read_csv(FALL_FRESH_BY_HIGH_SCHOOL)



# useful constants
fall_term='Fall Term'
measure_values='Measure Values'
measure_names = 'Measure Names'
university_wide = 'Universitywide'
app_values='app_values'
adm_values='adm_values'

# nice-to-have filters
#TODO: filter_factory...please
in_uc = HS_YEAR_PD['Campus'] == university_wide
in_berkeley = HS_YEAR_PD['Campus'] == 'Berkeley' 

app = HS_YEAR_PD['Measure Names'] == 'app'
adm = HS_YEAR_PD['Measure Names'] == 'adm'
All = HS_YEAR_PD['Uad Uc Ethn 6 Cat'] == "All"


# all applicants + adm
uc_all = HS_YEAR_PD[in_uc & All]
berkeley_all = HS_YEAR_PD[in_berkeley & All]




# In[99]:


def hs_gpa_stats(fr_gpa_by_inst_data_city_csv_file):
    # hs_gpa_stats
    # get university wide
    col_measure_value = 'Measure Values'
    col_fall_term = 'Fall Term'
    col_measure_names = 'Measure Names'
    
    df = pd.read_csv(fr_gpa_by_inst_data_city_csv_file)
    def _filter(_df):
        '''
        little helper to just filter
        since I'm too lazy to go and
        read the pandas docs..bambou
        '''
        #TODO: should take filters as input
        filter_app = _df['Measure Names'] == 'App GPA'
        filter_adm = _df['Measure Names'] == 'Adm GPA'
        #active_filter_univ_wide =  df['Campus'] = university_wide # beware, = is not == in python $(but in bash it is)
        filter_univ_wide = _df['Campus'] == university_wide
        
        #_df = _df[[col_fall_term, col_measure_names, col_measure_value, 'Campus' ]]
        
        num_cols = 8
        _df = _df.dropna(thresh=num_cols)
        
        
        _df = _df[filter_univ_wide]
        
        return _df
    
    #df = df[[col_fall_term, col_measure_names, col_measure_value ]]
    df = _filter(df)
    return df

fresh_gpa_fb_csv = "FR_GPA_by_Inst_data_fort_bragg.csv"
stats = hs_gpa_stats(fresh_gpa_fb_csv)
stats[:3]

#TODO get high-low value across each year's AdmGPA e.g  for 2017(4.09, 3.85)


# In[3]:





def ultimate_sort(df):
    # used by fall freshman from high school stats...poorly named
    df = df[[fall_term, measure_values, measure_names]]
    df = df.dropna(thresh=3)
    df = df.sort_values(by=fall_term)
    
    adm_df = df[measure_names] == 'adm'
    app_df = df[measure_names] == 'app'
    
    app_measure = df[app_df][[fall_term, measure_values]]
    app_measure.rename(columns={measure_values: app_values}, inplace=True)

    adm_measure = df[adm_df][[fall_term, measure_values]]
    adm_measure.rename(columns={measure_values: adm_values}, inplace=True)

    split_measures = pd.merge_ordered(app_measure, adm_measure, on=fall_term)
    return split_measures


# In[4]:


# berkeley admitted v applied (missing data in 2008 for some reason)
berkeley_app_adm_plot=ultimate_sort(berkeley_all)
#berkeley_app_adm_plot.plot(x=fall_term, kind='bar')


# In[5]:


# all uc applied v admitted
uc_app_adm_plot=ultimate_sort(uc_all)
uc_app_adm_plot.plot.bar(x=fall_term)


# In[6]:


# percent admitted per year
print(adm_values)
uc_app_adm_plot['perc_adm'] = (uc_app_adm_plot[adm_values] / uc_app_adm_plot[app_values]) * 100
uc_app_adm_plot[[fall_term, 'perc_adm']].plot.bar(x=fall_term)


# In[7]:


admitted_percent_great_80 = uc_app_adm_plot[uc_app_adm_plot['perc_adm'] > 80]
admitted_percent_less_70 = uc_app_adm_plot[uc_app_adm_plot['perc_adm'] < 70]


# In[8]:


# Fort Bragg percent admitted greater than 80%
admitted_percent_great_80


# In[9]:


# Fort Bragg percent admitted less than 70%
admitted_percent_less_70

