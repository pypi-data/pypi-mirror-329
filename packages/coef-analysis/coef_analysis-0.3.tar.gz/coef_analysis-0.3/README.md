# coef_analysis

Uma biblioteca simples para calcular coeficientes de correlação entre colunas de um DataFrame e uma variável alvo.

## Instalação

Instale a biblioteca com:
```bash
pip install coef_analysis
```

## Como usar

### Importação
```python
from coef_analysis import get_coef
import pandas as pd

# Criando um DataFrame de exemplo
dados = {
    "idade": [25, 30, 35, 40, 45],
    "salario": [3000, 4000, 5000, 6000, 7000],
    "horas_trabalho": [40, 38, 36, 35, 30]
}
df = pd.DataFrame(dados)

# Calculando a correlação com a variável alvo "salario"
resultado = get_coef(df, alvo="salario")
print(resultado)
```

## Parâmetros da função `get_coef`

| Parâmetro   | Tipo               | Descrição |
|-------------|----------------|-------------|
| `data`      | `pandas.DataFrame` | O DataFrame contendo os dados. |
| `alvo`      | `str`             | Nome da coluna alvo para cálculo da correlação. |
| `limite`    | `list` (default: `[-0.01, 0.01]`) | Intervalo de correlação considerada insignificante. |
| `ascending` | `bool` (default: `False`) | Se `True`, ordena os coeficientes de forma crescente. |

## Retorno
A função retorna um `pandas.DataFrame` contendo:
- **Valores**: Nome das colunas correlacionadas com a variável alvo.
- **Coeficiente de Correlação**: O valor da correlação calculado.

## Tratamento de Erros
- Se a variável alvo não existir no DataFrame, um `ValueError` será levantado.
- Se nenhuma correlação significativa for encontrada dentro dos critérios, a mensagem "Ajuste seu Limite" será exibida.

## Licença
Este projeto está licenciado sob a MIT License.

