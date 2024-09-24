
# 라이브러리

import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm

import seaborn as sns

import io
plt.rc('font', family='Malgun Gothic')
# font_list = [f.name for f in fm.fontManager.ttflist]
# st.write(font_list)  # 설치된 폰트 확인

# 함수

# 1. 파일 업로드 함수(only csv)
def read_file(file):
    if  'csv' in file.name:
        df = pd.read_csv(file)
        df = df.drop(columns='Unnamed: 0')
        st.success('파일업로드 완료', icon="🔥")
    else:
        st.warning("CSV 형식만 지원합니다.")
        
    return df

# 2. df columns 정보 함수
def create_summary(df):
    # 통계 요약 정보를 얻습니다.
    stats = df.describe(include='all').transpose()

    # 데이터 타입 정보를 얻습니다.
    data_types = df.dtypes

    # 결측치 개수를 계산합니다.
    missing_values = df.isnull().sum()

    # 데이터 정보를 입력합니다.
    data_description = {
        "date": "가동률 데이터 수집일",
        "client_id":"본점 ID", # 추후삭제
        "client_name":"본점명", # 추후삭제
        "branch_id":"지점 ID", # 추후삭제
        "branch_name":"지점명", # 추후삭제
        "company_id":"(담보물을 등록한) 회사 ID", 
        "company_name":"(담보물을 등록한) 회사명",
        "warranty_id":"담보물 ID", 
        "warranty_name":"담보물명",
        "model_name_x":"담보물 모델명",
        "serial_number_x":"담보물 식별 번호",
        "euid":"C&TECH 장비번호", # 추후삭제
        "last_battery":"최종 배터리", 
        "daily_operation":"일 가동률",
        "monthly_operaiton":"월 가동률(현재일부터 과거 30일 평균)",
        "is_detach":"탈착 여부",
        "is_move":"이동 여부 {1:미이동, 2:단거리, 3:장거리}",
        "is_normal":"정상 여부",
        "previous_month":"데이터 매칭을 위한 이전 달 계산",
        "target_ym":"previous_month와 매칭",
        "model_name_y":"담보물 모델명",
        "serial_number_y":"담보물 식별 번호",
        "control_number":"고객대출번호",
        "move_grade":"(구버전) 이동 등급",
        "confidence_grade":"(구버전) 신뢰성 등급",
        "operation_grade":"(구버전) 가동률 등급",
        "avg_operation_one_month":"(전월 기준) 1개월 평균 가동률",
        "avg_operation_three_month":"3개월 평균 가동률",
        "avg_operation_six_month":"6개월 평균 가동률",
        "move_grade_continous_a":"(이동) A등급 유지 카운트",
        "confidence_grade_continous_a":"(신뢰성) A등급 유지 카운트",
        "operation_grade_continous_a":"(가동률) A등급 유지 카운트",
        "registration_number":"사업자 등록번호",
        "mobility_new_grade":"(신버전) 이동 등급",
        "reliability_new_grade":"(신버전) 신뢰성 등급",
        "operability_new_grade":"(신버전) 가동률 등급",
        "date_count":"해당 담보물 데이터 수집일 합계"
        }

    # 위의 정보를 하나의 데이터프레임으로 결합합니다.
    summary = stats.copy()
    summary['Data Type'] = data_types
    summary['Missing Values'] = missing_values
    summary['description'] = data_description.values()

    # 컬럼 순서를 재배치합니다.
    cols = ['Data Type', 'Missing Values'] + [col for col in summary.columns if col not in ['Data Type', 'Missing Values', 'Description']]
    summary = summary[cols]

    return summary

# 시작 부분
st.title("IBK C&Tech Data Visualization")

# 공란 띄우기
st.header("")
st.header("")

st.header("1. 파일 업로드")
uploaded_files = st.file_uploader("", type=['parquet', 'csv'])

