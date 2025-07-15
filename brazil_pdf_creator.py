from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from brazil_analysis import df_evaluated as df_evaluated_brazil
from datetime import datetime

df = df_evaluated_brazil.copy()
df = df[['ticker', 'name', 'Portfolio %', 'Portfolio Value']]

df.columns = ['Ticker', 'Name', 'Portfolio %', 'Portfolio Value']

pdf_filename = "top10_brazil_stocks.pdf"

with PdfPages(pdf_filename) as pdf:

    # Configurar a figura para a tabela
    fig, ax = plt.subplots(figsize=(8, 6))  # Configurar o tamanho da página
    ax.axis('tight')
    ax.axis('off')  # Remover eixos

    # Adicionar o título
    plt.text(0.5, 0.9, f"Top 10 Best Brazilian Stocks - {datetime.now().strftime('%Y-%m-%d')}", fontsize=16, ha='center', va='center', transform=fig.transFigure)

    # Renderizar o DataFrame como uma tabela no Matplotlib
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))  # Ajustar a largura das colunas

    # Salvar a tabela no PDF
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)  # Fechar a figura para liberar memória