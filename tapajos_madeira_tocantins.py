import ee
import geemap
import os

def main():
    try:
        # 1. Inicializa o Earth Engine
        # O parâmetro 'project' é importante para autenticação em contas novas
        ee.Initialize(project="ee-passeionamatamapas")
    except Exception as e:
        print("Erro na autenticação. Tente rodar 'ee.Authenticate()' no terminal.")
        return

    # 2. Configura o Mapa Base
    Map = geemap.Map(basemap='Esri.WorldImagery')

    # 3. Carregar as Bacias Hidrográficas Globais (HydroSHEDS)
    basins = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_4")

    # 4. Filtrar as Bacias
    ids_bacias = [6040345000, 6040285990, 6040262220]
    # Usando um filtro unificado para simplificar o código
    bacias_selecionadas = basins.filter(ee.Filter.inList('HYBAS_ID', ids_bacias))

    # 5. Carregar dados de Ocorrência de Água (JRC)
    water = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select('occurrence')
    water_masked = water.updateMask(water.gt(10))

    # 6. Configurações de Visualização
    vis_bacia = {'color': '00FF00', 'fillColor': '00000000'} # Verde em Hexadecimal
    vis_agua = {'min': 0, 'max': 100, 'palette': ['lightblue', 'blue', 'darkblue']}

    # 7. Adicionar Camadas ao Mapa
    # Adicionamos o limite das bacias (todas de uma vez para performance)
    Map.addLayer(bacias_selecionadas, vis_bacia, 'Limites das Bacias')
    
    # Adicionamos a água recortada pela área de interesse
    Map.addLayer(water_masked.clip(bacias_selecionadas), vis_agua, 'Ocorrência de Água (%)')

    # 8. Centralizar o mapa
    Map.centerObject(bacias_selecionadas, 6)

    # 9. SALVAR O RESULTADO
    # Scripts .py não "mostram" o mapa vivo, então geramos um HTML
    output_file = "meu_mapa_hidrografia.html"
    Map.to_html(output_file)
    
    print(f"Sucesso! O mapa foi gerado e salvo como: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()
