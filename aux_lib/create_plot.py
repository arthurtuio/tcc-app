import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


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
            name="Medido",
            hovertext="kW"
        ))

        fig.add_trace(go.Scatter(
            x=labels,
            y=faturado,
            name="Faturado",
            hovertext="kW"
        ))

        fig.update_layout(
            annotations=[
                dict(
                    x=-0.07,
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
            title_text=f"Demanda Medida X Contratada para o Campus {self.selected_campus}",
            xaxis_tickangle=-60,
            height=600, width=900,
        )

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

    def medido_consumo_P_and_FP_plot(self):
        self.df.to_csv('output.csv', index=False)
        df = pd.read_csv('output.csv')

        labels = sorted(df['MM_YY_ref'].values.tolist())
        medido_consumo_P = df['Medido_consumo_P'].values.tolist()
        medido_consumo_FP = df['Medido_consumo_FP'].values.tolist()

        fig = make_subplots(rows=2, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.04,
                            subplot_titles=("Fora Ponta", "Ponta")
                            )

        fig.add_trace(go.Bar(x=labels, y=medido_consumo_FP, name="medido_FP", hovertext="kW"),
                      row=1, col=1)

        fig.add_trace(go.Bar(x=labels, y=medido_consumo_P, name="medido_P", hovertext="kW"),
                      row=2, col=1)

        fig.update_layout(
            annotations=[
                dict(
                    x=-0.07,
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
            title_text=f"Consumo Medido (kW) P e FP para o Campus {self.selected_campus}",
            xaxis_tickangle=-60,
            height=700, width=1000,
            barmode='stack'
        )

        return fig

    def gasto_consumo_P_and_FP_plot(self):
        self.df.to_csv('output.csv', index=False)
        df = pd.read_csv('output.csv')

        labels = sorted(df['MM_YY_ref'].values.tolist())

        valor_faturado_consumo_P = df['valor_faturado_consumo_P'].values.tolist()
        valor_faturado_consumo_FP = df['valor_faturado_consumo_FP'].values.tolist()

        fig = make_subplots(rows=2, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.04,
                            subplot_titles=("Plot 1", "Plot 2")
                            )

        fig.add_trace(go.Bar(x=labels, y=valor_faturado_consumo_FP, name="valor_faturado_FP", hovertext="R$"),
                      row=1, col=1)

        fig.add_trace(go.Bar(x=labels, y=valor_faturado_consumo_P, name="valor_faturado_P", hovertext="R$"),
                      row=2, col=1)

        fig.update_layout(
            annotations=[
                dict(
                    x=-0.07,
                    y=0.5,
                    showarrow=False,
                    text="Valores [R$]",
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
            title_text=f"Consumo gasto (R$) P e FP para o Campus {self.selected_campus}",
            xaxis_tickangle=-60,
            height=700, width=1000,
            barmode='stack'
        )

        return fig

    def compare_consumo_P_and_FP_plot(self):
        self.df.to_csv('output.csv', index=False)
        df = pd.read_csv('output.csv')

        labels = sorted(df['MM_YY_ref'].values.tolist())

        medido_consumo_P = df['Medido_consumo_P'].values.tolist()
        medido_consumo_FP = df['Medido_consumo_FP'].values.tolist()

        valor_faturado_consumo_P = df['valor_faturado_consumo_P'].values.tolist()
        valor_faturado_consumo_FP = df['valor_faturado_consumo_FP'].values.tolist()

        fig = make_subplots(rows=2, cols=1,
                            vertical_spacing=0.04,
                            shared_xaxes=True,
                            subplot_titles=("Plot 1", "Plot 2")
                            )

        fig.add_trace(go.Bar(x=labels, y=medido_consumo_FP, name="medido_consumo_FP", hovertext="R$"),
                      row=1, col=1)
        fig.add_trace(go.Bar(x=labels, y=medido_consumo_P, name="medido_consumo_P", hovertext="R$"),
                      row=1, col=1)

        fig.add_trace(go.Bar(x=labels, y=valor_faturado_consumo_FP, name="valor_faturado_consumo_FP", hovertext="R$"),
                      row=2, col=1)
        fig.add_trace(go.Bar(x=labels, y=valor_faturado_consumo_P, name="valor_faturado_consumo_P", hovertext="R$"),
                      row=2, col=1)

        fig.update_layout(
            annotations=[
                dict(
                    x=-0.07,
                    y=0.5,
                    showarrow=False,
                    text="Valores [R$]",
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
            title_text=f"Comparação [kW e R$] consumo P e FP para o Campus {self.selected_campus}",
            xaxis_tickangle=-60,
            height=700, width=1000,
            barmode="stack"
        )

        return fig

    # def relative_compare_consumo_P_and_FP_plot(self):
    #     # se eu quiser fazer esse grafico na vdd vou precisar dividir cada valor do P e FP pelo total, pra pegar a %
    #     self.df.to_csv('output.csv', index=False)
    #     df = pd.read_csv('output.csv')
    #
    #     labels = sorted(df['MM_YY_ref'].values.tolist())
    #
    #     medido_consumo_P = df['Medido_consumo_P'].values.tolist()
    #     medido_consumo_FP = df['Medido_consumo_FP'].values.tolist()
    #
    #     fig = go.Figure()
    #     fig.add_bar(x=labels, y=medido_consumo_P)
    #     fig.add_bar(x=labels, y=medido_consumo_FP)
    #     fig.update_layout(barmode="relative")
    #
    #     return fig

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

    def sunburst_month_and_UC(self, value_to_analyse):
        fig = px.sunburst(
            self.df,
            path=['Grupo_Tarifario', 'Campus_Unique_Name', 'year', 'MM_YY_ref'],
            values=value_to_analyse
        )

        fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        return fig
