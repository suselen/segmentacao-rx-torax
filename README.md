# Segmentação e Análise Quantitativa de Radiografias de Tórax

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SEU_USUARIO/segmentacao-rx-torax/blob/main/notebooks/segmentacao_rx_torax.ipynb)

Projeto acadêmico de **Processamento Digital de Imagens e Visão Computacional** para radiografias de tórax.

> **Aviso:** este projeto é educacional e experimental. Não substitui laudo, diagnóstico ou avaliação médica.

## Objetivo

Construir um pipeline reprodutível para:

1. carregar imagens PNG/JPG e arquivos DICOM;
2. remover identificadores dos metadados DICOM;
3. mascarar textos identificadores gravados nos pixels;
4. normalizar imagens para tons de cinza;
5. aplicar CLAHE e filtros;
6. analisar histogramas e níveis de cinza;
7. detectar bordas;
8. avaliar máscaras com Dice e IoU;
9. gerar uma descrição técnica quantitativa;
10. evoluir para segmentação dos pulmões, silhueta cardíaca e dispositivos.

## Versões planejadas

### v0.1 — Fundamentos de PDI

- leitura PNG/JPG/DICOM;
- anonimização de metadados;
- mascaramento manual de regiões com texto;
- CLAHE;
- filtros Gaussiano, mediana e bilateral;
- Sobel e Canny;
- histograma e estatísticas;
- Dice e IoU;
- tabela de resultados;
- rascunho técnico estruturado.

### v0.2 — Segmentação anatômica

- segmentação dos campos pulmonares;
- segmentação da silhueta cardíaca;
- máscaras de referência;
- avaliação quantitativa;
- cálculo exploratório do índice cardiotorácico;
- localização aproximada dos ângulos costofrênicos.

### v0.3 — Evolução por aprendizado profundo

- U-Net ou arquitetura equivalente;
- treinamento/validação;
- comparação com métodos clássicos;
- análise de erros e generalização.

### v0.4 — Dispositivos e integração

- detecção de eletrodos e cateteres;
- classificação de dispositivos;
- integração futura com XNAT/OHIF;
- relatório estruturado.

## Estrutura

```text
segmentacao-rx-torax/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── segmentacao_rx_torax.ipynb
├── src/
│   ├── anonymization.py
│   ├── io_utils.py
│   ├── preprocessing.py
│   ├── segmentation.py
│   ├── measurements.py
│   ├── metrics.py
│   ├── visualization.py
│   ├── report.py
│   └── devices.py
├── tests/
│   └── test_metrics.py
├── images/
│   └── exemplos/
├── data/
├── models/
└── results/
```

## Privacidade

O padrão do projeto é:

- remover nome, ID, accession number, instituição, médico e outros identificadores;
- remover ou substituir UIDs;
- preservar apenas `PatientSex`, quando necessário;
- não publicar data de nascimento completa;
- derivar idade ou faixa etária quando possível;
- mascarar textos gravados na própria imagem;
- nunca versionar imagens privadas no GitHub.

A simples troca do nome por um código é **pseudonimização**, não anonimização completa.

## Executando no Colab

1. Faça upload deste projeto para um repositório GitHub.
2. Troque `SEU_USUARIO` no botão do Colab.
3. Abra `notebooks/segmentacao_rx_torax.ipynb`.
4. Execute as células de cima para baixo.
5. Envie uma imagem de exemplo sem dados identificadores.

## Executando localmente

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Dados

Não inclua dados clínicos privados neste repositório.

Coloque apenas:

- exemplos públicos autorizados;
- imagens sintéticas;
- imagens previamente anonimizadas;
- links e instruções para baixar bases públicas.

## Licença

Código disponibilizado sob licença MIT. Dados e modelos podem possuir licenças próprias.