if uploaded_files is not None:
    # 공란 띄우기
    st.header("")
    st.header("")


    st.header("2. 전체 데이터 확인하기")
    df = read_file(uploaded_files)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', yearfirst=True) #.dt.strftime('%y-%m-%d')
    df['date'] = df['date'].dt.date
    st.dataframe(df.head(100))
    
    # 공란 띄우기
    st.header("")
    st.header("")

    st.header("3. 데이터 기본정보")
    summary_df = create_summary(df)    
    st.dataframe(summary_df)

                 
    # 각 컬럼에 대한 속성 정보를 표시
    attribute_infos = ""
    for idx, row in summary_df.iterrows():
        attribute_info = f"""
        **컬럼명:** {idx}
        - **설명:** {row['description']}
        - **예시 값:** {df[idx].dropna().unique()[:2]}
        ---
        """
        attribute_infos += attribute_info + "\n"

    with st.expander("🔍 컬럼 상세 설명"):
        st.info(attribute_infos)


    # 공란 띄우기
    st.header("")
    st.header("")
    # 사용자로부터 컬럼 선택받기
    st.header("4. 데이터 시각화")
    st.subheader("4-1. 수치형 데이터 히스토그램")

    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    selected_column = st.selectbox("시각화할 수치형 컬럼을 선택하세요:", numeric_columns, index=5)

    if selected_column:

        # 히스토그램 그리기
        fig, ax = plt.subplots()
        ax.hist(df[selected_column].dropna(), bins=30, color='skyblue', edgecolor='black')
        ax.set_title(f'{selected_column} hist')
        ax.set_xlabel(selected_column)
        ax.set_ylabel('frequency')
        st.pyplot(fig)

        # 박스플롯 그리기
        fig2, ax2 = plt.subplots()
        ax2.boxplot(df[selected_column].dropna())
        ax2.set_title(f'{selected_column} boxplot')
        ax2.set_ylabel(selected_column)
        st.pyplot(fig2)
    
    # 공란 띄우기
    st.header("")
    st.header("")

    # st.subheader("4-2. 수치형 데이터 산점도")
    # x_axis = st.selectbox("X축 변수 선택:", numeric_columns)
    # y_axis = st.selectbox("Y축 변수 선택:", numeric_columns)

    # if x_axis and y_axis:    
    #     fig3, ax3 = plt.subplots()
    #     scatter = ax3.scatter(df[x_axis], df[y_axis],  alpha=0.7)
    #     ax3.set_xlabel(x_axis)
    #     ax3.set_ylabel(y_axis)
    #     ax3.set_title(f'{x_axis} vs {y_axis} Scatter plot')

    #     st.pyplot(fig3)

    
    # 변수 줄인다음에 pair plots 그리기
    # fig4 = sns.pairplot(df, palette='coolwarm') #hue= 설정
    # st.pyplot(fig4)

    # 공란 띄우기
    st.header("")
    st.header("")

    st.header("5. 특정 회사 필터링 후 정보 확인")
    # Form 생성
    with st.form("company_filtering"):
        st.write("필터링 옵션을 선택하세요:")

        # 고유한 회사 ID 및 회사명 선택
        company_name = st.selectbox("회사명 선택:", options=[None] + df['company_name'].unique().tolist(), index=1)

        # 선택한 회사 ID에 따라 고유한 회사명 필터링
        if company_name is not None:
            matching_id = df[df['company_name'] == company_name]['company_id'].unique().tolist()
            maching_warranty_id = df[df['company_name'] == company_name]['warranty_id'].unique().tolist()
        else:
            matching_id = df['company_id'].unique().tolist()
            maching_warranty_id = df['warranty_id'].unique().tolist()

        
        company_id_all_selected = st.checkbox("모두 선택", value=False)

        # 멀티 선택: "모두 선택"이 체크된 경우 모든 ID를 선택, 아니면 개별 선택 가능
        if company_id_all_selected:
            company_id = st.multiselect("회사 ID 선택:", options=matching_id, default=matching_id)
            warranty_id = st.multiselect("담보물 ID 선택:", options=maching_warranty_id, default=maching_warranty_id)
        else:
            company_id = st.multiselect("회사 ID 선택:", options=matching_id)
            warranty_id = st.multiselect("담보물 ID 선택:", options=maching_warranty_id)


        # # 다른 필터링 항목 (필요시 추가 가능)
        # min_operation = st.slider("6개월 평균 가동률(최소값):", min_value=0, max_value=100, value=50)

        # 폼 제출 버튼
        submit_button = st.form_submit_button(label="필터 적용")

    # 폼 제출 후 필터링된 데이터 표시
    if submit_button:
        # 조건에 따른 데이터 필터링
        filtered_df = df.copy()
        
        if company_id is not None:
            filtered_df = filtered_df[filtered_df['company_id'].isin(company_id)]
        
        if company_name is not None:
            filtered_df = filtered_df[filtered_df['company_name']==company_name]

        if warranty_id is not None:
            filtered_df = filtered_df[filtered_df['warranty_id'].isin(warranty_id)]
        

        # 필터링된 데이터 출력
        # 공란
        st.header("")
        st.header("")
        st.subheader("5-1. 해당 회사 기본 정보")
        st.header("")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("담보물 개수", str(len(maching_warranty_id))+"개")
        col2.metric("회사 ID 개수", str(len(company_id))+"개")
        col3.metric("데이터 최초 수집일", str(filtered_df['date'].min()))
        col4.metric("데이터 최종 수집일", str(filtered_df['date'].max()))

        st.header("")
        st.header("")

        col5, col6, col7, col8 = st.columns(4)
        col5.metric("평균 가동률", str(round(filtered_df['daily_operation'].mean(),2)))
        col6.metric("최대 가동률", str(round(filtered_df['daily_operation'].max(),2)))
        col7.metric("최소 가동률", str(round(filtered_df['daily_operation'].min(),2)))
        col8.metric("가동률 표준편차", str(round(filtered_df['daily_operation'].std(),2)))


        

        st.header("")
        st.header("")
        st.subheader("5-2. 필터링 결과")
        st.dataframe(filtered_df)

        st.header("")
        st.header("")
        st.subheader("5-3. 가동률 시각화")
        # Seaborn을 사용한 시계열 플롯 생성
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=filtered_df, x='date', y='daily_operation', hue='warranty_id', marker='o')


        # warranty_name 별로 min, max, mean 값 계산

        if filtered_df['warranty_id'].nunique() == 1:
            filtered_df_grouped = filtered_df.groupby('warranty_id')['daily_operation'].agg(['min', 'max', 'mean', 'std']).reset_index()
            # Matplotlib의 ax 객체를 가져와 추가 라인을 그림
            ax = plt.gca()

            # warranty_name 별로 min, max, mean 수평선 추가
            for _, row in filtered_df_grouped.iterrows():
                warranty = row['warranty_id']
                # mean 수평선
                ax.axhline(row['mean'], linestyle='-', color='green', label=f'{warranty} mean', linewidth=2, alpha=0.7)

            # 이상치 필터링: 평균 ± 3 표준편차를 벗어난 값
            outliers = pd.DataFrame()

            for _, row in filtered_df_grouped.iterrows():
                mean = row['mean']
                std = row['std']
                warranty = row['warranty_id']
                
                # 이상치 기준
                upper_limit = mean + 2 * std
                lower_limit = mean - 2 * std
                
                # 이상치 필터링
                outliers_temp = filtered_df[
                    (filtered_df['warranty_id'] == warranty) &
                    ((filtered_df['daily_operation'] > upper_limit) | (filtered_df['daily_operation'] < lower_limit))
                ]
                
                outliers = pd.concat([outliers, outliers_temp])

            # 이상치 표시
            sns.scatterplot(data=outliers, x='date', y='daily_operation', color='red', s=100, label='Outliers(2std)', ax=ax)

            # 범례 중복 제거
            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys())




            # x축 날짜 레이블 자동 조정 (AutoDateLocator & AutoDateFormatter 사용)
            ax = plt.gca()
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))  # 7일 간격으로 날짜 표시
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            # x축 레이블의 회전 각도 설정
            plt.xticks(rotation=45, ha='right')
            # 제목과 축 레이블 설정
            plt.title("Warranty Daily Operation")
            plt.xlabel("Date")
            plt.ylabel("Daily Operation")

            # Streamlit에서 플롯 출력
            st.pyplot(plt)

        elif filtered_df['warranty_id'].nunique() >= 2:
            for warranty_id, group in filtered_df.groupby('warranty_id'):
                # 해당 warranty_id에 대한 통계 계산
                warranty_stats = group.groupby('warranty_id').agg(
                min=('daily_operation', 'min'),
                max=('daily_operation', 'max'),
                mean=('daily_operation', 'mean'),
                std=('daily_operation', 'std')
                ).reset_index()
                
                # 새로운 figure와 ax 객체를 생성
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # min, max, mean 수평선 추가
                ax.axhline(warranty_stats['mean'].values[0], linestyle='-', color='green', label=f'{warranty_id} mean', linewidth=2, alpha=0.7)


                # 이상치 필터링: 평균 ± 2 표준편차를 벗어난 값
                mean = warranty_stats['mean'].values[0]
                std = warranty_stats['std'].values[0]
                upper_limit = mean + 2 * std
                lower_limit = mean - 2 * std

                # 해당 warranty_id에 대한 이상치 필터링
                outliers = group[(group['daily_operation'] > upper_limit) | (group['daily_operation'] < lower_limit)]

                # 원본 데이터 라인 플롯
                sns.lineplot(data=group, x='date', y='daily_operation', ax=ax, label=f'{warranty_id} daily operation')

                # 이상치 표시
                if not outliers.empty:
                    sns.scatterplot(data=outliers, x='date', y='daily_operation', color='red', s=100, label='Outliers(2std)', ax=ax)

                # 범례 중복 제거
                handles, labels = ax.get_legend_handles_labels()
                by_label = dict(zip(labels, handles))
                plt.legend(by_label.values(), by_label.keys())

                # x축 날짜 레이블 자동 조정 (AutoDateLocator & AutoDateFormatter 사용)
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))  # 30일 간격으로 날짜 표시
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

                # x축 레이블의 회전 각도 설정
                plt.xticks(rotation=45, ha='right')

                # 제목과 축 레이블 설정
                plt.title(f"Warranty Daily Operation for {warranty_id}")
                plt.xlabel("Date")
                plt.ylabel("Daily Operation")

                # Streamlit에서 플롯 출력
                st.pyplot(fig)







