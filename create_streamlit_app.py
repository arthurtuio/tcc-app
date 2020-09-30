import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import squarify
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from aux_lib.create_plot import CreatePlot #nao tem problema aparecer errado, pq o streamlit tem que ler nessa path mesmo


def create_df_and_texts():
    st.title('Análise interativa faturas UDESC')
    st.markdown(
        """
        Essa é uma página interativa, criada com a lib _streamlit_. No canto esquerdo você verá as 
        **User Input Features**, que de acordo com sua escolha, irão modificar o que você verá em toda a análise.
        Você verá que também poderá baixar o output da análise que você criou, em CSV, e também escolher quais
        informações visualizar nessa página, selecionando botões para mostrar gráficos.

        Antes de iniciar a análise, Escolha na opção abaixo se você quer analisar uma unidade consumidora
        específica de um campus, ou o campus inteiro (somando todas as suas unidades consumidoras).

        Por favor, para iniciar a análise, selecione pelo menos um Campus ou grupo tarifário, e pelo menos 
        uma data que você gostaria de visualizar. 

        Observação: Note que você pode escolher mais de um campus e data.
        """)

    analysis_style = st.selectbox(
        "Tipo do dado que você deseja analisar",
        ("Unidade consumidora de um Campus", "Campus inteiro")
    )

    st.sidebar.header('User Input Features')

    enriched_csv = "enriched_result.csv"

    return pd.read_csv(enriched_csv), analysis_style


def create_sidebars(df, analysis_style):
    # Sidebar - Unique Campus, Date, and Grupo Tarifario
    if analysis_style == "Unidade consumidora de um Campus":
        sorted_unique_campus = df.Campus_Unique_Name.unique()
        selected_campus = st.sidebar.multiselect('Unidade Consumidora do Campus', sorted_unique_campus)

    elif analysis_style == "Campus inteiro":
        sorted_campus = df.Campus_Name.unique()
        selected_campus = st.sidebar.multiselect('Campus', sorted_campus)

    else:
        st.write("Por favor, escolha um tipo de análise para iniciar!")

    unique_grupo_tarifario = df.Grupo_Tarifario.unique()
    selected_grupo_tarifario = st.sidebar.multiselect('Grupo Tarifário', unique_grupo_tarifario)

    sorted_unique_date = sorted(df.MM_YY_ref.unique())
    selected_date = st.sidebar.multiselect('Date', sorted_unique_date, sorted_unique_date)

    return (
        selected_grupo_tarifario,
        selected_campus,
        selected_date
    )


def filter_showed_data(df, analysis_style):
    # Filtering data
    try:
        if analysis_style == "Unidade consumidora de um Campus":
            campus_column = "Campus_Unique_Name"
        elif analysis_style == "Campus inteiro":
            campus_column = "Campus_Name"

        if not selected_campus and selected_grupo_tarifario:
            df_input_filtered = df[
                (df.Grupo_Tarifario.isin(selected_grupo_tarifario)) &
                (df.MM_YY_ref.isin(selected_date))
                ]
        elif selected_campus:
            df_input_filtered = df[
                (df[campus_column].isin(selected_campus)) &
                (df.MM_YY_ref.isin(selected_date))
                ]

        return df_input_filtered

    except:
        st.markdown("**Para iniciar, por favor, escolha na User Input Features um campus ou um grupo tarifário.**")


