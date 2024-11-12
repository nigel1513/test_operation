import streamlit as st
import plotly.express as px
import pandas as pd


# Set page config
st.set_page_config(page_title="부도율 예측 알고리즘")


# 함수 정의
@st.cache_data
def load_data(file):
    if file is not None:
        df = pd.read_csv(file)  # Assuming it's a CSV file
        return df
    else:
        pass  # Return an empty DataFrame if no file is provided

# 

def space():
    st.write("")

st.header("시각화")


# 1. 파일 업로드
uploaded_file = st.file_uploader("")

# Load data if a file is uploaded
if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success("파일 업로드 완료")
    space()  
    space()
    space()  
    space() 
    space()  




    # 정상기업 & 부도기업 카운트
    taget_value_counts = df['overdue_yn'].value_counts().reset_index()    
    taget_value_counts["기업형태"] = taget_value_counts["overdue_yn"].map({0: "정상기업", 1: "부도기업"})
    taget_value_counts_fig = px.bar(
        taget_value_counts,
        x="기업형태",
        y="count",
        color="기업형태",
        height=400
    )
    taget_value_counts_fig.update_layout(
        title="1. 정상기업 vs 부도기업 현황",
        xaxis_title="기업형태",
        yaxis_title="Count",
        legend_title="기업형태"
    )
    st.plotly_chart(taget_value_counts_fig)

    space() 
    space()  

 

    # 정상기업 & 부도기업 업력별 카운트
    overdue_yn_chmt_dcd_counts = df[['overdue_yn', 'cmht_dcd']].value_counts().reset_index()
    overdue_yn_chmt_dcd_counts.columns = ['overdue_yn', 'cmht_dcd', 'count']
    total_counts = overdue_yn_chmt_dcd_counts.groupby('overdue_yn')['count'].transform('sum')
    overdue_yn_chmt_dcd_counts['proportion'] = overdue_yn_chmt_dcd_counts['count'] / total_counts
    overdue_yn_chmt_dcd_counts['기업형태'] = overdue_yn_chmt_dcd_counts['overdue_yn'].map({0: '정상기업', 1: '부도기업'})
    overdue_yn_chmt_dcd_counts_fig = px.bar(
        overdue_yn_chmt_dcd_counts,
        x='cmht_dcd',
        y='proportion',
        color='기업형태',
        labels={'proportion': 'Proportion', 'cmht_dcd': 'CMHT DCD'},
        barmode='group',
        height=400
    )
    overdue_yn_chmt_dcd_counts_fig.update_layout(
        title="2. 정상기업 & 부도기업 업력별 부도현황 비율",
        xaxis_title="CMHT_DCD",
        yaxis_title="Proportion",
        legend_title="기업형태",
    )
    overdue_yn_chmt_dcd_counts_fig.update_xaxes(type='category', tickvals=list(range(10)))
    st.plotly_chart(overdue_yn_chmt_dcd_counts_fig)

    space() 
    space()  

    overdue_yn_tpbs_clsf_dcd_counts = df[['overdue_yn', 'tpbs_clsf_dcd']].value_counts().reset_index()
    overdue_yn_tpbs_clsf_dcd_counts.columns = ['overdue_yn', 'tpbs_clsf_dcd', 'count']
    total_counts = overdue_yn_tpbs_clsf_dcd_counts.groupby('overdue_yn')['count'].transform('sum')
    overdue_yn_tpbs_clsf_dcd_counts['proportion'] = overdue_yn_tpbs_clsf_dcd_counts['count'] / total_counts
    overdue_yn_tpbs_clsf_dcd_counts['기업형태'] = overdue_yn_tpbs_clsf_dcd_counts['overdue_yn'].map({0: '정상기업', 1: '부도기업'})
    overdue_yn_tpbs_clsf_dcd_counts_fig = px.bar(
        overdue_yn_tpbs_clsf_dcd_counts,
        x='tpbs_clsf_dcd',
        y='proportion',
        color='기업형태',
        labels={'proportion': 'Proportion', 'tpbs_clsf_dcd': 'tpbs_clsf_dcd'},
        barmode='group',
        height=400
    )
    overdue_yn_tpbs_clsf_dcd_counts_fig.update_layout(
        title="3. 정상기업 vs 부도기업 산업별 부도현황 비율",
        xaxis_title="tpbs_clsf_dcd",
        yaxis_title="Proportion",
        legend_title="기업형태",
    )
    st.plotly_chart(overdue_yn_tpbs_clsf_dcd_counts_fig)

    space() 
    space() 

    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Violin Plot with density normalization
    overdue_yn_op_fig = px.violin(
        df,
        x='기업형태',
        y='avg_daily_operation_med',
        box=True,
        points="all",
        labels={'avg_daily_operation_med': 'Avg Daily Operation (Med)', 'status': 'Status'},
        title="4-1. 정상기업 & 부도기업 가동률 현황",
        height=400,  # Normalize by percentage to account for imbalance
    )
    st.plotly_chart(overdue_yn_op_fig)

    space() 
    space() 

    # Violin Plot with tpbs_clsf_dcd as color
    industry_op_fig_violin = px.violin(
        df,
        x='기업형태',
        y='avg_daily_operation_med',
        color='tpbs_clsf_dcd',  # Add tpbs_clsf_dcd as color
        box=True,
        points="all",
        labels={'avg_daily_operation_med_mean_tpbs_clsf_dcd': 'Avg industry Daily Operation (Med)', 'status': 'Status'},
        title="4-2. 정상기업 vs 부도기업 산업별 가동률 현황",
        height=400,
    )
    # Set all traces to legend-only (initially hidden)
    industry_op_fig_violin.for_each_trace(lambda trace: trace.update(visible="legendonly"))

    # Manually set a specific tpbs_clsf_dcd value to be visible (e.g., "A")
    for trace in industry_op_fig_violin.data:
        if trace.name == df['tpbs_clsf_dcd'].unique()[0]:  
            trace.visible = True
    st.plotly_chart(industry_op_fig_violin)

    space() 
    space() 

    op_fig_hist = px.histogram(
    df,
    x='avg_daily_operation_med',
    color='기업형태',
    histnorm='percent',
    labels={'avg_daily_operation_med': 'Avg Daily Operation (Med)', 'status': 'Status'},
    title="4-3. 정상기업 vs 부도기업 가동률 히스토그램",
    barmode='overlay',
    height=400,
    color_discrete_map={'정상기업': 'steelblue', '부도기업': 'coral'} 
    )
    st.plotly_chart(op_fig_hist)
    
    space() 
    space() 


    # Histogram with tpbs_clsf_dcd as color
    # Create a combined column for color mapping
    df['industry_tpbs'] = df['기업형태'] + " - " + df['tpbs_clsf_dcd']
    sorted_industry_tpbs = sorted(df['industry_tpbs'].unique())


    # Histogram with 기업형태_tpbs as color
    industry_op_fig_hist = px.histogram(
        df,
        x='avg_daily_operation_med',
        color='industry_tpbs',  # Use the combined column as color
        histnorm='percent',
        labels={'avg_daily_operation_med': 'Avg Daily Operation (Med)', 'status': 'Status'},
        title="4-4. 정상기업 vs 부도기업 산업별 가동률 히스토그램",
        barmode='overlay',
        height=400,
        category_orders={'industry_tpbs': sorted_industry_tpbs}
        )

    # Set all traces to legend-only (initially hidden)
    industry_op_fig_hist.for_each_trace(lambda trace: trace.update(visible="legendonly"))

    # Get the first unique value from `기업형태_tpbs` and set it to be visible
    first_value = df['industry_tpbs'].unique()[0]
    for trace in industry_op_fig_hist.data:
        if trace.name == first_value:
            trace.visible = True

    st.plotly_chart(industry_op_fig_hist)
    
    space() 
    space()         


    overdue_yn_op_fig = px.violin(
        df,
        x='기업형태',
        y='diff_avg_daily_operation_med_tpbs_clsf_dcd',
        box=True,
        points="all",
        labels={'diff_avg_daily_operation_med_tpbs_clsf_dcd': 'Avg Daily Operation (Med)', 'status': 'Status'},
        title="4-5. 정상기업 vs 부도기업 (Daily 가동률 - daily 산업평균 가동률 평균) 현황",
        height=400,  # Normalize by percentage to account for imbalance
    )
    st.plotly_chart(overdue_yn_op_fig)

    space() 
    space() 
   
    # Violin Plot with tpbs_clsf_dcd as color
    industry_op_fig_violin = px.violin(
        df,
        x='기업형태',
        y='diff_avg_daily_operation_med_tpbs_clsf_dcd',
        color='tpbs_clsf_dcd',  # Add tpbs_clsf_dcd as color
        box=True,
        points="all",
        labels={'diff_avg_daily_operation_med_tpbs_clsf_dcd': 'Avg industry Daily Operation (Med)', 'status': 'Status'},
        title="4-6. 정상기업 vs 부도기업 (Daily 가동률 - daily 산업평균 가동률 평균) 산업별 현황",
        height=400,
    )
    # Set all traces to legend-only (initially hidden)
    industry_op_fig_violin.for_each_trace(lambda trace: trace.update(visible="legendonly"))

    # Manually set a specific tpbs_clsf_dcd value to be visible (e.g., "A")
    for trace in industry_op_fig_violin.data:
        if trace.name == df['tpbs_clsf_dcd'].unique()[0]:  
            trace.visible = True
    st.plotly_chart(industry_op_fig_violin)

    space() 
    space() 
    
    
    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})


    avg_daily_op_med_12w_min_fig = px.violin(
        df,
        x='기업형태',
        y='avg_daily_operation_med_12week_min',
        box=True,
        points="all",
        labels={'avg_daily_operation_med_12week_min': 'avg_daily_operation_med_12week_min', 'status': 'Status'},
        title="avg_daily_operation_med_12week_min",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(avg_daily_op_med_12w_min_fig)

    
    space() 
    space() 

    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    #'diff_avg_operation_three_month_med_mean_tpbs_clsf_dcd_4week_std',
    #'diff_avg_operation_six_month_med_mean_tpbs_clsf_dcd_4week_std',

    avg_daily_op_6m_med_4w_std_fig = px.violin(
        df,
        x='기업형태',
        y='avg_operation_six_month_med_4week_std',
        box=True,
        points="all",
        labels={'avg_operation_six_month_med_4week_std': 'avg_operation_six_month_med_4week_std', 'status': 'Status'},
        title="avg_daily_op_6m_med_4w_std_fig",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(avg_daily_op_6m_med_4w_std_fig)

    
    space() 
    space() 


    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})


    diff_avg_daily_op_med_4w_std_fig = px.violin(
        df,
        x='기업형태',
        y='diff_avg_operation_one_month_med_mean_tpbs_clsf_dcd_4week_std',
        box=True,
        points="all",
        labels={'diff_avg_operation_one_month_med_mean_tpbs_clsf_dcd_4week_std': 'diff_avg_operation_one_month_med_mean_tpbs_clsf_dcd_4week_std', 'status': 'Status'},
        title="diff_avg_operation_one_month_med_mean_tpbs_clsf_dcd_4week_std",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(diff_avg_daily_op_med_4w_std_fig)

    
    space() 
    space() 



    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Violin Plot with density normalization
    overdue_yn_fcfn_bal_fig = px.violin(
        df,
        x='기업형태',
        y='fcfn_bal',
        box=True,
        points="all",
        labels={'fcfn_bal': 'Avg fcfn_bal', 'status': 'Status'},
        title="4-7. 정상기업 & 부도기업 Daily Avg 시설자금잔액 현황",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(overdue_yn_fcfn_bal_fig)

    
    space() 
    space() 

    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Violin Plot with density normalization
    overdue_yn_fcfn_bal_4w_fig = px.violin(
        df,
        x='기업형태',
        y='fcfn_bal_4week_min',
        box=True,
        points="all",
        labels={'fcfn_bal': 'Avg fcfn_bal', 'status': 'Status'},
        title="4-8. 정상기업 & 부도기업 4_week_min 시설자금잔액 현황",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(overdue_yn_fcfn_bal_4w_fig)

        
    space() 
    space() 

    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Violin Plot with density normalization
    overdue_yn_thmm_todp_avb_fig = px.violin(
        df,
        x='기업형태',
        y='thmm_todp_avb',
        box=True,
        points="all",
        labels={'thmm_todp_avb': 'Avg thmm_todp_avb', 'status': 'Status'},
        title="4-9. 정상기업 & 부도기업 당월총수신평잔 현황",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(overdue_yn_thmm_todp_avb_fig)


    space() 
    space() 

    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Violin Plot with density normalization
    overdue_yn_thmm_todp_avb_4w_min_fig = px.violin(
        df,
        x='기업형태',
        y='thmm_todp_avb_4week_min',
        box=True,
        points="all",
        labels={'thmm_todp_avb_4week_min': 'thmm_todp_avb_4week_min', 'status': 'Status'},
        title="4-10. 정상기업 & 부도기업 4주 당월총수신평잔 최소값 현황",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(overdue_yn_thmm_todp_avb_4w_min_fig)



    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Violin Plot with density normalization
    overdue_yn_thmm_todp_avb_fig = px.violin(
        df,
        x='기업형태',
        y='thmm_ondm_avb',
        box=True,
        points="all",
        labels={'thmm_ondm_avb': 'Avg thmm_ondm_avb', 'status': 'Status'},
        title="4-. 정상기업 & 부도기업 당월요구불평잔 현황",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(overdue_yn_thmm_todp_avb_fig)


    space() 
    space() 

    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Violin Plot with density normalization
    overdue_yn_thmm_todp_avb_4w_min_fig = px.violin(
        df,
        x='기업형태',
        y='thmm_ondm_avb_4week_min',
        box=True,
        points="all",
        labels={'thmm_ondm_avb_4week_min': 'thmm_ondm_avb_4week_min', 'status': 'Status'},
        title="4-. 정상기업 & 부도기업 4주 당월요구불평잔 최소값 현황",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(overdue_yn_thmm_todp_avb_4w_min_fig)


        # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Violin Plot with density normalization
    overdue_yn_bhcc06_fig = px.violin(
        df,
        x='기업형태',
        y='bhcc06',
        box=True,
        points="all",
        labels={'bhcc06': 'bhcc06', 'status': 'Status'},
        title="4-11. 정상기업 & 부도기업 사업체 통신요금 자동이체 정상 출금 기간(현재기준)",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(overdue_yn_bhcc06_fig)

    # 급여이체여부 sltf_yn

    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Calculate percentage of sltf_yn = 1 for each 기업형태
    percent_df = df.groupby('기업형태')['sltf_yn'].mean().reset_index()
    percent_df['sltf_yn_percent'] = percent_df['sltf_yn'] * 100

    # Bar plot for percentage
    sltf_yn_fig = px.bar(
        percent_df,
        x='기업형태',
        y='sltf_yn_percent',
        labels={'sltf_yn_percent': '급여이체여부 (%)'},
        title="4-12. 정상기업 & 부도기업 급여이체여부 비율 (현재기준)",
        height=400
    )

    st.plotly_chart(sltf_yn_fig)


    # Map `overdue_yn` to labels
    df['기업형태'] = df['overdue_yn'].map({0: '정상기업', 1: '부도기업'})

    # Violin Plot with density normalization
    sltf_yn_12w_violin_fig = px.violin(
        df,
        x='기업형태',
        y='sltf_yn_12week_sum',
        box=True,
        points="all",
        labels={'sltf_yn_12week_sum': 'sltf_yn_12week_sum', 'status': 'Status'},
        title="4-13. 정상기업 & 부도기업 최근 12주 급여이체 횟수 합계",
        height=400,  # Normalize by percentage to account for imbalance
    
    )

    st.plotly_chart(sltf_yn_12w_violin_fig)

else:
    pass



