import ee
import geemap
import os

def main():
    try:
        # Inicializa a API do Earth Engine
        ee.Initialize(project="ee-passeionamatamapas")
    except Exception as e:
        print("Erro de autenticação. Rode 'ee.Authenticate()' no seu terminal.")
        return

    # Cria o objeto do Mapa
    Map = geemap.Map()

    # 1. Carregar o limite territorial do Brasil (Dataset LSIB)
    brasil = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017") \
                .filter(ee.Filter.eq('country_na', 'Brazil'))

    # 2. Carregar as Bacias Hidrográficas (Nível 4)
    basins = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_4")
    bacias_brasil = basins.filterBounds(brasil)

    # 3. Converter para Imagem e Colorização Aleatória
    bacias_raster = bacias_brasil.reduceToImage(
        properties=['HYBAS_ID'],
        reducer=ee.Reducer.first()
    )
    bacias_coloridas = bacias_raster.randomVisualizer()

    # 4. Dados de Ocorrência de Água (JRC)
    water = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select('occurrence')
    water_masked = water.updateMask(water.gt(10))
    vis_agua = {'min': 0, 'max': 100, 'palette': ['#BDD7EE', '#2171B5', '#08306B']}

    # --- ADIÇÃO DA CAMADA WMS DA FUNAI ---
    # URL base do GeoServer da FUNAI
    wms_url = "https://geoserver.funai.gov.br/geoserver/Funai/wms"
    
    # Adicionando a camada WMS
    #Map.add_wms_layer(
    #    url=wms_url,
    #    layers='tis_poligonais_portarias',
    #    name='Terras Indígenas (FUNAI)',
    #    attribution='FUNAI',
    #    format='image/png',
    #    transparent=True
    #)
    # --------------------------------------

    # 5. Adicionar Camadas do Earth Engine ao Mapa
    # Bacias coloridas (fundo)
    Map.addLayer(bacias_coloridas.updateMask(0.6), {}, 'Bacias Hidrográficas')

    # Limites das bacias em branco
    bordas = ee.Image().paint(bacias_brasil, 0, 1)
    Map.addLayer(bordas, {'palette': 'white'}, 'Limites das Bacias')

    # Ocorrência de água
    Map.addLayer(water_masked.clip(bacias_brasil), vis_agua, 'Ocorrência de Água (%)')

    # Contorno do Brasil em vermelho
    Map.addLayer(brasil.style(fillColor='00000000', color='red'), {}, 'Limite do Brasil')

    # Adicionando a camada WMS
    Map.add_wms_layer(
        url=wms_url,
        layers='tis_poligonais_portarias',
        name='Terras Indígenas (FUNAI)',
        attribution='FUNAI',
        format='image/png',
        transparent=True
    )

    # 6. Configurações de exibição
    Map.centerObject(brasil, 3)
    Map.setOptions('SATELLITE')

    # 7. Salvar como HTML
    output_name = "mapa_bacias_e_ti_brasil.html"
    Map.to_html(output_name)
    
    print(f"Sucesso! Mapa gerado com camadas WMS em: {os.path.abspath(output_name)}")

if __name__ == "__main__":
    main()