def create_output_table(df):
    st.header('Tabela filtrada')
    st.markdown("Tabela criada através da seleção das **User Input Features**.")

    st.write(
        'Data Dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
    st.dataframe(df)


# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="dados_reduzidos_fatura_udesc.csv">Download CSV File</a>'
    return href


def create_header_for_individual_plots():
    st.header('Gráficos e Tabelas Individuais dos Campus')
    st.markdown(
        """
        Abaixo serão apresentados gráficos e tabelas de features do Campus que você selecionar.

        Perceba que os botões dos gráficos para visualizar dependem da sua escolha inicial de analisar
        uma unidade consumidora específica de um Campus, ou todo um Campus.

        **Para uso das tabelas, selecione também o Grupo Tarifário.**
        """
    )


def create_plots_based_on_unique_campus_or_all_campus(df, selected_campus, analysis_style, selected_grupo_tarifario):
    create_plot_obj = CreatePlot(df, selected_campus)

    if analysis_style == "Unidade consumidora de um Campus":
        if st.button('Demanda Medida X Contratada'):
            fig = create_plot_obj.medido_and_contratado_plot()
            st.plotly_chart(fig, use_container_width=True)

        if st.button('Razão Dem. Medida X Contratada'):
            fig = create_plot_obj.ratio_medido_faturado_plot()
            st.plotly_chart(fig, use_container_width=True)

        if st.checkbox('Consumo Medido (kW) e gasto (R$) P e FP'):
            if st.checkbox("Consumo Medido (kW)"):
                fig = create_plot_obj.medido_consumo_P_and_FP_plot()
                st.plotly_chart(fig, use_container_width=True)

            if st.checkbox("Consumo Medido (R$)"):
                fig = create_plot_obj.gasto_consumo_P_and_FP_plot()
                st.plotly_chart(fig, use_container_width=True)

            if st.checkbox("Comparação P e FP - total"):
                fig = create_plot_obj.compare_consumo_P_and_FP_plot()
                st.plotly_chart(fig, use_container_width=True)

            # if st.checkbox("Comparação P e FP - Relativa"):
            #     fig = create_plot_obj.relative_compare_consumo_P_and_FP_plot()
            #     st.plotly_chart(fig, use_container_width=True)

    elif analysis_style == "Campus inteiro":
        #if st.button("Composição Unidades Consumidoras Campus"):
        campus_df = df.loc[df.Campus_Name == selected_campus[0]]
        st.markdown(f"**UCs do Campus:** {campus_df.Campus_Unique_Name.unique()}")

        if st.checkbox("Tabela Soma Valores Faturados por UC (R$)"):
            df_valores_faturados = create_plot_obj.show_valores_faturados(selected_grupo_tarifario)
            st.dataframe(df_valores_faturados)
            if st.checkbox("Gráfico Soma Valores Faturados por UC (R$)"):
                create_plot_obj.bar_plot_valores_faturados(selected_grupo_tarifario)
                st.pyplot()

        if st.checkbox("Tabela Soma Valores Faturados por UC (kW)"):
            df_valores_faturados = create_plot_obj.show_valores_quantidade(selected_grupo_tarifario)
            st.dataframe(df_valores_faturados)
            if st.checkbox("Gráfico Soma Valores Faturados por UC (kW)"):
                create_plot_obj.bar_plot_valores_quantidade(selected_grupo_tarifario)
                st.pyplot()

        if st.checkbox("Tabela Soma Valores Medidos por UC (kW)"):
            df_valores_faturados = create_plot_obj.show_valores_medidos(selected_grupo_tarifario)
            st.dataframe(df_valores_faturados)
            if st.checkbox("Gráfico Soma Valores Medidos por UC (kW)"):
                create_plot_obj.bar_plot_valores_medidos(selected_grupo_tarifario)
                st.pyplot()


def create_header_for_algorythm_analysis():
    st.header("Análise via algoritmo")
    st.markdown("""
    Se você deseja que o algoritmo faça uma análise do resultado encontrado, 
    selecione o botão da análise desejada.

    Por hora, as análises possíveis são:
    - Análise de Demanda - Independe do grupo tarifário escolhido, já que só existe demanda em A-4;
    - Análise comparativa dos anos - Depende do grupo tarifário escolhido;
    - Análise do valor total cobrado em R$ por UC.mês - Feita para os dois grupos tarifários;
    """)


def analyse_demanda(df):
    st.subheader("Análise da Demanda")
    st.markdown("""
    Serão analisados, para os meses selecionados:
    - Quantos meses tiveram demanda Medida acima e abaixo do ideal, 
    de acordo com um limite que você vai definir abaixo, **pensando na razão Medido/Contratado**;
    - Qual o valor total perdido em R$ com demanda ultrapassada;
    - Qual o valor total perdido em R$ com sobrecontratação, ou seja, 
    em meses que a demanda medida veio abaixo da contratada;
    """)
    lim_inf = st.selectbox('Limite Inferior', (0.4, 0.5, 0.6, 0.7, 0.8))
    lim_sup = st.selectbox('Limite Superior', (1.1, 1.2, 1.3, 1.4, 1.5))

    count_sup, count_inf = 0, 0
    sum_custo_demanda_ultrapassada = 0
    sum_custo_sobrecontracacao_demanda = 0

    for index, row in df.iterrows():
        i_sup, i_inf = 0, 0
        if row['ratio_medido_faturado'] > lim_sup:
            i_sup = 1
        elif row['ratio_medido_faturado'] < lim_inf:
            i_inf = 1
        count_sup += i_sup
        count_inf += i_inf

        sum_custo_demanda_ultrapassada += round(row["valor_faturado_demanda_ultr"], 2)
        sum_custo_sobrecontracacao_demanda += round(row["lost_money_sobrecontratacao_demanda"], 2)

    med_valor_perdido_demanda_ultr = round(sum_custo_demanda_ultrapassada / df.shape[0], 2)
    med_valor_perdido_sobrecontratacao = round(sum_custo_sobrecontracacao_demanda / df.shape[0], 2)

    st.markdown(f"""
    **Output análise:**
    - Número vezes que ficou acima do lim superior: {count_sup}, e abaixo do inferior: {count_inf};
    - Valor perdido total e médio por demanda ultrapassada: R$ {round(sum_custo_demanda_ultrapassada, 2)}, R$ {med_valor_perdido_demanda_ultr}/mês.campus;
    - Valor perdido total e médio por sobrecontração de demanda: R$ {round(sum_custo_sobrecontracacao_demanda, 2)}, R$ {med_valor_perdido_sobrecontratacao}/mês.campus;
    """)


def comparative_year_analysis(df, selected_grupo_tarifario):
    st.subheader("Análise Comparativa dos anos")
    st.markdown("""
    Esta análise depende do Grupo Tarifário escolhido. Ela retornará gráficos dos seguintes params com base na escolha:
    - B3: Apenas será analisado o consumo medido, comparando-o ano a ano
    - A4: Será feita a mesma análise de consumo medido, só que dividida entre Ponta e fora Ponta.
    """)

    df_2018 = df.loc[df.year == 2018]
    df_2019 = df.loc[df.year == 2019]
    df_2020 = df.loc[df.year == 2020]

    labels_2018 = sorted(df_2018['month'].values.tolist())
    labels_2019 = sorted(df_2019['month'].values.tolist())
    labels_2020 = sorted(df_2020['month'].values.tolist())

    if len(selected_grupo_tarifario) == 2:
        pass

    elif selected_grupo_tarifario[0] == "B-3":
        consumo_med_2018 = df_2018['Medido_consumo'].values.tolist()
        consumo_med_2019 = df_2019['Medido_consumo'].values.tolist()
        consumo_med_2020 = df_2020['Medido_consumo'].values.tolist()

        media_consumo_mes = df.groupby("month").mean().Medido_consumo.tolist()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=labels_2018,
            y=consumo_med_2018,
            hovertext="kW",
            name='2018'))

        fig.add_trace(go.Bar(
            x=labels_2019,
            y=consumo_med_2019,
            hovertext="kW",
            name='2019'))

        fig.add_trace(go.Bar(
            x=labels_2020,
            y=consumo_med_2020,
            hovertext="kW",
            name='2020'))

        fig.add_trace(go.Scatter(
            x=labels_2018,
            y=media_consumo_mes,
            hovertext="kW",
            name='Média mensal'))

        fig.update_layout(
            annotations=[
                dict(
                    x=-0.1,
                    y=0.5,
                    showarrow=False,
                    text="Valores [kW]",
                    textangle=-90,
                    xref="paper",
                    yref="paper"
                )
            ],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1
            ),
            autosize=True,
            margin=dict(b=100),
            title_text=f"Comparação Consumo Medido (kW)",
            xaxis_tickangle=-60,
            height=600, width=900,
            barmode="group"
        )

        return fig

    elif selected_grupo_tarifario[0] == "A-4":
        consumo_P_med_2018 = df_2018['Medido_consumo_P'].values.tolist()
        consumo_P_med_2019 = df_2019['Medido_consumo_P'].values.tolist()
        consumo_P_med_2020 = df_2020['Medido_consumo_P'].values.tolist()

        consumo_FP_med_2018 = df_2018['Medido_consumo_FP'].values.tolist()
        consumo_FP_med_2019 = df_2019['Medido_consumo_FP'].values.tolist()
        consumo_FP_med_2020 = df_2020['Medido_consumo_FP'].values.tolist()

        media_consumo_P_mes = df.groupby("month").mean().Medido_consumo_P.tolist()
        media_consumo_FP_mes = df.groupby("month").mean().Medido_consumo_FP.tolist()

        fig = make_subplots(rows=2, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.12,
                            subplot_titles=("Consumo Medido Ponta", "Consumo Medido Fora Ponta"))

        fig.add_trace(go.Bar(
            x=labels_2018,
            y=consumo_P_med_2018,
            name='2018 Ponta'), row=1, col=1)
        fig.add_trace(go.Bar(
            x=labels_2019,
            y=consumo_P_med_2019,
            name='2019 Ponta'), row=1, col=1)
        fig.add_trace(go.Bar(
            x=labels_2020,
            y=consumo_P_med_2020,
            name='2020 Ponta'), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=labels_2018,
            y=media_consumo_P_mes,
            name='Média mensal Ponta'), row=1, col=1)

        fig.add_trace(go.Bar(
            x=labels_2018,
            y=consumo_FP_med_2018,
            name='2018 F.Ponta'), row=2, col=1)
        fig.add_trace(go.Bar(
            x=labels_2019,
            y=consumo_FP_med_2019,
            name='2019 F.Ponta'), row=2, col=1)
        fig.add_trace(go.Bar(
            x=labels_2020,
            y=consumo_FP_med_2020,
            name='2020 F.Ponta'), row=2, col=1)
        fig.add_trace(go.Scatter(
            x=labels_2018,
            y=media_consumo_FP_mes,
            name='FP Média mensal'), row=2, col=1)

        fig.update_layout(
            annotations=[
                dict(
                    x=-0.1,
                    y=0.5,
                    showarrow=False,
                    text="Valores [kW]",
                    textangle=-90,
                    xref="paper",
                    yref="paper"
                )
            ],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="right",
                x=1
            ),
            autosize=True,
            margin=dict(b=100),
            title_text=f"Comparação Consumo Medido (kW)",
            xaxis_tickangle=-60,
            height=600, width=900,
            barmode="group"
        )

        return fig


