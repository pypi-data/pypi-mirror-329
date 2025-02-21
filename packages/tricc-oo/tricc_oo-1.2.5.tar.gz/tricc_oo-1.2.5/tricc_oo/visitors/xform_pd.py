# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 11:21:39 2022

@author: kluera

Make subforms that allow to be releoaded seperately as a 'task' in CHT, 
allowing to simulate a pause functionality. 
"""

import pandas as pd
import json


def chf_clean_name(s, remove_dots=False):
    # Check if there is a dot in the string
    if "." in s:
        # Split the string into parts based on the dot
        s_p = s.split(".")
        # Return the formatted string
        if remove_dots:
          return "_".join(s_p)
        else:
          return f'["{".".join(s_p)}"]'
    else:
        # If no dot is present, return None or handle it as needed
        return s

# df is the dataframe to be split
# pausepoint is the index of the row after which the form should pause
def make_breakpoints(df, pausepoint, calculate_name=None):
    """
    Creates a dataframe for a follow-up questionnaire while preserving previous inputs.
    
    Args:
        df: Input dataframe containing the questionnaire
        pausepoint: Point where the questionnaire should pause
        calculate_name: Optional name for calculation fields
    """
    
    # Get data points collected before break
    if 'input end' not in df['name'].values:
        raise ValueError("input end field not found in input dataframe")
    end_inputs_loc = df.index[df['name'] == 'input end'][0]
    next_begin_group_loc = min([i for i in df.index[df['type'] == 'begin group'] if i > end_inputs_loc])
        
    df_input = df.loc[next_begin_group_loc:pausepoint]
    
    # Define field types to handle
    typesconvert = ['integer', 'decimal', 'select_', 'text']
    typeskeep = ['hidden', 'calculate', 'string'] 
    
    # Create masks for filtering
    type_mask = df_input['type'].str.contains('|'.join(typeskeep + typesconvert))
    optin_mask = ~df_input['name'].str.contains('more_info_optin', na=False)
    
    # Filter dataframe keeping important fields
    df_input = df_input.loc[type_mask & optin_mask]
    
    # Preserve existing hidden fields and their calculations
    existing_hidden = df_input[df_input['type'] == 'hidden'].copy()
    
    # Convert specified types to hidden while preserving their data
    mask_indices = df_input.index[df_input['type'].str.contains('|'.join(typesconvert))]
    df_input.loc[mask_indices, 'type'] = 'hidden'
    df_input.loc[mask_indices, 'calculation'] = 'hidden'    

    # Handle label columns while preserving existing labels where needed
    label_cols = [col for col in df.columns if 'label' in col]
    df_input.loc[mask_indices, label_cols] = 'NO_LABEL'
    
    # Clear non-essential columns while preserving crucial data
    essential_cols = ['name', 'type', 'calculation'] + label_cols
    other_cols = df_input.columns.drop(essential_cols)
    df_input[other_cols] = ''
    
    # Preserve calculations for existing hidden fields
    df_input.update(existing_hidden[['calculation']])
    
    # Handle indexing and grouping
    df_input.index = df_input.index.map(str)
    hidden_ids = df_input.loc[df_input['type']=='hidden'].index
    inputs_group_index = '0'
    new_hidden_ids = inputs_group_index + '.' + hidden_ids
    
    # Update indices
    index_map = dict(zip(hidden_ids, new_hidden_ids))
    df_input.rename(index=index_map, inplace=True)
    df_input.sort_index(inplace=True)
    df_input.reset_index(drop=True, inplace=True)
    

    # Get hidden field names
    hidden_names = list(df_input.loc[df_input['type']=='hidden', 'name'])
    
    
# put all together
    if 'data_load' not in df['name'].values:
        raise ValueError("data_load field not found in input dataframe")
    data_load_loc = df.index[df['name'] == 'data_load'][0]
    
    # Split the dataframe into three parts
    df_before_data_load = df.loc[:data_load_loc]  # Everything up to data_load
    df_until_begin_group = df.loc[data_load_loc+1:next_begin_group_loc-1]  # From data_load to next begin_group
    
    # Reset indices for proper concatenation
    df_input = df_input.reset_index(drop=True)
    df_before_data_load = df_before_data_load.reset_index(drop=True)
    df_until_begin_group = df_until_begin_group.reset_index(drop=True)
    
    # Concatenate in the correct order
    df_combined = pd.concat([
        df_before_data_load,  # First part until data_load
        df_input,            # Injected converted fields
        df_until_begin_group # Remaining part until next begin_group
    ]).reset_index(drop=True)
    
    # Handle post-break section
    df_after = df.loc[pausepoint+1:].reset_index(drop=True)
    if df_after.iloc[0,0] == 'end group':
        df_after = df_after.iloc[1:]
    
    # Final concatenation
    final_df = pd.concat([df_combined, df_after])
    if calculate_name:
        final_df.loc[final_df['name']=='hidden','calculation']='0'
    
    final_df.fillna('', inplace=True)
    final_df.reset_index(inplace=True, drop=True)
    
    return final_df, hidden_names



def get_tasksstrings(hidden_names, df_survey):
    '''This function makes a list of strings of hidden fields that will be loaded into a form that continues the consultation. 
    This is very handy as this string must be pasted into the tasks.js file in CHT. 
    @hidden_names: are the names of the 'hidden' fields in the input group of the follow up form
    @df_survey: is the survey tab of the complete (original) form without breaks, going from A to Z
    @tasks_strings: is the string that has to be pasted into tasks.js'''
    
    task_string_template = "content['{variableName}'] = getField(report, '{full_path}')"
    task_strings = {}
    for s in hidden_names:
        df_above_s = df_survey.iloc[:df_survey.loc[df_survey['name']==s].index[0]]
        df_above_s_groups = df_above_s.loc[df_above_s['type'].isin(['begin group', 'end group'])]
        above_s_grouprows = df_above_s_groups.index
        fullpath = []
        for i in above_s_grouprows:
            if df_above_s.iloc[i]['type']=='begin group':
                fullpath.append(df_above_s.iloc[i]['name'])
            else: 
                fullpath = fullpath[:-1]
        if len(fullpath)>0:
            line = task_string_template.format(
                variableName=s, full_path='.'.join(fullpath) + chf_clean_name(s)
            )
        else:
            line = task_string_template.format(
                variableName=s, full_path=chf_clean_name(s)
            )
        task_strings[s]=line
    return  list(task_strings.values())



def get_task_js(form_id, calculate_name, title, form_types, hidden_names, df_survey, task_title="'id: '+getField(report, 'g_registration.p_id')+'; age: '+getField(report, 'p_age')+getField(report, 'g_registration.p_gender')+' months; '+getField(report, 'p_weight') + 'kg; ' + getField(report, 'g_fever.p_temp')+'°'"):
    lines = get_tasksstrings(hidden_names, df_survey)
    indented_lines = '\n          '.join(lines)
    
    return f"""
    
