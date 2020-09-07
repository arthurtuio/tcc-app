import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import squarify
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class CreatePlot:
    def __init__(self, df, selected_campus):
        self.df = df
        self.selected_campus = selected_campus

    def medido_and_contratado_plot(self):
        # Import Data
        self.df.to_csv('output.csv', index=False)
        df = pd.read_csv('output.csv')

        labels = sorted(df['MM_YY_ref'].values.tolist())
        medido = df['Medido_demanda'].values.tolist()
        faturado = df['real_contracted_value_for_demanda'].values.tolist()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=labels,
            y=medido,
            name='Medido'
        ))
        fig.add_trace(go.Scatter(
            x=labels,
            y=faturado,
            name='Contratado'))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(barmode='group', xaxis_tickangle=-60, title="Demanda Medida X Contratada")
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ))

        return fig

    def ratio_medido_faturado_plot(self):
        self.df.to_csv('output.csv', index=False)
        df = pd.read_csv('output.csv')

        df['ideal_ratio'] = 1

        labels = sorted(df['MM_YY_ref'].values.tolist())
        real_ratio = df['ratio_medido_faturado'].values.tolist()
        ideal_ratio = df['ideal_ratio'].values.tolist()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=labels,
            y=real_ratio,
            name='Real Ratio'
        ))
        fig.add_trace(go.Scatter(
            x=labels,
            y=ideal_ratio,
            name='Ideal Ratio',
        ))

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(
            barmode='group',
            xaxis_tickangle=-60,
            height=600, width=900,
            title=f"Razão Demanda Medida e Contratada para {self.selected_campus}"
        )

        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ))

        return fig

    def medido_e_gasto_consumo_P_and_FP_plot(self):
        self.df.to_csv('output.csv', index=False)
        df = pd.read_csv('output.csv')

        labels = sorted(df['MM_YY_ref'].values.tolist())
        medido_consumo_P = df['Medido_consumo_P'].values.tolist()
        medido_consumo_FP = df['Medido_consumo_FP'].values.tolist()

        valor_faturado_consumo_P = df['valor_faturado_consumo_P'].values.tolist()
        valor_faturado_consumo_FP = df['valor_faturado_consumo_FP'].values.tolist()

        fig = make_subplots(rows=4, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.04)

        fig.add_trace(go.Bar(x=labels, y=medido_consumo_P, name="medido_P"),
                      row=1, col=1)

        fig.add_trace(go.Bar(x=labels, y=medido_consumo_FP, name="medido_FP"),
                      row=2, col=1)

        fig.add_trace(go.Bar(x=labels, y=valor_faturado_consumo_P, name="valor_faturado_P"),
                      row=3, col=1)

        fig.add_trace(go.Bar(x=labels, y=valor_faturado_consumo_FP, name="valor_faturado_FP"),
                      row=4, col=1)

        fig.update_layout(height=700, width=900,
                          title_text="Consumo Medido (W) e gasto (R$) P e FP")

        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ))

        return fig

    def treemap_UC_composition(self):
        self.df.to_csv('output.csv', index=False)
        df_raw = pd.read_csv('output.csv')

        # Prepare Data
        df = df_raw.groupby('Campus_Unique_Name').size().reset_index(name='counts')
        labels = df.apply(lambda x: str(x[0]) + "\n (" + str(x[1]) + ")", axis=1)
        sizes = df['counts'].values.tolist()
        colors = [plt.cm.Spectral(i / float(len(labels))) for i in range(len(labels))]

        # Draw Plot
        plt.figure(figsize=(12, 8), dpi=80)
        squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)

        # Decorate
        plt.title(f'Composição de Unidades Consumidoras para o Campus {self.selected_campus}')
        plt.axis('off')
        return plt.show()

    def show_valores_faturados(self, selected_grupo_tarifario):
        input_df_with_grupo_tarifario = self.df[
            (self.df.Grupo_Tarifario.isin(selected_grupo_tarifario))
        ]

        input_df_with_grupo_tarifario.to_csv('output.csv', index=False)
        df_raw = pd.read_csv('output.csv')

        grouped_df = df_raw.groupby('Campus_Unique_Name').sum()
        df_valores_faturados = grouped_df[[
            "valor_total_RS",
            "valor_faturado_consumo",
            "valor_faturado_band_amar",
            "valor_faturado_band_verm",
            "valor_faturado_consumo_P",
            "valor_faturado_consumo_FP",
            "valor_faturado_ener_reat_exc_P",
            "valor_faturado_ener_reat_exc_FP",
            "valor_faturado_demanda",
            "valor_faturado_demanda_ultr",
            "valor_faturado_cosip",
            "valor_faturado_custo_disp_sistema",
            "valor_faturado_comp_viol_meta_continuidade"
        ]]

        if len(selected_grupo_tarifario) == 2:
            pass

        elif selected_grupo_tarifario[0] == "B-3":
            df_valores_faturados.drop(columns=[
                "valor_faturado_consumo_P",
                "valor_faturado_consumo_FP",
                "valor_faturado_ener_reat_exc_P",
                "valor_faturado_ener_reat_exc_FP",
                "valor_faturado_demanda",
                "valor_faturado_demanda_ultr"
            ], inplace=True)

        elif selected_grupo_tarifario[0] == "A-4":
            df_valores_faturados.drop(columns=[
                "valor_faturado_consumo",
                "valor_faturado_custo_disp_sistema"
            ], inplace=True)

        else:
            st.write("Por favor, escolha pelo menos 1 grupo tarifário para continuar")

        return df_valores_faturados

    def show_valores_quantidade(self, selected_grupo_tarifario):
        input_df_with_grupo_tarifario = self.df[
            (self.df.Grupo_Tarifario.isin(selected_grupo_tarifario))
        ]

        input_df_with_grupo_tarifario.to_csv('output.csv', index=False)
        df_raw = pd.read_csv('output.csv')

        grouped_df = df_raw.groupby('Campus_Unique_Name').sum()
        df_valores_faturados = grouped_df[[
            "Quantidade_consumo",
            "Quantidade_consumo_P",
            "Quantidade_consumo_FP",
            "Quantidade_ener_reat_exc_P",
            "Quantidade_ener_reat_exc_FP",
            "Quantidade_demanda",
            "Quantidade_demanda_ultr",
            "Quantidade_custo_disp_sistema",
        ]]

        if len(selected_grupo_tarifario) == 2:
            pass

        elif selected_grupo_tarifario[0] == "B-3":
            df_valores_faturados.drop(columns=[
                "Quantidade_consumo_P",
                "Quantidade_consumo_FP",
                "Quantidade_ener_reat_exc_P",
                "Quantidade_ener_reat_exc_FP",
                "Quantidade_demanda",
                "Quantidade_demanda_ultr"
            ], inplace=True)

        elif selected_grupo_tarifario[0] == "A-4":
            df_valores_faturados.drop(columns=[
                "Quantidade_consumo",
                "Quantidade_custo_disp_sistema"
            ], inplace=True)
            return df_valores_faturados

        else:
            st.write("Por favor, escolha pelo menos 1 grupo tarifário para continuar")

        return df_valores_faturados

    def show_valores_medidos(self, selected_grupo_tarifario):
        input_df_with_grupo_tarifario = self.df[
            (self.df.Grupo_Tarifario.isin(selected_grupo_tarifario))
        ]

        input_df_with_grupo_tarifario.to_csv('output.csv', index=False)
        df_raw = pd.read_csv('output.csv')

        grouped_df = df_raw.groupby('Campus_Unique_Name').sum()
        df_valores_faturados = grouped_df[[
            "Medido_consumo",
            "Medido_consumo_P",
            "Medido_consumo_FP",
            "Medido_ener_reat_exc_P",
            "Medido_ener_reat_exc_FP",
            "Medido_demanda",
            "Medido_demanda_ultr",
            "Medido_energia_reat_indutiva"
        ]]

        if len(selected_grupo_tarifario) == 2:
            pass

        elif selected_grupo_tarifario[0] == "B-3":
            df_valores_faturados.drop(columns=[
                "Medido_consumo_P",
                "Medido_consumo_FP",
                "Medido_ener_reat_exc_P",
                "Medido_ener_reat_exc_FP",
                "Medido_demanda",
                "Medido_demanda_ultr",
                "Medido_energia_reat_indutiva",
            ], inplace=True)

        elif selected_grupo_tarifario[0] == "A-4":
            df_valores_faturados.drop(columns=["Medido_consumo"], inplace=True)

        else:
            st.write("Por favor, escolha pelo menos 1 grupo tarifário para continuar")

        return df_valores_faturados

    def bar_plot_valores_faturados(self, selected_grupo_tarifario):
        input_df_with_grupo_tarifario = self.df[
            (self.df.Grupo_Tarifario.isin(selected_grupo_tarifario))
        ]

        input_df_with_grupo_tarifario.to_csv('output.csv', index=False)
        df_raw = pd.read_csv('output.csv')

        grouped_df = df_raw.groupby('Campus_Unique_Name').sum()
        df_valores_faturados = grouped_df[[
            "valor_total_RS",
            "valor_faturado_consumo",
            "valor_faturado_band_amar",
            "valor_faturado_band_verm",
            "valor_faturado_consumo_P",
            "valor_faturado_consumo_FP",
            "valor_faturado_ener_reat_exc_P",
            "valor_faturado_ener_reat_exc_FP",
            "valor_faturado_demanda",
            "valor_faturado_demanda_ultr",
            "valor_faturado_cosip",
            "valor_faturado_custo_disp_sistema",
            "valor_faturado_comp_viol_meta_continuidade"
        ]]

        df_valores_faturados['Campus_Unique_Name'] = df_valores_faturados.index

        if len(selected_grupo_tarifario) == 2:
            st.markdown("**Por favor, escolha APENAS 1 Grupo Tarifário**")

        elif selected_grupo_tarifario[0] == "B-3":
            bar_columns_1 = [
                "valor_faturado_consumo",
            ]
            bar_columns_2 = [
                "valor_faturado_band_amar",
                "valor_faturado_band_verm",
                "valor_faturado_cosip",
            ]
            bar_columns_3 = [
                "valor_faturado_custo_disp_sistema",
            ]

        elif selected_grupo_tarifario[0] == "A-4":
            bar_columns_1 = [
                "valor_faturado_consumo_P",
                "valor_faturado_consumo_FP",
            ]
            bar_columns_2 = [
                "valor_faturado_band_amar",
                "valor_faturado_band_verm",
                "valor_faturado_cosip",
                "valor_faturado_ener_reat_exc_P",
                "valor_faturado_ener_reat_exc_FP",
            ]
            bar_columns_3 = [
                "valor_faturado_demanda",
                "valor_faturado_demanda_ultr"
            ]

        figure, axes = plt.subplots(1, 3)

        df_valores_faturados.plot(
            x="Campus_Unique_Name",
            y=bar_columns_1,
            kind="bar",
            rot=80,
            figsize=(16, 10),
            title="VFs Consumo em R$ por UC",
            ax=axes[0],
            grid='y'
        )
        df_valores_faturados.plot(
            x="Campus_Unique_Name",
            y=bar_columns_2,
            kind="bar",
            rot=80,
            figsize=(16, 10),
            title="VFs demais params 1/2 em R$ por UC",
            ax=axes[1],
            grid='y'
        )
        df_valores_faturados.plot(
            x="Campus_Unique_Name",
            y=bar_columns_3,
            kind="bar",
            rot=80,
            figsize=(16, 10),
            title="VFs demais params 2/2 em R$ por UC",
            ax=axes[2],
            grid='y'
        )

    def bar_plot_valores_quantidade(self, selected_grupo_tarifario):
        input_df_with_grupo_tarifario = self.df[
            (self.df.Grupo_Tarifario.isin(selected_grupo_tarifario))
        ]

        input_df_with_grupo_tarifario.to_csv('output.csv', index=False)
        df_raw = pd.read_csv('output.csv')

        grouped_df = df_raw.groupby('Campus_Unique_Name').sum()
        df_valores_faturados = grouped_df[[
            "Quantidade_consumo",
            "Quantidade_consumo_P",
            "Quantidade_consumo_FP",
            "Quantidade_ener_reat_exc_P",
            "Quantidade_ener_reat_exc_FP",
            "Quantidade_demanda",
            "Quantidade_demanda_ultr",
            "Quantidade_custo_disp_sistema",
        ]]

        df_valores_faturados['Campus_Unique_Name'] = df_valores_faturados.index

        if len(selected_grupo_tarifario) == 2:
            st.markdown("**Por favor, escolha APENAS 1 Grupo Tarifário**")

        elif selected_grupo_tarifario[0] == "B-3":
            bar_columns_1 = ["Quantidade_consumo"]
            bar_columns_2 = ["Quantidade_custo_disp_sistema"]


        elif selected_grupo_tarifario[0] == "A-4":
            bar_columns_1 = [
                "Quantidade_consumo_P",
                "Quantidade_consumo_FP",
            ]
            bar_columns_2 = [
                "Quantidade_ener_reat_exc_P",
                "Quantidade_ener_reat_exc_FP",
                "Quantidade_demanda",
                "Quantidade_demanda_ultr",
            ]

        figure, axes = plt.subplots(1, 2)

        df_valores_faturados.plot(
            x="Campus_Unique_Name",
            y=bar_columns_1,
            kind="bar",
            rot=80,
            figsize=(16, 10),
            title="VFs Consumo em W por UC",
            ax=axes[0],
            grid='y'
        )
        df_valores_faturados.plot(
            x="Campus_Unique_Name",
            y=bar_columns_2,
            kind="bar",
            rot=80,
            figsize=(16, 10),
            title="VFs demais params em W por UC",
            ax=axes[1],
            grid='y'
        )

    def bar_plot_valores_medidos(self, selected_grupo_tarifario):
        input_df_with_grupo_tarifario = self.df[
            (self.df.Grupo_Tarifario.isin(selected_grupo_tarifario))
        ]

        input_df_with_grupo_tarifario.to_csv('output.csv', index=False)
        df_raw = pd.read_csv('output.csv')

        grouped_df = df_raw.groupby('Campus_Unique_Name').sum()
        df_valores_faturados = grouped_df[[
            "Medido_consumo",
            "Medido_consumo_P",
            "Medido_consumo_FP",
            "Medido_ener_reat_exc_P",
            "Medido_ener_reat_exc_FP",
            "Medido_demanda",
            "Medido_demanda_ultr",
            "Medido_energia_reat_indutiva"
        ]]

        df_valores_faturados['Campus_Unique_Name'] = df_valores_faturados.index

        if len(selected_grupo_tarifario) == 2:
            st.markdown("**Por favor, escolha APENAS 1 Grupo Tarifário**")

        elif selected_grupo_tarifario[0] == "B-3":
            bar_columns_1 = ["Medido_consumo"]
            bar_columns_2 = ["Medido_energia_reat_indutiva"]

            df_valores_faturados.plot(
                x="Campus_Unique_Name",
                y=bar_columns_1,
                kind="bar",
                rot=45,
                figsize=(16, 10),
                title="VMs Consumo em W por UC",
                grid='y'
            )
        elif selected_grupo_tarifario[0] == "A-4":
            bar_columns_1 = [
                "Medido_consumo_P",
                "Medido_consumo_FP",
            ]
            bar_columns_2 = [
                "Medido_energia_reat_indutiva"
            ]
            bar_columns_3 = [
                "Medido_ener_reat_exc_P",
                "Medido_ener_reat_exc_FP",
                "Medido_demanda",
                "Medido_demanda_ultr",
            ]

            figure, axes = plt.subplots(1, 3)

            df_valores_faturados.plot(
                x="Campus_Unique_Name",
                y=bar_columns_1,
                kind="bar",
                rot=80,
                figsize=(16, 10),
                title="VMs Consumo em W por UC",
                ax=axes[0],
                grid='y'
            )
            df_valores_faturados.plot(
                x="Campus_Unique_Name",
                y=bar_columns_2,
                kind="bar",
                rot=80,
                figsize=(16, 10),
                title="VMs Ener.Reat.Indut. W por UC",
                ax=axes[1],
                grid='y'
            )
            df_valores_faturados.plot(
                x="Campus_Unique_Name",
                y=bar_columns_3,
                kind="bar",
                rot=80,
                figsize=(16, 10),
                title="VMs demais params em W por UC",
                ax=axes[2],
                grid='y'
            )


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

    enriched_csv = "/home/arthur/PycharmProjects/TCC/CSVs/enriched_csvs/enriched_result_05_set.csv"

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

    else:
        st.markdown("**Para iniciar, por favor, escolha na User Input Features um campus ou um grupo tarifário.**")

    return df_input_filtered