def custo_UC_mes_sunburst_analysis(df):
    st.subheader("Análise do valor total cobrado em R$ por UC.mês")
    st.markdown("""
    Análise feita usando um gráfico de pizza do tipo sunburst. \n
    Ref: https://plotly.com/python/sunburst-charts/
    
    **- Independe do Grupo Tarifário escolhido.** \n
    **- Depende do Campus Escolhido (aceita mais de uma escolha pra Campus).**
    
    Selecione abaixo que tipo de valor você quer analisar:
    
    É possível clicar nos itens do gráfico, que ele irá atualizar de acordo com os cliques.
    """)

    value_to_analyse = st.selectbox(
        "Tipo do dado que você deseja analisar",
        (
            "Valor total pago",
            "Valor pago por consumo",
            "Valor pago por consumo P",
            "Valor pago por consumo FP",
            "Valor pago por bandeira amarela",
            "Valor pago por bandeira vermelha",
            "Valor pago por excedente reativo P",
            "Valor pago por excedente reativo FP",
            "Valor pago por apenas por demanda",
            "Valor pago por apenas por demanda ultr.",
            "Valor pago por cosip",
            "Valor pago por custo disponibilidade sistema"
        )
    )

    df_col_mapper = {
        "Valor total pago": "valor_total_RS",
        "Valor pago por consumo": "valor_faturado_consumo",
        "Valor pago por consumo P": "valor_faturado_consumo_P",
        "Valor pago por consumo FP": "valor_faturado_consumo_FP",
        "Valor pago por bandeira amarela": "valor_faturado_band_amar",
        "Valor pago por bandeira vermelha": "valor_faturado_band_verm",
        "Valor pago por excedente reativo P": "valor_faturado_ener_reat_exc_P",
        "Valor pago por excedente reativo FP": "valor_faturado_ener_reat_exc_FP",
        "Valor pago por apenas por demanda": "valor_faturado_demanda",
        "Valor pago por apenas por demanda ultr.": "valor_faturado_demanda_ultr",
        "Valor pago por cosip": "valor_faturado_cosip",
        "Valor pago por custo disponibilidade sistema": "valor_faturado_custo_disp_sistema"
    }

    create_plot_obj = CreatePlot(df, selected_campus)
    fig = create_plot_obj.sunburst_month_and_UC(df_col_mapper[value_to_analyse])
    st.plotly_chart(fig, use_container_width=True)