const extras = require('./nools-extras');

const {{ addDays, getField}} = extras;

var task_title = "{task_title}"

module.exports = [
  {{
    name: '{form_id}_{calculate_name}',
    icon: 'icon-followup-general',
    title: '{title}',
    appliesTo: 'reports',
    appliesToType: ['{"','".join(form_types)}'],
    contactLabel: (contact, report) =>
      task_title,
    appliesIf: function (contact, report) {{
      return getField(report, 'source_id') === '' && getField(report, '{chf_clean_name(calculate_name)}') === '1';
   }},
    actions: [
      {{
        type: 'report',
        form: '{form_id}',
        modifyContent: function (content, contact, report) {{
          {indented_lines}
       }},
     }},
    ],
    events: [
      {{
        id:  '{form_id}_{calculate_name}',
        days: 1,
        start: 1,
        end: 0,
     }},
    ],
    resolvedIf: function (contact, report, event, dueDate) {{
      const startTime = Math.max(addDays(dueDate, -event.start).getTime(), report.reported_date);
      const endTime = addDays(dueDate, event.end + 1).getTime();
      const forms = ['reverse_alm_label_form_pause'];
      const matchingReports = contact.reports
        .filter((c_report) => forms.includes(c_report.form))
        .filter((c_report) => c_report.reported_date >= startTime && c_report.reported_date <= endTime)
        .filter((c_report) => getField(c_report, 'source_id') === report._id);
      return matchingReports.length > 0;
   }},
 }},
];
"""
