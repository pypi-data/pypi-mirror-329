# def get_legend_html(gdf):
#     legenda_html = """
#     <div style="position: fixed; top: 50px; right: 80px; width: 400px; height: auto; border:2px solid grey;
#                  z-index:9999; font-size:14px; background-color:white; padding: 10px;">
#         <div>
#             <h4 style="text-align: center; font-weight: bold;">LINHAS DE ÔNIBUS DE MONTES CLAROS - MG <br>(PADRÃO INSUFICIENTE)</h4>
#         </div>
#     </div>
#     """
    
#     # Adiciona elementos específicos da legenda para as linhas insuficientes
#     legenda_html += """
#     <div style="position: fixed; top : 250px; right: 150px; width: 250px; height: auto; border:2px solid grey;
#                 z-index:9999; font-size:14px; background-color:white; padding: 10px;">
#         <b>Legenda</b><br>
#         <div style="display: flex; justify-content: space-between;">
#         <div style="flex: 1;">
#     """
#     linhas_insuficiente = ['1501', '1601', '2201', '2203', '2604', '3301', '4701', '5101', '5601', '5702', '5803', '5901', '5902', '6201R', '6202', '6404', '6604', '6901', '7101', '8201']
#     cores = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'black', '#37FFEE', 'pink'] * 3

#     for count, (index, row) in enumerate(gdf.iterrows()):
#         linha = row.Name.strip().split('-')[0]
#         if linha in linhas_insuficiente:
#             legenda_html += f"""
#             <div style="display: flex; align-items: center; width: 120px; margin-bottom: 5px;">
#                 <div style="width: 40px; height: 10px; background-color: {cores[count]}; margin-right: 5px;"></div>
#                 {linha}
#             </div>
#             """
#     legenda_html += "</div></div></div>"
#     return legenda_html