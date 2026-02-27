import ee
import geemap
import os

def gerar_mapa_interativo():
    # 1. Inicialização do Earth Engine
    # Substitua pelo seu projeto se necessário
    try:
        ee.Initialize(project="ee-passeionamatamapas")
    except Exception as e:
        print("Autenticando no Earth Engine...")
        ee.Authenticate()
        ee.Initialize(project="ee-passeionamatamapas")

    # 2. Criar o mapa base
    Map = geemap.Map(basemap='Esri.WorldImagery')

    # --- Camadas (FeatureCollections) ---
    
    # PIDS
    hids_pids = ee.FeatureCollection("projects/ee-pigee/assets/hids_pids")
    vis_hids_pids = hids_pids.style(color='d488de', width=2, fillColor='d488de', pointSize=1)
    Map.addLayer(vis_hids_pids, {}, 'PIDS', True, 0.5)

    # HIDS
    hids = ee.FeatureCollection("projects/ee-pigee/assets/hids")
    vis_hids = hids.style(color='fa9e09', width=2, fillColor='fa9e09', pointSize=1)
    Map.addLayer(vis_hids, {}, 'HIDS', True, 0.5)

    # Hidrografia
    hidro = ee.FeatureCollection("projects/ee-pigee/assets/hidrografia_campinas")
    vis_hidro = hidro.style(color='031fbb', width=1, fillColor='0000FF', pointSize=1)
    Map.addLayer(vis_hidro, {}, 'Hidrografia')

    # Nascentes
    nascentes = ee.FeatureCollection("projects/ee-pigee/assets/nascentes_campinas")
    vis_nascentes = nascentes.style(color='13f2f9', width=2, fillColor='00000000', pointSize=2)
    Map.addLayer(vis_nascentes, {}, 'Nascentes')

    # Zonas de Amortecimento
    za = ee.FeatureCollection("projects/ee-pigee/assets/zonasAmortecimento")
    vis_za = za.style(color='f50618', width=1, fillColor='00000000', pointSize=30)
    Map.addLayer(vis_za, {}, 'Zonas de Amortecimento')

    # APPs
    app = ee.FeatureCollection("projects/ee-pigee/assets/areaPreservacaoPermanente")
    vis_app = app.style(color='90fe14', width=1, fillColor='00000000', pointSize=2)
    Map.addLayer(vis_app, {}, 'APPs')

    # APAs
    uc = ee.FeatureCollection("projects/ee-pigee/assets/UnidadesConservacaoCampinas")
    vis_uc = uc.style(color='f1fc07', width=2, fillColor='00000000', pointSize=2)
    Map.addLayer(vis_uc, {}, 'APAs')

    # Limite Municipal
    limite = ee.FeatureCollection("projects/ee-rogergodoytest/assets/limite_municipal")
    vis_limite = limite.style(color='000000', width=1, fillColor='00000000', pointSize=2)
    Map.addLayer(vis_limite, {}, 'Limite Municipal')

    # 3. Configurações de Visualização
    Map.centerObject(limite, 11)

    # 4. Legenda
    colors = ['#000000', '#90fe14', '#f1fc07', '#f50618', '#13f2f9', '#031fbb', '#fa9e09', '#d488de']
    keys = [
        'Limite de municipio - Campinas - SP', 
        'Áreas de Proteção Ambiental', 
        'Áreas de Preservação Permanente', 
        'Zonas de amortecimento',
        'Nascentes', 
        'Hidrografia', 
        'HIDS', 
        'PIDS'
    ]
    Map.add_legend(title="Legenda", colors=colors, keys=keys)

    # 5. Exportação para HTML
    output_html = "mapa_campinas_interativo.html"
    Map.to_html(output_html)
    
    print(f"Sucesso! O mapa foi exportado como: {os.path.abspath(output_html)}")

if __name__ == "__main__":
    gerar_mapa_interativo()