def create_header_for_prediction():
    st.header("Predições")
    st.markdown("""
    Nessa parte o algoritmo irá predizer valores para próximos meses, com base em média simples, mais com o intuito
    de mostrar o potencial que o algoritmo tem também para realizar predições. Por este motivo, ela ficou limitada
    também para até maio/2021, que é 1 ano a mais do mês que a fatura mais atual foi recebida (maio/2020).

    Os valores que podem ser preditos atualmente são:
    - Consumo Ponta e/ou Fora Ponta para meses futuros, de qualquer Campus ou UC específica do Campus;
    - Custos referentes à impostos para meses futuros, em qualquer Campus ou UC específica do Campus.

    Não é recomendado usar apenas essas predições para tomar decisões, e sim como estudo inicial sobre custos futuros. 

    Para iniciar a predição, use apenas a barra de seleção de Campus/UC. A de mês será escolhida na barra apresentada
    abaixo. 
    """)
    select_month_to_predict = st.slider(
        label="Selecione qual o mês que você quer predizer (1 para 06/2020 e 12 para 05/2021)",
        min_value=1,
        max_value=12
    )
    return select_month_to_predict


def predict_values(df, predicted_month_index):
    # st.dataframe(df)

    media_consumo_mes = df.groupby("month").mean().Medido_consumo.tolist()
    media_consumo_P_mes = df.groupby("month").mean().Medido_consumo_P.tolist()
    media_consumo_FP_mes = df.groupby("month").mean().Medido_consumo_FP.tolist()
    media_faturado_COSIP_mes = df.groupby("month").mean().valor_faturado_cosip.tolist()

    new_months_dict = {
        "prediction_index": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "mm_yy": [
            "2020_06",
            "2020_07",
            "2020_08",
            "2020_09",
            "2020_10",
            "2020_11",
            "2020_12",
            "2021_01",
            "2021_02",
            "2021_03",
            "2021_04",
            "2021_05"
        ],
        "month": [6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5]
    }
    pred_df = pd.DataFrame.from_dict(new_months_dict)
    pred_df["media_consumo"] = media_consumo_mes
    pred_df["media_consumo_P"] = media_consumo_P_mes
    pred_df["media_consumo_FP"] = media_consumo_FP_mes
    pred_df["media_cosip"] = media_faturado_COSIP_mes

    choosen_line = pred_df.loc[predicted_month_index - 1, :]

    choosen_month = choosen_line["mm_yy"]
    choosen_consumo = round(choosen_line["media_consumo"], 2)
    choosen_consumo_P = round(choosen_line["media_consumo_P"], 2)
    choosen_consumo_FP = round(choosen_line["media_consumo_FP"], 2)
    choosen_consumo_cosip = round(choosen_line["media_consumo_FP"] / 1000, 2)  # bug na leitura

    st.markdown(f"O valor predito para consumo medido para o mês **{choosen_month}** foi de **{choosen_consumo} kW**")
    st.markdown(
        f"O valor predito para consumo medido P para o mês **{choosen_month}** foi de **{choosen_consumo_P} kW**")
    st.markdown(
        f"O valor predito para consumo medido FP para o mês **{choosen_month}** foi de **{choosen_consumo_FP} kW**")
    st.markdown(
        f"O valor predito que será pago pela cosip para o mês **{choosen_month}** foi de **R$ {choosen_consumo_cosip}**")

    # st.dataframe(pred_df)


