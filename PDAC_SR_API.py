import os
import io
import pandas as pd
import streamlit as st
import openai

# OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    st.error('Please set the OPENAI_API_KEY environment variable.')
else:
    openai.api_key = openai_api_key


# prompt
prompt_template = """
Study ID: {study_id}
Free Text Report: {free_text_report}

## insert your own prompt instruction ##

{retry_reason}
"""

def create_prompt(study_id, free_text_report, retry_reason=""):
    return prompt_template.format(
        free_text_report=free_text_report,
        study_id=study_id,
        retry_reason=retry_reason
    )

def get_structured_report(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful radiology report assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=1500,
            frequency_penalty=0
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        st.error(f"API request failed: {e}")
        return None
    
def extract_csv_data(structured_report):
    csv_output_start = structured_report.find('CSV Output:')
    if csv_output_start != -1:
        csv_output = structured_report[csv_output_start:].split('\n', 1)[1].strip()
        csv_data = csv_output.split('\n')[0]
        return csv_data
    else:
        return None

# Streamlit interface
st.title("PDAC Structured Report Generator")

# Start button
if st.button("Start Processing"):
    # read a input excel file
    try:
        df = pd.read_excel('input.xlsx')
        st.write("Excel file 'input.xlsx' loaded successfully.")

        results = []

        for index, row in df.iterrows():
            st.header(f"Study {index + 1}")
            study_id = row['study_id']
            free_text_report = row['free_text_report']

            st.write(f"Generating structured report for study {study_id}")

            prompt = create_prompt(study_id, free_text_report)
            structured_report = get_structured_report(prompt)
            csv_data = extract_csv_data(structured_report)

            retry_count = 0
            max_retries = 3
            while csv_data and len(csv_data.split(',')) != 17 and retry_count < max_retries:
                st.write(f"Retrying for patient {study_id} due to incorrect format...")
                retry_reason = "The previous attempt failed to produce all subsections. The output must include study_id, all subsections, and resectability status (a total of 17 items)."
                prompt = create_prompt(study_id, free_text_report, retry_reason)
                structured_report = get_structured_report(prompt)
                csv_data = extract_csv_data(structured_report)
                st.write("csv data:", csv_data)
                retry_count += 1

            if csv_data and len(csv_data.split(',')) == 17:
                results.append(csv_data)
                st.success(f"Structured report for study {study_id} generated successfully!")             
                st.text_area(f"Structured Report for Study {study_id}", value=structured_report, height=1500)
            else:
                st.error(f"Failed to generate a valid structured report for patient {study_id} after {retry_count} retries.")

        results_split = [x.split(',') for x in results]

        if results_split:
            results_df = pd.DataFrame(results_split, columns=[
                "Study_ID", "1-1. Appearance", "1-2. Size", "1-3. Location", "1-4. Pancreatic duct", 
                "1-5. Biliary tree", "2-1. SMA Contact", "2-2. Celiac Axis Contact", "2-3. CHA Contact", 
                "3-1. MPV Contact", "3-2. SMV Contact", "4-1. Liver lesions", 
                "4-2. Peritoneal or omental nodules", "4-3. Ascites", "4-4. Suspicious lymph nodes", 
                "4-5. Other extrapancreatic disease", "5-1. Resectability"
            ])

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                results_df.to_excel(writer, index=False, sheet_name='Sheet1')
            excel_data = output.getvalue()

            # download button
            st.download_button(
                label="Download Excel sheet",
                data=excel_data,
                file_name='output.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    except Exception as e:
        st.error(f"Failed to read Excel file 'input.xlsx': {e}")

# fail to access API key
if not openai_api_key:
    st.warning('Please set the OPENAI_API_KEY environment variable in your system.')
