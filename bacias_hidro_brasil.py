import ee
import geemap
import os

def main():
    try:
        # Inicializa a API do Earth Engine
        # Substitua pelo seu ID de projeto se necessário
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

    # 3. Filtrar as bacias que intersectam o Brasil
    bacias_brasil = basins.filterBounds(brasil)

    # 4. Converter a FeatureCollection em Imagem para colorização aleatória
    # O atributo 'HYBAS_ID' serve como base para as cores distintas
    bacias_raster = bacias_brasil.reduceToImage(
        properties=['HYBAS_ID'],
        reducer=ee.Reducer.first()
    )

    # Aplicar o visualizador aleatório na imagem
    bacias_coloridas = bacias_raster.randomVisualizer()

    # 5. Dados de Ocorrência de Água (JRC)
    water = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select('occurrence')
    water_masked = water.updateMask(water.gt(10))

    # 6. Configurações de Visualização da Água
    vis_agua = {
        'min': 0, 
        'max': 100, 
        'palette': ['#BDD7EE', '#2171B5', '#08306B']
    }

    # 7. Adicionar Camadas ao Mapa
    
    # Adicionar as bacias coloridas com opacidade (0.6)
    Map.addLayer(bacias_coloridas.updateMask(0.6), {}, 'Bacias Hidrográficas (Cores Distintas)')

    # Adicionar apenas os contornos das bacias em branco
    bordas = ee.Image().paint(bacias_brasil, 0, 1)
    Map.addLayer(bordas, {'palette': 'white'}, 'Limites das Bacias')

    # Adicionar a ocorrência de água clipada para o território
    Map.addLayer(water_masked.clip(bacias_brasil), vis_agua, 'Ocorrência de Água (%)')

    # Adicionar contorno do Brasil em vermelho para referência
    Map.addLayer(brasil.style(fillColor='00000000', color='red'), {}, 'Limite do Brasil')

    # 8. Configurações de exibição
    Map.centerObject(brasil, 4)
    Map.setOptions('SATELLITE')

    # 9. Salvar como HTML
    output_name = "mapa_bacias_brasil.html"
    Map.to_html(output_name)
    
    print(f"Sucesso! O mapa foi gerado em: {os.path.abspath(output_name)}")

if __name__ == "__main__":
    main()