df_fatura, analysis_style = create_df_and_texts()

selected_grupo_tarifario, selected_campus, selected_date = create_sidebars(df_fatura, analysis_style)

df_input_filtered = filter_showed_data(df_fatura, analysis_style)

try:
    create_output_table(df_input_filtered)

    st.markdown(filedownload(df_input_filtered), unsafe_allow_html=True)

    create_header_for_individual_plots()

    create_plots_based_on_unique_campus_or_all_campus(
        df_input_filtered, selected_campus, analysis_style, selected_grupo_tarifario
    )

    create_header_for_algorythm_analysis()

    if st.checkbox("Análise de Demanda", key="dem_analysis"):
        analyse_demanda(df_input_filtered)

    if st.checkbox("Análise Comparativa dos anos do consumo"):
        fig = comparative_year_analysis(df_input_filtered, selected_grupo_tarifario)
        st.plotly_chart(fig, use_container_width=True)

    if st.checkbox("Análise do valor total cobrado em R$ por UC.mês"):
        custo_UC_mes_sunburst_analysis(df_input_filtered)


    predicted_month_index = create_header_for_prediction()
    predict_values(
        df=df_input_filtered,
        predicted_month_index=predicted_month_index
    )

except:
    st.write("**A tabela só aparecerá quando você fizer as escolhas dos dados.**")