def create_output_table(df):
    st.header('Output Table')
    st.markdown("Tabela criada através da seleção dos **User Input Features**.")

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

        if st.button('Consumo Medido (W) e gasto (R$) P e FP'):
            fig = create_plot_obj.medido_e_gasto_consumo_P_and_FP_plot()
            st.plotly_chart(fig, use_container_width=True)

    elif analysis_style == "Campus inteiro":
        if st.button("Composição Unidades Consumidoras Campus"):
            create_plot_obj.treemap_UC_composition()
            st.pyplot()

        if st.checkbox("Tabela Soma Valores Faturados por UC (R$)"):
            df_valores_faturados = create_plot_obj.show_valores_faturados(selected_grupo_tarifario)
            st.dataframe(df_valores_faturados)
            if st.checkbox("Gráfico Soma Valores Faturados por UC (R$)"):
                create_plot_obj.bar_plot_valores_faturados(selected_grupo_tarifario)
                st.pyplot()

        if st.checkbox("Tabela Soma Valores Faturados por UC (W)"):
            df_valores_faturados = create_plot_obj.show_valores_quantidade(selected_grupo_tarifario)
            st.dataframe(df_valores_faturados)
            if st.checkbox("Gráfico Soma Valores Faturados por UC (W)"):
                create_plot_obj.bar_plot_valores_quantidade(selected_grupo_tarifario)
                st.pyplot()

        if st.checkbox("Tabela Soma Valores Medidos por UC (W)"):
            df_valores_faturados = create_plot_obj.show_valores_medidos(selected_grupo_tarifario)
            st.dataframe(df_valores_faturados)
            if st.checkbox("Gráfico Soma Valores Medidos por UC (W)"):
                create_plot_obj.bar_plot_valores_medidos(selected_grupo_tarifario)
                st.pyplot()


def create_header_for_algorythm_analysis():
    st.header("Análise via algoritmo")
    st.markdown("""
    Se você deseja que o algoritmo faça uma análise do resultado encontrado, 
    selecione o botão da análise desejada.
    
    Por hora, as análises possíveis são:
    - Análise de Demanda;
    - Análise comparativa dos anos;
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
            name='2018'))

        fig.add_trace(go.Bar(
            x=labels_2019,
            y=consumo_med_2019,
            name='2019'))

        fig.add_trace(go.Bar(
            x=labels_2020,
            y=consumo_med_2020,
            name='2020'))

        fig.add_trace(go.Scatter(
            x=labels_2018,
            y=media_consumo_mes,
            name='Média mensal'))

        fig.update_layout(
            barmode='group', xaxis_tickangle=-60,
            title="Comparação Consumo Medido (W)",
            height=700, width=900
        )
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ))

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
            barmode='group', xaxis_tickangle=-60, height=700, width=900,
            title="Comparação Consumo Medido (W)"
        )

        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="right",
            x=1
        ))

        return fig

        return



def create_header_for_prediction():
    st.header("Predições")
    st.markdown("""
    Nessa parte o algoritmo irá predizer valores para próximos meses, com base no **reajuste tarifário anual, e no
    consumo esperado para os próximos meses**.
    
    **Sobre o reajuste:**
    
    - Por razões de simplificação, as predições serão feitas apenas até ago/2021, que é quando acontecerá o próximo
    reajuste anual tarifário. 
    - O reajuste tarifário de 2020, que foi anunciado em 22/08/2020, já foi anunciado, 
    e pode ser visto no site da Aneel: https://www.aneel.gov.br/resultado-dos-processos-tarifarios-de-distribuicao
    - O mesmo também pode ser visto nste documento: https://www2.aneel.gov.br/aplicacoes/tarifa/arquivo/NT_REH_2.756_2020_CELESC.pdf
    - Ainda sobre simplificações, **será usado para os cálculos o valor médio do reajuste, que é de +8,14%** 
    
    **Sobre o consumo:**
    - Será feita uma média do consumo dos meses anteriores para predizer qual será o consumo nos meses referentes do futuro.
    
    Você poderá escolher abaixo para quantos meses quer que a predição seja feita, 
    num range iniciando em 06/2020 até 08/2021.
    """)
    months_quantity_to_predict = st.slider(
        label="Selecione a quantidade de meses para a predição (1 para 06/2020 e 15 para 08/2021)",
        min_value=1,
        max_value=15
    )



df_fatura, analysis_style = create_df_and_texts()

selected_grupo_tarifario, selected_campus, selected_date = create_sidebars(df_fatura, analysis_style)

df_input_filtered = filter_showed_data(df_fatura, analysis_style)

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



create_header_for_prediction()
